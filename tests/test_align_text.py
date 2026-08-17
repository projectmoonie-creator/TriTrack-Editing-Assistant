import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import align_text
from tritrack_editing_assistant.contracts import validate_contract

SOURCE_BUNDLE_SHA = "1" * 64
REVISION_SHA = "2" * 64


def invented_transcript() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.transcript-bundle/v1",
        "profileId": "whisper-cpp-cpu-no-fallback-v1",
        "language": "en",
        "modelSha256": "3" * 64,
        "engine": {
            "name": "whisper-cli",
            "version": "whisper.cpp version: invented-1",
        },
        "takes": [
            {
                "takeId": "B.wav",
                "sourceSha256": "b" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 500,
                        "text": "Original first.",
                    },
                    {
                        "cueId": "cue-000002",
                        "startMs": 500,
                        "endMs": 1000,
                        "text": "Original second.",
                    },
                ],
            },
            {
                "takeId": "A.wav",
                "sourceSha256": "a" * 64,
                "status": "empty",
                "cues": [],
            },
        ],
    }


def invented_revision() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.text-revision/v1",
        "sourceBundleSha256": SOURCE_BUNDLE_SHA,
        "language": "en",
        "takes": [
            {
                "takeId": "B.wav",
                "sourceSha256": "b" * 64,
                "revisions": [
                    {
                        "cueId": "cue-000002",
                        "text": "  Corrected   second.  ",
                    }
                ],
            }
        ],
    }


class PureCueAlignmentTest(unittest.TestCase):
    def test_builds_strict_sorted_immutable_alignment(self) -> None:
        transcript = invented_transcript()
        revision = invented_revision()
        transcript_before = copy.deepcopy(transcript)
        revision_before = copy.deepcopy(revision)

        aligned = align_text.build_aligned_transcript(
            transcript,
            revision,
            source_bundle_sha256=SOURCE_BUNDLE_SHA,
            revision_sha256=REVISION_SHA,
        )

        validate_contract("aligned-transcript-v1", aligned)
        self.assertEqual(transcript, transcript_before)
        self.assertEqual(revision, revision_before)
        self.assertEqual(
            aligned,
            {
                "schemaVersion": "tritrack.aligned-transcript/v1",
                "alignmentProfileId": "cue-addressed-v1",
                "sourceBundleSha256": SOURCE_BUNDLE_SHA,
                "revisionSha256": REVISION_SHA,
                "language": "en",
                "takes": [
                    {
                        "takeId": "A.wav",
                        "sourceSha256": "a" * 64,
                        "status": "empty",
                        "cues": [],
                    },
                    {
                        "takeId": "B.wav",
                        "sourceSha256": "b" * 64,
                        "status": "completed",
                        "cues": [
                            {
                                "cueId": "cue-000001",
                                "startMs": 0,
                                "endMs": 500,
                                "text": "Original first.",
                                "disposition": "original",
                            },
                            {
                                "cueId": "cue-000002",
                                "startMs": 500,
                                "endMs": 1000,
                                "text": "Corrected second.",
                                "disposition": "revised",
                            },
                        ],
                    },
                ],
            },
        )

    def test_accepts_explicit_no_change_revision(self) -> None:
        revision = invented_revision()
        revision["takes"] = []

        aligned = align_text.build_aligned_transcript(
            invented_transcript(),
            revision,
            source_bundle_sha256=SOURCE_BUNDLE_SHA,
            revision_sha256=REVISION_SHA,
        )

        validate_contract("aligned-transcript-v1", aligned)
        completed = next(
            take for take in aligned["takes"] if take["status"] == "completed"
        )
        self.assertEqual(
            [cue["disposition"] for cue in completed["cues"]],
            ["original", "original"],
        )

    def test_rejects_bundle_hash_and_language_mismatch(self) -> None:
        bad_hash = invented_revision()
        bad_hash["sourceBundleSha256"] = "f" * 64
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ALIGNMENT_SOURCE_HASH_MISMATCH"
        ):
            align_text.build_aligned_transcript(
                invented_transcript(),
                bad_hash,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

        bad_language = invented_revision()
        bad_language["language"] = "zh"
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ALIGNMENT_LANGUAGE_MISMATCH"
        ):
            align_text.build_aligned_transcript(
                invented_transcript(),
                bad_language,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

    def test_rejects_duplicate_or_unknown_take_ids(self) -> None:
        duplicate_source = invented_transcript()
        duplicate_source["takes"].append(copy.deepcopy(duplicate_source["takes"][0]))
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ALIGNMENT_DUPLICATE_TAKE"
        ):
            align_text.build_aligned_transcript(
                duplicate_source,
                invented_revision(),
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

        unknown_take = invented_revision()
        unknown_take["takes"][0]["takeId"] = "Unknown.wav"
        with self.assertRaisesRegex(ValueError, "TRITRACK_ALIGNMENT_TAKE_UNKNOWN"):
            align_text.build_aligned_transcript(
                invented_transcript(),
                unknown_take,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

    def test_rejects_duplicate_or_unknown_cue_ids(self) -> None:
        duplicate_source = invented_transcript()
        duplicate_source["takes"][0]["cues"].append(
            copy.deepcopy(duplicate_source["takes"][0]["cues"][0])
        )
        with self.assertRaisesRegex(ValueError, "TRITRACK_ALIGNMENT_DUPLICATE_CUE"):
            align_text.build_aligned_transcript(
                duplicate_source,
                invented_revision(),
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

        unknown_cue = invented_revision()
        unknown_cue["takes"][0]["revisions"][0]["cueId"] = "cue-999999"
        with self.assertRaisesRegex(ValueError, "TRITRACK_ALIGNMENT_CUE_UNKNOWN"):
            align_text.build_aligned_transcript(
                invented_transcript(),
                unknown_cue,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

    def test_rejects_duplicate_revision_addresses(self) -> None:
        revision = invented_revision()
        revision["takes"].append(copy.deepcopy(revision["takes"][0]))
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ALIGNMENT_DUPLICATE_TAKE"
        ):
            align_text.build_aligned_transcript(
                invented_transcript(),
                revision,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

        revision = invented_revision()
        revision["takes"][0]["revisions"].append(
            copy.deepcopy(revision["takes"][0]["revisions"][0])
        )
        with self.assertRaisesRegex(ValueError, "TRITRACK_ALIGNMENT_DUPLICATE_CUE"):
            align_text.build_aligned_transcript(
                invented_transcript(),
                revision,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )


class AlignmentFileBoundaryTest(unittest.TestCase):
    def write_inputs(self, root: Path) -> tuple[Path, Path, bytes, bytes]:
        transcript_path = root / "transcript.json"
        revision_path = root / "revision.json"
        transcript_bytes = (
            json.dumps(
                invented_transcript(), ensure_ascii=False, indent=2, sort_keys=True
            )
            + "\n"
        ).encode("utf-8")
        transcript_path.write_bytes(transcript_bytes)
        revision = invented_revision()
        revision["sourceBundleSha256"] = hashlib.sha256(
            transcript_bytes
        ).hexdigest()
        revision_bytes = (
            json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        revision_path.write_bytes(revision_bytes)
        return transcript_path, revision_path, transcript_bytes, revision_bytes

    def test_publishes_stable_exact_byte_bound_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, transcript_before, revision_before = (
                self.write_inputs(root)
            )
            first = root / "first.json"
            second = root / "second.json"

            first_payload = align_text.align_and_publish(
                transcript, revision, output_path=first
            )
            second_payload = align_text.align_and_publish(
                transcript, revision, output_path=second
            )

            self.assertEqual(first_payload, second_payload)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(transcript.read_bytes(), transcript_before)
            self.assertEqual(revision.read_bytes(), revision_before)
            self.assertEqual(
                first_payload["sourceBundleSha256"],
                hashlib.sha256(transcript_before).hexdigest(),
            )
            self.assertEqual(
                first_payload["revisionSha256"],
                hashlib.sha256(revision_before).hexdigest(),
            )
            validate_contract("aligned-transcript-v1", first_payload)
            self.assertNotIn(str(root), first.read_text(encoding="utf-8"))

    def test_existing_output_and_missing_parent_fail_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, _, _ = self.write_inputs(root)
            output = root / "output.json"
            output.write_text("sentinel", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                align_text.align_and_publish(
                    transcript, revision, output_path=output
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
            ):
                align_text.align_and_publish(
                    transcript,
                    revision,
                    output_path=root / "missing" / "output.json",
                )

    def test_rejects_malformed_symlink_and_oversized_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, _, _ = self.write_inputs(root)

            revision.write_bytes(b"not-json")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_ALIGNMENT_REVISION_INVALID"
            ):
                align_text.align_and_publish(
                    transcript, revision, output_path=root / "malformed.json"
                )

            _, revision, _, _ = self.write_inputs(root)
            link = root / "transcript-link.json"
            link.symlink_to(transcript)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_ALIGNMENT_TRANSCRIPT_INVALID"
            ):
                align_text.align_and_publish(
                    link, revision, output_path=root / "symlink.json"
                )

            transcript.write_bytes(b"{" + b" " * (16 * 1024 * 1024))
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_ALIGNMENT_TRANSCRIPT_INVALID"
            ):
                align_text.align_and_publish(
                    transcript, revision, output_path=root / "oversized.json"
                )

    def test_detects_late_input_mutation_before_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, _, _ = self.write_inputs(root)
            output = root / "output.json"
            original_builder = align_text.build_aligned_transcript

            def mutate_after_build(*args, **kwargs):
                payload = original_builder(*args, **kwargs)
                transcript.write_bytes(transcript.read_bytes() + b" ")
                return payload

            with mock.patch.object(
                align_text,
                "build_aligned_transcript",
                side_effect=mutate_after_build,
            ), self.assertRaisesRegex(
                ValueError, "TRITRACK_ALIGNMENT_INPUT_CHANGED"
            ):
                align_text.align_and_publish(
                    transcript, revision, output_path=output
                )
            self.assertFalse(output.exists())

    def test_publication_race_does_not_overwrite_winner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision, _, _ = self.write_inputs(root)
            output = root / "output.json"

            def racing_link(source, destination):
                Path(destination).write_text("winner", encoding="utf-8")
                raise FileExistsError

            with (
                mock.patch.object(align_text.os, "link", side_effect=racing_link),
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                align_text.align_and_publish(
                    transcript, revision, output_path=output
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "winner")


class PureCueAlignmentValidationTest(unittest.TestCase):
    def test_rejects_source_hash_mismatch_and_empty_take_edit(self) -> None:
        wrong_source = invented_revision()
        wrong_source["takes"][0]["sourceSha256"] = "d" * 64
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ALIGNMENT_SOURCE_HASH_MISMATCH"
        ):
            align_text.build_aligned_transcript(
                invented_transcript(),
                wrong_source,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

        empty_edit = invented_revision()
        empty_edit["takes"][0] = {
            "takeId": "A.wav",
            "sourceSha256": "a" * 64,
            "revisions": [{"cueId": "cue-000001", "text": "Invented speech"}],
        }
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ALIGNMENT_EMPTY_TAKE_IMMUTABLE"
        ):
            align_text.build_aligned_transcript(
                invented_transcript(),
                empty_edit,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

    def test_rejects_invalid_source_timing(self) -> None:
        transcript = invented_transcript()
        transcript["takes"][0]["cues"][1]["startMs"] = 400
        with self.assertRaisesRegex(ValueError, "TRITRACK_ALIGNMENT_SOURCE_INVALID"):
            align_text.build_aligned_transcript(
                transcript,
                invented_revision(),
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )

    def test_rejects_invalid_revision_text(self) -> None:
        revision = invented_revision()
        revision["takes"][0]["revisions"][0]["text"] = "<|startoftranscript|>"
        with self.assertRaisesRegex(ValueError, "TRITRACK_ALIGNMENT_TEXT_INVALID"):
            align_text.build_aligned_transcript(
                invented_transcript(),
                revision,
                source_bundle_sha256=SOURCE_BUNDLE_SHA,
                revision_sha256=REVISION_SHA,
            )


if __name__ == "__main__":
    unittest.main()
