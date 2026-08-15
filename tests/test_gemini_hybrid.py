import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import align_text, gemini_hybrid
from tritrack_editing_assistant.contracts import validate_contract

EXACT_MODEL = "gemini-invented-exact"


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_alignment_inputs(root: Path) -> tuple[Path, Path, str]:
    transcript = {
        "schemaVersion": "tritrack.transcript-bundle/v1",
        "profileId": "whisper-cpp-cpu-no-fallback-v1",
        "language": "en",
        "modelSha256": "3" * 64,
        "engine": {
            "name": "whisper-cli",
            "version": "whisper.cpp version: invented-cli",
        },
        "takes": [
            {
                "takeId": "Invented.wav",
                "sourceSha256": "a" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 500,
                        "text": "Invented source text.",
                    }
                ],
            },
            {
                "takeId": "Empty.wav",
                "sourceSha256": "b" * 64,
                "status": "empty",
                "cues": [],
            },
        ],
    }
    transcript_path = root / "transcript.json"
    write_json(transcript_path, transcript)
    source_bundle_sha256 = hashlib.sha256(transcript_path.read_bytes()).hexdigest()
    revision = {
        "schemaVersion": "tritrack.text-revision/v1",
        "sourceBundleSha256": source_bundle_sha256,
        "language": "en",
        "takes": [
            {
                "takeId": "Invented.wav",
                "sourceSha256": "a" * 64,
                "revisions": [
                    {
                        "cueId": "cue-000001",
                        "text": "Invented revised text.",
                    }
                ],
            }
        ],
    }
    revision_path = root / "revision.json"
    write_json(revision_path, revision)
    return transcript_path, revision_path, source_bundle_sha256


def invented_receipt(source_bundle_sha256: str) -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.provider-receipt/v1",
        "provider": "gemini",
        "operation": "audio-transcription",
        "sourceBundleSha256": source_bundle_sha256,
        "takeId": "Invented.wav",
        "requestedModel": EXACT_MODEL,
        "observedModel": EXACT_MODEL,
        "audioSha256": "a" * 64,
        "requestStatus": "completed",
        "responseStatus": 200,
        "upload": {
            "status": "completed",
            "serverFileIdSha256": "e" * 64,
        },
        "serverFileDeletion": {
            "attempted": True,
            "confirmed": True,
            "statusCode": 200,
        },
    }


class OfflineHybridConformanceTest(unittest.TestCase):
    def prepare(self, root: Path) -> tuple[Path, Path, Path]:
        transcript, revision, source_hash = write_alignment_inputs(root)
        receipt = root / "receipt.json"
        write_json(receipt, invented_receipt(source_hash))
        return transcript, revision, receipt

    def test_publishes_byte_identical_local_alignment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, receipt = self.prepare(root)
            local_output = root / "local.json"
            hybrid_output = root / "hybrid.json"

            local_payload = align_text.align_and_publish(
                transcript, revision, output_path=local_output
            )
            hybrid_payload = gemini_hybrid.hybrid_and_publish(
                transcript,
                revision,
                [receipt],
                exact_model=EXACT_MODEL,
                output_path=hybrid_output,
            )

            self.assertEqual(hybrid_payload, local_payload)
            self.assertEqual(hybrid_output.read_bytes(), local_output.read_bytes())
            validate_contract("aligned-transcript-v1", hybrid_payload)

    def test_requires_exactly_one_receipt_per_revised_take(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, receipt = self.prepare(root)

            for label, receipts in (
                ("missing", []),
                ("duplicate", [receipt, receipt]),
            ):
                with self.subTest(label=label), self.assertRaisesRegex(
                    ValueError, "TRITRACK_HYBRID_RECEIPT_SET_INVALID"
                ):
                    gemini_hybrid.hybrid_and_publish(
                        transcript,
                        revision,
                        receipts,
                        exact_model=EXACT_MODEL,
                        output_path=root / f"{label}.json",
                    )
                self.assertFalse((root / f"{label}.json").exists())

            extra = root / "extra.json"
            extra_payload = invented_receipt(
                hashlib.sha256(transcript.read_bytes()).hexdigest()
            )
            extra_payload["takeId"] = "Foreign.wav"
            extra_payload["audioSha256"] = "f" * 64
            write_json(extra, extra_payload)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_HYBRID_RECEIPT_SET_INVALID"
            ):
                gemini_hybrid.hybrid_and_publish(
                    transcript,
                    revision,
                    [receipt, extra],
                    exact_model=EXACT_MODEL,
                    output_path=root / "extra-output.json",
                )
            self.assertFalse((root / "extra-output.json").exists())

    def test_rejects_nonconformant_receipt_state(self) -> None:
        variants: list[tuple[str, dict[str, object]]] = []
        base = invented_receipt("1" * 64)
        for label, path, value in (
            ("provider", ("provider",), "other"),
            ("bundle", ("sourceBundleSha256",), "f" * 64),
            ("audio", ("audioSha256",), "f" * 64),
            ("requested-model", ("requestedModel",), "gemini-other"),
            ("observed-model", ("observedModel",), "gemini-other"),
            ("null-model", ("observedModel",), None),
            ("request", ("requestStatus",), "failed"),
            ("response", ("responseStatus",), 500),
            ("upload", ("upload", "status"), "failed"),
            ("upload-id", ("upload", "serverFileIdSha256"), None),
            ("deletion-attempt", ("serverFileDeletion", "attempted"), False),
            ("deletion-code", ("serverFileDeletion", "statusCode"), 500),
        ):
            changed = copy.deepcopy(base)
            target = changed
            for key in path[:-1]:
                nested = target[key]
                assert isinstance(nested, dict)
                target = nested
            target[path[-1]] = value
            variants.append((label, changed))

        unconfirmed = copy.deepcopy(base)
        unconfirmed["requestStatus"] = "privacy-incomplete"
        deletion = unconfirmed["serverFileDeletion"]
        assert isinstance(deletion, dict)
        deletion.update({"attempted": True, "confirmed": False, "statusCode": None})
        variants.append(("deletion-unconfirmed", unconfirmed))

        for label, receipt_payload in variants:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                transcript, revision, source_hash = write_alignment_inputs(root)
                if label != "bundle":
                    receipt_payload["sourceBundleSha256"] = source_hash
                receipt = root / "receipt.json"
                write_json(receipt, receipt_payload)
                output = root / "output.json"

                with self.assertRaisesRegex(
                    ValueError, "TRITRACK_HYBRID_RECEIPT_REJECTED"
                ):
                    gemini_hybrid.hybrid_and_publish(
                        transcript,
                        revision,
                        [receipt],
                        exact_model=EXACT_MODEL,
                        output_path=output,
                    )
                self.assertFalse(output.exists())

    def test_rejects_invalid_model_and_receipt_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, receipt = self.prepare(root)

            for invalid_model in ("", "gemini\nother", "x" * 257):
                with self.subTest(model=invalid_model), self.assertRaisesRegex(
                    ValueError, "TRITRACK_HYBRID_MODEL_INVALID"
                ):
                    gemini_hybrid.hybrid_and_publish(
                        transcript,
                        revision,
                        [receipt],
                        exact_model=invalid_model,
                        output_path=root / "invalid-model.json",
                    )

            malformed = root / "malformed.json"
            malformed.write_bytes(b"not-json")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_HYBRID_RECEIPT_INVALID"
            ):
                gemini_hybrid.hybrid_and_publish(
                    transcript,
                    revision,
                    [malformed],
                    exact_model=EXACT_MODEL,
                    output_path=root / "malformed-output.json",
                )

            symlink = root / "receipt-link.json"
            symlink.symlink_to(receipt)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_HYBRID_RECEIPT_INVALID"
            ):
                gemini_hybrid.hybrid_and_publish(
                    transcript,
                    revision,
                    [symlink],
                    exact_model=EXACT_MODEL,
                    output_path=root / "symlink-output.json",
                )

            directory = root / "receipt-directory"
            directory.mkdir()
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_HYBRID_RECEIPT_INVALID"
            ):
                gemini_hybrid.hybrid_and_publish(
                    transcript,
                    revision,
                    [directory],
                    exact_model=EXACT_MODEL,
                    output_path=root / "directory-output.json",
                )

    def test_detects_receipt_mutation_before_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, receipt = self.prepare(root)
            output = root / "output.json"
            original_verify = align_text.verify_artifact_unchanged

            def mutate_receipt(artifact):
                if artifact.contract == "provider-receipt-v1":
                    receipt.write_bytes(receipt.read_bytes() + b" ")
                return original_verify(artifact)

            with (
                mock.patch.object(
                    gemini_hybrid.align_text,
                    "verify_artifact_unchanged",
                    side_effect=mutate_receipt,
                ),
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_ALIGNMENT_INPUT_CHANGED"
                ),
            ):
                gemini_hybrid.hybrid_and_publish(
                    transcript,
                    revision,
                    [receipt],
                    exact_model=EXACT_MODEL,
                    output_path=output,
                )
            self.assertFalse(output.exists())

    def test_existing_output_and_publication_race_do_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, receipt = self.prepare(root)
            output = root / "output.json"
            output.write_text("sentinel", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                gemini_hybrid.hybrid_and_publish(
                    root / "missing-transcript.json",
                    root / "missing-revision.json",
                    [root / "missing-receipt.json"],
                    exact_model=EXACT_MODEL,
                    output_path=output,
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

            output.unlink()

            def racing_link(source, destination):
                Path(destination).write_text("winner", encoding="utf-8")
                raise FileExistsError

            with (
                mock.patch.object(align_text.os, "link", side_effect=racing_link),
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                gemini_hybrid.hybrid_and_publish(
                    transcript,
                    revision,
                    [receipt],
                    exact_model=EXACT_MODEL,
                    output_path=output,
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "winner")


if __name__ == "__main__":
    unittest.main()
