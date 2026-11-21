# OSTF 5.0 — ファイル識別と提案識別子（5.0.0）

これは**規格内の識別子一覧**であり、IANAへの登録やURL公開を示すものではありません。ファイル拡張子、ZIPの名称、Draft番号、他文書の版からVersionを推測せず、下表の識別値で正しいSchemaを選択してください。

| 対象 | 本文で必須の識別 | Schema | Scoreとの関係 |
|---|---|---|---|
| Score5（`.ostf`） | `format:"OSTF"`, `version:"5.0.0"` | `schema/ostf-5.0.0.schema.json` | 楽曲正本 |
| Score4.3（旧版） | `format:"OSTF"`, `version:"4.3.0"` | `adopted-4.3/schema/ostf-4.3.0.schema.json` | 原文のままOSTFPへ同梱可能 |
| Production0.3 | `profile:"OSTF-Production-Session"`, `profileVersion:"0.3.0"` | `schema/ostf-production-session-0.3.schema.json` | Score5の元バイトにのみ固定 |
| Production0.2 | 同じ`profile`、`profileVersion:"0.2.0"` | `adopted-4.3/schema/ostf-production-session-0.2.schema.json` | Score4.3に固定 |
| Distributed0.3 | `profile:"OSTF-Distributed-Session-0.3"`, `recordType:"snapshot"|"event"` | `schema/ostf-distributed-session-0.3.schema.json` | ルートの`scoreSha256`でScore5へ固定。ネスト`score`と`profileVersion`は**存在しない** |
| Distributed0.2 | `profile:"OSTF-Distributed-Session-0.2"`, `recordType` | `adopted-4.3/schema/ostf-distributed-session-0.2.schema.json` | Score4.3に固定 |
| Package Manifest | `packageFormat:"OSTFP"`, `packageVersion:"1.0.0"` | `schema/ostf-package-manifest-1.0.schema.json` | 正本Score1件、他文書・素材は任意 |
| Plugin Context | `protocol:"OSTF-Plugin-Context"`, `protocolVersion:"1.0.0"` | `schema/ostf-plugin-context-1.0.schema.json` | 論理メッセージ、Score4.3/5.0双方を識別可能 |

**Manifestに記す版:** `documents[].version`はProductionなら`0.2.0`/`0.3.0`、Distributedなら`0.2`/`0.3`です。Distributedの本文には`profileVersion`欄がなく、`profile`文字列自体が版を表すためです。`documents[].family`は実際の`profile`値、`role`は`productionSession`/`distributedSession`と一致させます。

**ハッシュ:** Scoreピンと各素材のSHAは正本のUTF-8元バイト列、またはBinaryの元バイト列を対象にします。JSONを正規化したハッシュではありません。Schemaの`$id` URLは識別値であって現在そのURLが実際に配信されているという意味ではありません。OSTFP先頭の`mimetype`に置く`application/vnd.ostf-project+zip`は**提案された未登録の値**です。未登録値として扱い、ZIPとManifestの実際の識別を照合します。

**改訂・権限:** Core改訂後のProductionは明示的な再関連付け、Distributedは新Sessionと外部の権限確認が必要です。Plugin `ack:received`は保存成功ではありません。これらのVersionはDAW/VST3/AU/CLAPなどのソフト実行環境の互換性を保証しません。
