# OSTF 5.0 — 機能別適合宣言（5.0.0）

対応を表明するときは、**文書ファミリー・正確な版・操作・対応範囲**を示します。「OSTF 5完全対応」という包括的な表現だけでは、以下の機能を証明できません。JSON Schemaの構造合格と意味の解釈、保存、演奏や実際の権限は別の機能です。

| 能力 | 宣言するための最低限の範囲 | 宣言に含まれないこと |
|---|---|---|
| `score-read` / `score-write` | 4.3.0／5.0.0の正確なScore Schemaと宣言したCore意味の読み書き。無損失Writerは未知データの保持／拒否・損失報告 | ミキサー・素材・外部DAWでの再生 |
| `project-read` / `project-write` | OSTFP1.0 ZIP／フォルダの目録、原バイトハッシュ、パス安全性、Score／Profile／AssetとBinding規則 | プラグイン実体や音声復元、配布許諾 |
| `production-read` / `production-write` | 正確なProduction0.2／0.3版とScore固定、対象とするChannel／Mixer／Audio Region／Device／Automation／Sidechain機能 | 未対応Rack/Warp/Comp/Surround、DSP完全一致 |
| `distributed-read` | 正確なDistributed0.2／0.3のSnapshot／Event、Score SHA／Revision／Plan固定、未知記録の保持 | WAN接続やロボット実行 |
| `distributed-authority` | 外部権限の審査、状態改訂、重複イベント防止、Plan／Visit解釈 | JSONが本人確認や許可を与えること |
| `plugin-context-consume` | 部分Contextとして受信し、未提供Core情報を補完しない。Score／Host PPQの区別 | VST3/AU/CLAPの標準ホスト通信API |
| `plugin-edit-propose` | SHA／Revision固定、Stable ID／Pointer付き原子的提案 | ホストによる変更確定 |
| `plugin-edit-apply` | 外部許可を経たホストの全件原子的保存、実際の保存済みバイトAck | Production自動再関連付け／Distributed権限継承 |
| `loss-report` | 実際に提供された入力とExport範囲、対象ID／Pointer、欠損Bytes／未対応／近似と処理結果を報告 | 未提供情報の損失とみなすこと |

コード進行表示だけを行うVSTは、Score読取とPlugin Context受信だけを宣言しても構いません。OSTFPを書けるDAWでも、他社DSPの音質再現を保証するものではありません。未知のデータを未解釈のまま保持できても、その意味や実行機能を理解したことにはなりません。Productionと音源を実際に受領してScoreだけ書き出した場合、Score自体が無損失でもプロジェクト全体は部分Exportです。

規範参照は`SPECIFICATION.ja.md`、`PACKAGE_SPECIFICATION.ja.md`、`PRODUCTION_SESSION_0_3.ja.md`、`DISTRIBUTED_SESSION_0_3_SPECIFICATION.ja.md`、`PLUGIN_EXCHANGE_PROTOCOL.ja.md`、各Schemaと採択4.3原本です。本開発パッケージは実動作・独立パーサー・実際のDAW/Plugin/AI/ロボットの互換性認証を主張しません。
