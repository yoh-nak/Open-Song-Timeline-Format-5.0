# OSTF 5.0.0 — 正式仕様（日本語）

**版：5.0.0 · 2026年11月22日**

## 目的と提供形式

本規格は楽曲構造と制作プロジェクトの相互運用を目的とし、2種類のファイル形式を正式に定義します。**OSTF TEXT**（`.ostf`：BOMなしUTF-8のJSON）と、**OSTF PROJECT**（`.ostfp`：ZIP＋`manifest.json`＋楽曲JSON＋任意の制作Session・音声素材）です。独立したJSONであるProduction Session 0.3.0、Distributed Session 0.3と、プラグイン向け論理メッセージ仕様Plugin Context 1.0は、第三の必須ファイル拡張子を追加しません。

楽曲Coreは正式採択版OSTF 4.3.0の127定義を継承し、Scoreのルート`version`のみ`5.0.0`とします。音楽的意味の既存規則は`adopted-4.3/docs/SPECIFICATION.ja.md`等を正本として継承します。構造（項目型、必須性、enum、条件分岐）は版別の`schema/*.json`が正本です。5.0の変更箇所は本書・対応する5.0別冊仕様に限定し、過去のDraftの文言を現在の規範より優先させません。

## 正確な識別値

| 対象 | 識別 | Schema |
|---|---|---|
| OSTF TEXT | `format:"OSTF"` + `version:"5.0.0"` | `ostf-5.0.0.schema.json` |
| Production | `profile:"OSTF-Production-Session"` + `profileVersion:"0.3.0"` | `ostf-production-session-0.3.schema.json` |
| Distributed | `profile:"OSTF-Distributed-Session-0.3"` + `recordType:"snapshot"/"event"` | `ostf-distributed-session-0.3.schema.json` |
| OSTFP manifest | `packageFormat:"OSTFP"` + `packageVersion:"1.0.0"` | `ostf-package-manifest-1.0.schema.json` |
| Plugin Context | `protocol:"OSTF-Plugin-Context"` + `protocolVersion:"1.0.0"` | `ostf-plugin-context-1.0.schema.json` |

4.3時代のScore・Production 0.2・Distributed 0.2は**元の版を保ったまま**OSTFPへ同梱できます。勝手な版の書換えはしません。すべてのファイルを扱う義務はなく、DAW／VST3・AU・CLAP／Max for Live／AIは対応する版と機能ごとに適合を宣言します。

## 運用上の不変原則

- ScoreのSHA-256は正規化JSONではなく、**元のUTF-8バイト列そのもの**から計算します。
- `.ostfp`の作成・展開ではScoreとProfileとAssetのバイト列を勝手に変更しません。
- CoreのMIDI CCとProductionミキサー、Distributedでの確定イベントとCore Notes、Plugin提案とHost実保存は、それぞれ別の正本です。
- プラグインの読み取り用Contextは部分ビューであり、全Scoreとして再保存しません。編集提案はHostが権限と原本を確認し、全件一括適用して**保存が成功した場合のみ**`applied`を返します。
- 取得・実行・ロボット駆動・音源のライセンス許諾は、JSON参照やManifestにより発生しません。未知の情報・失った情報は明示します。

## 規範文書

`docs/COMPLETE_MANUAL.ja.md`が楽曲Coreからプロジェクト・プラグイン連携までを通読する全体マニュアル、`docs/PARAMETER_REFERENCE.ja.md`が全Schema宣言を含む項目リファレンスです。詳細は`PACKAGE_SPECIFICATION.ja.md`、`PRODUCTION_SESSION_0_3.ja.md`、`DISTRIBUTED_SESSION_0_3_SPECIFICATION.ja.md`、`PLUGIN_EXCHANGE_PROTOCOL.ja.md`、`MIGRATION_MATRIX.ja.md`、`CONFORMANCE.ja.md`を参照してください。

リリース条件から実機・独立パーサー検証および個別承認手続きを除外しましたが、検証済み・認証済みと表示するものではありません。
