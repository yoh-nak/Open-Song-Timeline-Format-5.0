# Open Song Timeline Format (OSTF) 5.0.0

**Version: 5.0.0 — Official written specification release**  
**Two file forms:** `.ostf` (OSTF TEXT, UTF-8 JSON) and `.ostfp` (OSTF PROJECT, ZIP container)  
**Release date:** 2026-11-22

OSTF is an open, DAW-independent description of music, harmony, lyrics, MIDI, phrase structure, performance intent and optional project/production state. **Score 5.0 retains all musical Core definitions of publisher-adopted 4.3.0.** No ZIP is required for copying an OSTF TEXT Score into AI, Max for Live, a browser or plug-in. `.ostfp` is the optional transport for the Score, audio assets, session JSON and preset/state bytes while keeping each file unchanged.

OSTF does **not** implement a DAW, VST/AU/CLAP host, a sound engine or a remote robotic service. VST3/AU/CLAP/Max for Live/AI clients may implement the defined partial Plugin Context and safely propose edits; the host retains permissions and saving authority.

## Start here

| Information | English | 日本語 |
|---|---|---|
| Official normative specification | [Specification](docs/SPECIFICATION.md) | [正式仕様](docs/SPECIFICATION.ja.md) |
| **Complete manual** | [Complete Manual](docs/COMPLETE_MANUAL.md) | [全網羅マニュアル](docs/COMPLETE_MANUAL.ja.md) |
| **Complete field reference** | [Parameter Reference](docs/PARAMETER_REFERENCE.md) | [全網羅パラメーターリファレンス](docs/PARAMETER_REFERENCE.ja.md) |
| Project ZIP and manifest | [Package](docs/PACKAGE_SPECIFICATION.md) | [パッケージ](docs/PACKAGE_SPECIFICATION.ja.md) |
| Audio, mixer, plugin state | [Production Session 0.3](docs/PRODUCTION_SESSION_0_3.md) | [制作Session 0.3](docs/PRODUCTION_SESSION_0_3.ja.md) |
| AI / distributed ensemble | [Distributed Session 0.3](docs/DISTRIBUTED_SESSION_0_3_SPECIFICATION.md) | [分散Session 0.3](docs/DISTRIBUTED_SESSION_0_3_SPECIFICATION.ja.md) |
| VST3 / AU / CLAP / M4L / AI context | [Plugin Context](docs/PLUGIN_EXCHANGE_PROTOCOL.md) | [プラグイン連携](docs/PLUGIN_EXCHANGE_PROTOCOL.ja.md) |
| **All samples** | [Example catalog](docs/EXAMPLES_GUIDE.md) | [全サンプル一覧](docs/EXAMPLES_GUIDE.ja.md) |
| Upgrade / data loss | [Migration](docs/MIGRATION_MATRIX.md) | [移行ルール](docs/MIGRATION_MATRIX.ja.md) |
| Conformance and host claims | [Conformance](docs/CONFORMANCE.md) | [適合能力](docs/CONFORMANCE.ja.md) |
| Safety & import | [Security](docs/SECURITY.md) | [セキュリティ](docs/SECURITY.ja.md) |

## Schemas and sample assets

- **5 JSON Schemas** in [`schema/`](schema/): Score5, Production0.3, Distributed0.3, Package Manifest1.0, Plugin Context1.0.
- **25 standalone OSTF TEXT scores** in [`examples/score/`](examples/score/): jazz, pop/vocals, techno, guitar, lyrics, phrase library, complex repeats, multi-voice and ensemble cases.
- **11 self-contained OSTFP archives** in [`examples/ostfp/`](examples/ostfp/): Score-only, audio and plugin-state stubs, distributed and production sessions, legacy Score4.3 and combined production+distributed scenarios.
- Supplemental JSON examples: [`examples/production/`](examples/production/), [`examples/distributed/`](examples/distributed/), [`examples/plugin/`](examples/plugin/).
- Original 4.3 adopted source: [`adopted-4.3/`](adopted-4.3/), kept **byte-identical**. This supplies full inherited normative manuals and parameter semantics.

## Reference tools

```bash
python -m pip install jsonschema
python tools/validate_examples.py
python tools/ostfp.py validate examples/ostfp/11-combined-production-distributed.ostfp
```

The included tools perform **static checks only**, not independent DAW/VST3/AU/CLAP/Max for Live/AI/robot execution tests, DSP equivalence, rights review or a security certification. The user intentionally excluded execution tests and individual approvals from the written-release GO conditions; such tests are **not represented as completed**.

## Exact family/version handling

- `.ostf` root: `format:"OSTF"` and `version:"5.0.0"`; standalone, directly editable JSON.
- `.ostfp`: ZIP with stored first member `mimetype` (proposed unregistered `application/vnd.ostf-project+zip`) and second member `manifest.json` version `1.0.0`.
- `Production Session`: `profileVersion:"0.3.0"`, bound to Score5 exact UTF-8 byte SHA.
- `Distributed Session`: `profile:"OSTF-Distributed-Session-0.3"`, bound by root `scoreSha256`, separate Snapshot/Event objects.
- `Plugin Context`: `protocolVersion:"1.0.0"`, partial read-only views and atomic, host-authorized edit proposals.
- Legacy 4.3 score and original matching companion versions remain valid in `.ostfp` as legacy documents, without relabeling.

## License, attribution and interoperability limits

Author-controlled specification and sample text/Schema: CC0 1.0 in [LICENSE](LICENSE); original reference tools: MIT in [LICENSE-CODE](LICENSE-CODE). [LICENSE-POLICY](LICENSE-POLICY.md), [NOTICE](NOTICE.md) and [provenance](docs/PROVENANCE.md) describe the scope. No rights over commercial audio, presets, copyrighted music or third-party plug-ins are granted. The package MIME is an **unregistered proposal**; Schema `$id` identifiers do not guarantee web hosting.

The written specification is ready for publication as v5.0.0. Repository upload, tag creation and third-party deployment are separate actions; creating this archive does not perform them.
