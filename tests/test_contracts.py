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
        "questions": [
            {
                "id": "question-001",
                "question": "What changed?",
                "answers": [
                    {
                        "takeId": "take-001",
                        "startMs": 500,
                        "endMs": 2500,
                    }
                ],
            }
        ],
        "reserve": [
            {
                "takeId": "take-002",
                "startMs": 0,
                "endMs": 1000,
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


if __name__ == "__main__":
    unittest.main()
