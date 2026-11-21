# Open Song Timeline Format 5.0.0 — Specification

**Release:** v5.0.0 · 2026-11-22 · Open Song Timeline Format (OSTF)

This publication specifies two interoperable file forms: **OSTF TEXT** (`.ostf`, BOM-free UTF-8 JSON Score) and **OSTF PROJECT** (`.ostfp`, ZIP container). Optional independently versioned document families are Production Session 0.3.0 and Distributed Session 0.3; Plugin Context Exchange 1.0 is a logical host/plugin message contract, **not a third file type or standardized real-time plug-in API**.

The publisher-adopted 4.3.0 Score musical grammar is retained, except for the exact Score root `version` discriminator `"5.0.0"`. The formally versioned Schema for each family is the structural authority; the adopted 4.3 normative texts remain the source of unchanged semantic rules. Explicit 5.0 deltas and package rules below take precedence only within their stated scope. Unknown meaning is not guessed, data loss is disclosed, external assets are not fetched or executed without host permission, and no plugin or DAW is certified by this document.

## Document selection and normative precedence

| Family | Required identification | Structural source | Semantic details |
|---|---|---|---|
| Score 5 | `format:"OSTF"`, `version:"5.0.0"` | `../schema/ostf-5.0.0.schema.json` | `SEMANTIC_DELTA_REFERENCE` (embedded in the complete manual), inherited 4.3 Score specification |
| Production 0.3 | `profile:"OSTF-Production-Session"`, `profileVersion:"0.3.0"` | `../schema/ostf-production-session-0.3.schema.json` | `PRODUCTION_SESSION_0_3.md` and inherited Production 0.2 |
| Distributed 0.3 | `profile:"OSTF-Distributed-Session-0.3"`, `recordType:"snapshot"|"event"` | `../schema/ostf-distributed-session-0.3.schema.json` | `DISTRIBUTED_SESSION_0_3_SPECIFICATION.md` and inherited Distributed 0.2 |
| Project Package 1 | `packageFormat:"OSTFP"`, `packageVersion:"1.0.0"` | `../schema/ostf-package-manifest-1.0.schema.json` | `PACKAGE_SPECIFICATION.md` |
| Plugin Context 1 | `protocol:"OSTF-Plugin-Context"`, `protocolVersion:"1.0.0"` | `../schema/ostf-plugin-context-1.0.schema.json` | `PLUGIN_EXCHANGE_PROTOCOL.md` |

Legacy Score 4.3.0 and its original Production 0.2.0 and Distributed 0.2 documents remain valid **at their original exact version**, and can be included inside OSTFP 1.0. They must not be silently relabeled to 5.0 or the newer companion versions. The adopted 4.3 source documents are preserved byte-for-byte under `../adopted-4.3/`. The integrated `COMPLETE_MANUAL.md` and `PARAMETER_REFERENCE.md` cover the complete inherited vocabulary plus the 5.0 semantics and Schema structural declarations. `MIGRATION_MATRIX.md`, `CONFORMANCE.md` and `SECURITY.md` define migration and host limitations.

## Normative implementation principles

- A Score's SHA-256 is calculated on **its original exact UTF-8 bytes**, not reserialized or canonicalized JSON; a content change invalidates the old digest.
- OSTFP ZIP packaging **MUST NOT rewrite** the content bytes of the enclosed Score, Production/Distributed JSON, or Assets. Document bindings use package-root paths, and unknown/unavailable material is never silently replaced.
- Production audio mixer Gain/Pan/Sends and Core MIDI CC Volume/Expression/Effect control are separate authorities; JSON profile records cannot execute plug-ins or guarantee identical audio.
- Distributed Session stores collaboration state and proposes/commits phrases in its own domain; it does not automatically mutate Core notes, and its Score pin uses root `scoreSha256`.
- Plugin Context contains read-only partial projections or untrusted edits. A host must validate original Snapshot IDs, paths, permissions, all changes atomically and the new saved bytes before issuing an `applied` acknowledgement.
- For each operation, an implementation MUST declare the exact family/version and implemented capabilities; advertising generic “OSTF compatible” is insufficient to guarantee all features.

## Normative family texts

Read the five versioned Schemas together with `PACKAGE_SPECIFICATION.md`, `PRODUCTION_SESSION_0_3.md`, `DISTRIBUTED_SESSION_0_3_SPECIFICATION.md`, `PLUGIN_EXCHANGE_PROTOCOL.md`, and the inherited 4.3 documents. The precise Schema takes precedence for types, required fields, structural unions and value bounds; the accompanying text governs semantic constraints beyond JSON Schema.

Runtime, independently developed parser, DAW/VST3/AU/CLAP/Max for Live and DSP/WAN interoperability testing were not criteria for this **written specification** release and are not claimed to have occurred. Schema acceptance alone does not establish implementation conformance or software execution safety.
