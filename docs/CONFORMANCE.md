# OSTF 5.0 — Capability-by-capability conformance (5.0.0)

An implementation shall state the **exact family and version, operation and subset** it supports. The bare claim "fully OSTF 5.0 compatible" does not establish any of the capabilities below. Semantic conformity extends beyond structural JSON Schema acceptance. Reader, writer, audio executor and permissions are separate competencies.

| Capability declaration | Minimum scope of an honest claim | Does NOT establish |
|---|---|---|
| `score-read` / `score-write` | Specific Score 4.3.0/5.0.0 Schema and the semantics of advertised Core fields; lossless writers preserve unknown data or explicitly refuse/report loss | Mix/asset/project, third-party DAW playback |
| `project-read` / `project-write` | OSTFP 1.0 ZIP/Directory inventory; exact source byte hashes; relative path safety; Score/Profile/Asset member and binding rules | Plugin binary availability, audio restoration or licenses |
| `production-read` / `production-write` | Exact Production0.2/0.3 profile and Score pin; explicit coverage of Channel/Mixer/Audio Region/Device/Automation/Sidechain | Unimplemented rack/warp/comp/surround or identical DSP |
| `distributed-read` | Exact Distributed0.2/0.3 `snapshot`/`event`, Source Score SHA/Revision/Plan pins, and preservation of unrecognized records | Live network transport or robotic actuation |
| `distributed-authority` | External authority policy, state-revision events, replay prevention and correct Visit/Plan semantics, for the declared version | Authentication or permissions granted by JSON content |
| `plugin-context-consume` | View a scoped partial Context without inventing omitted Core data; distinguish host and Score PPQ | Standardized VST3/AU/CLAP host delivery protocol |
| `plugin-edit-propose` | Send SHA/Revision-bound, atomic, stable-ID/Pointer-based proposals | Host applying the proposal |
| `plugin-edit-apply` | Externally authorized all-or-nothing host commit and actual persisted-byte Ack | Automatic Production rebinding or Distributed Session transfer |
| `loss-report` | Identify inputs actually supplied, export scope, affected IDs/Pointers, missing bytes, unsupported or approximated data and observed result | Claims that nonexistent input data was "lost" |

A VST that displays chords can implement Score read plus Plugin Context consume without claiming OSTFP or mixer support. A full DAW can declare Project write without claiming exact third-party DSP equivalence. Unknown optional data may be preserved as uninterpreted bytes; preservation is **not** evidence of semantic understanding or execution. A partial Score export from an input containing supplied Production/audio is a partial export, even if Score bytes are preserved.

Conformance requires documented behavior and the version-specific semantic constraints in `SPECIFICATION.md`, `PACKAGE_SPECIFICATION.md`, `PRODUCTION_SESSION_0_3.md`, `DISTRIBUTED_SESSION_0_3_SPECIFICATION.md`, `PLUGIN_EXCHANGE_PROTOCOL.md`, the Schema and adopted 4.3 sources. This development package does **not** claim runtime conformance tests, independent parsers or certification of any actual DAW, plug-in, Web service or robotic host.
