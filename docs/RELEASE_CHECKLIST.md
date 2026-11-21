# OSTF 5.0.0 — Written specification release checklist

**Publication decision:** GO for source/document specification publication as `v5.0.0`. Actual GitHub upload, tag creation, and repository rights management are separate publisher operations.

## Formal deliverables verified within this release

- [x] OSTF TEXT `.ostf` and OSTF PROJECT `.ostfp` are both documented as official file forms; Project Directory is a working representation, not a third extension.
- [x] Exactly **five** current JSON Schemas: Score 5.0.0, Production 0.3.0, Distributed 0.3, Package Manifest 1.0.0, Plugin Context 1.0.0.
- [x] Byte-identical set of **13** adopted 4.3 Core/Production/Distributed Schema + semantic reference source files is preserved in `adopted-4.3/`.
- [x] Full current **English and Japanese manuals**, **English and Japanese field/reference compendia** and all 1,601 enumerated Schema declarations, with archived 4.3 inherited normative content and versioned 5.0 semantics.
- [x] Full feature-oriented **25 `.ostf` Score JSON examples**, migrated explicitly from adopted 4.3 Scores by changing only Score `version`.
- [x] **11 `.ostfp` ZIP Project examples**, including legacy 4.3, audio, production, distributed, fictional plugin state, and a combined production/distributed case.
- [x] **2 standalone Production 0.3**, **3 Distributed 0.3**, and **4 Plugin Context 1.0** message examples.
- [x] Structure and exact SHA-256 byte digests checked for the samples; package member inventory and companion Score pins checked against the versioned Schemas. Built-in static scripts are `tools/validate_examples.py` and `tools/ostfp.py`.
- [x] Explicit rules for Score5↔4.3 migration, Package path safety, asset binding, plugin proposed-edit/actual-save ACK, session state, loss reporting and host-capability declarations.
- [x] CC0/MIT applicability and publisher-adopted source provenance, third-party rights boundaries, release notes and checksums included.
- [x] Exactly **100 top-level repository files** are included (nested `.ostfp` archive contents are counted as a single repository file each).

## What was NOT tested or certified

- No Ableton Live, VST3, AU, CLAP, DAW, third-party host, physical AI/robot or independent parser integration has been executed or certified by this written release process.
- No audible equality, DSP, plug-in-state restoration, real-time WAN clock, host permission/security audit, IANA MIME registration, deployed `$id` URL, or third-party sample copyright clearance is guaranteed.
- Runtime checks, independent parser tests and individual signoff were excluded by the publisher's requested written-specification release gate; their absence must **not** be described as passing tests.

## GitHub publishing steps

1. Extract the provided root-free `OSTF_5.0.0_GitHub_Release.zip` into the root of the intended GitHub repository, preserving `README.md` and directory paths.
2. Commit the files (including the original `adopted-4.3/` provenance documents and the binary `.ostfp` examples). Do not rename the `.ostfp` files to `.ostf`.
3. Create the release/tag `v5.0.0` and attach the original ZIP as a release asset, using `RELEASE_NOTES.md` for the release description.
4. Keep `SHA256SUMS.txt`, `NOTICE.md` and the license files together with the public materials; review any newly added third-party assets under their own licences before uploading.

**Static verification is editorial/structural evidence, not third-party software interoperability certification.**
