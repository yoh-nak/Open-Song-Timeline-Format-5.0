# OSTF 5 Production Session 0.3 — Interoperability semantics (5.0.0)

**This candidate inherits all fourteen named definitions from the byte-verified publisher-adopted 4.3 Production 0.2; only the Score 5 pin and typed automation differences are intentional.** The structural candidate is `schema/ostf-production-session-0.3.schema.json`. Identify a 5.0 Profile with `profile:"OSTF-Production-Session"`, `profileVersion:"0.3.0"`, `score.formatVersion:"5.0.0"` and the SHA-256 of the exact raw UTF-8 Score bytes. An incompatible family/version must not be silently relabeled.

## References and audio graph

The ID namespaces of Channels, Devices, Assets, Audio Regions, Automation Lanes, Sends (across all Channels) and Sidechains are each unique. Exactly one Master is required. A Track Channel references an existing Core Track; `audioTrack`, Bus and Master do not. Mapping one Core Track into more than one Channel is rejected unless a future explicitly documented duplication rule exists. Every Device is owned once; the order in `deviceIds[]` is the processing order. An Instrument can only be first on a Track Channel, at most once. Bus/Master do not host Instruments. A missing Plugin is not silently replaced by display name.

All non-Master output Channels must resolve. Send targets must be Buses. Sidechains must originate outside the Master, target an Effect Device owned by a different Channel and use a unique `(targetDeviceId,targetPortId)`. Build directed Channel dependencies from Outputs, Sends, and Sidechains (Sidechain target = owning Channel of its Device); cycles and unresolved references are invalid. Do not repair a cycle by deleting a Send without reporting loss.

## Assets and Audio Regions

`stateAssetId` resolves only to a `pluginState` Asset and `sourceAssetId` only to `audioSource`. Require `sourceStartFrame >= 0`, `sourceFrameCount > 0`, `sourceStartFrame + sourceFrameCount <= asset.frameCount`, and `fadeInTicks + fadeOutTicks <= durationTicks`. Audio Regions belong to Track or AudioTrack Channels, not Bus/Master. Source time is in the unmodified Score Tick domain. `native` uses Score Tempo to advance un-stretched frames; `fit` maps the declared source frame interval to Region Tick range with explicit `pitchPolicy`. No implied loops, crossfade, auto normalization, identical DSP algorithm, or waveform identity.

## Automation and ordered semantics

Automation Points use strictly increasing nonnegative Score source Ticks. The same source range played in multiple Visits applies the same source automation again. Duplicate `(target.kind, reference ID, parameter/parameterId)` Lanes are invalid. Boolean controls are Channel Mute, Send Enabled, Audio Region Mute, and DeviceControl Enabled/Bypass, using `valueType:boolean`, `interpolation:step`, and Points containing **both `atTick` and Boolean `value`**. Draft 0.7 fixes the conditional Schema branch that previously rejected `atTick`.

Numeric ranges: Channel/Send/Region gain in dB according to the field's declared Schema bounds; Pan in -1..1; plugin `device.parameterId` normalized 0..1 unless the Profile specifies otherwise. No implicit clamping. Before the first Point use the static value; after the last Point hold the last. Step holds the previous value, linear interpolation is performed in the declared numeric domain. DeviceControl is not an internal Plugin parameter. MIDI CC7/10/11/91/93 remains performance/instrument control and cannot overwrite Audio Mixer authority.

## Preservation and revisions

A changed Score raw digest invalidates previously pinned companion profiles until an explicit rebind or historical retention decision is made; a Plugin Context `ack` is not automatically an authorization to update Production identity. A Package can carry actual preset bytes but cannot provide Plugin runtime availability, licenses or cross-DAW sound equivalence. Preserve unsupported identities/state and the bytes actually provided, or refuse lossless write and describe the loss. The Profile does not standardize advanced warp/comp, surround, parallel racks, physical I/O, or DSP equivalence.

**Status:** cross-document, timebase and graph semantics are required implementation work beyond JSON Schema shape. The official 4.3 Production 0.2 source has been byte-verified and is included under `adopted-4.3/`; this 0.3 document is still a 5.0 development candidate, not a tested DAW implementation.

## Automation target type and domain (normative specification)

This amendment repairs a structural gap in the **Production Session 0.3 development Schema** where a boolean could otherwise be accepted as the value of a numeric target. OSTF Core 5.0, legacy 4.3 Production 0.2 and Distributed Sessions are unchanged.

| Target kind | Parameter | `valueType` | `points[].value` | Meaning |
|---|---|---|---|---|
| `channel` | `gainDb` | `number` | -120 to +24 dB | Audio-channel gain, independent of MIDI CC7 |
| `channel` | `pan` | `number` | -1 to +1 | Audio panning, independent of MIDI CC10 |
| `channel` | `mute` | `boolean` | `true` / `false` | Step interpolation only |
| `send` | `gainDb` | `number` | -120 to +24 dB | Audio send gain |
| `send` | `enabled` | `boolean` | `true` / `false` | Step interpolation only |
| `audioRegion` | `gainDb` | `number` | -120 to +24 dB | Region gain before channel processing |
| `audioRegion` | `mute` | `boolean` | `true` / `false` | Step interpolation only |
| `deviceControl` | `enabled`, `bypass` | `boolean` | `true` / `false` | Not an opaque plugin parameter |
| `device` | `parameterId` | `number` | 0 to 1 | Normalized opaque plugin parameter; actual plugin scale is host-dependent |

**Semantic conditions:** `points[]` contains at least one point; `atTick` must increase strictly without duplicates within each lane, in the original Score global Tick coordinate system. Revisited source sections reapply their original automation points. Duplicate lanes for the exact same target kind, target ID and parameter are invalid; array-order wins are not permitted. Numeric lanes allow `step` or `linear`, whereas boolean lanes allow `step` only. Before the first point, the corresponding static Channel/Send/Device/Region value applies; after the last point, the final point value holds. Missing IDs, unsupported parameters, and out-of-domain values must not be silently coerced; reject or explicitly disclose loss.

**Boundary:** The 0.3 development Schema can encode type/domain constraints. It does not independently prove cross-ID integrity, point ordering, duplicate-target exclusion or graph acyclicity; those are separate semantic obligations. It is not a DAW, audio or plugin compatibility certification. Example: `examples/production/04-numeric-boundaries-03.json`.


### Exact adopted-source inheritance note

All fourteen named definitions are inherited from the exact publisher-adopted Production Session 0.2 schema, including optional `channel.name`, required `plugin.name`, `plugin.namespace`, `asset.purpose=renderedAudio`, `asset.byteLength`, and `hostExtension.namespace` pattern. `sizeBytes` is a Package Manifest property, not a 0.3 Production Asset property. Version and Score pin were updated for 0.3 and per-target numeric Automation type/domain restrictions were added. See adopted-source reconciliation record.
