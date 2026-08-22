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
        "bindingId": "basic-title-v1",
        "phase": "prepared",
        "nextAction": "provide-revision",
        "manifestChain": [],
        "sources": [
            {
                "camera": "A",
                "mediaId": "A-001.MP4",
                "sha256": "a" * 64,
                "transcribed": True,
            }
        ],
        "artifacts": {
            "doctorReceipt": {"fileName": "doctor.json", "sha256": "b" * 64},
            "syncMap": {"fileName": "sync-map.json", "sha256": "c" * 64},
            "transcriptBundle": {
                "fileName": "transcript-bundle.json",
                "sha256": "d" * 64,
            },
            "stringOut": {
                "fileName": "string-out.fcpxml",
                "sha256": "e" * 64,
            },
        },
        "stages": [
            {
                "name": "doctor",
                "inputHashes": {"profile": "f" * 64},
                "outputHashes": {"doctorReceipt": "b" * 64},
            },
            {
                "name": "sync",
                "inputHashes": {"sourceSet": "1" * 64},
                "outputHashes": {"syncMap": "c" * 64},
            },
            {
                "name": "transcribe",
                "inputHashes": {"transcribedSources": "2" * 64},
                "outputHashes": {"transcriptBundle": "d" * 64},
            },
            {
                "name": "emit",
                "inputHashes": {"syncMap": "c" * 64},
                "outputHashes": {"stringOut": "e" * 64},
            },
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

VALID_CONTRACTS.update(
    {
        "sync-map-v2": {
            "schemaVersion": "tritrack.sync-map/v2",
            "profileId": "uhd-2997-ndf-fcpxml-1.14",
            "driftPrior": {
                "centreSeconds": 8.0,
                "toleranceSeconds": 2.0,
                "sampleCount": 5,
            },
            "groups": [
                {
                    "groupId": "group-001",
                    "anchor": {
                        "camera": "A",
                        "mediaId": "anchor.mov",
                        "durationSeconds": 600.0,
                        "startedAt": None,
                    },
                    "sources": [
                        {
                            "camera": "B",
                            "mediaId": "relay.mov",
                            "offsetFromAnchorSeconds": 0.0,
                            "durationSeconds": 300.0,
                            "confidence": 8.0,
                            "overlapSeconds": 300.0,
                            "match": "correlation",
                            "startedAt": None,
                        }
                    ],
                    "audioMaster": "A",
                }
            ],
            "singles": [{"camera": "B", "mediaId": "single.mov"}],
            "warnings": [],
        },
        "transcription-report-v1": {
            "schemaVersion": "tritrack.transcription-report/v1",
            "profileId": "whisper-cpp-cpu-no-fallback-v1",
            "requestedTakeIds": ["take-001"],
            "runSettings": {
                "language": "zh",
                "recognitionModelSha256": "f" * 64,
                "voiceActivity": "off",
                "voiceActivityModel": None,
            },
            "takes": [
                {
                    "takeId": "take-001",
                    "status": "completed",
                    "selectedSourceSha256": "a" * 64,
                    "attempts": [
                        {
                            "ordinal": 1,
                            "sourceSha256": "a" * 64,
                            "outcome": "completed",
                            "failureCode": None,
                            "settings": {
                                "language": "zh",
                                "recognitionModelSha256": "f" * 64,
                                "voiceActivity": "off",
                                "voiceActivityModel": None,
                            },
                        }
                    ],
                }
            ],
        },
        "transcription-result-manifest-v1": {
            "schemaVersion": "tritrack.transcription-result-manifest/v1",
            "bundle": {
                "fileName": "transcript-bundle.json",
                "sha256": "a" * 64,
            },
            "report": {
                "fileName": "transcription-report.json",
                "sha256": "b" * 64,
            },
        },
        "transcription-report-v2": {
            "schemaVersion": "tritrack.transcription-report/v2",
            "profileId": "whisper-cpp-cpu-no-fallback-v1",
            "requestedTakeIds": ["take-001"],
            "runSettings": {
                "language": "zh",
                "recognitionModelSha256": "f" * 64,
                "voiceActivity": "off",
                "voiceActivityModel": None,
            },
            "sparsePolicy": {
                "charactersPerSecond": 1.0,
                "minimumDurationMs": 30000,
                "contentDefinition": "unicode-letters-numbers-symbols-v1",
            },
            "summary": {
                "sourceAttemptCount": 1,
                "sparseSourceCount": 0,
                "retryAttemptCount": 0,
                "rescuedTakeCount": 0,
                "unrescuedTakeCount": 0,
            },
            "takes": [
                {
                    "takeId": "take-001",
                    "status": "completed",
                    "selectedSourceSha256": "a" * 64,
                    "selectionReason": "primary-usable",
                    "sharedAlternativeWithTakeIds": [],
                    "attempts": [
                        {
                            "ordinal": 1,
                            "sourceSha256": "a" * 64,
                            "outcome": "completed",
                            "failureCode": None,
                            "settings": {
                                "language": "zh",
                                "recognitionModelSha256": "f" * 64,
                                "voiceActivity": "off",
                                "voiceActivityModel": None,
                            },
                            "metrics": {
                                "durationMs": 60000,
                                "characterCount": 180,
                                "charactersPerSecond": "3.000",
                                "sparse": False,
                            },
                        }
                    ],
                }
            ],
        },
        "transcription-result-manifest-v2": {
            "schemaVersion": "tritrack.transcription-result-manifest/v2",
            "bundle": {
                "fileName": "transcript-bundle.json",
                "sha256": "a" * 64,
            },
            "report": {
                "fileName": "transcription-report.json",
                "sha256": "b" * 64,
            },
            "densityTable": {
                "fileName": "transcription-density.txt",
                "sha256": "c" * 64,
            },
        },
    }
)

_RUN_MANIFEST_V2 = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
_RUN_MANIFEST_V2["schemaVersion"] = "tritrack.run-manifest/v2"
_RUN_MANIFEST_V2["artifacts"].update(
    {
        "transcriptionReport": {
            "fileName": "transcription-report.json",
            "sha256": "6" * 64,
        },
        "transcriptionResult": {
            "fileName": "transcription-result-manifest.json",
            "sha256": "7" * 64,
        },
    }
)
_RUN_MANIFEST_V2["stages"][2]["outputHashes"].update(
    {
        "transcriptionReport": "6" * 64,
        "transcriptionResult": "7" * 64,
    }
)
VALID_CONTRACTS["run-manifest-v2"] = _RUN_MANIFEST_V2
_RUN_MANIFEST_V3 = copy.deepcopy(_RUN_MANIFEST_V2)
_RUN_MANIFEST_V3["schemaVersion"] = "tritrack.run-manifest/v3"
_RUN_MANIFEST_V3["artifacts"]["transcriptionDensity"] = {
    "fileName": "transcription-density.txt",
    "sha256": "8" * 64,
}
_RUN_MANIFEST_V3["stages"][2]["outputHashes"]["transcriptionDensity"] = "8" * 64
VALID_CONTRACTS["run-manifest-v3"] = _RUN_MANIFEST_V3


class ContractValidationTest(unittest.TestCase):
    def test_task_14_contract_names_are_closed_and_installed(self):
        self.assertTrue(
            {
                "sync-map-v2",
                "transcription-report-v1",
                "transcription-result-manifest-v1",
                "run-manifest-v2",
            }.issubset(contracts.CONTRACT_NAMES)
        )

    def test_v2_sparse_contract_names_are_closed_and_installed(self):
        self.assertTrue(
            {
                "transcription-report-v2",
                "transcription-result-manifest-v2",
                "run-manifest-v3",
            }.issubset(contracts.CONTRACT_NAMES)
        )

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

    def test_task_10_manifest_rejects_mutable_or_phase_inconsistent_state(self):
        invalid_cases = []

        mutable_stage = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
        mutable_stage["stages"][0]["status"] = "running"
        invalid_cases.append(mutable_stage)

        timestamped = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
        timestamped["createdAt"] = "2026-08-17T00:00:00Z"
        invalid_cases.append(timestamped)

        wrong_next_action = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
        wrong_next_action["nextAction"] = "complete"
        invalid_cases.append(wrong_next_action)

        wrong_chain_length = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
        wrong_chain_length["manifestChain"] = ["9" * 64]
        invalid_cases.append(wrong_chain_length)

        extra_artifact = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
        extra_artifact["artifacts"]["workingCut"] = {
            "fileName": "working-cut.json",
            "sha256": "8" * 64,
        }
        invalid_cases.append(extra_artifact)

        duplicate_source = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
        duplicate_source["sources"].append(
            copy.deepcopy(duplicate_source["sources"][0])
        )
        invalid_cases.append(duplicate_source)

        for payload in invalid_cases:
            with self.subTest(payload=payload), self.assertRaises(ValidationError):
                contracts.validate_contract("run-manifest-v1", payload)

    def test_task_14_report_rejects_text_paths_and_implicit_settings(self):
        invalid_cases = []

        with_text = copy.deepcopy(VALID_CONTRACTS["transcription-report-v1"])
        with_text["takes"][0]["attempts"][0]["text"] = "not report authority"
        invalid_cases.append(with_text)

        with_path = copy.deepcopy(VALID_CONTRACTS["transcription-report-v1"])
        with_path["takes"][0]["attempts"][0]["path"] = "/invented/source.mov"
        invalid_cases.append(with_path)

        missing_off_setting = copy.deepcopy(
            VALID_CONTRACTS["transcription-report-v1"]
        )
        del missing_off_setting["runSettings"]["voiceActivity"]
        invalid_cases.append(missing_off_setting)

        for payload in invalid_cases:
            with self.subTest(payload=payload), self.assertRaises(ValidationError):
                contracts.validate_contract("transcription-report-v1", payload)

    def test_task_14_result_manifest_rejects_unsafe_file_names(self):
        payload = copy.deepcopy(
            VALID_CONTRACTS["transcription-result-manifest-v1"]
        )
        payload["bundle"]["fileName"] = "../transcript-bundle.json"

        with self.assertRaises(ValidationError):
            contracts.validate_contract("transcription-result-manifest-v1", payload)

    def test_v2_report_requires_metrics_on_every_attempt(self):
        payload = copy.deepcopy(VALID_CONTRACTS["transcription-report-v2"])
        del payload["takes"][0]["attempts"][0]["metrics"]

        with self.assertRaises(ValidationError):
            contracts.validate_contract("transcription-report-v2", payload)

    def test_v2_sparse_outcome_requires_sparse_metrics(self):
        payload = copy.deepcopy(VALID_CONTRACTS["transcription-report-v2"])
        attempt = payload["takes"][0]["attempts"][0]
        attempt["outcome"] = "sparse"
        attempt["metrics"]["sparse"] = False

        with self.assertRaises(ValidationError):
            contracts.validate_contract("transcription-report-v2", payload)

    def test_v2_completed_attempt_requires_measured_metrics(self):
        payload = copy.deepcopy(VALID_CONTRACTS["transcription-report-v2"])
        payload["takes"][0]["attempts"][0]["metrics"] = {
            "durationMs": None,
            "characterCount": None,
            "charactersPerSecond": None,
            "sparse": None,
        }

        with self.assertRaises(ValidationError):
            contracts.validate_contract("transcription-report-v2", payload)

    def test_v2_result_manifest_requires_density_table(self):
        payload = copy.deepcopy(
            VALID_CONTRACTS["transcription-result-manifest-v2"]
        )
        del payload["densityTable"]

        with self.assertRaises(ValidationError):
            contracts.validate_contract("transcription-result-manifest-v2", payload)


if __name__ == "__main__":
    unittest.main()
