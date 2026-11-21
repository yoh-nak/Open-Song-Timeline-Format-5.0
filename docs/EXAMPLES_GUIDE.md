# OSTF 5.0.0 — Complete examples catalog (English)

Every file in `examples/score/` is an independent, valid **OSTF 5.0.0 Score JSON**. Each comes from one of the 25 publisher-adopted 4.3 examples: conversion changes **only the root version label** to 5.0.0 and retains the original musical content. The originals remain available in the independent 4.3 release; do not assume the conversion changes music semantics. Archive samples in `examples/ostfp/` are **real ZIP files** whose member 0 is `mimetype` and member 1 is `manifest.json`. Some include inert demonstration audio and fictional invalid plug-in state; those are not playable commercial presets.

## All 25 standalone OSTF TEXT files

| Name | Musical focus |
|---|---|
| `01-minimal.ostf` | Minimal required Score object |
| `02-guitar-solo.ostf` | Guitar melody and solo notes |
| `03-jazz-comping.ostf` | Jazz harmony, comping and multiple tracks |
| `04-aaba-performance-plan.ostf` | Finite AABA performance plan / repeat visits |
| `05-rnb-vocal-open.ostf` | R&B vocal intent and open realization |
| `06-scat.ostf` | Scat and non-lexical vocalization |
| `07-vocal-alternatives.ostf` | Lyric and melody alternatives |
| `08-gospel-response.ostf` | Gospel call-and-response ensemble |
| `09-techno-variation.ostf` | Techno pattern and motivic variations |
| `10-physical-robot-requirements.ostf` | Performance requirements and physical-agent constraints (data only) |
| `11-harmony-plus-phrasing.ostf` | Harmony and phrasing direction |
| `12-visit-scoped-response.ostf` | Visit-scoped response interaction |
| `13-fixed-notes-and-directions.ostf` | Fixed notes versus directions |
| `14-tempo-map-reentry.ostf` | Tempo-map reentry and revisit |
| `15-vocal-response-phrasing.ostf` | Vocal response with phrasing |
| `16-inherited-comprehensive-core.ostf` | Broad inherited 4.x Core feature coverage |
| `17-fixed-note-source-cut.ostf` | Source note cut and partial visit |
| `18-visit-role-override.ostf` | Visit role override |
| `19-concurrent-voice-directions.ostf` | Concurrent multi-voice directions |
| `20-phrasing-with-motif-reference.ostf` | Motif library reference and phrasing |
| `21-visit-and-range-intersection.ostf` | Visit and source-range intersection |
| `22-pinned-session-aaba.ostf` | Pinned session AABA music material |
| `23-range-visit-and-label.ostf` | Range visit and label |
| `24-intra-track-voices-response.ostf` | Two lyric voices on the same Track |
| `25-source-note-repeated-visits.ostf` | Repeated source-note visits |

## OSTF PROJECT archives / OSTFPパッケージ（11件）

| File | Purpose / 内容 |
|---|---|
| `01-score-only.ostfp` | Score-only archive |
| `02-audio-stub.ostfp` | Score plus declared synthetic silence |
| `03-score-production.ostfp` | Production audio region and Asset binding |
| `04-inert-plugin-state.ostfp` | Fictional inert plugin state and source audio |
| `05-score-distributed-session.ostfp` | Distributed Snapshot, Plan and Score pin |
| `06-legacy-4.3-compatible.ostfp` | Legacy 4.3 Score packaged without relabeling |
| `07-guitar-solo.ostfp` | Guitar score as a portable project |
| `08-techno-variation.ostfp` | Techno phrasing as a project |
| `09-vocal-alternatives.ostfp` | Vocal alternatives in portable form |
| `10-comprehensive-core.ostfp` | Broad-feature Score inside project ZIP |
| `11-combined-production-distributed.ostfp` | Score, Production audio, Distributed snapshot together |

## Additional standalone JSON documents / その他のJSON例

- **Production 0.3**: `01-production-03.json` (audio region with PCM sample descriptor), `03-boolean-and-device-automation-03.json` (Boolean, bypass and device controls). The actual referenced silent WAV bytes are embedded in OSTFP 02, 03, 04 and 11.
- **Distributed 0.3**: `01-prepared.json` (Snapshot before playback), `04-phrase-proposed.json` (Event), `06-playing-committed.json` (Snapshot with accepted phrase). Context and complete event sequences are inside the full 4.3 normative source and the OSTFP 05/11 examples.
- **Plugin Context 1.0**: `01-context.json`, `02-edit-proposal.json`, `04-stale-rejection.json`, `05-applied-with-new-score.json` distinguish read-only views, proposals, rejection and actual persisted acknowledgement.

## Extraction and verification

From the repository root run `python tools/validate_examples.py`. To validate a single project, run `python tools/ostfp.py validate examples/ostfp/01-score-only.ostfp`. To inspect manually, unzip any `.ostfp` and examine the first `mimetype` member, `manifest.json`, `score/song.ostf`, optional `sessions/` and `assets/`. Always use `manifest.score.sha256` on the raw uncompressed Score bytes. No package has the authority to override its source Score or grant license/host permission.
