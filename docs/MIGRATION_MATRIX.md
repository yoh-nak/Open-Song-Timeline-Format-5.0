# OSTF 4.3 ⇄ 5.0 — Migration, binding and information-loss rules (5.0.0)

## Representation-preserving operations

| Input/operation | Exact rule |
|---|---|
| Read 4.3 Score | Select the 4.3 Schema and semantics by exact `version`; no silent conversion |
| Package a 4.3 Score | Include its unchanged raw bytes, record `manifest.score.version="4.3.0"` and original SHA |
| Package 4.3 + Production0.2 or Distributed0.2 | Preserve 4.3 Score byte pin, matching Profile version and original identity; packaging is not authorization to execute |
| Package 5.0 + Production0.3 or Distributed0.3 | Preserve 5.0 Score raw-byte pin and use a separately versioned Profile; do not relabel 0.2 |
| Package ↔ Project Directory | Preserve each Score/Profile/Asset member byte-for-byte and corresponding Manifest references; regenerated ZIP metadata need not be byte-identical |
| Consume partial Plugin Context | The payload is only a view; do not infer omitted fields or serialize it as a full `.ostf` |

## Explicit Score conversion 4.3 → 5.0

1. Load the 4.3 file with its **official adopted Schema**, retain raw source bytes, digest and any document/revision identifiers.
2. Since Core5 inherits all 127 music definitions unchanged, preserve musical data and explicitly write a **new** Score with `version:"5.0.0"`; do not invent missing optional fields.
3. Compute the new SHA-256 from the exact **new UTF-8 byte sequence**, not from parsed-JSON normalization. Any document/revision change must be consistent with Core identity semantics and actual save operation.
4. Do **not** auto-relabel Production0.2 as0.3. Check the changed Score pin, every referenced track/device/asset and the 0.3 numeric automation type/domain restrictions. Refuse unsupported non-lossy migration or make an explicitly disclosed separate lossy export.
5. Treat Distributed0.2 as *historical* session data; never promote an active 4.3 session's participants, authority, clock anchors, or events by string substitution. A Score5 Session is a new session with explicitly selected ID, authority and Plan/Visit pin.
6. Reconstruct the Manifest from actual new Score/Profile bytes only. Never “fix” stale Profile bindings by editing their SHA field in isolation.

The inverse 5.0 → 4.3 operation is likewise a new Score serialization. Changing a version changes raw SHA; 0.3 Profiles cannot be attached to 4.3 without explicit translation. No claim of fully lossless *project* conversion follows from a valid Score-only conversion.

## Data-loss classification and minimum disclosure

- Only Score supplied → only Score exported: potentially **Score-scope lossless**; absent, never-supplied Profile assets are not a loss.
- Supplied Score + Production + WAV → Score-only export: **provided production information omitted** even if Score is intact.
- Supplied only URI/SHA asset descriptor → descriptor preserved, but audio/state **bytes not possessed**.
- Supplied plugin-state bytes without matching plugin → state bytes may be preserved; matching DSP/audio **not proven**.
- Supplied unknown extensions → preserve original data or refuse lossless save; disclose affected IDs/JSON pointers and any approximation.
- Stale Score pin → explicit reattachment or a new session required; never rehash old Profile silently.
- Rejected edit proposal → source Score, Sessions and Assets unchanged; `received` is not `applied`.

A loss report SHOULD identify operation, exact family/version, material actually provided, target save/export scope, affected stable IDs/JSON Pointers, category (`omitted`, `approximated`, `unavailable`, `unsupported`, `unresolved`, `stale_binding`), whether original bytes were preserved, and result (refused, explicitly lossy new artifact, or lossless within stated scope). This is a reporting vocabulary, **not a new mandatory file extension or Core field**.

## Boundaries

Packaging alone never edits JSON or grants external-fetch permission. Manifest asset existence is not plugin/license availability. Structural validation is not an audible-result guarantee. Execution tests and individual publisher approvals are explicitly excluded from this user's GO gate, and must not be misreported as completed.
