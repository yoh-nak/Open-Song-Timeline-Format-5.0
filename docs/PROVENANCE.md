# OSTF 5.0.0 — Official 4.3 inheritance and source provenance

The complete OSTF 5.0 Score's music grammar, Producer 0.3 Profile and Distributed 0.3 Profile are derived from the **publisher-adopted OSTF 4.3.0 specification archive**, preserving its source materials under `adopted-4.3/` byte-for-byte. The 4.3 source is not an unapproved development snapshot.

- Source archive: `OSTF_4.3.0_Publisher_Approved_Specification.zip` (external provenance, not nested inside this 100-file release)
- Source SHA-256: `1440d16a440ba26d679bf940fe4fc8a68c5ad86c9944c6e35471bbbc7fdd6351`
- This package includes 13 original adopted 4.3 formal Schema/reference/specification files. Original Draft comments inside those historical references are untouched and do not describe the current 5.0 status.
- Core5: full 4.3 Core 127 `$defs` inherited. Only the Score root exact `version` is 5.0.0.
- Production0.3: 4.3 Production0.2 14 `$defs` inherited, with Score5 pin and typed automation changes.
- Distributed0.3: 4.3 Distributed0.2 16 `$defs` inherited; exact version discriminator, source pin and state semantics are preserved according to 5.0 published deltas.
- Package Manifest1.0 and Plugin Context1.0 are new schemas; neither is part of 4.3 musical Core.

## Original file digests (exact bytes)

| Source path | SHA-256 |
|---|---|
| `adopted-4.3/docs/COMPLETE_MANUAL.md` | `25f4a52316861e9cb588a1374cc2eaa972d6f93bc362e9e66223dc3eaf15acfe` |
| `adopted-4.3/docs/PARAMETER_REFERENCE.md` | `d0d83af99a98701061713f52aaf7347fd2afb17068a68c7db3519298dc67dedf` |
| `adopted-4.3/docs/PRODUCTION_PARAMETER_REFERENCE.md` | `24cf4a3c53f3beffbe10bd934c24d809b9cc53ea867e7ef2652b9d68d749b8e2` |
| `adopted-4.3/docs/PRODUCTION_SESSION_PROFILE.ja.md` | `132ae206526eb92f4c042ce234bc702a95d7553ea51d4d603de8f6501594f023` |
| `adopted-4.3/docs/PRODUCTION_SESSION_PROFILE.md` | `42f12628afbcbdce72787b94675f5ba1e292ae7ccccae079cf1bc3c8174ba61b` |
| `adopted-4.3/docs/SESSION_PARAMETER_REFERENCE.md` | `700e8f0731a18ab8b1e8b0d1ec91ab77f682799ce45f44e39fa3796930917915` |
| `adopted-4.3/docs/SESSION_PROFILE.ja.md` | `4b8e8f3f94eff07d24b3dc54dedca57051a365de3ce2020ea66d256b5405aa65` |
| `adopted-4.3/docs/SESSION_PROFILE.md` | `18196c82e9eeac97b79b639245637b89c43233671ddde834c6407a76d8b07dd2` |
| `adopted-4.3/docs/SPECIFICATION.ja.md` | `bc5b06e6edd413f1c11fd6bc513e73954005fead0aa82b9bd2f9cd96311f9989` |
| `adopted-4.3/docs/SPECIFICATION.md` | `075a51db61239fa75cc27d8e402f67759bc852cbe0b8e196dcd9539fc2c8a145` |
| `adopted-4.3/schema/ostf-4.3.0.schema.json` | `72bf44666b42a760c883fbfa87e1da891467768032ee8e96fbee9fb47f673fc7` |
| `adopted-4.3/schema/ostf-distributed-session-0.2.schema.json` | `f79832adea0e48d6042c820a7d7a51e7a7288944bde833e255ce96c22b5ed0e7` |
| `adopted-4.3/schema/ostf-production-session-0.2.schema.json` | `1ac57129bfc1def9d5e1529b32d3905495c86e0d0b1f7530199a4dce72037e29` |

The self-contained 5.0 and 4.3 documents remain independently versioned; a 4.3 session is not a 5.0 session merely because the raw bytes are included in OSTFP. Licence and other material boundaries are in `../LICENSE-POLICY.md` and `../NOTICE.md`. Publication of this technical written specification is not a promise of IANA MIME registration or host/runtime certification.
