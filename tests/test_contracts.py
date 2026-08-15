import copy
import unittest

from jsonschema import ValidationError

from tritrack_editing_assistant import contracts

VALID_CONTRACTS = {
    "compatibility-profile-v1": {
        "schemaVersion": "tritrack.compatibility-profile/v1",
        "profileId": "uhd-2997-ndf-fcpxml-1.14",
        "fcpxmlVersion": "1.14",
        "frameDuration": "1001/30000s",
        "width": 3840,
        "height": 2160,
        "timecodeFormat": "NDF",
        "audioRate": 48000,
        "colorSpace": "1-1-1 (Rec. 709)",
    },
    "sync-map-v1": {
        "schemaVersion": "tritrack.sync-map/v1",
        "profileId": "uhd-2997-ndf-fcpxml-1.14",
        "pairs": [
            {
                "pairId": "pair-001",
                "mediaA": "camera-a-001",
                "mediaB": "camera-b-001",
                "offsetBFromASeconds": -1.25,
                "confidence": 18.5,
                "overlapSeconds": 42.0,
                "audioMaster": "A",
                "durationASeconds": 45.0,
                "durationBSeconds": 44.0,
                "startedAt": None,
            }
        ],
        "singleA": ["camera-a-002"],
        "singleB": [],
        "warnings": [{"code": "SYNC_AUDIO_MISSING", "mediaId": "camera-a-002"}],
    },
    "grouping-v1": {
        "schemaVersion": "tritrack.grouping/v1",
        "alignedTranscriptSha256": "4" * 64,
        "questions": [
            {
                "id": "question-001",
                "question": "What changed?",
                "order": 1,
                "answers": [
                    {
                        "id": "answer-001",
                        "order": 1,
                        "takeId": "Take-A.wav",
                        "startCueId": "cue-000001",
                        "endCueId": "cue-000002",
                        "note": "Primary answer",
                    }
                ],
            }
        ],
        "reserve": [
            {
                "id": "reserve-001",
                "order": 1,
                "takeId": "Take-B.wav",
                "startCueId": "cue-000003",
                "endCueId": "cue-000003",
                "reason": "Alternate answer",
            }
        ],
    },
    "working-cut-v1": {
        "schemaVersion": "tritrack.working-cut/v1",
        "organizationProfileId": "cue-addressed-question-groups-v1",
        "alignedTranscriptSha256": "4" * 64,
        "groupingSha256": "5" * 64,
        "questions": [
            {
                "id": "question-001",
                "question": "What changed?",
                "order": 1,
            }
        ],
        "segments": [
            {
                "id": "answer-001",
                "storyOrder": 1,
                "questionId": "question-001",
                "takeId": "Take-A.wav",
                "sourceSha256": "a" * 64,
                "startCueId": "cue-000001",
                "endCueId": "cue-000002",
                "startMs": 0,
                "endMs": 1200,
                "note": "Primary answer",
            }
        ],
        "reserve": [
            {
                "id": "reserve-001",
                "order": 1,
                "takeId": "Take-B.wav",
                "sourceSha256": "b" * 64,
                "startCueId": "cue-000003",
                "endCueId": "cue-000003",
                "startMs": 2000,
                "endMs": 2500,
                "reason": "Alternate answer",
            }
        ],
    },
    "title-binding-v1": {
        "schemaVersion": "tritrack.title-binding/v1",
        "bindingId": "basic-title-v1",
        "effectName": "Basic Title",
        "effectUid": ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti",
        "parameters": [
            {"name": "fontSize", "value": 72.0},
            {"name": "alignment", "value": "center"},
        ],
    },
    "transcript-bundle-v1": {
        "schemaVersion": "tritrack.transcript-bundle/v1",
        "profileId": "whisper-cpp-cpu-no-fallback-v1",
        "language": "zh",
        "modelSha256": "f" * 64,
        "engine": {
            "name": "whisper-cli",
            "version": "whisper.cpp version: 1.9.1",
        },
        "takes": [
            {
                "takeId": "A-001.MP4",
                "sourceSha256": "a" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 1250,
                        "text": "Invented local words.",
                    }
                ],
            },
            {
                "takeId": "A-002.MP4",
                "sourceSha256": "b" * 64,
                "status": "empty",
                "cues": [],
            },
        ],
    },
    "text-revision-v1": {
        "schemaVersion": "tritrack.text-revision/v1",
        "sourceBundleSha256": "1" * 64,
        "language": "en",
        "takes": [
            {
                "takeId": "Take-A.wav",
                "sourceSha256": "2" * 64,
                "revisions": [
                    {"cueId": "cue-000001", "text": "Corrected words"}
                ],
            }
        ],
    },
    "aligned-transcript-v1": {
        "schemaVersion": "tritrack.aligned-transcript/v1",
        "alignmentProfileId": "cue-addressed-v1",
        "sourceBundleSha256": "1" * 64,
        "revisionSha256": "3" * 64,
        "language": "en",
        "takes": [
            {
                "takeId": "Take-A.wav",
                "sourceSha256": "2" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 500,
                        "text": "Corrected words",
                        "disposition": "revised",
                    }
                ],
            }
        ],
    },
    "run-manifest-v1": {
        "schemaVersion": "tritrack.run-manifest/v1",
        "toolVersion": "0.1.0a0",
        "runId": "run-001",
        "profileId": "uhd-2997-ndf-fcpxml-1.14",
        "stages": [
            {
                "name": "sync",
                "status": "completed",
                "inputHashes": {"cameraA": "a" * 64, "cameraB": "b" * 64},
                "receiptSha256": "c" * 64,
            }
        ],
    },
    "provider-receipt-v1": {
        "schemaVersion": "tritrack.provider-receipt/v1",
        "provider": "gemini",
        "operation": "audio-transcription",
        "sourceBundleSha256": "1" * 64,
        "takeId": "Take-A.wav",
        "requestedModel": "gemini-test-model",
        "observedModel": "gemini-test-model",
        "audioSha256": "d" * 64,
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
    },
}


class ContractValidationTest(unittest.TestCase):
    def test_all_declared_contracts_accept_their_minimum_valid_shape(self):
        for name, payload in VALID_CONTRACTS.items():
            with self.subTest(name=name):
                contracts.validate_contract(name, payload)

    def test_all_declared_contracts_reject_unknown_fields(self):
        for name, payload in VALID_CONTRACTS.items():
            with self.subTest(name=name):
                changed = copy.deepcopy(payload)
                changed["unexpected"] = True
                with self.assertRaises(ValidationError):
                    contracts.validate_contract(name, changed)

    def test_all_declared_contracts_reject_version_drift(self):
        for name, payload in VALID_CONTRACTS.items():
            with self.subTest(name=name):
                changed = copy.deepcopy(payload)
                changed["schemaVersion"] = "tritrack.some-future-contract/v9"
                with self.assertRaises(ValidationError):
                    contracts.validate_contract(name, changed)

    def test_unknown_contract_name_is_not_a_resource_path(self):
        with self.assertRaisesRegex(ValueError, "TRITRACK_CONTRACT_UNKNOWN"):
            contracts.validate_contract("../provider-receipt-v1", {})

    def test_schema_resources_use_draft_2020_12(self):
        for name in VALID_CONTRACTS:
            with self.subTest(name=name):
                schema = contracts.load_schema(name)
                self.assertEqual(
                    schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
                )

    def test_task_8_contracts_reject_invalid_state_shapes(self):
        invalid_cases = []

        revision_without_cues = copy.deepcopy(VALID_CONTRACTS["text-revision-v1"])
        revision_without_cues["takes"][0]["revisions"] = []
        invalid_cases.append(("text-revision-v1", revision_without_cues))

        completed_without_cues = copy.deepcopy(
            VALID_CONTRACTS["aligned-transcript-v1"]
        )
        completed_without_cues["takes"][0]["cues"] = []
        invalid_cases.append(("aligned-transcript-v1", completed_without_cues))

        empty_with_cues = copy.deepcopy(VALID_CONTRACTS["aligned-transcript-v1"])
        empty_with_cues["takes"][0]["status"] = "empty"
        invalid_cases.append(("aligned-transcript-v1", empty_with_cues))

        missing_receipt_binding = copy.deepcopy(
            VALID_CONTRACTS["provider-receipt-v1"]
        )
        del missing_receipt_binding["sourceBundleSha256"]
        invalid_cases.append(("provider-receipt-v1", missing_receipt_binding))

        unsafe_take_id = copy.deepcopy(VALID_CONTRACTS["text-revision-v1"])
        unsafe_take_id["takes"][0]["takeId"] = "../Take-A.wav"
        invalid_cases.append(("text-revision-v1", unsafe_take_id))

        for name, payload in invalid_cases:
            with (
                self.subTest(name=name, payload=payload),
                self.assertRaises(ValidationError),
            ):
                contracts.validate_contract(name, payload)

    def test_task_9_contracts_reject_invalid_state_shapes(self):
        invalid_cases = []

        missing_binding = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
        del missing_binding["alignedTranscriptSha256"]
        invalid_cases.append(("grouping-v1", missing_binding))

        unsafe_question_id = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
        unsafe_question_id["questions"][0]["id"] = "../question"
        invalid_cases.append(("grouping-v1", unsafe_question_id))

        missing_answer_order = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
        del missing_answer_order["questions"][0]["answers"][0]["order"]
        invalid_cases.append(("grouping-v1", missing_answer_order))

        timing_in_grouping = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
        timing_in_grouping["questions"][0]["answers"][0]["startMs"] = 0
        invalid_cases.append(("grouping-v1", timing_in_grouping))

        text_in_segment = copy.deepcopy(VALID_CONTRACTS["working-cut-v1"])
        text_in_segment["segments"][0]["text"] = "Not a second authority"
        invalid_cases.append(("working-cut-v1", text_in_segment))

        wrong_profile = copy.deepcopy(VALID_CONTRACTS["working-cut-v1"])
        wrong_profile["organizationProfileId"] = "future-profile"
        invalid_cases.append(("working-cut-v1", wrong_profile))

        for name, payload in invalid_cases:
            with (
                self.subTest(name=name, payload=payload),
                self.assertRaises(ValidationError),
            ):
                contracts.validate_contract(name, payload)


if __name__ == "__main__":
    unittest.main()
