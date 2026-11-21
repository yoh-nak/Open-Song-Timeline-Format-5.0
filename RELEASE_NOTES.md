# OSTF 5.0.0 — GitHub Release Notes

**Version:** 5.0.0  
**Recommended Git tag:** `v5.0.0`  
**Format:** OSTF TEXT `.ostf` and OSTF PROJECT `.ostfp`

## Highlights

**OSTF 5.0 unifies music text interchange and optional project packaging without changing the underlying 4.3 musical vocabulary.** Write songs and share their complete structured musical meaning as plain JSON. For full DAW-style project interchange, preserve the original Score, Production/Distributed Session documents and assets in the packaged form.

This source release provides 5 current JSON Schema families, full inherited 4.3 normative provenance (13 source files), English/Japanese **complete manuals**, **full field references** with 1,601 explicit Schema declarations, 25 standalone `.ostf` examples and 11 self-contained `.ostfp` examples. Includes optional static `tools/ostfp.py` and `tools/validate_examples.py`.

## New in 5.0

- **Production Session 0.3.0**: Score5-bound mixer, audio regions, plugin states, sends, sidechain and strictly typed automation.
- **Distributed Session 0.3**: explicit Snapshot/Event identity, score pin, state revisions and participant collaboration semantics; no automatic Core mutation.
- **Plugin Context Exchange 1.0**: read-only context projections and host-authorized atomic edit proposals for VST3, AU, CLAP, Max for Live, AI tools or DAWs.
- **OSTFP Package 1.0**: ZIP manifest, exact byte hashes, safe paths, optional local audio/presets and clear missing-asset/loss rules; 4.3 files can remain unchanged inside packages.

## Start here

Read [English README](README.md) / [日本語 README](README.ja.md), then [Complete Manual](docs/COMPLETE_MANUAL.md) or [全網羅マニュアル](docs/COMPLETE_MANUAL.ja.md). See [Reference](docs/PARAMETER_REFERENCE.md), [日本語リファレンス](docs/PARAMETER_REFERENCE.ja.md), and [Examples](docs/EXAMPLES_GUIDE.md).

## Scope and limitations

**This is a formal release of the written specification and examples, not a certification of implementations.** No DAW, audio/DSP, VST3/AU/CLAP/M4L, AI service, WAN or robot device was verified by this publication. Runtime, independent-parser and separate-approval gates were excluded by the user's publishing criteria; their exclusion must not be presented as passing tests. Commercial media rights, plugin licenses and the proposed unregistered MIME remain external obligations. Hosting and GitHub tag creation are separate manual actions.
