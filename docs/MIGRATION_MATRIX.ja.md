# OSTF 4.3 ⇄ 5.0：移行・関連付け・情報損失規則（5.0.0）

## 1. データの変更を伴わない操作

| 操作 | 実装が守るべき境界 | 報告 |
|---|---|---|
| 4.3 Scoreの**読み込み** | 元の`version:"4.3.0"`で4.3 Schema/意味を適用 | 対応範囲／未対応意味を告知 |
| 4.3 Scoreの**OSTFP格納** | Score原文バイトをそのまま格納。Manifestに4.3.0と実SHA | Score変換したと称さない |
| 4.3 Score＋Production0.2同梱 | `score.formatVersion=4.3.0`と原SHA・存在すればDocument/Revision一致 | 不足Asset・Plugin Stateがあれば区別 |
| 5.0 Score＋Production0.3同梱 | `score.formatVersion=5.0.0`と原SHA、0.3 Schemaを適用 | 0.2と混ぜて未宣言なVersion変換禁止 |
| 4.3 Score＋Distributed0.2同梱 | 4.3のSession identityと原SHA/Planを維持 | アーカイブ化は同期・演奏の承認ではない |
| 5.0 Score＋Distributed0.3同梱 | 5.0の**新しいセッション**と原SHA/Planを固定 | 旧4.3 Sessionの生きた権限を自動移行しない |
| OSTFP → Project Directory → OSTFP | 同じManifest・同じパスのJSON/Asset原バイトを保持 | ZIPメタデータ自体のバイト同一性までは要求しない |
| Plugin Contextの`context` | 投影データのみ受信。ホストが提供しなかった部分は未知 | 受信部分のみ扱ったと表示 |

## 2. Score 4.3 → 5.0の明示変換（提案）

1. 原Scoreの形式・正確な版を判定し、**正式な4.3 Schema**と意味規則を用いて読み込む。元バイト列・SHA・Document/Revisionを記録する。
2. 5.0 Coreに追加の音楽フィールドはない（4.3の127定義を構造継承）ため、Score本体の音楽情報を保持したうえで、**明示的な新文書保存操作**として`version:"5.0.0"`へ変更する。失われたフィールドを推測・自動補充しない。
3. 保存後のUTF-8実バイトから**新しいSHA**を計算する。アプリがDocument Revisionを変更する場合は、既存のDocument正本ルールと矛盾しない形で新Revisionにする。改訂を名乗らず元Revisionだけを使い回してProfileと整合したと主張しない。
4. Production0.2は**自動的に0.3へ移行しない**。変換する場合、新Scoreとの意味・Track/Device/Asset参照を照合し、0.3の数値Automation制約も満たすか確認する。条件を満たさなければ拒否または別名の明示的Lossを伴う出力とする。旧0.2は原文保持可能。
5. Distributed0.2は**保存済みの履歴として保持**できるが、実行中Sessionをコピーして0.3に改名しない。5.0 Scoreでは新`sessionId`、権限・参加者・時計基準・Plan固定を**別セッション操作として**決定し、過去Eventを実行指令に変換しない。
6. PackageのManifestは格納された新Scoreのバイト・Digest・新しい各Profile本文に合わせて**再構築**する。旧Profileと新ScoreのPin不一致を埋めるためにSHAだけを書き換えない。

**無損失の範囲**：Score-onlyの音楽情報が保持されたとしても、同時に供給されたAudio Asset、Production/Distributed文書、Plugin Stateを省略した「プロジェクト全体の無損失移行」は主張できない。

## 3. Score 5.0 → 4.3

Score5 Coreは原則4.3と同じ音楽構造である。ただし元バイトが変わるので、`version`の変更は**新しい出力**でありSHA/関連付けが必ず変わる。Profile0.3/Distributed0.3はそのまま4.3に取り付けられない。Production0.3のAutomationが旧0.2構造に適合しても、意味・参照・出力バイトの整合を明示確認せず「完全ダウングレード」を宣言しない。別ファイル出力とLoss開示を用いる。

## 4. 情報損失の分類

| 状況 | 断定できる内容 | 禁止する主張 |
|---|---|---|
| Scoreのみ入力、Scoreのみ出力 | 受領したScore範囲での無損失保存 | 受領していないProduction/Audioを「失った」 |
| Score＋Production＋WAV入力、Scoreのみ出力 | Score正本は保持できるが、**提供済み制作情報を省略** | 完全プロジェクト無損失 |
| AssetのURI/SHA記述子のみ提供 | 記述子の保持 | 音声実体を保持／復元した |
| Plugin StateのBytesはあるがPlugin不在 | 状態Bytesの保存可能性 | 音色やDSP再現に成功した |
| 未知の4.3/5.0拡張をWriterが理解不能 | 元JSON保持か保存拒否、明示Loss | 黙って削除して無損失を名乗る |
| 古いScore SHAを指すProfile | `stale_binding`を報告し新Profileの明示操作を要求 | 旧SHAを新SHAへ暗黙に差し替える |
| HostがEdit Proposalを拒否 | Score/Session/Assetは変更なし | `received`を`applied`と表示 |

**最小Loss Report（推奨語彙であり必須新Schemaではない）**：操作名、入力に実際に提供された文書・実体、保存範囲、対象Version、影響するID/JSON Pointer、`omitted/approximated/unavailable/unsupported/unresolved/stale_binding`の分類、保存結果（拒否／明示的な損失あり出力／無損失）、原バイトの保持有無を報告する。固定のファイル拡張子は追加しない。

## 5. 実装者の注意

ZIP化だけでScoreやProfileを再フォーマットしない。`manifest.json`を作り直す場合はSHA／Binding／Path／Profile参照と一致させる。JSON構造の妥当性と再生音の同一性は別の問題。個別承認・実機検証は今回の正式GO条件から除外するが、未実施なのに「合格済み」「完全互換」を名乗らない。
