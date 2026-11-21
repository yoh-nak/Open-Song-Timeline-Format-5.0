# OSTF Plugin Context Exchange 1.0 — 規範案（5.0.0）

## 1. 論理契約とホストの責任

本仕様は**JSONメッセージの論理契約**です。第三のOSTFファイル拡張子、VST3/AU/CLAP/Max for LiveのSDK、音響DSP、リアルタイムAPI、書込権限ではありません。`schema/ostf-plugin-context-1.0.schema.json`が`protocol:"OSTF-Plugin-Context"`、`protocolVersion:"1.0.0"`、一意な`messageId`、`operation`、`score`、`scope`、任意`transport`、操作別`payload`を定義します。

`score.format:"OSTF"`、`score.version:"4.3.0"|"5.0.0"`、`score.sha256`は実際のScore元UTF-8**バイト列**を識別します。任意の`documentId/revisionId`も原本と一致させます。Protocolが1.0であるという理由だけでScoreを5.0として処理しません。Score、Production、Distributedのいずれもメッセージ単体に正本更新権限を与えません。通信経路、認証、Pluginライフサイクルはホスト側の仕様です。

## 2. 範囲と時間座標

`scope.startTick/durationTicks`はScore PPQの半開区間`[startTick,startTick+durationTicks)`で、任意の`trackIds/sectionIds`は表示対象の絞り込みです。**編集権限ではありません。** `transport.positionTick`は`transport.hostPpq`によるホスト位置であり、`transport.scorePpq`のScore位置ではありません。Tempo/Meter、ループ、Seek、再生位置の不連続はホストAdapterが処理します。到着JSONからサンプル精度の発音・権限を推測してはいけません。

## 3. `context`（読取専用）

`payload:{"partial":true,"data":{...}}`は**部分投影**であり、完全な`.ostf`ではありません。任意の`unavailableFields[]`で未提供部分を示せます。提供されなかったHarmony、Tracks、Lyrics等を空欄と解釈したり、欠損値を補って正本として保存したりしてはいけません。実際のScore保存には別のホスト許可操作が必要です。

## 4. `editProposal`（原子的な編集提案）

`proposalId`、`baseSha256`、`mode:"atomic"`、1件以上の`changes[]`、任意`baseRevisionId`を持ちます。`baseSha256`は`score.sha256`および現行Scoreの実バイトSHAと一致し、Revisionは独立に照合します。同一`proposalId`／同一**パース済JSONツリー**の再送は冪等、同一ID／異なる内容は競合として拒否します。提案は**書込権限ではありません**。

各`change`は`op:"add"|"replace"|"remove"`と、ルート置換ではないRFC 6901絶対JSON Pointerの`path`を持ちます。`~0`/`~1`を正しく復号します。`add`は`containerId/newEntityId/value`を必須とし、配列末尾への`/-`追加または未存在オブジェクトキーへの追加に限定します。新エンティティのIDは`newEntityId`と一致させます。`replace`は`targetId/expected/value`、`remove`は`targetId/expected`を必須とし、元SnapshotのJSON値を**型も含め厳密一致**で比較します。PointerとStable IDは同じ対象を指さなければなりません。編集提案を認めるのは`/timeline`、`/harmony`、`/tracks`、`/lyrics`の配下だけで、実際の編集許可範囲は別のホスト側権限判断によります。`/format`、`/version`、`/ppq`、`/document`、拡張定義等はこのプロトコルで更新できません。

すべてのPointer、期待値、IDを**共通の変更前Score Snapshot**に対して解決します。親子の重複編集、配列添字の不明瞭なシフト、既存キー上書き、ID重複、Scope違反を拒否します。変更前を基準に検査した後、提案の順番でコピーへ全変更を反映します。一つでも失敗すれば**全件拒否**し、部分適用や最後の値優先を使いません。

## 5. Host Applyと永続保存`ack`

ホストは外部の認証・権限、Score版・元SHA・任意Revision、Scope、Stable ID、JSON Pointerと`expected`を照合し、新しい**完全な**Scoreを構造Schemaと参照意味の双方で確認して、許可された保存操作として原子的にCommitします。**実際に保存成功した後に限り**`ack.payload.status:"applied"`と保存された新バイトの`effectiveScoreSha256`、任意の`appliedRevisionId`を送れます。`ack.payload.inReplyTo`は元の`messageId`で、`proposalId`ではありません。

`status:"received"`は受信しただけ、`status:"rejected"`は未適用です。この2状態では`effectiveScoreSha256`と`appliedRevisionId`を**両方禁止**します。拒否時にCoreを変更してはいけません。Core編集が成功してもProductionやDistributedのScore参照を勝手に更新しません。Productionは明示的に再関連付け、DistributedはScore／Plan／Revisionに変更があるとき新Sessionの開始が必要です。

## 6. `diagnostic`とLoss

診断には`invalid`、`unsupported`、`stale`、`scopeViolation`、`permissionDenied`、`conflict`、`informationLoss`、`internalError`を使い、対象Pointerを必要に応じて記録します。診断メッセージは実行命令ではありません。未知の情報を黙って破棄せず、未対応や損失を報告します。編集提案の拒否は保存の損失とは別物です。

## 7. 第三者の適合宣言と非対象

VST3/AU/CLAPの音源、MIDI生成、エフェクト、AI、Max for Live等は、Context読取のみ・提案送信のみで対応を宣言でき、OSTFP作成やProductionの実装は不要です。Hostは別にApply対応を宣言できます。`CONFORMANCE.ja.md`の機能別・版別・操作別で対応範囲を記述します。Pluginバイナリ仕様、DAWのTransport API、パラメーター動作、実音・DSP、ライセンス／DRM、ロボット制御は規格化しません。
