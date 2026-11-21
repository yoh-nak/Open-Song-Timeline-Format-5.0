# OSTF 5.0.0 — 全網羅サンプルガイド（日本語）

`examples/score/`の25ファイルはそれぞれ**単体で利用できるOSTF 5.0 JSONテキスト**です。正式4.3の採択済み例からルートの`version`を5.0.0に変換し、音楽情報の中身は保持しています。`examples/ostfp/`の11ファイルは**実際のZIPパッケージ**です。実音、商用プリセット、VST実行の再現や外部ソフトの互換性を保証する例ではありません。

## 25種類のOSTF TEXTサンプル

| ファイル名 | 主な対象 |
|---|---|
| `01-minimal.ostf` | 最小楽曲構造 |
| `02-guitar-solo.ostf` | ギターソロとノート |
| `03-jazz-comping.ostf` | ジャズの和声とコンピング |
| `04-aaba-performance-plan.ostf` | AABA・有限演奏計画 |
| `05-rnb-vocal-open.ostf` | R&B歌唱・自由度 |
| `06-scat.ostf` | スキャット・非言語歌唱 |
| `07-vocal-alternatives.ostf` | 歌詞・旋律の選択肢 |
| `08-gospel-response.ostf` | ゴスペルの掛け合い |
| `09-techno-variation.ostf` | テクノの変奏・モチーフ |
| `10-physical-robot-requirements.ostf` | フィジカルAI向け演奏条件（記述のみ） |
| `11-harmony-plus-phrasing.ostf` | ハーモニーとフレージング |
| `12-visit-scoped-response.ostf` | Visit単位の応答関係 |
| `13-fixed-notes-and-directions.ostf` | 固定ノートと演奏指示 |
| `14-tempo-map-reentry.ostf` | テンポマップと再訪問 |
| `15-vocal-response-phrasing.ostf` | 歌唱応答とフレージング |
| `16-inherited-comprehensive-core.ostf` | 旧Coreの総合例 |
| `17-fixed-note-source-cut.ostf` | ノートの部分的切断 |
| `18-visit-role-override.ostf` | Visitごとの役割変更 |
| `19-concurrent-voice-directions.ostf` | 複数Voiceの並行指示 |
| `20-phrasing-with-motif-reference.ostf` | フレーズLibrary参照 |
| `21-visit-and-range-intersection.ostf` | Visit・元区間の交差 |
| `22-pinned-session-aaba.ostf` | 固定されたAABA演奏素材 |
| `23-range-visit-and-label.ostf` | 範囲再訪とラベル |
| `24-intra-track-voices-response.ostf` | 同一Trackの複数Voice |
| `25-source-note-repeated-visits.ostf` | 同一Sourceノートの繰り返し |

## OSTF PROJECT archives / OSTFPパッケージ（11件）

| File | Purpose / 内容 |
|---|---|
| `01-score-only.ostfp` | 楽曲JSONのみを格納 |
| `02-audio-stub.ostfp` | 単体Score＋合成無音WAV |
| `03-score-production.ostfp` | 制作Session＋オーディオ領域＋Asset参照 |
| `04-inert-plugin-state.ostfp` | 架空の不活性プラグイン状態とオーディオ |
| `05-score-distributed-session.ostfp` | 分散SessionとPlan、ScoreのSHA固定 |
| `06-legacy-4.3-compatible.ostfp` | 旧4.3 Scoreを変更せず梱包 |
| `07-guitar-solo.ostfp` | ギターソロのプロジェクト梱包 |
| `08-techno-variation.ostfp` | テクノ変奏のプロジェクト梱包 |
| `09-vocal-alternatives.ostfp` | 歌詞・歌唱選択肢のプロジェクト梱包 |
| `10-comprehensive-core.ostfp` | Coreの総合例をZIPに格納 |
| `11-combined-production-distributed.ostfp` | Score・制作Session・分散Snapshotを同梱 |

## Additional standalone JSON documents / その他のJSON例

- **Production 0.3**：`01-production-03.json`（録音用Audio RegionとAsset）、`03-boolean-and-device-automation-03.json`（Mute、Bypassなどのオートメーション）。参照WAVの実体はOSTFP 02・03・04・11に含まれます。
- **Distributed 0.3**：`01-prepared.json`（準備中Snapshot）、`04-phrase-proposed.json`（提案Event）、`06-playing-committed.json`（確定フレーズ）。OSTFP 05・11にも実体があります。
- **Plugin Context 1.0**：`01-context.json`、`02-edit-proposal.json`、`04-stale-rejection.json`、`05-applied-with-new-score.json`（部分読取・原子的編集提案・競合拒否・実保存ACK）。

## 確認と取り出し

リポジトリ直下で`python tools/validate_examples.py`を実行してSchemaとサンプル構造の整合を点検できます。単独パッケージの検査は`python tools/ostfp.py validate examples/ostfp/01-score-only.ostfp`です。`.ostfp`はZIPとして展開でき、`mimetype`、`manifest.json`、`score/song.ostf`、任意の`sessions/`と`assets/`が見られます。Scoreの元バイトSHAの不一致は失敗として扱い、パッケージの存在だけで権限・著作権許諾が与えられることはありません。
