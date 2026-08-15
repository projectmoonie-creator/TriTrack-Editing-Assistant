"""Invented, public-safe Task 9 fixtures shared by focused tests."""


ALIGNED_SHA256 = "a" * 64
GROUPING_SHA256 = "b" * 64


def invented_aligned() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.aligned-transcript/v1",
        "alignmentProfileId": "cue-addressed-v1",
        "sourceBundleSha256": "1" * 64,
        "revisionSha256": "2" * 64,
        "language": "en",
        "takes": [
            {
                "takeId": "A.wav",
                "sourceSha256": "3" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 500,
                        "text": "Invented first answer.",
                        "disposition": "original",
                    },
                    {
                        "cueId": "cue-000002",
                        "startMs": 500,
                        "endMs": 1100,
                        "text": "Invented continuation.",
                        "disposition": "revised",
                    },
                ],
            },
            {
                "takeId": "B.wav",
                "sourceSha256": "4" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 100,
                        "endMs": 700,
                        "text": "Invented second answer.",
                        "disposition": "original",
                    },
                    {
                        "cueId": "cue-000002",
                        "startMs": 900,
                        "endMs": 1400,
                        "text": "Invented reserve.",
                        "disposition": "original",
                    },
                ],
            },
            {
                "takeId": "C.wav",
                "sourceSha256": "5" * 64,
                "status": "empty",
                "cues": [],
            },
        ],
    }


def invented_grouping() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.grouping/v1",
        "alignedTranscriptSha256": ALIGNED_SHA256,
        "questions": [
            {
                "id": "question-001",
                "question": "What changed?",
                "order": 1,
                "answers": [
                    {
                        "id": "answer-001",
                        "order": 1,
                        "takeId": "A.wav",
                        "startCueId": "cue-000001",
                        "endCueId": "cue-000002",
                        "note": "Primary invented answer",
                    }
                ],
            },
            {
                "id": "question-002",
                "question": "What comes next?",
                "order": 2,
                "answers": [
                    {
                        "id": "answer-002",
                        "order": 1,
                        "takeId": "B.wav",
                        "startCueId": "cue-000001",
                        "endCueId": "cue-000001",
                    }
                ],
            },
        ],
        "reserve": [
            {
                "id": "reserve-001",
                "order": 1,
                "takeId": "B.wav",
                "startCueId": "cue-000002",
                "endCueId": "cue-000002",
                "reason": "Alternate invented answer",
                "note": "Keep available",
            }
        ],
    }
