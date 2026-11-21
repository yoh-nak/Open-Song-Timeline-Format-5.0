# OSTF 5.0 — Exact format identity and provisional identifiers (5.0.0)

This is the **specification-internal registry**, not an IANA registration or a hosted web endpoint. The exact wire discriminators below are normative for choosing the corresponding JSON Schema. A host MUST NOT infer family/version from file extension, ZIP filename, draft number or another document's version.

| Logical record | Required discriminator | Schema | Relationship |
|---|---|---|---|
| Score5 (`.ostf`) | `format:"OSTF"`, `version:"5.0.0"` | `schema/ostf-5.0.0.schema.json` | The musical authority |
| Score4.3 (legacy) | `format:"OSTF"`, `version:"4.3.0"` | `adopted-4.3/schema/ostf-4.3.0.schema.json` | Accepted unchanged into an OSTFP |
| Production0.3 | `profile:"OSTF-Production-Session"`, `profileVersion:"0.3.0"` | `schema/ostf-production-session-0.3.schema.json` | Only a pinned Score5 |
| Production0.2 | same `profile`, `profileVersion:"0.2.0"` | `adopted-4.3/schema/ostf-production-session-0.2.schema.json` | Only a pinned Score4.3 |
| Distributed0.3 | `profile:"OSTF-Distributed-Session-0.3"`, `recordType:"snapshot"|"event"` | `schema/ostf-distributed-session-0.3.schema.json` | Root `scoreSha256` pins Score5; **no** `profileVersion` or nested `score` |
| Distributed0.2 | `profile:"OSTF-Distributed-Session-0.2"`, `recordType` | `adopted-4.3/schema/ostf-distributed-session-0.2.schema.json` | Pins Score4.3 |
| Project manifest | `packageFormat:"OSTFP"`, `packageVersion:"1.0.0"` | `schema/ostf-package-manifest-1.0.schema.json` | One Score, optional session/asset bytes |
| Plugin Context | `protocol:"OSTF-Plugin-Context"`, `protocolVersion:"1.0.0"` | `schema/ostf-plugin-context-1.0.schema.json` | Operation-specific logical message, Score 4.3/5.0 permitted |

**Exact Manifest document-version mapping:** `documents[].version` for Production is `0.2.0`/`0.3.0`; for Distributed it is `0.2`/`0.3`, since the Distributed profile literal itself names that version and has no `profileVersion`. The manifest descriptor `family` must equal the underlying production/distributed `profile` literal. The paired `role` is `productionSession`/`distributedSession` respectively.

**Byte identifiers:** all Score pins and member digests refer to exact source UTF-8 bytes or raw binary bytes, not a canonicalized JSON tree. A schema URL in `$id` is an identifier; its current use does not promise HTTP availability. **MIME**: OSTFP's first ZIP member must contain exactly the proposed, as-yet-unregistered ASCII string `application/vnd.ostf-project+zip`. Hosts SHOULD dispatch with the exact manifest and ZIP signature, not assume a registered MIME database already recognizes this proposed value.

**Revision handling:** editing a Score creates new Score bytes/digest. Production needs an explicitly validated rebind; Distributed needs a fresh Session pin and independent authority. Plugin `ack:received` does not mean persist/commit. User or host permissions are external to all serialized records. The data-format version numbers here do **not** imply equal releases of VST3/AU/CLAP or a DAW binary.
