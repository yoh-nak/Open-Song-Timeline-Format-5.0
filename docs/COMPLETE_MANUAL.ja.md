# OSTF 5.0.0 — 全網羅マニュアル（日本語）

**OSTF 5.0.0の完全な構造・規範・制作フロー・サードパーティー実装のための統合マニュアルです。** 楽曲Coreについては正式採択された4.3日本語規範、Production／Distributedについても正式採択版の日本語規範を併記し、5.0での変更・新規規格を別章で上書きします。旧資料内のDraft表現は当時の原文に由来します。正式5.0の構造の正本は本ZIPの版別Schemaであり、規範の版を混ぜてはいけません。

## 目次

1. OSTF 5の二形式・役割・識別値
2. 楽曲構造・和声・MIDI・歌唱・演奏意図の4.3継承仕様全文
3. 旧Production Session 0.2の継承仕様全文
4. 旧Distributed Session 0.2の継承仕様全文
5. OSTF 5.0の音楽意味差分
6. Production Session 0.3
7. Distributed Session 0.3
8. OSTFPと素材・バイト整合・ZIPセキュリティ
9. VST3/AU/CLAP/Max for Live/AIのPlugin Context
10. 4.3との移行・互換・損失・サードパーティー適合
11. 実装と配布に使うサンプルの参照方法

全フィールド・定義・条件付き制約は`PARAMETER_REFERENCE.ja.md`、具体的なサンプル用途は`EXAMPLES_GUIDE.ja.md`を参照してください。


---

## 1. OSTF 5.0.0 総合仕様

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


---

## 2. 楽曲Coreの正式4.3日本語規範の継承全文

> **現行採択候補：Draft 0.77（未承認）。** 冒頭の参照解決判定表を現行提案とし、下位の旧Draft番号を持つ節は履歴であって並列の現行規範ではありません。今回の変更は編集上の特定であり、Schemaやシリアライズ形式は変更しません。

# Draft 0.73 — 現行の参照解決判定表（未採択の規範案）

**承認対象：D01。** 以下が現行の採択候補であり、後続のDraft 0.62〜0.72の記述は改訂履歴として保持する。古い判定例を並立する現行規則として扱わない。発行者の採択前に規範として確定したわけではない。Schema・シリアライズ形式は変更しない。

| 優先順 | 条件 | 実装側の診断 |
|---|---|---|
| 1 | ProfileのJSON・必須pin・形式が不正 | `INVALID`（4状態の対象外） |
| 2 | Profileの形式・版が未対応 | `UNSUPPORTED`（4状態の対象外） |
| 3 | 許可範囲が未定義、候補列挙未完了、必要なScore実体を取得不可 | `NOT_EVALUATED`（暫定情報は別途報告、確定4状態を返さない） |
| 4 | 明示的に許可された完全な候補集合にScore実体が0件 | `MISSING`（評価範囲内に限る） |
| 5 | Scoreの実体はあるが、元バイト列のSHA-256がpinと一致しない | `MISMATCH`（評価範囲内に限る） |
| 6 | ハッシュ一致したScoreが構造的に不正または解析不可 | Score形式エラー（`RESOLVED`ではない） |
| 7 | 一致する正常なScore内のTrack/Plan/Visit/range等の必須参照が欠落・重複・不正 | `AMBIGUOUS`＋具体的な診断（`missing_referent`、`nonunique_referent`等） |
| 8 | 元バイト列とハッシュが一致し、必要な参照がすべて一意に解決 | `RESOLVED`（評価範囲内に限る） |

**同一性と権限の境界：** 宣言されたハッシュ対象の元Scoreファイルのバイト列を使用する。Unicode正規化、改行変換、BOM除去、JSONの再シリアライズ、ZIP全体のハッシュによる代替は禁止する。同じバイト列のコピーは同一のバイト同一性を持つ。ファイル名、URI、キャッシュしたハッシュ、音楽上の等価性だけでは同一としない。探索に失敗した候補を黙って除外せず、範囲を狭める場合は新しい評価として明示する。診断名はJSON Schemaに追加するフィールドではない。ハッシュ一致は著作権、信頼性、アクセス権、音響再現、遠隔実行、ロボット安全性を保証しない。編集後の付け替えには明示的承認と新しいpinが必要。

**公開管理：** D01〜D05はすべて未承認。独立パーサー、DAW／プラグイン／DSP、歌唱、WAN／分散実行、フィジカルAI／ロボットの動作検証は公開GO条件から除外し、実施済みとも主張しない。

---

# Draft 0.72 — 編集上の優先順位と採択範囲（未承認）

**採択対象：D01／Core Score 4.3。** 正式採択の対象は、承認記録で特定する本文と既存Schemaに限る。過去Draft 0.62〜0.70の参照判定例は改訂履歴として残し、並立する定義として扱わない。矛盾する参照診断については**現行候補内で**Draft 0.71の「許可された候補集合の列挙・取得が完了してから判定」する規則を優先し、未完了ならJSONに新項目を追加せず外部診断`NOT_EVALUATED`とする。

第三者実装は、(a)未知データの読込・保持、(b)ラウンドトリップ保存、(c)編集、(d)意味解釈、(e)実行を区別する。いずれか一つの対応を他の操作まで拡大して表明しない。ハッシュ一致は分散演奏実施、ミキサーの音響再現、ロボット動作の保証にならない。これらの規範案は**D01が発行者により正式採択された場合のみ**規範効力を持つ。

> **Current proposed editorial precedence: Draft 0.71.** This first section supersedes the Draft 0.70 incomplete-enumeration RESOLVED exception; historical sections below are retained as version history. No publisher adoption is implied.

## Draft 0.71 — 参照判定の探索完了条件（未採択の規範案）

Draft 0.70の「探索が未完了でも追加候補で結果が変わらないと予測できればRESOLVEDにできる」という例外を撤回する。未確認候補に関する予測を検証済みの根拠として扱ってはならない。

1. Profileの構造と対応バージョンを先に確認する。不正・未対応なら参照判定とは別の`INVALID`／`UNSUPPORTED`を報告する。URIやハッシュの存在はScore実体へのアクセス許可にならない。
2. **明示された有限かつアクセスが許可された候補集合**を定義し、その範囲、列挙完了、各候補の実バイト取得とSHA-256計算の有無を記録する。判定は宣言された範囲に限定し、世界中に存在しないと断定しない。
3. 候補列挙が未完了、または必要な候補の元バイトが取得できない場合は、外部診断`NOT_EVALUATED`と取得済みの根拠を示す。ハッシュ一致候補が1つ見つかっても4つの確定状態を報告しない。より狭い集合を明示的に定義し直して再評価してもよいが、除外した候補と探索範囲変更を必ず開示する。
4. 列挙と取得が完了した集合について、候補が0件なら`MISSING`、候補があるが生バイト列のSHA-256一致が0件なら`MISMATCH`、一致したScoreの必須参照が欠落・重複・無効なら`AMBIGUOUS`、一致と全必須参照の一意解決が揃った場合のみ`RESOLVED`とする。
5. 同じScoreバイト列の複数コピーは同一データとして扱う。名称、URL、音楽内容、申告ハッシュだけで一致としない。改訂Scoreへの付け替えには明示的な許可と新ハッシュの指定が必要。参照判定だけで実行・通信・音響・プラグイン・ロボット制御を許可しない。

`NOT_EVALUATED`／`INVALID`／`UNSUPPORTED`／診断補足は報告用で、JSONフィールドやSchema enumの追加ではない。4つの判定名称も新しいシリアライズ項目ではない。この規則はD01・D02・D03の正式採択前の提案で、動作・相互運用検証は未実施である。

---

# Draft 0.69 — Score候補の探索範囲と判定の確実性（未採択）

**R04/R11/R13/R14の提案規範。** 4種類の参照診断は、対象操作について**明示的に提供・許可された候補集合内**で判定する。無関係なローカルフォルダーや遠隔URL、リポジトリを勝手に探索して`MISSING`を`RESOLVED`へ変更してはならない。利用者またはホストが追加の元バイト列を許可した場合は**新たな評価**として再判定する。

- **許可された元バイト列候補が0件：** `MISSING`。あくまで評価対象内で未発見であり、Scoreの世界全体における消失を断定しない。
- **候補が1件以上あるがピンのハッシュと一致しない：** `MISMATCH`。候補がすべて新しいリビジョンでも同じ。旧Scoreが全世界から消えたとは断定しない。
- **ハッシュ一致・Score構造不正：** `RESOLVED`ではなくScore形式エラー。
- **ハッシュ一致・必須参照先が0件または複数件：** `AMBIGUOUS`に詳細`missing_referent`または`nonunique_referent`を付す（JSONに追加するフィールドではない）。
- **必要な参照がすべて一意に確定：** 評価対象内で`RESOLVED`。同じバイト列の複製は単一の同一性として扱う。

キャッシュされたハッシュ、ファイル名、URL、署名付きリンク、索引の一致だけでは、実際のScoreの元バイト列による照合を代替できない。候補の元バイト列を取得できず評価自体が行えなかった場合、操作側で`not_evaluated`/`unknown`等を報告してよいが、これはOSTFの第5の参照状態ではない。確認済みの`MISSING`や`MISMATCH`と偽ってはならない。参照診断はデータの真正性、発音、プラグイン復元、ロボットの実行許可を保証しない。**D01～D03、D05、D04は未承認。**

---

# Draft 0.68 — 参照診断の判定順序と過去の事例表の整合（未採択）

**現行の提案（R04/R11/R13/R14）:** 明示的に許可されたScore候補だけを用い、次の順序で判定する。過去のDraftの表が異なる場合、この節を現行の編集提案とし、過去の記録は履歴として残す。

1. Companionの形式・バージョン・必須ハッシュが不正／未対応なら`INVALID / UNSUPPORTED`。4種類の参照診断には含めない。
2. Scoreの元バイト列の候補が1件もなければ`MISSING`。ファイル名やメタデータの一致は候補とみなさない。
3. 候補が存在するが元バイト列のSHA-256が1件も一致しなければ`MISMATCH`。**新版Scoreだけが存在する場合も同様**。Draft 0.62の旧事例でこの場合を`MISSING`とした記述は現行提案では採用しない。
4. 一致したScoreが解析不能または必須構造違反なら、参照成功とせずScore形式エラーとして報告する。
5. 一致して正常なScoreの必須参照を全件調べる。参照先0件は`AMBIGUOUS`と詳細`missing_referent`、複数件は`AMBIGUOUS`と`nonunique_referent`、矛盾・範囲違反は`AMBIGUOUS`とその詳細を示す。複数の問題があればそれぞれ報告する。
6. 必須参照がすべて一意に解決した場合のみ`RESOLVED`。同じバイト列を持つ複数のパスは1つのScore同一性として数える。

この状態名・詳細は**実装側の診断指針**であり、新しいJSONフィールドやSchema列挙値ではない。認証、演奏実行、無断ネットワーク取得、権利許諾、自動的な再関連付けを許可しない。日本語版と英語版の意味が異なる場合は採択を保留する。D01〜D05は未承認。実機・独立パーサー等の検証は条件外かつ未実施。

---

# Draft 0.67 — 参照診断の意味規則の確定候補（未採択）

**公開前の要判断事項（R04/R11/R13/R14）:** Draft 0.64では、必須のTrack/Plan参照先が「存在しない」ケースを`AMBIGUOUS`と呼んでいます。一方、通常の意味では`AMBIGUOUS`は「候補が複数で一意に定まらない」ことを表します。これは提案文書の解釈上の曖昧さであり、Schemaの欠陥や検証結果ではありません。

**採択推奨:** 新しいJSONフィールドや状態の列挙値は導入せず、既存の4つの人間向け診断分類を維持します。対応するProfileを構造的に確認し、許可された元Scoreの**生バイト列**のSHA-256一致を先に要求します。その後、必須Track/Plan/Visit参照先の件数が**0件**ならサマリーは`AMBIGUOUS`とし、診断詳細で`missing_referent`を示します。**2件以上**なら同じサマリーでも詳細は`nonunique_referent`とします。各必須参照が1件に確定した場合のみ`RESOLVED`です。詳細ラベルは推奨診断名であり、OSTFの新規フィールド・enum値・保存必須データではありません。`MISSING`は元Scoreの正確なバイト列がない場合に限り使用し、Score内部の参照欠落には流用しません。

**参照元の信頼境界:** 呼出元が明示的に提供・許可したScore候補のみ参照できます。ファイル名、URL、タイトル、意味的に等しい再シリアライズ結果は生バイト一致の証拠になりません。外部ネットワークからの無断取得、暗黙の付け替え、根拠のない可逆保存の表明は禁止する方針を採択候補とします。

**審査状況:** D01〜D03による採択・修正・却下が必要です。D04/D05も未承認です。動作・独立パーサー・DAW・WAN・ロボットの検証は対象外で未実施です。

---

# Draft 0.66 — 現行審査基準（未採択）

この節は**現行Draft 0.66の審査基準**です。本文に残る旧Draft番号の追記は経緯を示す資料であり、独立した現行版の規範ではありません。Schema・サンプル・ツールは変更していません。

- **Core 4.3:** `schema/ostf-4.3.0.schema.json`と現行Core仕様書・意味規則。4.3で変更を明記していない部分は4.2を継承します。
- **Distributed Session 0.2:** Versionに対応するSchemaと日英Session仕様書。セッションのイベントや同期状態は、ネットワークサービスの保証やロボット実行の許可ではありません。
- **Production Session 0.2:** Versionに対応するSchemaと日英Production仕様書。ミキサー設定・プラグイン記述・アセット参照は、実際のDSP実行や音声再現を保証しません。
- **権限の優先順位（採択案）:** 構造制約は該当バージョンのSchema、意味制約は該当バージョンの規範仕様を参照します。例示、旧版追記、チェックリストはこれらを上書きできません。Schemaと規範仕様が矛盾した場合は、任意解釈を認めず公開阻害要因として修正します。
- **Score参照:** 先にProfileの形式・Versionを検査し、元Scoreのバイト列のSHA-256一致を確認後、必要な参照を解決します。RESOLVED／MISSING／MISMATCH／AMBIGUOUSは診断用の名称でJSONフィールドではありません。不正形式・未対応版は4状態に含めません。参照先不足の具体的な原因を記録し、暗黙の再関連付けを禁止します。
- **対応表明:** Score／Distributed／Production、Version、読込／編集／保存／保持／実行を区別し、未対応や欠落を表示します。

R01〜R14の一括採択は提案段階です。D01〜D03の発行者承認、D05の権利承認、D04の最終ZIP承認は引き続き未完了です。動作・独立実装・実機検証は公開判定から除外し、実施済みとは表記しません。

---

## Draft 0.64 — 形式検証と参照解決の境界（未採択の規範案）

Draft 0.63の4状態は、**形式上有効かつ認識可能な関連Profile**について、元Scoreの参照が解決するかを表す診断である。JSONフィールドや通信上の状態コード、動作認証ではない。判定順序は次のとおり。

1. **関連Profileを先に形式検証する。** Profile種別と版、規定の位置にある必須SHA-256参照の書式を確認する。未対応版や必須参照の不正は**INVALID / UNSUPPORTED**であり、`MISSING`や`AMBIGUOUS`としない。
2. **利用を許可されたScore候補の元バイト列を列挙する。** 候補がなければ`MISSING`。候補はあるが元バイト列のSHA-256が一致しなければ`MISMATCH`。ファイル名、タイトル、音楽内容が同じJSON再出力によって代用しない。
3. **ハッシュ一致後に必要な参照を解決する。** Profileが要求する識別子・Track・Plan・Visit・範囲・改訂などを確認し、すべて矛盾なく一意に解決した場合のみ`RESOLVED`。一致するハッシュがあっても必須参照が欠落・矛盾・非一意なら、人間向け参照診断として`AMBIGUOUS`とし、根本のエラーを併記する。
4. **暗黙の修復は禁止する。** これらの状態はハッシュ書換え、Score付替え、未知データ削除、保存・演奏成功の認定を許可しない。再関連付けは別の明示的に権限を得た編集であり、確定するまで元のScoreとProfileを保持する。

ハッシュ一致のScoreが解析不能、または必須Core制約に違反する場合は**Score形式検証エラー**を明示し、参照が整合していると装ったり、同名の別Scoreへ自動で変更したりしない。4状態によって前提となる形式エラーを隠さない。この案は真正性・権限・機器安全・分散合意を保証しない。**R04/R11/R13/R14およびD01〜D03は未承認。**

---

> **Historical editorial snapshot: Draft 0.64 (unratified); D01–D05 pending.**


## Draft 0.63 — 関連ProfileとScoreの参照解決を行う判定手順（未採択の規範明確化案）

この手順は、与えられた関連Profileを入手済みのScoreバイト列に対して解釈できるかを判断するものである。JSON Schemaを変更せず、ネットワーク取得や実行をホストへ義務付けない。

1. Profileの版に応じて**必須の参照ハッシュおよび識別子**を読む。Distributed 0.2はルートの`scoreSha256`、Production 0.2は`score.sha256`を使用する。必須ハッシュが欠落・不正、または未対応の版である場合は`MISSING`ではなく、**不正な／未対応のProfile**として4状態の対象外とする。
2. 対象の参照に対し、**明示的に渡された、またはローカルでアクセスが許可されたScoreの元バイト列**のみを候補にする。ファイル名、タイトル、パス、Track名、最新版による推測でハッシュを代替しない。ネットワークから暗黙に取得しない。
3. JSONの再シリアライズ前に、**元のバイト列**のSHA-256を計算する。同じバイト列の複数ファイルは1つのバイト同一性として扱う。ハッシュ一致はこの判定におけるバイト同一性の根拠であり、著作者・真正性の証明ではない。
4. 次の優先順位で判定する。
   - 元Scoreの候補バイト列が全くない：**MISSING**。
   - 一致するバイト同一性が1つあり、Scoreの識別子・改訂、参照Track、および必要なPlan／Visit／範囲が規範Profileに従って解決する：**RESOLVED**。
   - ハッシュ一致の候補はあるが、必須の参照先が欠落・矛盾・一意に特定できない：意味上の参照は**AMBIGUOUS**。ハッシュ一致だけでRESOLVEDとはしない。
   - 候補は存在するが一致するハッシュが1つもない：**MISMATCH**。不一致候補が複数あっても、それだけでAMBIGUOUSにしない。
   - 検査後も相異なるハッシュ一致バイト同一性や矛盾する参照解決が残る：**AMBIGUOUS**。恣意的に1件を選ばない。通常のSHA-256同一性の前提では前者は例外的であり、観測済みと主張しない。
5. 関連Profileの参照が整合していると表明できるのは**RESOLVED**のみである。それ以外ではハッシュや識別子を暗黙に書き換えない。明示的な再関連付けは別の権限付き編集であり、必須参照を見直し、Profileが要求する場合は新しい改訂として保存する。未確定または失敗した場合、旧Profileと旧Scoreを維持する。

この優先順位により、通常のファイル探索における`MISMATCH`と`AMBIGUOUS`の混同を防ぐ。4状態は**人間向けの仕様解釈ラベル**であり、必須のJSON列挙値、標準エラーコード、一般的な信頼モデル、動作検証の結果を意味しない。R04/R11/R13/R14およびD01〜D03の採択待ちである。

---

> **Historical editorial snapshot: Draft 0.62 (unratified).** Companion binding resolution states clarified; D01–D05 pending. Runtime tests excluded, not passed.


## Draft 0.62 — Scoreと関連Profileの参照解決状態（未採択の規範案）

Distributed／Productionの関連Profileを開く際、参照元Scoreのハッシュに対して、**RESOLVED**（元Scoreの正確なバイト列が存在しダイジェスト一致）、**MISSING**（元Scoreの実体が存在しない）、**MISMATCH**（候補は存在するがダイジェスト不一致）、**AMBIGUOUS**（候補または同一性が複数あり意図した参照を特定できない）を区別することを推奨する。表示名・ファイルパス・音楽的に等価な書き出しだけではRESOLVEDと判定しない。同一バイト列の複数コピーは同一のバイト同一性であり、曖昧さには該当しない。

RESOLVED以外の状態で最新Scoreやトラック名から参照を**暗黙に付け替えてはならない**。参照未解決のProfileを読み取り専用表示することはできるが、再関連付けはTrack／Plan／Visit／範囲の参照確認を伴う明示的な操作とする。必要な参照が解決していないセットを完全な無損失保存と主張してはならない。これはR04/R11/R13/R14およびD01–D03向けの**未採択案**であり、新しいJSONフィールド、診断メッセージの標準書式、ネットワーク取得許可、実装の動作検証結果を追加するものではない。

---

## Draft 0.61 — 旧Scoreの保持と障害復旧の境界（提案・未承認）

**依存先の保持：** 旧Scoreの正確なバイト列のハッシュを参照するProfileが整合性を維持できるのは、対応する旧Scoreのバイト列も引き続き取得できる場合に限る。Profileだけの保持では十分ではない。新Scoreと旧Scoreを参照する未変更Profileの組を「新バージョンの整合した一式」と表示してはならない。安全な結果は、(i)旧Scoreと旧Profileを対応付けて保持する、(ii)参照先を確認したうえで選択したProfileを明示的に再関連付けする、(iii)参照未解決・分離状態を報告して無損失の一式と主張しない、のいずれかとする。

**部分的な保存失敗：** 一時ファイルへの出力は、それだけではアトミックなトランザクションではない。クラッシュ、リネーム失敗、権限不足、通信中断などでは、実際に確定したScore/Profileのバイト列と未確定・参照未解決のものを区別し、状態が不明なら成功とみなさない。旧Scoreを黙って破棄せず、未確認のハッシュ更新も行わない。ManifestやUIの表示はアトミックな保存の証明ではない。

**新しいJSONプロパティの追加ではない：** 保存場所、確定処理、バックアップ・復旧画面の詳細は実装責任とする。本節はファイルシステムAPIを定義せず、相互運用上の結果を提案する。DistributedとProduction双方に適用する。R04/R11/R13/R14およびD01〜D03の採択は保留中である。

---

## Draft 0.60 — 楽曲編集後の関連Profileのトランザクション的な再関連付け（未採択案）

楽曲の意味が同じでも、書き出したScoreの**元バイト列**が変われば参照先の同一性は変わります。以下は編集ツール向けの提案手順であり、OSTFの新しいJSON命令やファイルシステムの原子的更新を要求するものではありません。

1. 元Scoreのバイト列とハッシュ、参照元のDistributed／Production Profileを、明示的な新Scoreの書き出しが確定するまで変更せず保持する。参照不明のProfileも個別に記録する。
2. 新Scoreの実際の書き出しバイト列からハッシュを算出する。パース後のオブジェクト、空白の正規化、音楽的同等性、Manifestの値で代用しない。
3. 各Profileを「元Scoreを引き続き参照」「新Scoreへ明示的に再関連付け」「不明・未解決」に分類し、利用者が選んでいないものを暗黙に再関連付けしない。トラック名の一致だけで判断しない。
4. 再関連付けするProfileについて、元の参照ハッシュを確認し、新Score上で参照ID・範囲が解決できることを確認する。解決不能ならProfileを変更せず、具体的な不整合を報告する。イベント、オートメーション、歌唱情報を黙って削除しない。
5. 変更対象は確定まで別の出力先へ書き出す。全ファイル一括成功を約束する実装だけが一括ロールバック責任を負う。OSTF自体はファイル／ZIP／ネットワークの原子的トランザクションを提供しない。
6. 新Scoreのハッシュ、Profileごとの判断、未知データの保持、欠落、Asset不足を報告する。一括処理できない場合は元Profileを元Scoreに紐付けたままScoreだけ出力するか、出力を中止する。未解決の組を無損失・整合済みと表明しない。

Sessionでのイベント確定はScoreの変更承認ではなく、Productionのミキサー設定もScoreのMIDI CCを上書きしません。未知データの保持はその内容の解釈を意味しません。再関連付けはプラグイン／ネットワーク／ロボット実行権限を付与しません。R04/R11/R13/R14およびD01〜D03の**未採択**規範候補であり、JSONフィールドの追加はありません。

---

## Draft 0.56 — 操作別の保持責任と明示的な再関連付け（未採択案）

**読込解析・データ保持・編集・実行・音響再現**は異なる能力です。以下の「しなければならない」はD01〜D03での正式採択を前提とした**規範案**であり、版別JSON Schemaには新しい必須項目を追加しません。

- Scoreの読取専用インポートはSessionイベントを確定せず、Production状態を書き換えません。編集可能範囲だけを「対応」と表明できますが、書出しで未対応情報を削除・変換した場合は欠落を開示します。
- Scoreのバイト単位のハッシュが変化した場合、音楽的に同一でもProfileの関連付けを自動移行しません。明示的な確認と再関連付けが必要です。旧Scoreへの参照を保持する選択もできます。
- Sessionのイベント受理・確定は発音、ロボット動作、オーディオ生成の証拠ではありません。同様にProductionのプラグイン記述子は実行可能なプラグインが存在する証拠ではありません。
- URI・ハッシュ・メタデータが残っていても、実際の外部Assetのバイト列がない場合は欠落として申告します。Mixer/Automationを再現するためにScoreのノート・MIDIイベントを暗黙に改変してはいけません。
- 情報欠落の報告には対象のファミリーとバージョン、操作、影響範囲・外部参照、保持／変換／省略／利用不可の区別を含めることを推奨します。これは**OSTF本体外の報告方式**であり、新規の直列化項目ではありません。

必要なデータを保持も欠落申告もできない場合は「完全互換」を主張せず、対応操作の範囲を限定します。詳細は`CONFORMANCE.md`と`PUBLISHER_RELEASE_DECISIONS.md`のR14を参照してください。

# OSTF 4.3.0 — 楽曲Coreの規範仕様案（Draft 0.55）

> **現行編集版：Draft 0.59（未採択）。** 下記の古いDraft見出しは、累積した策定経緯を示し、現在のJSON版識別子を変更しません。6件の版別Schemaは不変です。公開判定の正本は [RELEASE_READINESS.md](RELEASE_CHECKLIST.md) とし、D01〜D05はすべて承認待ちです。動作・独立実装検証は判定から除外していますが、完了とは扱いません。

## Draft 0.44 — 意味規則IDの重複解消（D01/D04未承認）

従来の`SEMANTIC_RULES.md`ではS13とS14が2つずつ存在し、遠隔Sessionと
Core音楽側の規則を同じ番号で参照していました。本Draftでは先に定義された
**S13=Sessionの状態Revision**、**S14=Session開始・確定範囲**を維持し、
後から追加した**連続fixed区間とhard cutをS22**、**歌詞・歌唱選択をS23**に分離します。
S21は既存のSession音楽テンポ参照として保持します。番号は仕様書の参照IDであり、
優先順位やJSONパラメーターを意味しません。既存4.2の正本・Schemaは変更しません。
英日文書の最終承認D04と意味規則の正式採用D01はまだ完了していません。

## Draft 0.43 — 有限Performance Planでの歌詞・歌唱表現の選択（未採択）

既存4.2のLyric Voice・Unit・Alignment・VocalPerformanceが元Scoreの正本です。`fixed`のVisitごとに選択された**Noteの発音開始出現**と生存ゲートを先に解決し、そのうえでVoice所属と元の歌詞Alignmentの対応を評価します。複数Noteへ結び付くAlignmentの一部だけが選択された場合は**部分選択**であり、元のAlignmentの不正や歌詞全体の再現成功を意味しません。元Noteが連続するSectionをまたぐ場合は一つの出現として扱い、音素や歌唱曲線を結合境界で再トリガーしません。ジャンプによるhard cutでNoteが短縮された場合、元のphonemeEvents・pitchCurves・expressionCurvesの残りを勝手に演奏済みと宣言したり、別Noteへ付け替えたりしません。固定歌唱データに実体化する際は新しいNote IDと整合するVoice/Unit/Alignment/Performance参照を明示的に生成し、不明・近似・欠落を開示します。詳細は`NOTE_AND_MIDI_CUT_SEMANTICS.md`のDraft 0.43節と`examples/15-vocal-response-phrasing.ostf`です。Schema変更・歌唱合成機能・D01/D04承認は伴いません。


## Draft 0.33 — 第三者製ソフトの操作境界（未採択）

同じOSTFのデータを使用しても、**読込、編集プレビュー、Score保存、Production再関連付け、Distributed Sessionのイベント確定、部分Export、規格の正式公開**は異なる操作です。ある操作の成功を別の操作の許可や成功として扱ってはいけません。

| 要求された操作 | 扱う正本 | 無断で実行してはいけないこと |
| --- | --- | --- |
| Scoreを読む・表示する | Scoreのみ | Note生成・Profile変更・プラグイン実行・Assetの自動取得・ロボット制御 |
| 編集内容をプレビュー | 影響を受ける安定IDとsource Tick | 原データやSession履歴の自動更新 |
| Scoreを保存 | 変更対象のScoreと明示したRevision | 元バイトが変更されたのに旧Production/Distributedのハッシュを流用すること |
| Productionを保存・再関連付け | Score原本のSHA-256と制作Profile | 未提供Asset実体の捏造・音源ロード・Score本体の無断変更 |
| Session Eventを確定 | 承認されたSession状態Revision | Score Note・制作Automation・ロボット運動の自動更新 |
| 部分Export | 明示した出力範囲 | 提供済みProfile/Assetを省略して「制作データ一式を無損失保存」と表示 |
| 公開版として出す | 実際に承認された完成アーカイブ | Draft作成やライセンステンプレートを著作者許諾と扱うこと |

**失敗時：** ある保存やイベントの受理が拒否された場合、承認済み状態への部分的変更が起きたかのように報告してはいけません。複数ファイルの保存が部分成功した場合は、ファイル単位で成功・失敗・未実施と情報損失を開示します。すべてのソフトに共通のトランザクション実装方式やレポート用JSONを追加するものではありません。`sourceTick`と展開後の`performanceTick`、Score NoteとSession Phrase、MIDIイベントとProduction Automationの正本は混同しません。

本節はD01〜D04の著作者承認待ちの意味規則案で、JSON Schemaの追加、動作確認、公開承認を意味しません。

---

## Draft 0.32 — 原本バイトの同一性と情報の無損失保持の区別（未採択の編集案）

次の3種類を混同してはなりません。

| 主張 | 必要な根拠 | 保証しないこと |
| --- | --- | --- |
| **Score原本のバイト同一性** | 実際に供給された`.ostf` UTF-8原本バイトのSHA-256照合 | JSONの意味一致、再生、外部取得権限 |
| **Scoreの音楽的情報を保持した保存** | 版に適合する構造・ID・参照・元の音楽情報と、未知情報の保持／損失報告 | JSONの文字列・空白・キー順序まで同一であること |
| **制作データ一式・Asset実体のバイト保持** | 指定された保存範囲について、実際に受領したScore／Profileと不透明なAsset実体バイトを列挙し保持した証拠 | プラグイン実行、同一音色、ロボット動作、未提供Asset実体の保存 |

**関連付け規則案：** JSONを読み取って再保存すると、音楽的な値が同じでも原本のバイト列が変わる場合があります。その場合、以前の`scoreSha256`／`score.sha256`は新しいScore原本を証明しません。旧ハッシュを黙って再利用してはいけません。原本のバイトを不変で保持するか、新しいバイトのSHA-256を計算して当該Profileを**明示的な改訂・再関連付け規則に従って**更新するか、処理を拒否／損失を明示した部分出力とする必要があります。ハッシュ一致のためだけに旧Revisionや稼働中Sessionを書き換えてはいけません。Core 4.3はJSONの正規化ハッシュ方式を定義しません。

HTTPの圧縮やヘッダーはScore原本バイトに含まれません。元のデータを取得できない場合、URLやETag、他Profileのハッシュ申告だけでは原本の同一性を検証できません。**この追補はD01〜D04の未採択候補であり、新しいJSONフィールド・自動公開承認・動作検証の完了を意味しません。**

---

## Draft 0.29 — 第三者製ソフトの診断分類と情報損失の報告（未採択の編集案）

この追補は新しい`.ostf`のフィールド、診断結果を保存する必須JSON形式、APIエンドポイントを定義するものではありません。JSONとして読めること、参照できること、意味を理解できること、無損失に保存できること、実際に音を鳴らせることを**別の能力**として扱います。

| 診断カテゴリー（提案） | 内容 | 原則的な扱い |
| --- | --- | --- |
| `invalid_document` | JSON/Schemaまたはfamily/version識別が不正 | 無断で古いバージョンとみなさず拒否 |
| `unresolved_reference` | Track・Voice・Visit・Assetなどの参照が解決できない | Stable ID・JSON Pointer等を明示して報告 |
| `semantic_conflict` | 同種指示の競合・セッションRevision衝突等 | 配列の最後を優先せず、該当操作を拒否 |
| `unsupported_semantics` | 読めるが意味機能を実装していない | 無損失保存では原データを保持し、未対応を表示 |
| `missing_asset_bytes` | URI/ハッシュのみでプラグイン/音声の実体なし | 記述子の保持とAsset実体の保持を区別 |
| `explicit_loss` | 提供されたProfile/Region/Note/Asset等を省略 | 省略対象IDと範囲を明示した部分・損失ありExport |
| `stale_binding` | 別RevisionやSHAのScoreに付属Profileが残る | 明示的な再関連付けまたは新Sessionを要求 |
| `execution_unverified` | DAW/プラグイン/ロボットの実行結果は未確認 | データの妥当性を可聴再現・安全性の証明としない |

保存・書き出し操作では、**文書ファミリーと正確な版、操作、採否、カテゴリー、影響する安定ID/JSON Pointer、実際に提供された入力データとAsset実体、保持/省略/近似/未解決の範囲**を識別できる報告を推奨します。カテゴリー名は相互運用の説明用語彙であり、新しいSchema列挙値や標準診断ファイルの導入ではありません。

例えば4.3 Scoreを解釈できない旧Readerでも、未知のDirectionを完全に保持できるなら、その保存能力と意味解釈能力は別に報告できます。供給されたProduction ProfileをScoreだけのExportで省略した場合はScoreが完全でも集合全体としては部分Exportです。遠隔イベントが承認されてもCore NotesやStudio情報を書き換えません。各規範文書に矛盾を発見した場合は曖昧な優先順位で解決せず著作者の採用・修正判断へ戻します。

**本追補はDraft 0.29の未承認提案で、実機・独立パーサー検証やライセンス承認の証拠ではありません。** D01〜D05の最終採用が必要です。

---

## Draft 0.28 — 第三者製ソフトの保存・書き出しトランザクション（未承認の規範候補）

この追補は**新しいJSONフィールド、制作プロジェクト用ZIP規格、音声処理・ロボット制御機能を導入しません**。一回の保存・Exportの対象と、実際に入力として提供されたScore・Profile・Asset実体を区別するための編集案です。

| 事例 | 入力として提供されたデータ | 出力 | 正確に表明できる範囲 |
| --- | --- | --- | --- |
| A：Scoreのみの編集 | Scoreのみ。Profileは元から渡されていない | 改訂Score | Score内のすべてを保持できれば「Scoreのみ無損失」。未提供Profileは損失ではない |
| B：制作環境からScoreだけExport | Score、Production Profile、実体の音声・プラグイン状態Asset | Scoreのみ | Scoreが完全でも、**提供済み制作データの一部を省略した部分Export**。省略したProfile、ID、Asset実体を明示 |
| C：状態Assetの記述子だけ受領 | Scoreと、状態ファイルのURI/ハッシュを持つProduction Profile。実体バイトは未提供 | ScoreとProfile | 「記述子の保持」は可。「状態バイトの保持」や「プラグイン再現成功」は不可 |
| D：提供データ全体を保持 | Score、実際に渡された両Profile、実体Asset | 全入力を保持する集合 | バイトと意味の保持が実際に成立する範囲で全提供データの保持と表明可。音声・ロボット動作は別 |
| E：遠隔でフレーズが確定 | Scoreと承認済みDistributedイベント | Core Scoreを保存 | Core Notesは**自動変更されない**。分散イベントは対応Profileを保持した場合だけ継承 |

推奨判断手順：（1）実際に受領した文書のfamily/versionを特定、（2）保存・Exportの対象範囲を明示、（3）Assetの参照記述子と実体バイトを別に棚卸し、（4）提供された各情報について保存・欠落・近似・未解決を判定、（5）Stable IDとパスで影響を説明、（6）無損失で保存できない場合は拒否するか、利用者が理解して選択した別名の部分／損失ありExportとする。

ProfileのScore SHA-256は元のOSTF JSONのUTF-8**原本バイト**に対するものです。Score改訂時にハッシュだけを書き換えて再関連付けを完了したことにしたり、古いセッションの権限・イベント・ロボット制御を暗黙に引き継いだりしません。本提案はD01〜D05の正式採択待ちであり、実機や相互運用検証の結果ではありません。

---

## Draft 0.27 公開者確認（編集用）

正式採用前に`PUBLISHER_RELEASE_DECISIONS.md`のD01〜D05を著作者が個別に判断し、`CONFORMANCE.md`の文書ファミリー・版・対応操作別の表明と、提供済みAssetバイトと参照だけの違いを確認します。これは新しいJSON項目や外部機器を実行する許可ではありません。新規の規範意味規則は未承認のままです。

---

## OSTF 4.3.0 — 規範仕様案（Draft 0.29、未承認）

**策定中・未公開確定。** 4.3はDAW・AI・ジャンル・楽器・通信方式に依存しないUTF-8 JSONの音楽情報交換規格です。音源、演奏エンジン、ネットワークサービス、フィジカルAI制御器ではありません。4.2の全Coreを継承し、作曲・即興・アンサンブルに共通する音楽的意味情報を任意追加します。

## Draft 0.26 — 第三者実装における形式識別と適合範囲（未採択案）

外部ソフトは、JSONのフィールドが似ているという理由で別バージョンを推測してはならない。Scoreは`format`と`version`、Distributed Session 0.2はバージョンを含む`profile`文字列と`recordType`（`profileVersion`は使用しない）、Production Session 0.1.0／0.2.0は`profile`と必須の`profileVersion`で、対象のSchemaを厳密に選択する。未対応のバージョンは無損失に保持するか、破壊的保存を拒否する。JSON読込と、Score/Profile原本照合、外部Asset実体の保持、DSP・WAN同期・ロボット実行は別の対応機能である。詳細な対応表は`CONFORMANCE.md` Draft 0.26を参照する。4.2継承仕様と既存JSONフィールドは変更せず、日英校了と著作者の正式採用は未了である。

本書は4.3で新たに定義する意味規則です。4.2から継承する項目は本パッケージ内の`schema/ostf-4.2.0.schema.json`と公式4.2仕様（`docs/SOURCE_RECONCILIATION.md`参照）に従います。構造の正本は`schema/ostf-4.3.0.schema.json`、詳細な英文規範意味規則は`docs/SPECIFICATION.md`、全項目の正本は`docs/PARAMETER_REFERENCE.md`です。

## 1. 正本の維持

Timelineは構成・テンポ・拍子、Harmonyは和声、Tracks/Clips/Notes/MIDI Eventsは具体的な演奏、LyricsとAlignmentは歌詞・ノートの対応、VocalPerformanceは歌唱表現、Track Directionは生成・解釈に利用する演奏意図、Generation/Provenanceは履歴です。新4.3項目はこれらの正本を置換しません。読込時の自動生成、URL自動取得、AIへの外部送信、物理アクチュエータの自動駆動を行うよう指示するものではありません。

全ての時間付き新Core要素は既存PPQ/Tickに従います。絶対区間は`[start,start+duration)`の半開区間です。Track Directionは別時計を作りません。IDは表示名ではなく安定した文書内識別子です。既存Coreがもつ正本、重複禁止、未知データ保持の原則を継承します。

## 2. phrasing Direction

`tracks[].directions[]`に`type:"phrasing"`を追加します。既存Directionの封筒（`id`, `type`, `start`, `duration`, `parameters`）をそのまま使います。`parameters.adherence`（strict / preferred）は必須です。ほかに少なくとも1つの音楽パラメーターを指定します。

- `phraseLengthTicks`: `{min,max}`、それぞれ正の整数、`min<=max`。フレーズ分割の意図を表すものでClipを自動分割しません。
- `onsetGroupsPerQuarter`: `{min,max}`、0～128、`min<=max`。同一Track内の同Tick同時発音は1つの発音開始グループとし、フレーズ中の異なる発音開始数×PPQ÷フレーズ長Tickを密度とします。複数の同時和声音は1群です。
- `development`: repetition / motivicVariation / sequence / contrast / free。
- `contour`: ascending / descending / arch / valley / stable / free。全体的な音高輪郭であり、局所的な逆方向移動をすべて禁じる意味ではありません。
- `energyShape`: rising / falling / arch / valley / stable / free。抽象的な盛り上がりであり、Velocityや音量カーブの正本ではありません。
- `motifRef`: 既存`phraseLibrary.templates[]`に存在するIDを参照します。

音階は既存`improvisation`、音域は`pitchRange`、役割は`playingRole`が担当します。`phrasing`自体は実際のノートを変更しません。既存の具体的フレーズ境界が明示されない場合、strictなフレーズ長・発音開始密度の充足は機械的に確定できません。実装は任意の独自分割を規格唯一の正解と主張してはいけません。

## 3. vocalFreedom Direction

既存Direction封筒を用い、`parameters.voiceId`、`textPolicy`、`melodyPolicy`、`adherence`を必須とします。Voiceは同じTrackに属する既存`lyrics.voices[]`のIDに解決しなければなりません。歌詞とメロディの自由度はそれぞれ独立です。

- `textPolicy`: fixed（既存テキストを固定）、alternatives（明示した候補Phrase列から選択）、open（未確定）。
- `melodyPolicy`: fixed（既存旋律を固定）、ornamentable（装飾可）、open（未確定）。
- `vocalizationKind`: lexical / scat / humming / nonLexical（任意）。
- `candidatePhraseSets`: alternativesの場合に限り2個以上必須。各候補の`phraseIds[]`は対象VoiceのLyric Documentに属する既存Phrase ID列を参照し、完全に同じ候補を繰り返してはいけません。

候補選択・テキスト生成・旋律生成では、具体的なLyrics/Notes/Alignmentを書き換える前に明示的な編集操作を必要とします。生成されていない歌詞やノートを偽のプレースホルダーとして正本へ追加しません。発声表現は既存4.2のVocalPerformanceを使います。`melodic` Trackだからという理由だけでボーカルと推測しません。

## 4. ensembleInteractions

ルート任意配列`ensembleInteractions[]`はTrack/Voice間の方向付き関係です。`actorTrackId`は行動する側、`partnerTrackId`は対象です。異なる実在Trackの組合せを通常としますが、**同一Track内の異なる2つのLyric Voice**であれば同一Track IDの組合せも許します。この場合は`actorVoiceId`と`partnerVoiceId`がともに必須で、異なる実在Voiceを参照し、両方の`trackId`がそのTrackと一致しなければなりません。同じVoiceが自分自身を相手にする関係は不正です。異なるTrack間の関係ではVoice IDは任意ですが、指定する場合は所有Trackと一致する必要があります。

Relationは`respondTo`、`followRhythm`、`alternateWith`、`leaveSpaceFor`、`reinforce`の5種です。`adherence`は必須です。適用条件としてsourceの`start+duration`または`scope:{performancePlanId,visitId}`の少なくとも片方が必要です。双方がある場合は、そのVisitのsource区間との交差する部分だけに適用し、交差がなければ不正です。方向付きなので逆向き関係を自動追加しません。`responseWindowTicks`は音楽時間であり、ネットワーク遅延を表しません。

## 5. performancePlans

ルート任意配列`performancePlans[]`は`mode:"orderedFinite"`の有限の演奏順序です。各Planの`visits[]`は0から連続する一意の`ordinal`を持ちます。各Visitは参照するSection ID列またはSource Rangeのどちらか1つを必須とします。同一Visit内でSection区間が重複してはいけません。別Visitで同じSectionを再訪することは可能です。

訪問された元区間`[S,S+L)`が展開先Tick `P`から始まる場合、範囲内Tick `t`の演奏上位置は`P+(t-S)`です。Source Tickは元曲の正本であり、Performance TickはVisit展開から導かれる二次座標です。元のNote/Chord/SectionのIDを複製したことにはなりません。切替位置でSourceのTempo/Meter/Key/Harmonyを必ず再評価します。元の小節を無関係な前のVisitのテンポで演奏してはいけません。

`parts[].realization`はfixed（確定sourceノートを使用）、open（このVisitでは既存ノートも再生せず未確定の演奏として扱う）、silent（無音）の3つです。未記載TrackはPlanの`defaultRealization`（fixed/silent/unspecified）に従います。unspecifiedを勝手にfixedとみなして完全再生できるとは主張できません。

Visit固有の`parts[].role`は元Trackのデフォルト役割を当該Visitで一時的に置き換えます。同じsource区間に矛盾する`playingRole` Directionがあれば、`replacesDirectionIds`に該当IDを明示して衝突解決します。元Directionの削除・変更はしません。

### Source区間の境界での確定ノート／MIDI

`fixed`ではSource Noteの開始Tickが選択半開区間`[S,E)`内にある攻撃（Note On）のみを選択します。開始前から持続するNoteに境界SでNote Onを作りません。ただし**同一Visit内で前区間の終了Source Tickと次区間の開始Source Tickが一致し、同じTrackが双方で`fixed`のままなら連続結合**です。この場合、前区間内で開始したNoteのゲートを連続する次区間へ持続させ、境界で人工的なNote Off/Onを挿入しません。Source Tickのジャンプ・ギャップ、Visit変更、`open`/`silent`への切替ではハードカットし、残るゲートをその位置で終えます。元Noteの長さ・IDは変更しません。新区間の開始Tickで始まる別Noteはその新しい半開区間に一度だけ属します。連続結合では既に選択したMIDI制御状態を通常の時間順に保持できますが、不連続カットでは過去のCC/Program Change/Pitch Bendを暗黙に再生成・複製してはいけません。再生に必要な状態が不足すれば、その状態不足を報告します。詳しくは`docs/NOTE_AND_MIDI_CUT_SEMANTICS.md`を参照してください。

### Draft 0.40 追補 — `fixed`と演奏結果の決定性（未承認案）

`fixed`は各Visitで**既存のsource Note/MIDIイベントを選ぶ方式**を確定しますが、すべてのNoteが必ず発音し、常に同じVelocityになることは保証しません。OSTF 4.2の`track.enabled`、`clip.enabled`、`note.enabled`による再生可否を尊重し、無効な要素があっても元データを消さないでください。

- `note.probability`は0〜1、未指定は1。0は発音しません。0より大きく1より小さい場合、実際に選ばれる発音結果は未確定です。OSTFは乱数列・シード・Visitごとの抽選方法を標準化しません。同じsource Noteが2回出現しても同じ発音結果を強制しません。
- `note.velocityDeviation`は既存の相対的なVelocity変動終点で、未指定は0です。非ゼロ値だけでは具体的なVelocityの抽選結果は一意に決まりません。`velocity`自体が未指定の場合も、勝手に既定値を保存してはいけません。`releaseVelocity`と`pitchRole`などの4.2の意味は変更しません。
- 完全に決定的なNote/MIDI出力を主張する場合は、確定した発音の採否とVelocityを明示したノートへ具体化する必要があります。元Scoreを無断変更せず、必要に応じて新RevisionのScoreに異なるVisit出現ごとに固有Note IDを割り当てます。未確定のMIDI CC/Program状態についても別途報告します。
- `fixed`に含まれる不発音/確率的Noteと、`open`（元の固定演奏を使用しない）や`silent`（演奏させない）は異なります。どちらもファイル読込だけでAIに作曲や即興を実行させる指示ではありません。

この追補は4.2のNote状態の**意味の整理**であり、4.3 Schema/JSONフィールドや乱数方式の新設ではありません。例は`examples/25-source-note-repeated-visits.ostf`を参照してください。正式採用D01と文書・例の承認D04は保留中です。

## 6. performanceRequirements

`tracks[].performanceRequirements`は演奏者の能力の申告ではなく、**その楽曲パートの実現に必要な音楽上の能力**です。任意に`requiredPolyphony`、`requiredPitchRange`、`requiredArticulations`、`peakOnsetGroupsPerQuarter`を持ちます。既存`instrument.playablePitchRange`と矛盾する音域を定義してはいけません。演奏者の実力、ロボットの速度、関節、モーター、安全停止、レイテンシーはこのCoreの対象外です。

## 7. ID・重複・互換性

新Core要素IDは既存ID空間に属し、文書全体で一意とします。同Trackの`phrasing`同士は重複禁止。同Trackかつ同Voiceの`vocalFreedom`同士も時間重複禁止ですが、異なるVoice同士は重複できます。異なるDirection種類は独立であり、配列順や「後勝ち」は優先順位になりません。

4.2に存在しない任意情報を新規に推測せず、4.2有効文書を4.3へ移行できるようにします。4.3から4.2へ情報損失を伴って書き戻す場合は、失われるJSON Pointerを明示し、元の4.3文書を保持します。不明な情報を理解できないEditorは非破壊保存または保存拒否を行い、黙って破棄しません。

## 8. Distributed Session Profileとの境界

遠隔人間・AI・フィジカルAIは、楽曲Coreとは別のSession Profileで参加者・役割割当て・音楽演奏位置・時計観測・提案・承認イベントを共有します。Draft 0.6では`OSTF-Distributed-Session-0.2`を別冊として提案します。個別の通信プロトコルを規格の必須条件にせず、イベント受信だけでロボットを駆動しません。セッション提案や演奏状態は元の`.ostf`文書を自動変更しません。詳細は`docs/SESSION_PROFILE.ja.md`および`docs/SESSION_STATE_MACHINE.md`を参照します。

## 9. 機能適合と公開判定

OSTF Core Reader/Writer、Direction-aware、Ensemble-aware、Plan-aware、Vocal-aware、Requirement-aware、Session-profile-awareは独立した対応段階です。フォーマットに対応したというだけではAI生成能力・音質・ネットワーク遅延・ロボット動作を保証しません。今回の策定では動作・実機・独立パーサー検証をリリース判定条件から除外していますが、それらを検証済みとみなすものではありません。公開権利確認と編集上の仕様確定は引き続き必要です。

## 10. Draft 0.4 補足 — 同一Trackの複数VoiceとPlan展開後のNote識別

同一Track内で合いの手を行う複数のLyric Voiceは、`ensembleInteractions`で両方のVoice IDを明示し、異なるVoice IDである場合に限り相互関係を記述できます。Voiceは4.2のLyric Voiceが正本であり、同じTrackだからといってVoiceを統合したり音声チャンネルを自動追加したりしません。

同じSource Noteを複数のVisitで参照して演奏する場合、**元Note IDは同一**ですが、演奏上の各出現は`performancePlanId + visitId + sourceSegmentOrdinal + sourceNoteId`で識別できるものとします。この組はPlan解釈時の内部識別子であって、新しいCore NoteのIDではありません。Clip内相対Tickはまず元のSong Tickへ変換してからSource区間の半開境界を判定します。Source Noteを繰り返しても元のNotesを複製・変更しません。

Planの演奏結果を固定した新しいOSTF文書に保存する場合は、各出現のNoteに新しい一意のCore IDを付け、新文書Revisionと由来を記録します。読込やPlan参照だけではこの書き込みを行いません。

## 11. Draft 0.5 補足 — 固定Visitの歌詞・歌唱表現

同じ元Noteが複数Visitで演奏されても、元の`lyrics.units`や`lyrics.alignments`のIDは複製しません。各Visitでの演奏は異なる**出現**ですが、元の歌詞・ノート・VocalPerformanceの正本は変わりません。Source区間境界でNoteのゲートが切られた際、音素タイミングや歌唱表現の曲線が境界を越えている場合、それらを無条件に切り詰めて完全再現と宣言してはいけません。複数Noteに関連付く歌詞Unitの一部だけが選択される場合も、欠落・曖昧さを明示したうえで新しい文書への明示的な具体化を行います。`docs/SPECIFICATION.md`を参照してください。

## 12. Draft 0.5 補足 — 分散セッションの演奏開始

別冊Profile 0.2に`sessionStarted`を追加し、`prepared`から`playing`への遷移を明示します。演奏位置の時計アンカーはCore OSTFではなくSnapshot/Eventで管理します。任意の`commitmentWindow`によって確定済みSessionフレーズの完了範囲を主張できますが、未記載なら完全性の保証はありません。通信やロボットの安全性・実行能力は依然としてCoreの対象外です。

## 13. Draft 0.6 — 遠隔Sessionフレーズの確定条件

今回のCore Schema自体は変更しません。別冊Profile 0.2で承認されたフレーズは、固定されたPerformance Planの**明示的に`open`と指定された対象Track Part**の範囲にのみ割り当てられます。`fixed`に重ねる、`silent`を鳴らす、`unspecified`を未承認のまま`open`と解釈する操作は、規格上許されません。フレーズ全体が同一Visitに収まらない場合は分割・再提案します。`prepared`の段階でもPlanが固定されていなければ確定できません。詳しい意味規則は`docs/SESSION_STATE_MACHINE.md`です。4.3 Coreの正本や元のNoteは変えません。

## 14. Draft 0.7 — 楽曲Revisionの固定と遠隔演奏の履歴の分離

OSTF Coreの楽曲構造・演奏・歌詞の正本は、セッションの受信イベントでは変更されません。別冊Profile 0.2の1つのSessionは、同じ`documentId`・`revisionId`・有限の`performancePlanId`を参照し続けます。Web APIで新しい楽曲Revisionを取得しても、現在のSessionの楽曲を自動で入れ替えてはいけません。同じ文書ID・Revision IDで異なる内容を受け取った場合は、同一の演奏位置を共有できると見なさず、整合性の問題を報告します。

承認済み`phraseCommitted`はセッション内の**確定履歴**であり、音が鳴った証拠ではありません。`visitChanged`で後のVisitへジャンプして以前に確定したフレーズを飛ばした場合、または`sessionStopped`で将来の演奏が停止した場合、元の確定レコードは保持しますが、飛ばした/停止後のフレーズを演奏済みと表示してはいけません。Profile 0.2の演奏Tickは原則として前方へ進み、同一Sessionでの巻き戻しや新しい楽曲Revisionへの切替は扱いません。これらが必要な場合は、新しいSessionまたは将来の拡張仕様が必要です。

イベントの再送は`eventId`と内容の一致を**先に**調べ、既に承認済みの同一イベントなら、Revisionが進んでいても二重採用しません。同じIDの内容違いは不正であり、別IDで古い`baseStateRevision`のイベントも採用しません。演奏トラックの担当参加者を変更しても、確定済みフレーズを他のロボットへ自動実行させる意味にはなりません。必要な残作業と判定条件は別冊`docs/SESSION_STATE_MACHINE.md`に詳述します。

これは**4.3 Coreではなく別冊Session Profileに対する意味規則**です。Schemaは変更せず、公開者による採用判断が必要な策定案です。

## 15. Draft 0.8 — 別冊Distributed Session Profileのデータ整合性

OSTF 4.3 Coreを変更せず、未公開の別冊Session Profile 0.2の`assignmentChanged`では`position`と`targetVisitId`をそれぞれ禁止します。以前のSchema条件式は`position`の単独混入を拒否できなかったため、今回は構造的に修正しました。担当者の変更は演奏の時計アンカーを変更できません。時計アンカーを持つ遷移は`sessionStarted`のみです。保持されたすべての`committedPhrase`のNoteは、`commitmentWindow`の有無にかかわらず親Phraseの半開区間内に収まらなければなりません。停止やスキップによって歴史的な承認済みPhraseが残っていても、現在の担当者や実発音の存在を証明しません。再送された同一IDを確認する際は認証・固定楽曲Revisionの照合を先に行い、その後にID内容の一致を確認し、新規イベントだけに状態Revisionの新旧照合を適用します。数値の比較は十進数の正確な値で行い、損失のある型変換で同一と推測しません。詳細は`SESSION_STATE_MACHINE.md` Draft 0.8節を参照してください。これらは公開者の承認前の案です。

## Draft 0.9 — 別冊分散セッションのPlan固定とバイト列照合

OSTF 4.3 CoreのSchemaおよび4.2から継承した音楽上の正本は変更しません。**別冊の未公開Distributed Session Profile 0.2のみ**、全SnapshotとEventにルート直下の`performancePlanId`と`scoreSha256`を必須としました。`prepared`でPositionがなくても参照する有限Performance Planを確定できるようになります。`scoreSha256`は取得した元OSTFの正確なUTF-8バイト列のSHA-256であり、文書名・Revisionだけが一致する異なるJSONを無断で同じ演奏に使わないための照合値です。Position内のPlan IDはルートと一致させます。SHA-256は認証・所有権・実機駆動の許諾ではありません。詳細と規範的な判定順序は`SESSION_STATE_MACHINE.md` Draft 0.9節に定義します。

## Draft 0.10 — 遠隔Visit切替の時計基準

**別冊の未承認Distributed Session Profile 0.2のみ**を改訂します。従来`visitChanged`は移動先Visit IDだけを記述していましたが、遠隔演奏の切替時刻を再特定する必要があるため、`position`を必須とします。`position.visitId == targetVisitId`、`position.performanceTick == Event.effectivePerformanceTick == 対象Visitの開始演奏Tick`とし、`sourceTick`はVisitが最初に参照するソース区間の開始Tickとします。UTC時刻`epochUtc`はそのTickを示す推定時計基準で、受信時刻ではありません。これは演奏位置の意味情報であり、通信・ロボット制御の安全性や音声出力を保証しません。OSTF 4.3 Core、4.2正本、既存NoteやLyricsは変更しません。

## Draft 0.11 — 分散セッションの時計ドメインとテンポの整合（未承認）

別冊Profile 0.2では、`sessionStarted`で設定した音楽時計の`clockDomainId`を、演奏中のSnapshotと`visitChanged`の新しい時計基準位置でも維持しなければならない。演奏途中の時計ドメイン変更はProfile 0.2では表現できず、新しいSessionを必要とする。`position.tempoBpm`は説明情報で、元OSTFの`timeline.tempoChanges`の`sourceTick`で有効な値と一致しなければならない。Session側のテンポで元の楽曲を書き換えない。`sessionStopped.effectivePerformanceTick`は記録上の位置であり、将来停止予約またはロボットの緊急停止命令ではない。詳細は`SESSION_STATE_MACHINE.md` Draft 0.11および`SESSION_PROFILE.ja.md`を参照する。これらはCore 4.3への新パラメーター追加ではなく、公開者の最終採用待ちの意味規則である。

## Draft 0.12追補：遠隔セッションの有効テンポと時計基準（未承認）

別冊Distributed Session Profile 0.2の`playing` Snapshot、`sessionStarted`および`visitChanged`が提示する`position`は、固定されたOSTF原曲の`sourceTick`において有効なTempoを解決できなければなりません。`position.tempoBpm`の省略をデフォルトテンポの存在と解釈してはいけません。テンポ未解決の演奏中時計位置は`E-SESSION-TEMPO-UNRESOLVED`として拒否します。元の曲の選択区間とテンポ変更点ごとに `60 × Tick差 / (PPQ × BPM)` を積算し、省略区間の時間やテンポを暗黙に継承してはいけません。これは理想的な音楽時刻の定義で、遠隔地での実時計精度や物理動作の保証ではありません。さらに別冊ProfileのSnapshotの`participants[]`は1名以上必要です。いずれも4.3 Coreの楽曲フィールドを変更しない編集案です。

## Draft 0.13 — 別冊Production Session Profile 0.1.0

第三者製の独立した音楽制作アプリのために、Mixer（Mute/Solo/音量/Pan）、音声Bus/Send、エフェクト・音源の順序付きDevice Chain、Plug-in IDと不透明State参照、Automation、Host固有データを表す任意の別冊JSON Profile案を追加します。**OSTF 4.3 CoreとDistributed Session Profile 0.2のSchemaは変更しません。** Core `track.enabled`とAudio Mixer Mute、MIDI CCと音声Mixerは異なる正本として維持します。定義案は`PRODUCTION_SESSION_PROFILE.ja.md`、型と値域は`PRODUCTION_PARAMETER_REFERENCE.md`を参照してください。著作者による採用承認は未了です。

## Draft 0.20：別冊ProfileとScore改訂時の責任分離

本改訂ではOSTF 4.3 Coreのフィールド・定義を変更しない。Scoreが新しい実体バイト列・Revisionになった場合、別冊Production Profileは旧版を保持したまま、Track参照と元source Tickの録音/Automationを著者がレビューして新しいコピーへ明示的に再関連付けできる。一方、Distributed Sessionは旧Score/Plan/Clock/Event履歴をそのまま維持し、**新しいSession IDが必要**である。`score.sha256`だけの書換えで安全な無損失変換とみなしたり、Web APIの自動取得・プラグイン実行・ロボット動作の権限を認めたりしてはならない。未採用の規範候補の詳細はProduction Profile日英第26節。

## Draft 0.21 — 無損失保存とProfileの対象範囲

新しいCoreフィールドは追加しない。OSTF ScoreとProduction/Distributed Session Profileは独立した正本・版番号を持つ。Coreのみを読み込むソフトは別冊Profileを無視してよいが、受領した制作プロジェクト全体の「無損失保存」を主張しながら、別冊Profileや不透明Asset本体を黙って破棄してはならない。未対応の新しい意味情報を保存できないWriterは、無損失上書きを拒否するか、利用者に損失を明示した別のExportとする。Score原本のバイト列が変われば旧Profileのハッシュ固定は無効で、Productionの再関連付けは著者が新しいコピーとして明示的に行う。Distributedの既存Sessionには付け替えず、新しいSession IDを用いる。具体的な未採用規範案は`CONFORMANCE.md`とProduction Profile第27節。ソフトウェアの実装・プラグイン実行・フィジカルAIの動作を定義するものではない。

## Draft 0.22 — Coreと別冊Profileの正本の分離（未採用）

OSTF 4.3はバージョン付きの**楽曲Score JSON**である。Production Session ProfileとDistributed Session Profileは**別々の版を持つ任意のJSON文書**であり、隠れたOSTF Coreフィールドではない。各Schemaは宣言された文書の構造にのみ適用し、CoreのNote、Track、Harmony、Lyrics、MIDIの正本を変更しない。開発ZIP、`PACKAGE_MANIFEST.json`、`SHA256SUMS.txt`は規格配布用であり、制作プロジェクトの標準コンテナーやHTTP APIを定義するものではない。

規格の適合では、各Schemaの構造、独立した規範案、例示、外部Assetの**実体の有無**、DAW/ロボット等の実行を区別する。旧Draftと現行規範案に解釈の矛盾があれば、文書の更新順や配列順から暗黙の優先順位を作らず、公開者の編集上の決定として解消する。`CONFORMANCE.md`とProduction Profile第28節を参照。新しいCoreパラメーターは追加しない。

## Draft 0.23 — Score・別冊Profileの解釈順序（未採用の編集案）

過去Draftの記述を残しているため、実装者は以下を現行案の基準とする。フィールドの型・必須性は**文書ごとの版に一致するJSON Schema**、4.2から継承する音楽的な意味は正式4.2仕様、4.3の新しい意味は本書の現行4.3規範案、Distributed/Productionの意味は**各別冊Profileの版別規範案**で解釈する。以前の編集履歴を、現在の原本ハッシュ固定や元Score Tickの扱いを上書きする代替規則として使ってはならない。現行規範案同士が矛盾する場合は公開者が決定する未解決事項であり、配列順や「新しい記述優先」をアプリが推測してはならない。

`scoreSha256`と`score.sha256`はそれぞれ**別冊Profile**のフィールドであり、Core 4.3の新しいルート項目ではない。元ScoreのUTF-8**実バイト列**を照合する。セッション内の`phraseCommitted`はDistributed Sessionの履歴であり、Scoreの`notes[]`、Productionの`audioRegions[]`、プラグイン設定を自動変更しない。複数文書の関連付けは、外部リソースの取得・ソフトのインストール・ロボット駆動の許可にはならない。**新しいJSON項目は追加しない。**

## Draft 0.24 — 3領域の版選択と状態変更の責任分界（未採択案）

OSTF楽曲本体はルート`format:"OSTF"`と`version:"4.3.0"`で識別します。分散セッションSnapshot/Eventは`profile:"OSTF-Distributed-Session-0.2"`と`recordType`で識別し、**`profileVersion`を持ちません**。Production Profileは`profile:"OSTF-Production-Session"`と`profileVersion:"0.1.0"`または`"0.2.0"`で識別します。構造上、これらを1つのJSONへ暗黙統合する仕様ではありません。

分散セッションの新規状態変更イベントは、現在のRevisionと`baseStateRevision`が一致しなければ確定してはいけません。一方、元から承認済みで全データが等しい同一`eventId`再送は、認証・楽曲固定情報の照合後、冪等な無操作とします。異なる内容への再利用は禁止です。詳細は`SESSION_STATE_MACHINE.md`に委ね、CoreのNote/MIDI/歌詞は変更しません。著作者の正式採用と公開権利承認は引き続き未完了です。

## Draft 0.25 — 第三者実装と正本の分離（未採択案）

OSTF 4.3の確定済みノート・MIDI、音楽的演奏指示、遠隔セッションの承認イベント、制作環境のミキサー/音声リージョン/プラグイン状態は、それぞれ別の正本を持つ。JSONを読み込めても、全データの無損失保存、音声処理、ロボット制御まで対応したとは主張できない。**元のAssetバイトが未入手なら、参照記述子の保存は「音源実体の保持」と同義ではない。** 分散セッションの承認フレーズはScoreのノートを自動追加しない。Scoreの新Revisionに従属Production/Distributedを暗黙に移行しない。

詳しい第三者実装の対応表・失われる情報の分類・規範資料の参照先は`CONFORMANCE.md`のDraft 0.25を参照する。4.2継承の正本と6 Schemaは変更せず、日英校了・著作者による新規規範採用・公開権利承認を要する。



## Draft 0.35 — Schema選択・サンプル対応表（規範案・未承認）

データの読み込み時には、楽曲Coreの `format` と `version`、Distributed Sessionの `profile` と `recordType`、Production Sessionの `profile` と `profileVersion` を識別し、厳密に対応するSchemaを選択する。未知の版を既知の版に無断で置き換えない。

同梱45件のJSONサンプルは、Core楽曲25件、Distributed Session 17件（0.1の2件と0.2の15件）、Production Session 3件（0.1の2件と0.2の1件）である。ファイルごとの対応は `docs/EXAMPLES_GUIDE.md` に示す。これは同梱例の索引であり、機能の網羅性や独立実装の相互運用性を保証するものではない。

対応を表明するソフトウェアは、構造的読込、参照の整合、受領した情報の無損失保持、意味の解釈、音響・ロボット実行をそれぞれ区別しなければならない。Schemaへの適合だけでプラグイン起動・遠隔イベント受理・ロボット制御を許可しない。これらの文面はD01〜D04で正式採択待ちである。

### Draft 0.41 — 連続するSource区間の結合と不連続カット（未採択）

A `[0,3840)`→B `[7680,11520)`は元の時間軸が飛ぶため、Aの終端3840で持続中のNoteを切ります。一方B `[7680,11520)`→C `[11520,15360)`が同一Visitで、該当Trackの`fixed`を維持するなら連続結合です。Bで11280から720 Tick持続するNoteはCの先頭をまたぎ、元Source Tick12000まで持続できます。C開始11520に別NoteがあればC側のNote Onとして一度だけ扱います。次のVisitへ移る場合は、Source Tickが偶然連続していてもハードカットとします。新しいフィールドではなく、Performance Planの再生対象となるSource Note/MIDIの選択・ゲートの意味規則案です。`probability`や`velocityDeviation`の実際の決定、楽器音源の音声Tailや録音リージョンのFade、音素・ロボット動作の連続性を保証するものではありません。D01（音楽的意味規則）とD04（翻訳/例の校了）の明示的承認が必要です。


## Draft 0.42 — 有限Performance Planにおけるノート指定MIDIイベント（D01/D04未承認）

4.2から継承するCC、Pitch Bend、Channel Pressure、Poly Pressureの`targetNoteId`は、**保存済みの元Noteとの意味上の関連**です。MIDI Channel/Pitchの伝送上の意味や実際のMPEルーティングを置き換えるものではありません。以下は`fixed`の演奏区間を展開する際の規範候補であり、元の4.2データの改変を要求しません。

1. MIDI Eventの元楽曲位置は`clip.start + midiEvent.start`とし、各Visitの`fixed` Partが選んだ半開区間に入るイベントだけを、その元IDで一度選択します。区間の終端Tickは次の区間に属します。省略された小節のイベントからProgram/CC等の初期状態を捏造しません。
2. `targetNoteId`のないイベントは元のChannel/Busのイベントです。省略区間のコントローラー状態は補完されず、ハードカット直後には状態が不明な場合があります。
3. `targetNoteId`のあるイベントの**演奏上の対象Note**を確定できるのは、そのNoteの発音開始が選択され、当該Tickまで同一Visit内の連続した`fixed`区間でゲートが有効なときだけです。選択外の小節で発音したNoteは、その後のCC等の時刻が選択区間に入っても自動的には選択されません。連続Sectionで持続中のNoteは、元の攻撃位置に対応する一つの出現のままです。
4. 対象Noteが選択されない、無効化されている、または発音確率により実出力が未確定の場合、当該イベントを**別のNoteやtargetなしのChannelイベントに無断で読み替えてはいけません**。元のEventのバイト/参照は保持します。確定MIDI出力には明示的な省略・保持・近似の方針と損失報告、または出力拒否が必要です。MPE/マルチティンバーでは特に重要です。元Scoreの構造不正とは限りません。
5. 展開した診断上のNote出現は`(performancePlanId, visitId, sourceAttackSegmentOrdinal, sourceNoteId)`、イベント出現は`(performancePlanId, visitId, eventSegmentOrdinal, midiEventId)`で識別できます。連続SectionをまたいでNoteが持続すると、両者のSegmentOrdinalは異なっても構いません。これらは保存用の新しいCore IDではありません。新しいScoreに確定保存する場合にのみ、新規Core IDと妥当な`targetNoteId`参照を生成します。
6. 4.2の`order`は同TickのMIDI Event順序に従来どおり適用しますが、MIDI EventとNote Onとのすべての順序を新規に定義しません。決まらない実行順序を勝手に確定したと扱いません。

**サンプル17：** `target-prior-note-selected`は選択されたNoteを参照します。`ctrl-omitted-gap`は選択外です。`target-prior-note-not-selected`の元Noteの攻撃Tickは7400で、次のSectionに含まれないため対象を確定できません。一方`target-across-contiguous-join`は、連続するTwo→Threeの境界を越えて持続しているNoteを参照できます。これは静的な規格例であり、DAW/MIDI音声処理・ロボット実機検証を意味しません。

## Draft 0.45 — Voice／Clip全体の歌唱表現の投影（S24、未承認）

4.2の`VocalPerformance`では、`noteId`を持たない`phonemeEvents`、
`targetNoteId`を持たない`techniques`や`expressionCurves`、独立した
`breathEvents`を記録できます。これらを、歌詞Alignmentが存在するだけで
特定Noteに結び付けてはいけません。4.3の有限`fixed` Planでは、個々の
時間付きイベントの開始位置を`clip.start + item.start`でSource Tickに
変換し、選択した半開区間に開始位置がある場合にだけ派生出現を認めます。
選択外の開始位置を区間先頭に移動しません。同一Visitの連続fixed区間を
またぐイベントは一回の出現として継続し、ジャンプやVisit変更による
hard cutでは残りを切断します。`noteId`を持たない音素の`unitId`を、
根拠なくNoteのAlignmentへ変換しません。

`targetNoteId`を持たない表現カーブはVoice／Clip全体の情報です。
複数点の場合は元Source Tickでの指定点間のみ既存4.2の補間が定義され、
範囲外は未指定です。一点だけのカーブは元Clip／Voiceの適用範囲で
定数です。区間ジャンプ後に前Visitの値を持ち越さず、未指定値を
`0.5`などで補完せず、原本への境界点の自動追加もしません。
既存のNote単位のカーブとの置換関係は4.2の規則を継承し、二重加算しません。
ブレスなどの非Note対象イベントは、休符中に存在してもNoteの実発音を
証明しません。確定歌唱として書き出す場合は新RevisionとID再対応、
切断・近似・未解決音素の情報損失を明示します。具体例は
`examples/15-vocal-response-phrasing.ostf`、詳細は英語規範案のS24です。
これらはD01/D04の採用待ちで、Schemaの新フィールドではありません。


## Draft 0.70 — 候補集合の探索完了と慎重な参照判定（未採択）

参照の4状態は、**実際に評価できた範囲での判定**であり、インターネット上の全候補を探索した保証ではない。実装は許可された候補の探索範囲、およびその列挙と実体バイト取得の完了・未完了を明示しなければならない。ファイル名、申告されたハッシュ、HTTPヘッダー、音楽的な一致だけでは検証済みとはしない。

1. 許可された候補集合の列挙またはバイト取得が不完全な場合は、外部診断 **NOT_EVALUATED** とする。これはOSTFの新しいJSON値ではない。
2. 候補集合の探索と取得が完了している場合、候補Scoreが0件ならその範囲において **MISSING**、Scoreが1件以上存在しても元バイト列のSHA-256一致がなければ **MISMATCH** とする。世界中に存在しないという意味ではない。
3. ハッシュ一致候補の同一バイト列は重複コピーとしてまとめ、Track／Plan／Visitなど必須参照が欠落または一意に解決できない場合は **AMBIGUOUS** とする。`missing_referent` と `nonunique_referent` はJSONに格納しない診断補足とする。
4. ハッシュと必須参照がすべて整合して初めて **RESOLVED** とする。
5. 許可された候補の列挙または実体バイト取得が一つでも未完了なら、一致候補をすでに観測していても **NOT_EVALUATED** と報告する。部分的・条件付きの **RESOLVED** は認めない。未完了の探索範囲を明示し、候補集合が未完了のままMISSING・MISMATCH・AMBIGUOUS・RESOLVEDを推定してはならない。古いProfileを改訂Scoreへ暗黙に付け替えてはならない。

INVALID／UNSUPPORTEDは形式・バージョンに関する事前エラーであり、4状態とは別扱い。SHA-256だけで著作者の認証やDAW・プラグイン・遠隔AI・ロボットへの実行権限は得られない。本規則はD01〜D03の正式採択前の仕様候補であり、実装検証済みではない。


## Draft 0.76 — 参照判定規則の文書統合（未採択）

上記Draft 0.70の第5項に残っていた部分的`RESOLVED`の例外を撤回し、Draft 0.71／0.73の現行優先規則と一致させた。INVALID／UNSUPPORTEDは参照判定前の形式エラー、許可済み候補の列挙・取得が未完了なら外部診断`NOT_EVALUATED`、探索完了後にのみMISSING／MISMATCH／AMBIGUOUS／RESOLVEDを判定できる。探索完了前に得たハッシュ一致は暫定証拠であり、**RESOLVEDではない**。新しいJSONフィールドやネットワーク探索義務は追加しない。D01〜D03の正式採択前の規範案である。


---

## 3. 制作Session 0.2の正式4.3日本語規範の継承全文

> **現行採択候補：Draft 0.77（未承認）。** 冒頭の参照解決判定表を現行提案とし、下位の旧Draft番号を持つ節は履歴であって並列の現行規範ではありません。今回の変更は編集上の特定であり、Schemaやシリアライズ形式は変更しません。

# Draft 0.73 — 現行の参照解決判定表（未採択の規範案）

**承認対象：D03。** 以下が現行の採択候補であり、後続のDraft 0.62〜0.72の記述は改訂履歴として保持する。古い判定例を並立する現行規則として扱わない。発行者の採択前に規範として確定したわけではない。Schema・シリアライズ形式は変更しない。

| 優先順 | 条件 | 実装側の診断 |
|---|---|---|
| 1 | ProfileのJSON・必須pin・形式が不正 | `INVALID`（4状態の対象外） |
| 2 | Profileの形式・版が未対応 | `UNSUPPORTED`（4状態の対象外） |
| 3 | 許可範囲が未定義、候補列挙未完了、必要なScore実体を取得不可 | `NOT_EVALUATED`（暫定情報は別途報告、確定4状態を返さない） |
| 4 | 明示的に許可された完全な候補集合にScore実体が0件 | `MISSING`（評価範囲内に限る） |
| 5 | Scoreの実体はあるが、元バイト列のSHA-256がpinと一致しない | `MISMATCH`（評価範囲内に限る） |
| 6 | ハッシュ一致したScoreが構造的に不正または解析不可 | Score形式エラー（`RESOLVED`ではない） |
| 7 | 一致する正常なScore内のTrack/Plan/Visit/range等の必須参照が欠落・重複・不正 | `AMBIGUOUS`＋具体的な診断（`missing_referent`、`nonunique_referent`等） |
| 8 | 元バイト列とハッシュが一致し、必要な参照がすべて一意に解決 | `RESOLVED`（評価範囲内に限る） |

**同一性と権限の境界：** 宣言されたハッシュ対象の元Scoreファイルのバイト列を使用する。Unicode正規化、改行変換、BOM除去、JSONの再シリアライズ、ZIP全体のハッシュによる代替は禁止する。同じバイト列のコピーは同一のバイト同一性を持つ。ファイル名、URI、キャッシュしたハッシュ、音楽上の等価性だけでは同一としない。探索に失敗した候補を黙って除外せず、範囲を狭める場合は新しい評価として明示する。診断名はJSON Schemaに追加するフィールドではない。ハッシュ一致は著作権、信頼性、アクセス権、音響再現、遠隔実行、ロボット安全性を保証しない。編集後の付け替えには明示的承認と新しいpinが必要。

**公開管理：** D01〜D05はすべて未承認。独立パーサー、DAW／プラグイン／DSP、歌唱、WAN／分散実行、フィジカルAI／ロボットの動作検証は公開GO条件から除外し、実施済みとも主張しない。

---

# Draft 0.72 — 編集上の優先順位と採択範囲（未承認）

**採択対象：D03／Production Session 0.2。** 正式採択の対象は、承認記録で特定する本文と既存Schemaに限る。過去Draft 0.62〜0.70の参照判定例は改訂履歴として残し、並立する定義として扱わない。矛盾する参照診断については**現行候補内で**Draft 0.71の「許可された候補集合の列挙・取得が完了してから判定」する規則を優先し、未完了ならJSONに新項目を追加せず外部診断`NOT_EVALUATED`とする。

第三者実装は、(a)未知データの読込・保持、(b)ラウンドトリップ保存、(c)編集、(d)意味解釈、(e)実行を区別する。いずれか一つの対応を他の操作まで拡大して表明しない。ハッシュ一致は分散演奏実施、ミキサーの音響再現、ロボット動作の保証にならない。これらの規範案は**D03が発行者により正式採択された場合のみ**規範効力を持つ。

> **Current proposed editorial precedence: Draft 0.71.** This first section supersedes the Draft 0.70 incomplete-enumeration RESOLVED exception; historical sections below are retained as version history. No publisher adoption is implied.

## Draft 0.71 — 参照判定の探索完了条件（未採択の規範案）

Draft 0.70の「探索が未完了でも追加候補で結果が変わらないと予測できればRESOLVEDにできる」という例外を撤回する。未確認候補に関する予測を検証済みの根拠として扱ってはならない。

1. Profileの構造と対応バージョンを先に確認する。不正・未対応なら参照判定とは別の`INVALID`／`UNSUPPORTED`を報告する。URIやハッシュの存在はScore実体へのアクセス許可にならない。
2. **明示された有限かつアクセスが許可された候補集合**を定義し、その範囲、列挙完了、各候補の実バイト取得とSHA-256計算の有無を記録する。判定は宣言された範囲に限定し、世界中に存在しないと断定しない。
3. 候補列挙が未完了、または必要な候補の元バイトが取得できない場合は、外部診断`NOT_EVALUATED`と取得済みの根拠を示す。ハッシュ一致候補が1つ見つかっても4つの確定状態を報告しない。より狭い集合を明示的に定義し直して再評価してもよいが、除外した候補と探索範囲変更を必ず開示する。
4. 列挙と取得が完了した集合について、候補が0件なら`MISSING`、候補があるが生バイト列のSHA-256一致が0件なら`MISMATCH`、一致したScoreの必須参照が欠落・重複・無効なら`AMBIGUOUS`、一致と全必須参照の一意解決が揃った場合のみ`RESOLVED`とする。
5. 同じScoreバイト列の複数コピーは同一データとして扱う。名称、URL、音楽内容、申告ハッシュだけで一致としない。改訂Scoreへの付け替えには明示的な許可と新ハッシュの指定が必要。参照判定だけで実行・通信・音響・プラグイン・ロボット制御を許可しない。

`NOT_EVALUATED`／`INVALID`／`UNSUPPORTED`／診断補足は報告用で、JSONフィールドやSchema enumの追加ではない。4つの判定名称も新しいシリアライズ項目ではない。この規則はD01・D02・D03の正式採択前の提案で、動作・相互運用検証は未実施である。

---

# Draft 0.69 — Score候補の探索範囲と判定の確実性（未採択）

**R04/R11/R13/R14の提案規範。** 4種類の参照診断は、対象操作について**明示的に提供・許可された候補集合内**で判定する。無関係なローカルフォルダーや遠隔URL、リポジトリを勝手に探索して`MISSING`を`RESOLVED`へ変更してはならない。利用者またはホストが追加の元バイト列を許可した場合は**新たな評価**として再判定する。

- **許可された元バイト列候補が0件：** `MISSING`。あくまで評価対象内で未発見であり、Scoreの世界全体における消失を断定しない。
- **候補が1件以上あるがピンのハッシュと一致しない：** `MISMATCH`。候補がすべて新しいリビジョンでも同じ。旧Scoreが全世界から消えたとは断定しない。
- **ハッシュ一致・Score構造不正：** `RESOLVED`ではなくScore形式エラー。
- **ハッシュ一致・必須参照先が0件または複数件：** `AMBIGUOUS`に詳細`missing_referent`または`nonunique_referent`を付す（JSONに追加するフィールドではない）。
- **必要な参照がすべて一意に確定：** 評価対象内で`RESOLVED`。同じバイト列の複製は単一の同一性として扱う。

キャッシュされたハッシュ、ファイル名、URL、署名付きリンク、索引の一致だけでは、実際のScoreの元バイト列による照合を代替できない。候補の元バイト列を取得できず評価自体が行えなかった場合、操作側で`not_evaluated`/`unknown`等を報告してよいが、これはOSTFの第5の参照状態ではない。確認済みの`MISSING`や`MISMATCH`と偽ってはならない。参照診断はデータの真正性、発音、プラグイン復元、ロボットの実行許可を保証しない。**D01～D03、D05、D04は未承認。**

---

# Draft 0.68 — 参照診断の判定順序と過去の事例表の整合（未採択）

**現行の提案（R04/R11/R13/R14）:** 明示的に許可されたScore候補だけを用い、次の順序で判定する。過去のDraftの表が異なる場合、この節を現行の編集提案とし、過去の記録は履歴として残す。

1. Companionの形式・バージョン・必須ハッシュが不正／未対応なら`INVALID / UNSUPPORTED`。4種類の参照診断には含めない。
2. Scoreの元バイト列の候補が1件もなければ`MISSING`。ファイル名やメタデータの一致は候補とみなさない。
3. 候補が存在するが元バイト列のSHA-256が1件も一致しなければ`MISMATCH`。**新版Scoreだけが存在する場合も同様**。Draft 0.62の旧事例でこの場合を`MISSING`とした記述は現行提案では採用しない。
4. 一致したScoreが解析不能または必須構造違反なら、参照成功とせずScore形式エラーとして報告する。
5. 一致して正常なScoreの必須参照を全件調べる。参照先0件は`AMBIGUOUS`と詳細`missing_referent`、複数件は`AMBIGUOUS`と`nonunique_referent`、矛盾・範囲違反は`AMBIGUOUS`とその詳細を示す。複数の問題があればそれぞれ報告する。
6. 必須参照がすべて一意に解決した場合のみ`RESOLVED`。同じバイト列を持つ複数のパスは1つのScore同一性として数える。

この状態名・詳細は**実装側の診断指針**であり、新しいJSONフィールドやSchema列挙値ではない。認証、演奏実行、無断ネットワーク取得、権利許諾、自動的な再関連付けを許可しない。日本語版と英語版の意味が異なる場合は採択を保留する。D01〜D05は未承認。実機・独立パーサー等の検証は条件外かつ未実施。

---

# Draft 0.67 — 参照診断の意味規則の確定候補（未採択）

**公開前の要判断事項（R04/R11/R13/R14）:** Draft 0.64では、必須のTrack/Plan参照先が「存在しない」ケースを`AMBIGUOUS`と呼んでいます。一方、通常の意味では`AMBIGUOUS`は「候補が複数で一意に定まらない」ことを表します。これは提案文書の解釈上の曖昧さであり、Schemaの欠陥や検証結果ではありません。

**採択推奨:** 新しいJSONフィールドや状態の列挙値は導入せず、既存の4つの人間向け診断分類を維持します。対応するProfileを構造的に確認し、許可された元Scoreの**生バイト列**のSHA-256一致を先に要求します。その後、必須Track/Plan/Visit参照先の件数が**0件**ならサマリーは`AMBIGUOUS`とし、診断詳細で`missing_referent`を示します。**2件以上**なら同じサマリーでも詳細は`nonunique_referent`とします。各必須参照が1件に確定した場合のみ`RESOLVED`です。詳細ラベルは推奨診断名であり、OSTFの新規フィールド・enum値・保存必須データではありません。`MISSING`は元Scoreの正確なバイト列がない場合に限り使用し、Score内部の参照欠落には流用しません。

**参照元の信頼境界:** 呼出元が明示的に提供・許可したScore候補のみ参照できます。ファイル名、URL、タイトル、意味的に等しい再シリアライズ結果は生バイト一致の証拠になりません。外部ネットワークからの無断取得、暗黙の付け替え、根拠のない可逆保存の表明は禁止する方針を採択候補とします。

**審査状況:** D01〜D03による採択・修正・却下が必要です。D04/D05も未承認です。動作・独立パーサー・DAW・WAN・ロボットの検証は対象外で未実施です。

---

# Draft 0.66 — 現行審査基準（未採択）

この節は**現行Draft 0.66の審査基準**です。本文に残る旧Draft番号の追記は経緯を示す資料であり、独立した現行版の規範ではありません。Schema・サンプル・ツールは変更していません。

- **Core 4.3:** `schema/ostf-4.3.0.schema.json`と現行Core仕様書・意味規則。4.3で変更を明記していない部分は4.2を継承します。
- **Distributed Session 0.2:** Versionに対応するSchemaと日英Session仕様書。セッションのイベントや同期状態は、ネットワークサービスの保証やロボット実行の許可ではありません。
- **Production Session 0.2:** Versionに対応するSchemaと日英Production仕様書。ミキサー設定・プラグイン記述・アセット参照は、実際のDSP実行や音声再現を保証しません。
- **権限の優先順位（採択案）:** 構造制約は該当バージョンのSchema、意味制約は該当バージョンの規範仕様を参照します。例示、旧版追記、チェックリストはこれらを上書きできません。Schemaと規範仕様が矛盾した場合は、任意解釈を認めず公開阻害要因として修正します。
- **Score参照:** 先にProfileの形式・Versionを検査し、元Scoreのバイト列のSHA-256一致を確認後、必要な参照を解決します。RESOLVED／MISSING／MISMATCH／AMBIGUOUSは診断用の名称でJSONフィールドではありません。不正形式・未対応版は4状態に含めません。参照先不足の具体的な原因を記録し、暗黙の再関連付けを禁止します。
- **対応表明:** Score／Distributed／Production、Version、読込／編集／保存／保持／実行を区別し、未対応や欠落を表示します。

R01〜R14の一括採択は提案段階です。D01〜D03の発行者承認、D05の権利承認、D04の最終ZIP承認は引き続き未完了です。動作・独立実装・実機検証は公開判定から除外し、実施済みとは表記しません。

---

## Draft 0.64 — 形式検証と参照解決の境界（未採択の規範案）

Draft 0.63の4状態は、**形式上有効かつ認識可能な関連Profile**について、元Scoreの参照が解決するかを表す診断である。JSONフィールドや通信上の状態コード、動作認証ではない。判定順序は次のとおり。

1. **関連Profileを先に形式検証する。** Profile種別と版、規定の位置にある必須SHA-256参照の書式を確認する。未対応版や必須参照の不正は**INVALID / UNSUPPORTED**であり、`MISSING`や`AMBIGUOUS`としない。
2. **利用を許可されたScore候補の元バイト列を列挙する。** 候補がなければ`MISSING`。候補はあるが元バイト列のSHA-256が一致しなければ`MISMATCH`。ファイル名、タイトル、音楽内容が同じJSON再出力によって代用しない。
3. **ハッシュ一致後に必要な参照を解決する。** Profileが要求する識別子・Track・Plan・Visit・範囲・改訂などを確認し、すべて矛盾なく一意に解決した場合のみ`RESOLVED`。一致するハッシュがあっても必須参照が欠落・矛盾・非一意なら、人間向け参照診断として`AMBIGUOUS`とし、根本のエラーを併記する。
4. **暗黙の修復は禁止する。** これらの状態はハッシュ書換え、Score付替え、未知データ削除、保存・演奏成功の認定を許可しない。再関連付けは別の明示的に権限を得た編集であり、確定するまで元のScoreとProfileを保持する。

ハッシュ一致のScoreが解析不能、または必須Core制約に違反する場合は**Score形式検証エラー**を明示し、参照が整合していると装ったり、同名の別Scoreへ自動で変更したりしない。4状態によって前提となる形式エラーを隠さない。この案は真正性・権限・機器安全・分散合意を保証しない。**R04/R11/R13/R14およびD01〜D03は未承認。**

---

> **Historical editorial snapshot: Draft 0.64 (unratified); D01–D05 pending.**


## Draft 0.63 — 関連ProfileとScoreの参照解決を行う判定手順（未採択の規範明確化案）

この手順は、与えられた関連Profileを入手済みのScoreバイト列に対して解釈できるかを判断するものである。JSON Schemaを変更せず、ネットワーク取得や実行をホストへ義務付けない。

1. Profileの版に応じて**必須の参照ハッシュおよび識別子**を読む。Distributed 0.2はルートの`scoreSha256`、Production 0.2は`score.sha256`を使用する。必須ハッシュが欠落・不正、または未対応の版である場合は`MISSING`ではなく、**不正な／未対応のProfile**として4状態の対象外とする。
2. 対象の参照に対し、**明示的に渡された、またはローカルでアクセスが許可されたScoreの元バイト列**のみを候補にする。ファイル名、タイトル、パス、Track名、最新版による推測でハッシュを代替しない。ネットワークから暗黙に取得しない。
3. JSONの再シリアライズ前に、**元のバイト列**のSHA-256を計算する。同じバイト列の複数ファイルは1つのバイト同一性として扱う。ハッシュ一致はこの判定におけるバイト同一性の根拠であり、著作者・真正性の証明ではない。
4. 次の優先順位で判定する。
   - 元Scoreの候補バイト列が全くない：**MISSING**。
   - 一致するバイト同一性が1つあり、Scoreの識別子・改訂、参照Track、および必要なPlan／Visit／範囲が規範Profileに従って解決する：**RESOLVED**。
   - ハッシュ一致の候補はあるが、必須の参照先が欠落・矛盾・一意に特定できない：意味上の参照は**AMBIGUOUS**。ハッシュ一致だけでRESOLVEDとはしない。
   - 候補は存在するが一致するハッシュが1つもない：**MISMATCH**。不一致候補が複数あっても、それだけでAMBIGUOUSにしない。
   - 検査後も相異なるハッシュ一致バイト同一性や矛盾する参照解決が残る：**AMBIGUOUS**。恣意的に1件を選ばない。通常のSHA-256同一性の前提では前者は例外的であり、観測済みと主張しない。
5. 関連Profileの参照が整合していると表明できるのは**RESOLVED**のみである。それ以外ではハッシュや識別子を暗黙に書き換えない。明示的な再関連付けは別の権限付き編集であり、必須参照を見直し、Profileが要求する場合は新しい改訂として保存する。未確定または失敗した場合、旧Profileと旧Scoreを維持する。

この優先順位により、通常のファイル探索における`MISMATCH`と`AMBIGUOUS`の混同を防ぐ。4状態は**人間向けの仕様解釈ラベル**であり、必須のJSON列挙値、標準エラーコード、一般的な信頼モデル、動作検証の結果を意味しない。R04/R11/R13/R14およびD01〜D03の採択待ちである。

---

> **Historical editorial snapshot: Draft 0.62 (unratified).** Companion binding resolution states clarified; D01–D05 pending. Runtime tests excluded, not passed.


## Draft 0.62 — Scoreと関連Profileの参照解決状態（未採択の規範案）

Distributed／Productionの関連Profileを開く際、参照元Scoreのハッシュに対して、**RESOLVED**（元Scoreの正確なバイト列が存在しダイジェスト一致）、**MISSING**（元Scoreの実体が存在しない）、**MISMATCH**（候補は存在するがダイジェスト不一致）、**AMBIGUOUS**（候補または同一性が複数あり意図した参照を特定できない）を区別することを推奨する。表示名・ファイルパス・音楽的に等価な書き出しだけではRESOLVEDと判定しない。同一バイト列の複数コピーは同一のバイト同一性であり、曖昧さには該当しない。

RESOLVED以外の状態で最新Scoreやトラック名から参照を**暗黙に付け替えてはならない**。参照未解決のProfileを読み取り専用表示することはできるが、再関連付けはTrack／Plan／Visit／範囲の参照確認を伴う明示的な操作とする。必要な参照が解決していないセットを完全な無損失保存と主張してはならない。これはR04/R11/R13/R14およびD01–D03向けの**未採択案**であり、新しいJSONフィールド、診断メッセージの標準書式、ネットワーク取得許可、実装の動作検証結果を追加するものではない。

---

## Draft 0.61 — 旧Scoreの保持と障害復旧の境界（提案・未承認）

**依存先の保持：** 旧Scoreの正確なバイト列のハッシュを参照するProfileが整合性を維持できるのは、対応する旧Scoreのバイト列も引き続き取得できる場合に限る。Profileだけの保持では十分ではない。新Scoreと旧Scoreを参照する未変更Profileの組を「新バージョンの整合した一式」と表示してはならない。安全な結果は、(i)旧Scoreと旧Profileを対応付けて保持する、(ii)参照先を確認したうえで選択したProfileを明示的に再関連付けする、(iii)参照未解決・分離状態を報告して無損失の一式と主張しない、のいずれかとする。

**部分的な保存失敗：** 一時ファイルへの出力は、それだけではアトミックなトランザクションではない。クラッシュ、リネーム失敗、権限不足、通信中断などでは、実際に確定したScore/Profileのバイト列と未確定・参照未解決のものを区別し、状態が不明なら成功とみなさない。旧Scoreを黙って破棄せず、未確認のハッシュ更新も行わない。ManifestやUIの表示はアトミックな保存の証明ではない。

**新しいJSONプロパティの追加ではない：** 保存場所、確定処理、バックアップ・復旧画面の詳細は実装責任とする。本節はファイルシステムAPIを定義せず、相互運用上の結果を提案する。DistributedとProduction双方に適用する。R04/R11/R13/R14およびD01〜D03の採択は保留中である。

---

## Draft 0.60 — 楽曲編集後の関連Profileのトランザクション的な再関連付け（未採択案）

楽曲の意味が同じでも、書き出したScoreの**元バイト列**が変われば参照先の同一性は変わります。以下は編集ツール向けの提案手順であり、OSTFの新しいJSON命令やファイルシステムの原子的更新を要求するものではありません。

1. 元Scoreのバイト列とハッシュ、参照元のDistributed／Production Profileを、明示的な新Scoreの書き出しが確定するまで変更せず保持する。参照不明のProfileも個別に記録する。
2. 新Scoreの実際の書き出しバイト列からハッシュを算出する。パース後のオブジェクト、空白の正規化、音楽的同等性、Manifestの値で代用しない。
3. 各Profileを「元Scoreを引き続き参照」「新Scoreへ明示的に再関連付け」「不明・未解決」に分類し、利用者が選んでいないものを暗黙に再関連付けしない。トラック名の一致だけで判断しない。
4. 再関連付けするProfileについて、元の参照ハッシュを確認し、新Score上で参照ID・範囲が解決できることを確認する。解決不能ならProfileを変更せず、具体的な不整合を報告する。イベント、オートメーション、歌唱情報を黙って削除しない。
5. 変更対象は確定まで別の出力先へ書き出す。全ファイル一括成功を約束する実装だけが一括ロールバック責任を負う。OSTF自体はファイル／ZIP／ネットワークの原子的トランザクションを提供しない。
6. 新Scoreのハッシュ、Profileごとの判断、未知データの保持、欠落、Asset不足を報告する。一括処理できない場合は元Profileを元Scoreに紐付けたままScoreだけ出力するか、出力を中止する。未解決の組を無損失・整合済みと表明しない。

Sessionでのイベント確定はScoreの変更承認ではなく、Productionのミキサー設定もScoreのMIDI CCを上書きしません。未知データの保持はその内容の解釈を意味しません。再関連付けはプラグイン／ネットワーク／ロボット実行権限を付与しません。R04/R11/R13/R14およびD01〜D03の**未採択**規範候補であり、JSONフィールドの追加はありません。

---

## Draft 0.56 — 操作別の保持責任と明示的な再関連付け（未採択案）

**読込解析・データ保持・編集・実行・音響再現**は異なる能力です。以下の「しなければならない」はD01〜D03での正式採択を前提とした**規範案**であり、版別JSON Schemaには新しい必須項目を追加しません。

- Scoreの読取専用インポートはSessionイベントを確定せず、Production状態を書き換えません。編集可能範囲だけを「対応」と表明できますが、書出しで未対応情報を削除・変換した場合は欠落を開示します。
- Scoreのバイト単位のハッシュが変化した場合、音楽的に同一でもProfileの関連付けを自動移行しません。明示的な確認と再関連付けが必要です。旧Scoreへの参照を保持する選択もできます。
- Sessionのイベント受理・確定は発音、ロボット動作、オーディオ生成の証拠ではありません。同様にProductionのプラグイン記述子は実行可能なプラグインが存在する証拠ではありません。
- URI・ハッシュ・メタデータが残っていても、実際の外部Assetのバイト列がない場合は欠落として申告します。Mixer/Automationを再現するためにScoreのノート・MIDIイベントを暗黙に改変してはいけません。
- 情報欠落の報告には対象のファミリーとバージョン、操作、影響範囲・外部参照、保持／変換／省略／利用不可の区別を含めることを推奨します。これは**OSTF本体外の報告方式**であり、新規の直列化項目ではありません。

必要なデータを保持も欠落申告もできない場合は「完全互換」を主張せず、対応操作の範囲を限定します。詳細は`CONFORMANCE.md`と`PUBLISHER_RELEASE_DECISIONS.md`のR14を参照してください。

# OSTF Production Session Profile 0.1 / 0.2 — 日本語規範仕様案（Draft 0.55）

> **現行編集版：Draft 0.59（未採択）。** 下記の古いDraft見出しは、累積した策定経緯を示し、現在のJSON版識別子を変更しません。6件の版別Schemaは不変です。公開判定の正本は [RELEASE_READINESS.md](RELEASE_CHECKLIST.md) とし、D01〜D05はすべて承認待ちです。動作・独立実装検証は判定から除外していますが、完了とは扱いません。

## Draft 0.33 — Production保存・再関連付けの操作境界（未採択）

Productionの保存や新Scoreへの再関連付けは、Scoreの作曲編集やDistributed Sessionイベントの確定と独立した操作です。参照情報があるだけでプラグイン状態・外部Asset実体の完全保存を主張してはいけません。Profileの参照解決によってScore Note、Session状態、実際の音声素材を書き換えてはいけません。複数文書を扱う場合、変更／未保存／損失を文書ごとに開示します。詳細は`CONFORMANCE.md`。Schema変更はありません。

---

## Draft 0.32 — Score再保存後のProduction関連付け（未採択）

`score.sha256`はJSONの意味ではなく、**実際のScore原本バイト**に対応します。音楽情報に変更がなくてもJSONの再保存によりハッシュが変わる場合があります。その場合、既存Profileのハッシュだけを無断で書き換えることはできません。新しいScoreに対して明示的なProduction Profileの複製・再関連付けと、必要なTrack／Tick／Planの影響確認を行うか、集合全体の無損失保存の主張を取り下げて損失の範囲を報告します。URLや記述子だけではScore原本やAsset実体バイトが実際に供給された証拠になりません。`CONFORMANCE.md` Draft 0.32を参照。Schema変更はありません。

---

## Draft 0.29 — 制作ソフトの診断と保存能力の区別（未採択）

`docs/CONFORMANCE.md`と`docs/SPECIFICATION.ja.md`のDraft 0.29診断カテゴリー案を参照。プラグイン状態のURI/ハッシュのみを保持することと実体バイトの保持、未対応Sidechainの意味解釈と情報の無損失保持、Score単独Exportと制作環境全体の保持、旧Revisionへの参照と明示的再関連付けを分けて報告する。これは新しいProduction JSON項目ではなく、著作者採択待ちの説明規則。

---

## Draft 0.28 公開候補 — 保存対象と実体バイトの範囲

一回の書き出しで「Scoreのみ」「Scoreと実際に提供されたProduction Profile」「Profileに列挙されたが提供されていないAsset記述子」「実体バイトも含む全提供データ」を区別します。`docs/SPECIFICATION.ja.md`のDraft 0.28事例A〜Eと`docs/CONFORMANCE.md`を参照してください。**Profileが元から無い場合は損失と判定しませんが、入力として渡されたProfile/Asset実体を省略した書き出しは無損失の制作環境Exportとは表明できません。** スコア改訂時の再関連付けには明示的な確認が必要です。これらは採択待ちの編集案です。

---

## OSTF Production Session Profile 0.1.0 / 0.2.0 — 日本語仕様案

**策定状況：OSTF 4.3 Draft 0.29付属の未承認実験仕様。正式採用・公開権利は未確定。** 1〜11節は旧Profile 0.1の規範案、12節以降は0.2の追加案である。`profileVersion`ごとに別Schemaを用いる。

## 1. 目的と責任分界

本Profileは、OSTF 4.3の音楽的Coreとは独立して、第三者の音楽制作ソフトが使用する**ミキサー・Solo/Mute・音量・Pan・音源/エフェクトの順序・プラグイン識別子・状態参照・音声Bus/Send・Automation**を交換するための別冊JSON仕様である。

「Production Session」は**保存された制作環境**を意味する。遠隔AI/ロボットの参加者・演奏同期イベントを表す別冊「Distributed Session Profile 0.2」とは別物である。OSTF Coreも本Profileもソフトウェアではなく、プラグインを実行する機能は含まない。

規範的な構造は `schema/ostf-production-session-0.1.schema.json`、意味規則の詳述は英語版 `docs/PRODUCTION_SESSION_PROFILE.md` に置く。日本語版は意味を一致させることを目標とする出版候補であり、最終編集承認は未実施。

## 2. ファイル構造とScoreの固定

必須ルート項目：`profile:"OSTF-Production-Session"`、`profileVersion:"0.1.0"`、`score`、1件以上の`channels[]`。`devices[]`、`assets[]`、`automation[]`、`hostExtensions[]`は任意。

`score.formatVersion`は`4.3.0`。`score.sha256`は参照元`.ostf`の**UTF-8の元バイト列**に対する小文字64桁SHA-256である。JSONを整形・保存し直すとハッシュは変わる。`documentId`と`revisionId`を記す場合は元のCoreのDocument情報と一致しなければならない。`score.sourceUri`は情報上の参照であり、自動ダウンロード命令ではない。ハッシュ一致は著作者認証・実行権限を意味しない。

## 3. TrackとMixerの分離

`channels[].kind`は`track`、`bus`、`master`。`track`の場合だけCoreの`tracks[].id`を`trackId`で参照する。Coreの`track.enabled`、`clip.enabled`、`note.enabled`などは**音楽情報側の再生対象**であり、Production Profileの`mute`、`solo`とは別の正本である。`track.enabled=false`の曲を、Mixerの`mute=false`によって勝手に有効化してはならない。

各Channelは`id`、`kind`、`audioChannels`（1または2）、`gainDb`（-120〜+24、0がユニティ）、`pan`（-1左〜+1右）、`mute`、`solo`、`soloSafe`、順序付き`deviceIds[]`を持つ。未指定のGain/Mute等に隠れたデフォルト値を補完しない。`master`は全Profile中1つで、出力先は持たない。その他のChannelはBusまたはMasterへの`outputChannelId`を指定する。出力＋Sendの音声グラフは循環禁止、Sendの宛先はBusに限定する。

`mute=true`は原則としてそのChannelの音声出力とSendを抑止する意図を示す。`solo`はミキサー上のオーディション選択、`soloSafe`はSolo選択中に保持する意図を示す。特にBus Solo、Pre-fader Send、Sidechainの厳密な発音動作はホスト差があるため、音の完全な同一性は保証しない。対応できない場合は警告とデータ保持を行う。

CoreのMIDI CC7（Volume）、CC10（Pan）、CC11（Expression）、CC91/93（Effect Send）は**MIDI演奏/音源制御**であり、本Profileの音声ミキサーGain/Pan/Sendへ置き換えない。両者を同一の正本にしない。

## 4. 音源・エフェクトチェーン

Channelの`deviceIds[]`は並び順が処理順である。Device IDは全Profile内で独立・一意で、1つのDeviceは1つのChannelにのみ属する。`instrument`はTrack Channelの先頭に最大1件、`effect`と`utility`は後続の列として利用できる。Bus/MasterにはEffect/Utilityを置けるが、Instrumentは置かない。複数段のRack、並列FX、マルチインストゥルメントは0.1では未定義。

`devices[]`は`id`、`role`、`plugin`、`enabled`、`bypass`を必須とし、任意の`stateAssetId`と`onUnavailable`を持つ。`plugin.format`は`vst2/vst3/clap/au/aax/builtin/hostNative/other`、`plugin.pluginId`はその形式の識別名前空間内でのみ意味を持つ不透明な文字列である。表示名やVendor文字列だけで別のプラグインと同定しない。プラグインのファイルパス、ライセンス、実行可能コードをここで標準化しない。

`enabled=false`（Deviceスロットを不使用）と`bypass=true`（スロットの処理をバイパス）は区別する。これらはCore Trackのenabledと同一ではない。

## 5. プラグイン状態・代替処理

プラグイン独自のStateバイナリはJSONに直接埋めず、`assets[]`の`purpose:"pluginState"`と`stateAssetId`で参照する。Assetには`uri`、元バイト列SHA-256、任意のサイズ・MIMEを保持する。パスはZIPなどのパッケージ内でのPOSIX形式相対参照、または明示的な権限で利用するHTTPSを想定する。`file://`、親フォルダへの遡り、任意の自動外部アクセスを拒否する。OSTFはプラグインバイナリ仕様の互換性を保証しない。

未インストールのプラグインについて、`onUnavailable`に`reportAndPreserve`、`preserveAndBypass`、`preserveAndSilence`を指定できる。どれも*音色の完全復元*を保証しない。未知の状態参照と識別子を保ち、読み込み不能・バイパス・無音などの損失を通知する。同名別製品への自動置換は禁止。

## 6. Audio Bus / Send

Coreの`midi.buses[]`は論理MIDI出力先であり、Production ProfileのAudio Busとは別概念である。`channels[].outputChannelId`は音声出力先、`sends[]`は`id`、`targetChannelId`、`gainDb`、`preFader`、`enabled`で構成する。物理オーディオI/O、Sidechain、Feedback、Surround、並列Rackは0.1の対象外であり、欠落なく再現できない場合は警告する。

## 7. Automation

`automation[]`は対象Channel（Gain/Pan/Mute）またはDeviceパラメーターの時間系列を記述する。`points[]`は各`{atTick,value}`で、TickはScoreの**元のGlobal Tick**。Tickは非負の昇順・重複なし、同一ターゲットにつき1 Laneとする。繰り返しのVisitで同じ元区間が演奏される場合、元区間のAutomationを再適用し、以前のVisitの制御状態を無断継承しない。

- MuteのAutomationは`valueType:boolean`＋`interpolation:step`。
- Gainは-120〜+24 dB、Panは-1〜+1の数値。
- Device Parameterは識別子`parameterId`と0〜1の正規化数値。パラメーター名や尺度のホスト間の互換性は保証しない。
- 初回Point以前は静的なChannel/Device値、最終Point後は最後の値を保持する。数値Laneは`linear`または`step`。SoloのAutomationはv0.1では定義しない。
- AutomationはMIDI CCやopaque Plugin Stateを自動的に書き換えない。該当パラメーターの再生時値を決めるのみ。

## 8. サードパーティー独自拡張

`hostExtensions[]`は`namespace`、任意の`version`、非実行JSONの`data`からなる。独自ソフトのWindow配置、製品固有機能、ホストの設定等を記述できるが、Coreや標準Mixerフィールドの正本を密かに上書きしてはいけない。非破壊保存を宣言するソフトは未知の標準/独自フィールドを保持する。保存できなければ明示的に損失を報告する。

## 9. 携帯用の配布・公開

`score.ostf`、`production.ostfprod.json`、`assets/…`をZIPにまとめる運用は推奨例だが、OSTFの必須拡張子・公式パッケージ標準ではない。Coreだけを読み取るアプリはProfileを実装せずに利用できる。Web APIはScore JSONまたはProfile JSONを別々に提供できるが、HTTP認証/プラグイン実行権限はOSTF規格外である。

## 10. 適合性と公開判断

Profile 0.1のSchema・参照規則に対応するReader、Writer、Device Adapter等の適合宣言は機能別に行う。Schemaに合格してもプラグイン音質の一致・状態復元・DAW互換性を保証しない。演奏できないDevice、欠落Asset、出力/Sendのループ、未知Track、無効なAutomation、CoreとProfileのScore SHA不一致について、エラーと損失警告を区別する。

付属の`tools/validate_production_profile.py`は編集用の構造・部分的意味チェックであり、VST3/CLAP、DAW、フィジカルAI、WANの実行テストではない。ユーザー指定によりこれら実機/独立検証を公開判定条件から除外するが、検証済みとは記載しない。

## 11. 既存規格との関係

DAWprojectは音声Region、Automation、Mixer、デバイスStateをより深く交換する既存規格であり、実装上の重要な参考となる。本Profileの導入はDAWprojectを廃止・代替するものではない。相互変換では再現不能な項目を明示する。関連資料： https://github.com/bitwig/dawproject/blob/main/Project.xsd 。

## 12. Production Session Profile 0.2の位置付け

Profile 0.2.0は`profile:"OSTF-Production-Session"`と`profileVersion:"0.2.0"`を持つ**独立した制作環境JSON**であり、構造の正本は`schema/ostf-production-session-0.2.schema.json`である。従来の0.1は別バージョンとして保持し、そのScore固定・Mixer・プラグインチェーン・Bus/Send・Automation・非実行拡張の意味規則を継承する。0.1の値を推測して変換してはならない。変更されるのは制作Profileのみで、音楽Core 4.3、元の4.2、遠隔演奏用Distributed Session Profile 0.2は変更しない。

新規に、①Coreに存在しない録音・ミックス専用の`audioTrack`、②音声ファイルを参照する`audioRegions[]`、③別チャンネルからエフェクトのサイドチェーン入力へ送る`sidechainConnections[]`を追加する。これらの要素はすべて任意である。対象範囲はモノ/ステレオ、直列プラグインチェーン、固定素材と簡易伸縮、循環しない信号依存関係に限定する。音声録音機器、プラグインのDSPアルゴリズム、マルチポイントWarp、複数TakeのComp、並列Rack、サラウンド、PDCなどはまだ標準化しない。非対応項目はLoss報告を要する。

## 13. 録音専用トラックとScoreの関係

`channels[].kind:"audioTrack"`はProfile専用チャンネルであり、Core `tracks[]`の要素ではないため`trackId`を**持たない**。既存の`kind:"track"`のみ、対応するCore Track IDを`trackId`に必須とする。`bus`/`master`にも`trackId`を付けない。Audio Regionは`track`または`audioTrack`のみに配置し、Bus/Masterを音声Clipの所属先とみなさない。

同一`track`チャンネル上にMIDI InstrumentとAudio Regionが存在してもよい。MIDI音源の出力とRegionの音声は同じ音声チャンネルのエフェクト処理入口で合成する。これはScore NoteやClipの追加、再生成ではない。複数Regionの重なりは加算されるが、暗黙の音量正規化やCrossfadeを行わない。Core `track.enabled`とProduction Channel `mute/solo`、Region `mute`はそれぞれ別の正本である。

## 14. Audio Assetとフレーム

`assets[].purpose:"audioSource"`には、元のエンコード済みファイルのSHA-256、`uri`、`mediaType`、`sampleRateHz`、`frameCount`、`audioChannels`を必須とする。`frameCount`はファイルをデコードした音声の**時間フレーム数**であり、ステレオでも左右のサンプル数の合計ではない。`sampleRateHz`はそのフレームの秒あたりの数。0.2のポータブル範囲は1/2チャンネルに限定し、暗黙のアップミックスやダウンミックスを行わない。実際に取得したAssetバイトのSHAが違う、デコーダで読み取れない、申告したフレーム数などと違う場合には、正確な復元を主張せずエラーまたは明示的な損失を報告する。

URIは自動ダウンロード命令・ファイル操作権限・著作権許諾ではない。安全な相対パスおよび明示的な許可を得たHTTPSのみを使う。Plugin Stateのデータと音源のAssetは目的が異なる。

## 15. Audio Regionの時間・伸縮

各`audioRegions[]`は一意の`id`、`channelId`、`sourceAssetId`、元OSTF ScoreのグローバルTickによる`startTick`と正の`durationTicks`、非負の`sourceStartFrame`と正の`sourceFrameCount`、`playbackMode`、`gainDb`、`mute`を持つ。対象は半開区間`[startTick,startTick+durationTicks)`。`sourceStartFrame+sourceFrameCount`はAssetの全`frameCount`以下とする。

`playbackMode:"native"`では、開始Tickと開始Frameを対応付け、OSTFの`ppq`および有効なTempo変更を積算して求めた**経過秒数**に基づき、宣言された`sampleRateHz`で元音声を進める。指定Frameの終端またはRegionの終端で停止し、余ったRegion時間は無音になる。暗黙のループやタイムストレッチはしない。`pitchPolicy`は指定してはならない。Tempoが未定義なら推測してサンプル正確な復元を主張してはならない。

`playbackMode:"fit"`では、元OSTFのTick上の位置を指定されたSource Frame区間に等比対応させる。概念式は`sourceStartFrame + sourceFrameCount × ((currentTick-startTick)/durationTicks)`。`pitchPolicy`を必須とし、`preserve`は元の音高維持の意図、`followRate`は再生速度に従う音高変化を意味する。実際の伸縮・リサンプリングアルゴリズムや小数Frameの丸めはホスト依存であり、同一波形を保証しない。サンプル復元不能ならProfileの値を保持して警告する。

Region `gainDb`は音声リージョンの段階で適用する音量、`mute`はRegion固有の発音停止であり、Channel MuteやCore Track enabledと置き換えない。

## 16. Fadeと繰り返し・切断

`fadeInTicks`と`fadeOutTicks`は省略時0であり、和が`durationTicks`を超えてはならない。Fadeは**振幅で線形**。Fade-inの開始は振幅ゼロ、指定長で通常Gainに到達する。Fade-outはRegion末尾の指定長で開始し、終端でゼロへ向かう。複数Regionの交差部分に自動Crossfadeを生成しない。

Performance Planが元のSource範囲の一部を選ぶ場合、Regionとの交差部分だけがVisitへ投影される。切断時にRegionのID、元Source Frameとの時間対応、Fadeの相対位置をリセットせず、元座標で解釈する。同じ範囲を参照する複数Visitには同じRegionが出現しうるが、元のCore NoteやProduction Regionを勝手に書き換えない。Coreの`realization:"open"`は録音許可でもセッション確定フレーズの採用許可でもない。ProductionをScoreだけに書き出す場合は音声素材の損失を報告する。

## 17. Sidechain入力

`sidechainConnections[]`は可聴のBus/Sendと異なる**検出用入力**である。必須項目は`id`、`sourceChannelId`、`targetDeviceId`、`targetPortId`、`tapPoint`、`followMute`、`gainDb`、`enabled`。送信元はMaster以外、宛先は別Channelに所属する`effect` Device。1個のPlugin Portには1つのSourceだけを指定できる。複数入力をまとめたい場合はBusで明示的にミックスする。

`tapPoint:"preFader"`は直列Device処理後・Channel Gain/Pan前、`postFader`はGain/Pan後から検出用信号を採る。`followMute:true`では元ChannelのMuteによってSidechain信号も抑止し、falseでは可聴出力がMuteでもSidechain入力を残せる。`gainDb`はSidechainにのみ適用する。Plugin Port IDは不透明な識別子であり、実在のポートであることはHostが別途解決する。同名の入力へ自動変換しない。

Output、Send、SidechainによるChannel依存グラフ全体は**循環禁止**とする。自己Sidechain、暗黙のFeedback、PDC・Lookahead、DSPの動作や音質は標準化しない。Deviceが不在でも接続の意味情報は保持する。

## 18. バージョン移行・情報損失・適合性

正しい0.1文書を0.2へ移行する場合は、0.2 Schemaと意味規則のチェック後に`profileVersion`のみを書き換えてよい。新しいAudio RegionやSidechainを推測して生成しない。0.2から0.1への無損失変換は`audioTrack`、`audioRegions`、`sidechainConnections`、`audioSource` Assetなど0.2専用内容が一切ない場合に限り可能とする。0.2専用情報がある場合は、損失項目を明示して許容を得るか保存を拒否する。

本Profileは音声を演奏・生成するソフトではない。Schemaの正当性と実機・プラグイン・サンプル波形の同一性は別の条件である。ローカルの`validate_production_profile.py`は0.1/0.2の選択的な静的確認を補助するだけで、DAWやプラグインの独立相互運用テストではない。正式な出版には著作者による規範採択、英日文書整合、権利とライセンスの承認が必要で、いずれも現時点では未完了である。

## 19. 対象・対象外とサンプル

0.2では録音専用トラック、モノ/ステレオAudio Region、トリミング、簡易Fade、`native/fit`の伸縮意図、Sidechain入力を表現する。DAWprojectレベルのあらゆるオーディオ編集機能、複数TakeのComp、マルチポイントWarp、サラウンド、並列Rack、正確なプラグインState復元、物理録音I/Oやネットワーク演奏は対象外である。補足の違いは本文英語版第19節の役割表に従う。

`examples/production/03-audio-regions-sidechain-02.json`は元のScoreをSHA固定し、録音専用Channel、WAVテスト音源を2つのモードで参照するRegion、架空のBass CompressorへのSidechainを示す。`assets/example-audio.wav`はこのDraftのために生成した220Hzの合成音であり、商用ソフトの録音やプリセットではない。旧0.1例は変更せずに保持する。


## 21. Production Profile 0.2のAutomation対象拡張（Draft 0.15）

この追補は未公開の**Production Profile 0.2.0案だけ**を変更する。OSTF 4.3音楽Core、継承4.2、遠隔Distributed Session Profile 0.2、歴史的なProduction Profile 0.1のSchemaは変更しない。0.2はまだ正式公開されていないため、今回の追加を確定公開済みの0.2へ黙って導入したものとして扱わない。

旧来の`channel`（Mixer Gain/Pan/Mute）と`device`（プラグイン固有の0〜1正規化数値Parameter）に加え、`automation[].target`に以下の候補を追加する。

| Target kind | 参照ID | 操作対象 | 値型 |
|---|---|---|---|
| `send` | `sendId` | `gainDb`, `enabled` | 数値dB、真偽値 |
| `audioRegion` | `audioRegionId` | `gainDb`, `mute` | 数値dB、真偽値 |
| `deviceControl` | `deviceId` | `enabled`, `bypass` | 真偽値 |

Send IDはProfile全体の全Channelを通じて一意でなければならず、各参照は対象の実在を要求する。`deviceControl`の有効/Bypassはプラグイン内部のパラメータとは区別し、`kind:"device"`の`parameterId`として自動変換してはならない。単一の型付きTargetには1つのAutomation Laneだけを持てる。Laneを作成してもSend、Region、Deviceの実体を生成しない。

Automationの位置は従来どおり**元のOSTF楽曲の絶対Tick**である。Tickは非負かつ厳密昇順、同一Tickの重複は禁止。真偽値のLaneは`boolean`＋`step`が必須。数値のLaneは`number`であり、Panは-1〜+1、音量系dBは-120〜+24、プラグイン固有値は0〜1。新しいSend/Regionの音量にプラグイン固有の0〜1スケールを適用してはならない。

最初の点より前は対象オブジェクトの明示された静的値を適用し、その後は最後の有効点を保持する。数値`linear`は隣接点の区間内のみ補間する。プラグイン内部の最初の静的値が不明な場合、その区間の値は未規定であり勝手に補完しない。RegionへのAutomationが存在しても、もとのRegionの半開区間外では発音せず、Regionを延長しない。繰返しVisitで再び区間を利用するときは**元のScore Tickから状態を再解決**し、前のVisitの状態を持ち越さない。RegionのMute/GainはFade、Trimなどとは別の操作であり、元データを書き換えない。

`send.enabled:false`はSendの発音を止め、`audioRegion.mute:true`はそのRegionを消音する。Deviceの`enabled:false`は処理Slotを無効、Slot有効中の`bypass:true`は処理をバイパスする意図である。ただし実際のDSPと音源状態の等価性は保証しない。AutomationはCoreのTrack.enabled、MIDI CC、Soloの操作、プラグイン実行権限ではない。非対応Hostは全Laneの保存と不足機能の開示を行い、未対応の値を破棄して「損失なし」と呼んではならない。`send`/`audioRegion`/`deviceControl` Laneがある0.2から0.1へのダウングレードは情報損失を伴う。

`examples/production/03-audio-regions-sidechain-02.json`に6種類の新ターゲット操作を追加した。これらは構造・意味の例示であり、実際にプラグインを制御できたことの証拠ではない。英語版21節を詳細な規範候補とし、公開前に日英の最終編集承認が必要である。


## 22. ポータブルなMixer/Solo/Solo Safe・音源権威の境界（Draft 0.16候補）

この節は、未公開の**Production Profile 0.2.0候補**に対し、第三者製HostがSolo/Muteをどう解釈するかの**演奏源選択の共通基準**を提案する。旧Profile 0.1のSchemaと既存データは変更しない。これはDSP、Pan Law、遅延補正、音質まで統一する規則ではなく、いずれの素材が音声経路に参加し得るかを明示する規則である。

### 22.1 音源の種類と正本

- `channel.kind:"track"`と`"audioTrack"`を**source channel**とする。`"bus"`は受信/分配する経路、`"master"`は最終出力であり、いずれもそれ自体では新しい楽曲音源を生成しない。
- Scoreに紐付く`"track"`において、Coreの`track.enabled`、`clip.enabled`、Note/MIDIは**Core由来の演奏**だけの参加可否を決める。同じProduction Channelに置いた独立の`audioRegion`まで自動消音してはならない。Region自身の位置・MuteとStudio Mixerは別々に適用する。
- `"audioTrack"`はCoreの`trackId`を持たない。Channelの存在だけで発音は生まれない。
- Channel Mute、Send enabled、Region Mute、Device enabled/bypass、Automationは異なる制御層である。`solo`/`soloSafe`はミキサーの試聴状態であって、楽曲Noteの変更やプラグイン起動権限ではない。MasterのSolo/SoloSafeは音源選択に関与しない。新規作成時はMasterの両方をfalseとすることを推奨するが、旧ファイルにある値を勝手に書き換えてはならない。

### 22.2 Solo中に選択する演奏源（Profile 0.2の提案規則）

1. `outputChannelId`と、**その元Score Tickで有効な**Send（`send.enabled`のAutomation適用後）の矢印で、出力グラフを作る。Sidechainはこのグラフに含めない。Muteによって接続情報を削除しない。
2. Master以外で`solo:true`のChannel集合を`S`とする。`S`が空ならすべての`track`/`audioTrack`源が選択される。
3. `S`が空でなければ、演奏源Channelは①自分がSolo、②自分がSoloSafe、③有効な出力/Send経路をたどってSolo中のBusへ到達できる、のいずれかで選択される。**SoloSafeのBusだけでは、それまで非選択だった他の演奏源を復活させない。**
4. 選択された演奏源の直接出力と有効なSendは、Mute/音源状態/後段の経路に従って利用可能となる。そのためBusをSoloしたとき、上流源のDry出力も選択対象になり得る。Wetのみを試聴するHostは、その差を開示して元のSolo情報を保持する。SoloSafeのBusは選択源の信号を通してよいが、非選択源を新規に選ぶ機能ではない。
5. Send EnabledのAutomationやVisit再入で到達関係が変わった場合、元Score Tickから選択状態を再計算し、前のVisitの選択を持ち越さない。0.2ではSoloとSoloSafeそのものは**静的な値でありAutomation対象外**である。

この共通規則に従わないDAWのBus Solo/試聴動作をそのまま実行することは許されるが、元データを保全し、結果の非互換性を表示して、等価再生を保証してはならない。

### 22.3 Mute・Send・Sidechain・処理順

- Score由来の演奏とProductionのAudio Regionは独立して参加判定し、そのChannel内で合成した後、順序付きDevice Chainへ送る。Coreの`track.enabled:false`は独立したProduction Audio RegionのMuteではない。
- ポータブルな信号順序を、**演奏入力→Device Chain→Pre-fader Tap→Gain/Pan→Post-fader Tap→出力/Send→Master**とする。`send.preFader:true`はPre-fader、falseはPost-faderから取る。Pan LawやDSPのビット単位の一致は規定しない。
- Channel MuteはSolo中でも優先し、Pre/Postに関係なく**可聴出力とSendの両方**を抑制する。Mute中のBusも同様。無効なSendは接続を抑制する。Deviceの`enabled`/`bypass`はChannel Muteとは別の状態。
- Sidechainは検出用経路でありSoloの選択対象にはならない。`followMute:true`ならソースChannelのMuteで検出信号を抑制し、falseならMute中も元信号を検出へ送ることができる。ただしfalseは、Soloで非選択の音源やCore側で無効のNote入力まで復活させない。Sidechainの`enabled:false`は常に検出入力を抑制する。Host独自のSoloとKey Listening規則の差は開示する。
- Masterは選択・有効な音声を受け取り、自身のGain/Pan/Muteを適用する最終経路である。MasterをSoloしても無効な音源は発音しない。

### 22.4 アセットパスの安全な解決

Production Profileの`asset.uri`が相対パスなら、Profile文書を含むディレクトリの**内部だけ**で解決する。`..`などの字面チェックだけでなく、シンボリックリンク経由で外部ファイルへ脱出する場合も拒否する。SHA-256の一致はファイル閲覧権限を与えない。HTTPS URLは情報として保持し、無断取得しない。付属Pythonチェッカーはこの基本的な境界判定を追加したが、完全なセキュリティ監査を実施したという意味ではない。

### 22.5 選択の例

| 状態 | 選択される源Channel | 備考 |
|---|---|---|
| Soloが存在しない | 全track/audioTrack源 | 実際の発音はMuteやCore/Region状態に従う |
| サンプル03のSax Solo・Reverb Bus SoloSafe | `sax-channel` | Reverb BusのSoloSafeだけでPianoのSendは復活しない |
| Reverb Bus Solo・有効Piano Send | `piano-channel` | Dryも選択され得る（Wet限定Hostとの違いに注意） |
| Reverb Bus Solo・Piano Send無効 | 当該Bus経由の選択源なし | Send Automationで選択が変化 |
| Sax Solo・Piano Channel SoloSafe | `sax-channel`, `piano-channel` | どちらもMuteで抑制可能 |

チェッカーの`--explain-audition --at-tick N`は、元Tick時点の静的な演奏源選択を表示する説明機能である。音声レンダリング・DAW互換検証・ロボット実機検証ではない。この追補で新しいJSONフィールドは追加せず、既存の6 SchemaはDraft 0.15から変更しない。**公開前に著作者の意味規則採用が必要である。**

## 23. Asset URIの厳密な解釈とScore/Productionの権威分離（Draft 0.17候補）

### 23.1 相対Asset URIの移植性と安全性

`assets[].uri`が相対URIである場合、OSの生パスではなく**URIパス**として解釈する。0.1と0.2共通の規範候補として、文字通りの`/`で空でない成分に分け、パーセントエスケープを成分ごとに**1回だけ**厳密なUTF-8として復号する。`.`/`..`、`%2F`/`%5C`のような隠れた区切り、`%252e`のように2度目の復号で意味が変わる残存`%`、不正なUTF-8、制御文字、前後の空白・末尾のピリオド、Windowsで予約された文字・`CON`や`NUL`等のデバイス名を禁止する。生の空白は使わず`%20`で符号化する（例：`assets/My%20Take.wav`はファイル`My Take.wav`）。

復号後はProduction Profile JSONのディレクトリ以下に解決し、シンボリックリンクを含めて実際の解決先がディレクトリ外なら拒否する。URI文字列自体はJSONのデータとして保持する。アクセス権限の確認なしにファイルを読まず、外部HTTPSも自動取得しない。SHA-256は許可された取得後に元バイト列へ適用する。Unicode正規化や2度目のURI復号を行ってはならない。復元不能なら原文を保持して理由を報告する。この規則は安全監査が完了したという意味ではない。

具体例：`assets/%2e%2e/private.bin`、`assets/%252e%252e/private.bin`、`assets/%2Fetc.bin`、`assets/note%FF.wav`、`assets/CON.txt`は拒否対象。URI文字列以外のSchema項目は追加しない。

### 23.2 Performance Plan `realization` とAudio Regionの関係

Core `performancePlans[].visits[].parts[].realization`（`fixed`/`open`/`silent`）は**Core由来の演奏**を規定し、同じScore Trackに紐付いたProduction Channel上の独立`audioRegions[]`を自動変更・消音しない。例えばギターのPlan Partを`silent`にしても、該当するSource Tickに置かれた録音Regionは、独自のRegion/Channel MuteやAutomationなどが許す限り再生候補のままである。Production専用の`audioTrack`も、同名というだけでCore Plan Partにはならない。

MIDIと録音素材を含む全体を消音したい場合は、Production Profile側でRegion/ChannelのMuteなどを**明示的に**指定する。逆にMixer MuteはCore Noteや`open`/`silent`という演奏意図を書き換えない。異なる動作をするホストは差分を開示し、元データを保持する。Visitの再出現でもこの権威分離を守る。

**現在は著作者の正式採択・日英最終編集前の規範候補である。** 本記述は実行・音声DSP・OS権限・ネットワーク・ロボット実機の検証結果ではない。

## 24. Performance Plan再入時のAudio RegionとAutomationの位置・状態規則（Draft 0.18候補）

### 24.1 Source TickとPerformance Tickを混同しない

未公開の**Production Session Profile 0.2.0案**に適用する規範候補であり、第7・15・16・21〜23節を補足する。**source Tick `t`**は元のOSTF楽曲の絶対Tick、**performance Tick `P`**は有限Performance PlanのVisitを展開した位置、実機/サンプルの時計はホストの責任である。元の半開区間`[S,E)`を演奏位置`Q`へ配置すると、選択中は`P=Q+(t-S)`となる。Visitを繰り返しても、元のRegion ID、Automationポイント、Scoreハッシュ、確定MIDIイベントは変更しない。

### 24.2 Regionの一部分だけを選択したとき

Regionの元範囲`[R,R+L)`とVisitの選択区間`[S,E)`の**半開区間の共通部分**`[max(S,R), min(E,R+L))`だけが対象である。VisitがRegionの途中から始まっても、元の`sourceStartFrame`へ巻き戻してはならず、元のsource Tickから対応するフレーム位置を計算する。後のVisitで同じ元区間を再度選択した場合は、その区間に対応する元の素材位置を再び利用し、前Visitの再生カーソルを継承しない。

- `playbackMode:"native"`では、source Tick `t`の理想連続フレーム位置は`sourceStartFrame + sampleRateHz × T(R,t)`とする。`T(R,t)`はRegion開始`R`から`t`まで**元の楽曲のテンポマップ**を積分した理想秒数で、テンポ一定の小区間ごとに`60 × deltaTicks/(ppq × bpm)`を足す。途中のsource区間がPerformance Planで省略されていても、素材内の開始フレームを求める際には**元のRegion開始からの経過**を用いる。この積分は、**展開後の演奏時間に省略区間を足すことではない**。選択された`sourceFrameCount`を超えたら無音とし、素材を自動ループ・先頭再生しない。
- `playbackMode:"fit"`では`sourceStartFrame + sourceFrameCount × (t-R)/L`を利用する。Visitの途中開始・区間切断でも元のRegion-local Tickによる位置を維持する。小数フレームの丸め、タイムストレッチ、ピッチ保持のDSPはホスト依存であり、音声データの同一性を保証しない。
- `fadeInTicks`/`fadeOutTicks`は元のRegion境界を基準に評価する。Visitの切断位置で新しいFadeを暗黙に作らない。カットによって不連続・クリックが生じ得るが、ホスト独自のCrossfade/平滑化を用いた場合は等価再生とは主張せず、その近似を開示する。
- **MIDI Noteの元区間外の発音開始を作り直さない規則とは区別する**。Regionは途中位置の音声フレームを参照できるが、確定Noteは元区間にNote Onがなければ新しいNote Onを生成しない。過去のMIDI CCやProgram Changeの状態をこのProduction規則で復元するわけでもない。

### 24.3 Visit開始時のAutomationは元のsource Tickから解決する

Automation Laneの有効値は、現在の**元のsource Tick `t`**から全ポイントを用いて計算する。現在のVisitが省略した元区間にあるポイントも、状態評価に必要なら参照する（省略区間を演奏イベントとして再出力するわけではない）。ポイントと同じTickでは当該ポイント値が有効。`step`は直近ポイントを保持し、`linear`は隣接する数値ポイントのsource Tick比で補間し、最後のポイント以後は値を保持する。最初のポイント前はChannel/Send/Region/DeviceControlに明示された静的値を使う。一方、`kind:"device"`のプラグイン数値Parameterは**型付きの静的初期値がProfileにない**ため、最初のポイント前はプラグインStateを解釈できない限り**未解決**である。0、0.5、最初のポイント値、前Visitの最終値を勝手に採用しない。

元のsource Tickが切断やVisit再入で巻き戻った場合、Sendの`enabled`、Channel/RegionのMute、Deviceのenabled/bypass、Gainなど、すべて**新しいsource Tickで再評価**する。**前VisitのAutomation状態は持ち越さない**。RegionのAutomationは元のRegion範囲外に新しい音声を作らない。これは元のsource Tickに対する状態関数の評価であり、選択した区間の前にあるCore MIDI CC/Programイベントを新たに送る処理ではない。Profile 0.2にはVisitごとのMixer Automation上書きはない。同じ元Tickなら、異なるVisitでも同じAutomation値となる。

### 24.4 計算例（音声再生検証ではない）

PPQ=960、BPM=120、sampleRateHz=48000、Region開始Tick=0、開始フレーム0なら、source Tick 960は`48000 × (60/120)=24000`フレーム相当である。`[960,1920)`から始まるVisitでもフレーム0から再生しない。`fit`のRegionが`R=1920`、`L=1920`、`sourceStartFrame=0`、`sourceFrameCount=11025`なら、元Tick 2880で理想フレーム位置は5512.5である。実際の小数フレームの取り扱いはホスト依存。

付属`03-audio-regions-sidechain-02.json`では、`reverb-send-on-automation`にsource Tick 7680で`enabled:false`がある。VisitがそのTick以降の元区間に途中から入った場合でも、**当該ポイントを経過して演奏していなくても**Sendは無効と解釈する。次のVisitで元Tick 0へ戻れば`enabled:true`を再評価する。また`room-clip-native`は44100Hzで11025フレーム＝0.25秒しか素材がない。BPM=120・PPQ=960では元Tick 480で素材が尽きるため、Region自体が960 Tickでも`[480,960)`からの選択で先頭へ戻らない。

### 24.5 未解決情報・互換性・公開状態

Nativeの素材位置決定に必要な元テンポが不明、またはプラグインStateから最初のAutomationポイントより前の数値が復元できない場合は、元のデータを保持して未解決を報告し、確定した音声再現を主張してはならない。診断コード案：`E-PRODUCTION-NATIVE-TEMPO-UNRESOLVED`、`W-PRODUCTION-DEVICE-BASELINE-UNKNOWN`、`W-PRODUCTION-CUT-DISCONTINUITY`、`W-PRODUCTION-VISIT-LOCAL-MIX-UNREPRESENTABLE`。ホスト独自のVisit別Automation、Fade、演奏状態持ち越しによる差異も情報損失・近似として開示する。

**Draft 0.18ではSchemaの追加・変更、Profile版番号の変更は行わない。** これらは公開前の規範候補であり、著作者による正式採用、日英最終編集、ライセンス承認が必要。独立パーサー・DAW/DSP・WAN・ロボット実機の検証は行ったとは主張しない。

## 25. Production ProfileとDistributed Session Profileを同じOSTFへ関連付ける規則（Draft 0.19候補）

### 25.1 三つの文書を明示的に関連付ける

本節は、独立した**OSTF Production Session Profile 0.1/0.2**と**Distributed Session Profile 0.2**のSnapshot/Eventが、同じ**OSTF 4.3楽曲の実体バイト列**を参照するときだけ適用する、未公開の意味規則案である。新しいJSONフィールド・Schema・Profileバージョンは追加しない。Studio専用ソフトがDistributed Profileを必要とすることも、遠隔SessionがProduction Profileを必要とすることもない。

Productionの`score.sha256`とDistributedルートの`scoreSha256`は、**同じOSTF原本のUTF-8実体バイト列**に対するSHA-256である。三文書を同一Scoreとして関連付ける場合、両方の宣言値と原本から計算した値が**すべて一致しなければならない**。IDやRevision名だけが同じでも一致の代用にはならない。JSONの整形・再直列化、Web APIからの自動取得、原本の暗黙書換えによってハッシュを無理に一致させない。ハッシュは署名・許諾・本人確認・セッション参加権限を意味しない。Production `score.sourceUri`は参考URIであり、読み込んだだけで取得権限を与えない。Production Profileだけを編集しても、元OSTFのSHA-256は変わらない。

Productionの`score.documentId`/`score.revisionId`があるときは、Distributedの必須`documentId`/`revisionId`およびOSTF原本の`document.id`/`document.revisionId`と一致する必要がある。Productionで未指定なら推測しない。Distributedの必須`performancePlanId`は、原本Scoreの`performancePlans[]`に存在するIDを明示的に指す。原本を確認できない場合、2つのProfileが宣言するハッシュの文字列一致は**主張の整合**であり、楽曲実体・Plan・Track参照を検証できたとは表示できない。

### 25.2 Trackの一致から音声出力やロボット制御を推測しない

Productionの`channels[kind:"track"].trackId`とDistributedの`participants[].assignedTrackIds`/`targetTrackId`はいずれもCoreの`tracks[].id`を参照する。しかし同じIDでも、Remote Participantを特定のStudio Channel・Plugin・物理出力・ロボット関節へ割り当てたことには**ならない**。Production ChannelがないCore TrackはMuteや参加不可を意味しない。Production専用`kind:"audioTrack"`はCore Trackではなく、名前の類似から遠隔参加者や`open` Partへ暗黙割当しない。

分散PlanのVisit/PositionはScore由来演奏の範囲を指定する。独立したProduction Audio Region/Automationは第23～24節の元`source Tick`規則で解釈し、前VisitのMute等を持ち越さない。Core `realization:"silent"`は独立したStudio録音を自動Muteしない。遠隔`phraseCommitted`は明示された`open` Partの**セッション確定フレーズ**であり、元ScoreのNote、Production Automation/Audio Region/Device状態、プラグインの実行やロボット動作を自動変更しない。元Scoreを編集したら、新Revision/新ハッシュに基づきProfileとの関連付けを明示的にやり直す必要がある。

### 25.3 拒否条件と表示

任意の`OSTF 4.3 Cross-Profile Binding Reader`を名乗るアダプターは、Scoreハッシュの不一致、明示ID/Revisionの不一致、原本があるのに未解決のPlan/Track参照がある場合、**自動関連付けを拒否**し、両Profileの内容を変更せず保存する。独立した未関連の文書として表示することはできる。原本がなく検証できない場合、`W-CROSS-PROFILE-SCORE-UNAVAILABLE`などで未確認を明示する。関連付け成功を、音声の一致、遠隔同期、MIDI状態復元、プラグイン実行、安全なロボット制御の証拠としてはならない。

候補の診断コード：`E-CROSS-PROFILE-SCORE-HASH`、`E-CROSS-PROFILE-DOCUMENT`、`E-CROSS-PROFILE-REVISION`、`E-CROSS-PROFILE-PLAN`、`E-CROSS-PROFILE-TRACK`、`W-CROSS-PROFILE-SCORE-UNAVAILABLE`、`W-CROSS-PROFILE-ROUTING-UNDEFINED`。これはSchemaの新しいenumではない。

### 25.4 既存の3つのサンプルを用いた例

`examples/22-pinned-session-aaba.ostf`を原本とし、`examples/production/03-audio-regions-sidechain-02.json`と`examples/session/03-snapshot-02.json`を関連付けられる。いずれも原本のハッシュと文書ID/Revisionが一致し、Distributedの`performancePlanId:"form"`は元のPlanを参照する。一方、Productionの`bass-channel`と遠隔Participantの`bass`担当が同じScore Trackを参照していても、Remoteロボットの音声をそのStudio Channelに流すことは指示されていない。

**公開状態：Draft 0.19の意味規則候補。** Schema・例のJSONは変更しない。独立実装によるDAW/プラグイン/DSP/遠隔ロボット動作や公開承認の証拠ではなく、従来の著作者決定事項は未解決のままである。

## 26. Score改訂後の明示的な再関連付け（Draft 0.20・未採用の規範案）

### 26.1 制作環境の引継ぎと遠隔Sessionの引継ぎを混同しない

OSTF楽曲のJSONバイト列が変更された場合、意味が似ていても**以前とは別の固定されたScore実体**である。制作環境を記録するProduction Profile 0.1/0.2は、新しいScore改訂版に**明示的な再関連付け**を行える。一方、演奏中・停止後のDistributed Session Profile 0.2のセッションを**その場で別Scoreへ付け替えてはならない**。この候補規則は新規フィールド・Schema・通信方式を追加せず、既存の正本と権限境界を明確にするものである。Production `score.sha256`の文字列だけを書き換え、安全または無損失の引継ぎが完了したと宣言してはならない。

Note、Harmony、Tempo、Section、Track、Performance Planなどを編集した場合、新しいScoreの実体が必要になる。同じ作品の改訂と主張するなら、`document.id`を維持し、新しい`document.revisionId`を明示する。`document.id`が異なる場合は同一曲のRevisionではなく別作品への再割当である。Coreの文書メタデータは任意だが、IDまたはRevisionがないときに曲名・ハッシュだけから改訂系譜を証明してはならない。同じ `(document.id, document.revisionId)` や固定URLのまま別バイト列を公開してはならない。空白などのJSON整形だけの変更でも、原本バイトハッシュが変わるため再固定が必要である。

### 26.2 Production Profileを引き継ぐための必須確認

専用ソフトは、従来のScoreとProduction Profileを保存したまま、**新しいProduction Profileのコピー**を作成してよい。ただし以下をすべて明示的に扱うこと。旧データの削除は別途の著者指示が必要である。

1. 旧Production `score.sha256`が旧Scoreの**実体バイト列**と一致し、新Scoreのバイト列から新しいハッシュを計算できること。Productionに旧文書ID/Revisionが明示されていれば旧Scoreと一致させる。新コピーには新Scoreのハッシュを設定し、明示する場合は新文書ID/Revisionも更新する。旧IDを無条件でコピーしない。
2. 新ScoreのTrack IDをすべて解決すること。**同じTrack IDは同じ参照先の識別を意味するが、演奏内容や発音時刻まで同一とは限らない。** Trackの削除や付け替えには、著者承認の明示的な再割当、別Profileとしての保持、または情報損失を開示した変換が必要である。Channel名の一致だけから新Trackを生成したり、不正なTrack参照を含む新Profileを黙って保存してはならない。
3. **元Scoreのsource Tick**を使う`audioRegions[]`や`automation[].points[]`について、PPQ、Sections、Tempo/Meter、選択したPerformance Plansの差分を確認する。Tempoを変えれば`native`素材の元フレーム時刻に影響し、PPQや構成を変えればRegionの開始/長さ、Fade、Automationの音楽的な位置が変わりうる。Plan変更は同じsource TickでもVisitへの投影を変える。ハッシュ更新・Track名・小節ラベルだけを根拠に自動移動、伸縮、カット、直前Visitの値持越しを行ってはならない。
4. 不透明なプラグイン状態、音声Asset、独立Audio Region、Bus/Send、Device ID、`hostExtensions`は**Production側の正本**である。Scoreの更新を理由に自動上書き・実行してはならない。意図通りに再対応できない場合、著者による配置確認を求め、非破壊であれば旧Profileを保持する。損失変換なら、失う具体的なChannel/Region/Automation/Device IDと意味を報告する。

結果の状態を区別すること：**旧Scoreに固定されたまま**、**新Scoreへの再関連付け候補（要レビュー）**、**著者承認済みの新Score/新Productionコピー**。単に新ハッシュと同じTrack IDがあるだけで最後の状態を主張してはならない。プラグインの音質まで一致することは保証しない。

### 26.3 Distributed Sessionは新Scoreごとに新セッション

Distributed Profile 0.2は`documentId/revisionId/performancePlanId/scoreSha256`と受理済みイベント履歴に固定されている。Score Revisionが変わったら、**新しい`sessionId`**で遠隔セッションを開始すること。既存の`stateRevision`、`eventId`、確定`phraseCommitted`、Visit位置、共通時計位置、参加者割当を、新Scoreへ暗黙で移してはならない。旧イベント履歴は元Scoreと結び付いた記録として残る。フレーズを新セッションで再利用したい場合は、新しい識別子・明示的な著者の移行操作・必要な損失報告を伴う新規データにする。既存JSONを読み込んだことはロボット動作の認可ではない。

Web APIの`latest` URLやHTTP `ETag`が変わっても演奏中の元Scoreを切り替えない。参加者の名前、同じTrack ID、新しく表示された曲名は移行の承認とはみなさない。ハッシュは発信者認証やプラグインロード権限ではない。

### 26.4 読取専用の再関連付けプレビュー

付属`tools/validate_production_profile.py`にDraft 0.20の`--score OLD.ostf --rebind-target NEW.ostf`を追加する。旧・新原本のハッシュ/ID/Revision、Track参照、source時刻・Performance Planの変更可能性を**表示するだけ**である。結果は原則`REVIEW_REQUIRED`であり、プレビューが通っても自動変換・無損失証明・動作検証にはならない。目標Scoreが不正なら`BLOCKED`とし、既存ファイルを書き換えない。

診断名案：`E-REBIND-SCORE-INVALID`、`E-REBIND-IDENTITY`、`E-REBIND-REVISION-REUSE`、`E-REBIND-TRACK-UNRESOLVED`、`W-REBIND-SOURCE-TIME-CHANGED`、`W-REBIND-PLAN-CHANGED`、`W-REBIND-NEEDS-AUTHOR-REVIEW`、`W-DISTRIBUTED-NEW-SESSION-REQUIRED`。Schema enumを追加するものではない。

**状態：Draft 0.20の規範候補であり著作者未採用。** 4.3 Core、正式4.2継承Schema、別冊Distributed/ProductionのSchema、既存デモJSONは変更しない。著作者による意味規則の正式採用、日英仕様書とサンプルの最終承認、公開権利・ライセンス許諾が未完であり、検証を除外してもNO-GOを維持する。

## 27. データ保持・機能別対応の明示（Draft 0.21・未採用規範候補）

### 27.1 保存・解釈・実行を区別する

OSTF Score、Production Session Profile、Distributed Session Profileは**独立した文書と版番号**を持つ。JSONを失わず保持できること、音楽上の意味を解釈できること、プラグインを実際に動かして同じ音を出すこと、遠隔ロボットを制御できることは、すべて別の能力である。第三者製ソフトはこれらを混同して「完全対応」と称してはならない。Coreだけを読むViewerは別冊Profileを無視してもよいが、**受領した制作プロジェクト全体を無損失で再保存する**と明示するWriterは、別冊Profileと参照Assetを保持するか、欠落を個別に説明しなければならない。

### 27.2 参照Assetと再保存時の正本

無損失のデータ保存では、受領した文書の実体と、利用可能な不透明Assetバイト（プラグイン状態・録音音声等）を保持するか、明示的に新しい版・ID・参照を作成して整合させる。Score JSONを整形し直しただけでも、**元バイト列**に対するSHA-256は変化する。古いProduction/DistributedのScoreハッシュをそのまま新しいScoreへ結び付けてはならない。Asset ID・ファイル名・URIだけが残り、Asset本体が欠けている状態は**参照情報のみの保持**であり、完全な無損失移送ではない。未知の`hostExtensions`やプラグイン状態をそのまま保持する場合でも、音色の再現・プラグインの起動・ライセンス有効性を保証しない。

### 27.3 未対応機能・損失の報告

要求された情報を保持できない場合、無損失上書きを拒否するか、利用者が明示的に選んだ損失ありExportへ切り替える。報告には、影響するTrack・Channel・Device・Region・Asset・Automation・Voice・Plan・Event等の安定IDを可能な限り含め、**削除、近似、Asset本体の未取得、実行未対応、再現性未確認**を区別する。これは診断の区分案であり、**新しいJSONフィールドやSchemaのenum値ではない**。プラグイン状態のバイト列を保存してDSPをバイパスする場合は「データ保持・音響面の劣化」であり、状態バイトそのものを破棄すれば「データ損失」となる。Score単独のExportでは、別途保持していないMixer・録音Regionなどの情報が失われる。

### 27.4 Score改訂・遠隔Sessionの責任分離

Scoreが編集・再整形された場合、旧Scoreと既存Profileの関連付けは履歴として保持する。Productionは第26節に従い、`score.documentId`、`score.revisionId`、`score.sourceUri`、`score.sha256`の存在する項目と、元source Tickの録音/Automationを確認して、新しいProfileコピーとして明示的に再関連付けする。`sourceUri`は参照先のヒントであり、ハッシュの代替でも自動取得の命令でもない。Distributed Sessionは新しいScore Revisionを扱う場合、**新しい`sessionId`**と新しい演奏状態を必要とし、旧Event・Clock・確定フレーズを無断移植しない。ハッシュ一致は著作者認証でも機器制御の認可でもない。

### 27.5 機能別の対応表明

Core Reader/Writer、Production Profile 0.1/0.2 Reader/Writer、Opaque Asset保持、Cross-Profile Binding Reader、Plan-aware、Distributed Snapshot/Event Readerなどは**対象版と操作別**に対応を表明する。データを読み込めるだけで、DAWの音や遠隔AI・ロボットの実動作を保証したことにしてはならない。将来の未知のVersionを無断で旧Versionへ読み替えない。

**公開状態：** 本節は実行を伴わない未承認の規範候補。Schemaパラメーターは追加しない。著作者による正式採用、日英校了、ライセンス・権利の確認が必要であり、動作検証を行ったとは主張しない。

## 28. 規格の配布ZIPと制作環境データ一式の区別（Draft 0.22・未採用案）

### 28.1 標準化した制作プロジェクトのアーカイブ形式は存在しない

Production Session Profile 0.1.0/0.2.0が規定するのは**JSON、安定ID、参照・Asset URIの意味**である。独立した制作プロジェクトのZIP構造、ディレクトリ配置、共通マニフェスト形式、暗号化、署名、ネットワークAPI、プラグイン本体の梱包仕様を規定しない。`OSTF_4.3_Draft_*_Development_Package.zip`は規格文書の**配布パッケージ**であり、利用者の制作プロジェクトを交換する標準コンテナーではない。配布用の`PACKAGE_MANIFEST.json`や`SHA256SUMS.txt`を楽曲・制作Profileの規範フィールドとして扱ってはならない。

### 28.2 実際に受け取ったデータに基づいて無損失保存を表明する

ソフトウェアはScore、任意の独立Profile、参照された外部Assetの実バイト列を、独自のフォルダー/アーカイブ/許可されたサービスから受け取ってよい。受け取った**原本Score/Profile JSON**、受け取った**不透明Assetの実体**、記述子だけで**実体が未入手のAsset**を区別する。これは報告上の区別であり、新しいJSONプロパティではない。

「受領したデータ一式を無損失で保持」と表明するソフトウェアは、表明の対象である**実際に渡された**バージョン付きJSONとAsset実体を欠落・無断改変なく保存しなければならない。保持できない場合は無損失を主張せず、拒否するか対象IDを含む損失報告を提示する。実体のないAsset記述子だけでは制作環境の完全復元を主張できない。一方、**元々提供されていないProfile**を保存していないことを、ソフトウェアによるデータ削除とみなしてはいけない。主張の対象となる入力セットを明示する。

### 28.3 原本ハッシュと実行の責任分離

既存のScore SHA-256は**原本OSTFファイルの正確なバイト列**に対する値であり、外側のZIP、URL、JSON再整形後の内容のハッシュではない。Scoreを書き換えたら第26節の新Revision・再関連付け手順が必要である。プラグイン状態・音声Assetのチェックサムは、それぞれ元のAsset実体について解釈する。外部コンテナー独自の暗号化・署名・権限・圧縮機能はOSTFが保証する機能ではない。

### 28.4 適合の表記

「Core Reader」「Production 0.2 JSON Reader」「受領したAssetを含む無損失Writer」「明示したデータ一式の無損失保持」「DAW/プラグインの実音レンダリング」は互いに別の能力である。配布用ZIPの展開だけではいずれも証明されない。将来、制作プロジェクトをまとめるアーカイブ形式を標準化する場合は、独立したバージョンを持つ新提案と著作者承認が必要である。

**公開状態：** 未採用のDraft 0.22規範案。新たなSchema・JSON項目はなく、動作検証・権利承認も済んだものではない。

## 29. 3文書の関連付けと更新権限の現行解釈（Draft 0.23・未採用）

OSTFのScore、Production Session Profile、Distributed Session Profileはそれぞれ独立した版・正本を持つ。**3文書の関連付けは宣言内容の照合であって、状態変更ではない。** 過去Draftの規範候補を累積している本書について、現行案の解釈を次のように整理する。

| 入力・処理 | Score Coreへの影響 | Productionへの影響 | Distributedへの影響 |
| --- | --- | --- | --- |
| 認可されたAPIから版付きScoreを取得 | 元バイトの同一性・Schema・意味を確認 | `score.sha256`照合は別途行う | `scoreSha256`照合は別途行う |
| `phraseProposed`を受信 | Noteの追加なし | RegionやPluginを変更しない | 提案にすぎず、確定フレーズではない |
| 有効な`phraseCommitted`を受理 | **Scoreの`notes[]`を自動更新しない** | **録音Region・Automation・Pluginを自動更新しない** | 認可された`open` Visit Partの確定履歴を更新する |
| 確定演奏を新Scoreへ保存 | 著者操作で新バイト列・RevisionのScoreを作る | 元source TickとTrackを照合した**新Profileコピー**を作る場合のみ関連付けを更新 | Scoreが変われば**新Session ID**を必要とする |
| Profileと元Scoreのハッシュ不一致 | 旧Scoreを無断で書き換えない | 無断で新Scoreへ移行せず、未関連状態を表示 | 元の固定Sessionを保持 |
| 実体がないAsset記述子 | Core音声を推測生成しない | 参照メタデータのみ保持。音声・音色の復元とは区別 | ロボットへの実行権限を与えない |

元Scoreの実体バイトが未入手なら、2つのProfileに記載されたハッシュが等しいことは**宣言値の一致**にすぎず、実際の原本・Track・Planの検証にはならない。URL、HTTP ETag、ZIP名、Track表示名も同一性の代替ではない。Session権限はミキサー変更やプラグイン起動の権限ではなく、Production Writerの操作は分散Eventの確定権限ではない。従来§25〜28の詳細規則は維持する。**新しいJSON項目・通信APIは追加しない。**

## 30. Draft 0.24 — ProductionとDistributedの版識別（未採択案）

Production Profile 0.1.0/0.2.0は`profile:"OSTF-Production-Session"`および必須の`profileVersion:"0.1.0"`/`"0.2.0"`で版を選択します。Distributed Session Profile 0.2は代わりに`profile:"OSTF-Distributed-Session-0.2"`と`recordType`を持ち、**`profileVersion`を持ちません**。既存のSchemaとサンプルが正本であり、この追補で新しいJSON項目は追加しません。分散イベントの確定・再送はMixer Automationやプラグイン状態を変更しません。詳細は`CONFORMANCE.md`および`SESSION_STATE_MACHINE.md`を参照してください。著作者の正式採用と公開承認は未完了です。


## Draft 0.70 — 候補集合の探索完了と慎重な参照判定（未採択）

参照の4状態は、**実際に評価できた範囲での判定**であり、インターネット上の全候補を探索した保証ではない。実装は許可された候補の探索範囲、およびその列挙と実体バイト取得の完了・未完了を明示しなければならない。ファイル名、申告されたハッシュ、HTTPヘッダー、音楽的な一致だけでは検証済みとはしない。

1. 許可された候補集合の列挙またはバイト取得が不完全な場合は、外部診断 **NOT_EVALUATED** とする。これはOSTFの新しいJSON値ではない。
2. 候補集合の探索と取得が完了している場合、候補Scoreが0件ならその範囲において **MISSING**、Scoreが1件以上存在しても元バイト列のSHA-256一致がなければ **MISMATCH** とする。世界中に存在しないという意味ではない。
3. ハッシュ一致候補の同一バイト列は重複コピーとしてまとめ、Track／Plan／Visitなど必須参照が欠落または一意に解決できない場合は **AMBIGUOUS** とする。`missing_referent` と `nonunique_referent` はJSONに格納しない診断補足とする。
4. ハッシュと必須参照がすべて整合して初めて **RESOLVED** とする。
5. 許可された候補の列挙または実体バイト取得が一つでも未完了なら、一致候補をすでに観測していても **NOT_EVALUATED** と報告する。部分的・条件付きの **RESOLVED** は認めない。未完了の探索範囲を明示し、候補集合が未完了のままMISSING・MISMATCH・AMBIGUOUS・RESOLVEDを推定してはならない。古いProfileを改訂Scoreへ暗黙に付け替えてはならない。

INVALID／UNSUPPORTEDは形式・バージョンに関する事前エラーであり、4状態とは別扱い。SHA-256だけで著作者の認証やDAW・プラグイン・遠隔AI・ロボットへの実行権限は得られない。本規則はD01〜D03の正式採択前の仕様候補であり、実装検証済みではない。


## Draft 0.76 — 参照判定規則の文書統合（未採択）

上記Draft 0.70の第5項に残っていた部分的`RESOLVED`の例外を撤回し、Draft 0.71／0.73の現行優先規則と一致させた。INVALID／UNSUPPORTEDは参照判定前の形式エラー、許可済み候補の列挙・取得が未完了なら外部診断`NOT_EVALUATED`、探索完了後にのみMISSING／MISMATCH／AMBIGUOUS／RESOLVEDを判定できる。探索完了前に得たハッシュ一致は暫定証拠であり、**RESOLVEDではない**。新しいJSONフィールドやネットワーク探索義務は追加しない。D01〜D03の正式採択前の規範案である。


---

## 4. 分散Session 0.2の正式4.3日本語規範の継承全文

> **現行採択候補：Draft 0.77（未承認）。** 冒頭の参照解決判定表を現行提案とし、下位の旧Draft番号を持つ節は履歴であって並列の現行規範ではありません。今回の変更は編集上の特定であり、Schemaやシリアライズ形式は変更しません。

# Draft 0.73 — 現行の参照解決判定表（未採択の規範案）

**承認対象：D02。** 以下が現行の採択候補であり、後続のDraft 0.62〜0.72の記述は改訂履歴として保持する。古い判定例を並立する現行規則として扱わない。発行者の採択前に規範として確定したわけではない。Schema・シリアライズ形式は変更しない。

| 優先順 | 条件 | 実装側の診断 |
|---|---|---|
| 1 | ProfileのJSON・必須pin・形式が不正 | `INVALID`（4状態の対象外） |
| 2 | Profileの形式・版が未対応 | `UNSUPPORTED`（4状態の対象外） |
| 3 | 許可範囲が未定義、候補列挙未完了、必要なScore実体を取得不可 | `NOT_EVALUATED`（暫定情報は別途報告、確定4状態を返さない） |
| 4 | 明示的に許可された完全な候補集合にScore実体が0件 | `MISSING`（評価範囲内に限る） |
| 5 | Scoreの実体はあるが、元バイト列のSHA-256がpinと一致しない | `MISMATCH`（評価範囲内に限る） |
| 6 | ハッシュ一致したScoreが構造的に不正または解析不可 | Score形式エラー（`RESOLVED`ではない） |
| 7 | 一致する正常なScore内のTrack/Plan/Visit/range等の必須参照が欠落・重複・不正 | `AMBIGUOUS`＋具体的な診断（`missing_referent`、`nonunique_referent`等） |
| 8 | 元バイト列とハッシュが一致し、必要な参照がすべて一意に解決 | `RESOLVED`（評価範囲内に限る） |

**同一性と権限の境界：** 宣言されたハッシュ対象の元Scoreファイルのバイト列を使用する。Unicode正規化、改行変換、BOM除去、JSONの再シリアライズ、ZIP全体のハッシュによる代替は禁止する。同じバイト列のコピーは同一のバイト同一性を持つ。ファイル名、URI、キャッシュしたハッシュ、音楽上の等価性だけでは同一としない。探索に失敗した候補を黙って除外せず、範囲を狭める場合は新しい評価として明示する。診断名はJSON Schemaに追加するフィールドではない。ハッシュ一致は著作権、信頼性、アクセス権、音響再現、遠隔実行、ロボット安全性を保証しない。編集後の付け替えには明示的承認と新しいpinが必要。

**公開管理：** D01〜D05はすべて未承認。独立パーサー、DAW／プラグイン／DSP、歌唱、WAN／分散実行、フィジカルAI／ロボットの動作検証は公開GO条件から除外し、実施済みとも主張しない。

---

# Draft 0.72 — 編集上の優先順位と採択範囲（未承認）

**採択対象：D02／Distributed Session 0.2。** 正式採択の対象は、承認記録で特定する本文と既存Schemaに限る。過去Draft 0.62〜0.70の参照判定例は改訂履歴として残し、並立する定義として扱わない。矛盾する参照診断については**現行候補内で**Draft 0.71の「許可された候補集合の列挙・取得が完了してから判定」する規則を優先し、未完了ならJSONに新項目を追加せず外部診断`NOT_EVALUATED`とする。

第三者実装は、(a)未知データの読込・保持、(b)ラウンドトリップ保存、(c)編集、(d)意味解釈、(e)実行を区別する。いずれか一つの対応を他の操作まで拡大して表明しない。ハッシュ一致は分散演奏実施、ミキサーの音響再現、ロボット動作の保証にならない。これらの規範案は**D02が発行者により正式採択された場合のみ**規範効力を持つ。

> **Current proposed editorial precedence: Draft 0.71.** This first section supersedes the Draft 0.70 incomplete-enumeration RESOLVED exception; historical sections below are retained as version history. No publisher adoption is implied.

## Draft 0.71 — 参照判定の探索完了条件（未採択の規範案）

Draft 0.70の「探索が未完了でも追加候補で結果が変わらないと予測できればRESOLVEDにできる」という例外を撤回する。未確認候補に関する予測を検証済みの根拠として扱ってはならない。

1. Profileの構造と対応バージョンを先に確認する。不正・未対応なら参照判定とは別の`INVALID`／`UNSUPPORTED`を報告する。URIやハッシュの存在はScore実体へのアクセス許可にならない。
2. **明示された有限かつアクセスが許可された候補集合**を定義し、その範囲、列挙完了、各候補の実バイト取得とSHA-256計算の有無を記録する。判定は宣言された範囲に限定し、世界中に存在しないと断定しない。
3. 候補列挙が未完了、または必要な候補の元バイトが取得できない場合は、外部診断`NOT_EVALUATED`と取得済みの根拠を示す。ハッシュ一致候補が1つ見つかっても4つの確定状態を報告しない。より狭い集合を明示的に定義し直して再評価してもよいが、除外した候補と探索範囲変更を必ず開示する。
4. 列挙と取得が完了した集合について、候補が0件なら`MISSING`、候補があるが生バイト列のSHA-256一致が0件なら`MISMATCH`、一致したScoreの必須参照が欠落・重複・無効なら`AMBIGUOUS`、一致と全必須参照の一意解決が揃った場合のみ`RESOLVED`とする。
5. 同じScoreバイト列の複数コピーは同一データとして扱う。名称、URL、音楽内容、申告ハッシュだけで一致としない。改訂Scoreへの付け替えには明示的な許可と新ハッシュの指定が必要。参照判定だけで実行・通信・音響・プラグイン・ロボット制御を許可しない。

`NOT_EVALUATED`／`INVALID`／`UNSUPPORTED`／診断補足は報告用で、JSONフィールドやSchema enumの追加ではない。4つの判定名称も新しいシリアライズ項目ではない。この規則はD01・D02・D03の正式採択前の提案で、動作・相互運用検証は未実施である。

---

# Draft 0.69 — Score候補の探索範囲と判定の確実性（未採択）

**R04/R11/R13/R14の提案規範。** 4種類の参照診断は、対象操作について**明示的に提供・許可された候補集合内**で判定する。無関係なローカルフォルダーや遠隔URL、リポジトリを勝手に探索して`MISSING`を`RESOLVED`へ変更してはならない。利用者またはホストが追加の元バイト列を許可した場合は**新たな評価**として再判定する。

- **許可された元バイト列候補が0件：** `MISSING`。あくまで評価対象内で未発見であり、Scoreの世界全体における消失を断定しない。
- **候補が1件以上あるがピンのハッシュと一致しない：** `MISMATCH`。候補がすべて新しいリビジョンでも同じ。旧Scoreが全世界から消えたとは断定しない。
- **ハッシュ一致・Score構造不正：** `RESOLVED`ではなくScore形式エラー。
- **ハッシュ一致・必須参照先が0件または複数件：** `AMBIGUOUS`に詳細`missing_referent`または`nonunique_referent`を付す（JSONに追加するフィールドではない）。
- **必要な参照がすべて一意に確定：** 評価対象内で`RESOLVED`。同じバイト列の複製は単一の同一性として扱う。

キャッシュされたハッシュ、ファイル名、URL、署名付きリンク、索引の一致だけでは、実際のScoreの元バイト列による照合を代替できない。候補の元バイト列を取得できず評価自体が行えなかった場合、操作側で`not_evaluated`/`unknown`等を報告してよいが、これはOSTFの第5の参照状態ではない。確認済みの`MISSING`や`MISMATCH`と偽ってはならない。参照診断はデータの真正性、発音、プラグイン復元、ロボットの実行許可を保証しない。**D01～D03、D05、D04は未承認。**

---

# Draft 0.68 — 参照診断の判定順序と過去の事例表の整合（未採択）

**現行の提案（R04/R11/R13/R14）:** 明示的に許可されたScore候補だけを用い、次の順序で判定する。過去のDraftの表が異なる場合、この節を現行の編集提案とし、過去の記録は履歴として残す。

1. Companionの形式・バージョン・必須ハッシュが不正／未対応なら`INVALID / UNSUPPORTED`。4種類の参照診断には含めない。
2. Scoreの元バイト列の候補が1件もなければ`MISSING`。ファイル名やメタデータの一致は候補とみなさない。
3. 候補が存在するが元バイト列のSHA-256が1件も一致しなければ`MISMATCH`。**新版Scoreだけが存在する場合も同様**。Draft 0.62の旧事例でこの場合を`MISSING`とした記述は現行提案では採用しない。
4. 一致したScoreが解析不能または必須構造違反なら、参照成功とせずScore形式エラーとして報告する。
5. 一致して正常なScoreの必須参照を全件調べる。参照先0件は`AMBIGUOUS`と詳細`missing_referent`、複数件は`AMBIGUOUS`と`nonunique_referent`、矛盾・範囲違反は`AMBIGUOUS`とその詳細を示す。複数の問題があればそれぞれ報告する。
6. 必須参照がすべて一意に解決した場合のみ`RESOLVED`。同じバイト列を持つ複数のパスは1つのScore同一性として数える。

この状態名・詳細は**実装側の診断指針**であり、新しいJSONフィールドやSchema列挙値ではない。認証、演奏実行、無断ネットワーク取得、権利許諾、自動的な再関連付けを許可しない。日本語版と英語版の意味が異なる場合は採択を保留する。D01〜D05は未承認。実機・独立パーサー等の検証は条件外かつ未実施。

---

# Draft 0.67 — 参照診断の意味規則の確定候補（未採択）

**公開前の要判断事項（R04/R11/R13/R14）:** Draft 0.64では、必須のTrack/Plan参照先が「存在しない」ケースを`AMBIGUOUS`と呼んでいます。一方、通常の意味では`AMBIGUOUS`は「候補が複数で一意に定まらない」ことを表します。これは提案文書の解釈上の曖昧さであり、Schemaの欠陥や検証結果ではありません。

**採択推奨:** 新しいJSONフィールドや状態の列挙値は導入せず、既存の4つの人間向け診断分類を維持します。対応するProfileを構造的に確認し、許可された元Scoreの**生バイト列**のSHA-256一致を先に要求します。その後、必須Track/Plan/Visit参照先の件数が**0件**ならサマリーは`AMBIGUOUS`とし、診断詳細で`missing_referent`を示します。**2件以上**なら同じサマリーでも詳細は`nonunique_referent`とします。各必須参照が1件に確定した場合のみ`RESOLVED`です。詳細ラベルは推奨診断名であり、OSTFの新規フィールド・enum値・保存必須データではありません。`MISSING`は元Scoreの正確なバイト列がない場合に限り使用し、Score内部の参照欠落には流用しません。

**参照元の信頼境界:** 呼出元が明示的に提供・許可したScore候補のみ参照できます。ファイル名、URL、タイトル、意味的に等しい再シリアライズ結果は生バイト一致の証拠になりません。外部ネットワークからの無断取得、暗黙の付け替え、根拠のない可逆保存の表明は禁止する方針を採択候補とします。

**審査状況:** D01〜D03による採択・修正・却下が必要です。D04/D05も未承認です。動作・独立パーサー・DAW・WAN・ロボットの検証は対象外で未実施です。

---

# Draft 0.66 — 現行審査基準（未採択）

この節は**現行Draft 0.66の審査基準**です。本文に残る旧Draft番号の追記は経緯を示す資料であり、独立した現行版の規範ではありません。Schema・サンプル・ツールは変更していません。

- **Core 4.3:** `schema/ostf-4.3.0.schema.json`と現行Core仕様書・意味規則。4.3で変更を明記していない部分は4.2を継承します。
- **Distributed Session 0.2:** Versionに対応するSchemaと日英Session仕様書。セッションのイベントや同期状態は、ネットワークサービスの保証やロボット実行の許可ではありません。
- **Production Session 0.2:** Versionに対応するSchemaと日英Production仕様書。ミキサー設定・プラグイン記述・アセット参照は、実際のDSP実行や音声再現を保証しません。
- **権限の優先順位（採択案）:** 構造制約は該当バージョンのSchema、意味制約は該当バージョンの規範仕様を参照します。例示、旧版追記、チェックリストはこれらを上書きできません。Schemaと規範仕様が矛盾した場合は、任意解釈を認めず公開阻害要因として修正します。
- **Score参照:** 先にProfileの形式・Versionを検査し、元Scoreのバイト列のSHA-256一致を確認後、必要な参照を解決します。RESOLVED／MISSING／MISMATCH／AMBIGUOUSは診断用の名称でJSONフィールドではありません。不正形式・未対応版は4状態に含めません。参照先不足の具体的な原因を記録し、暗黙の再関連付けを禁止します。
- **対応表明:** Score／Distributed／Production、Version、読込／編集／保存／保持／実行を区別し、未対応や欠落を表示します。

R01〜R14の一括採択は提案段階です。D01〜D03の発行者承認、D05の権利承認、D04の最終ZIP承認は引き続き未完了です。動作・独立実装・実機検証は公開判定から除外し、実施済みとは表記しません。

---

## Draft 0.64 — 形式検証と参照解決の境界（未採択の規範案）

Draft 0.63の4状態は、**形式上有効かつ認識可能な関連Profile**について、元Scoreの参照が解決するかを表す診断である。JSONフィールドや通信上の状態コード、動作認証ではない。判定順序は次のとおり。

1. **関連Profileを先に形式検証する。** Profile種別と版、規定の位置にある必須SHA-256参照の書式を確認する。未対応版や必須参照の不正は**INVALID / UNSUPPORTED**であり、`MISSING`や`AMBIGUOUS`としない。
2. **利用を許可されたScore候補の元バイト列を列挙する。** 候補がなければ`MISSING`。候補はあるが元バイト列のSHA-256が一致しなければ`MISMATCH`。ファイル名、タイトル、音楽内容が同じJSON再出力によって代用しない。
3. **ハッシュ一致後に必要な参照を解決する。** Profileが要求する識別子・Track・Plan・Visit・範囲・改訂などを確認し、すべて矛盾なく一意に解決した場合のみ`RESOLVED`。一致するハッシュがあっても必須参照が欠落・矛盾・非一意なら、人間向け参照診断として`AMBIGUOUS`とし、根本のエラーを併記する。
4. **暗黙の修復は禁止する。** これらの状態はハッシュ書換え、Score付替え、未知データ削除、保存・演奏成功の認定を許可しない。再関連付けは別の明示的に権限を得た編集であり、確定するまで元のScoreとProfileを保持する。

ハッシュ一致のScoreが解析不能、または必須Core制約に違反する場合は**Score形式検証エラー**を明示し、参照が整合していると装ったり、同名の別Scoreへ自動で変更したりしない。4状態によって前提となる形式エラーを隠さない。この案は真正性・権限・機器安全・分散合意を保証しない。**R04/R11/R13/R14およびD01〜D03は未承認。**

---

> **Historical editorial snapshot: Draft 0.64 (unratified); D01–D05 pending.**


## Draft 0.63 — 関連ProfileとScoreの参照解決を行う判定手順（未採択の規範明確化案）

この手順は、与えられた関連Profileを入手済みのScoreバイト列に対して解釈できるかを判断するものである。JSON Schemaを変更せず、ネットワーク取得や実行をホストへ義務付けない。

1. Profileの版に応じて**必須の参照ハッシュおよび識別子**を読む。Distributed 0.2はルートの`scoreSha256`、Production 0.2は`score.sha256`を使用する。必須ハッシュが欠落・不正、または未対応の版である場合は`MISSING`ではなく、**不正な／未対応のProfile**として4状態の対象外とする。
2. 対象の参照に対し、**明示的に渡された、またはローカルでアクセスが許可されたScoreの元バイト列**のみを候補にする。ファイル名、タイトル、パス、Track名、最新版による推測でハッシュを代替しない。ネットワークから暗黙に取得しない。
3. JSONの再シリアライズ前に、**元のバイト列**のSHA-256を計算する。同じバイト列の複数ファイルは1つのバイト同一性として扱う。ハッシュ一致はこの判定におけるバイト同一性の根拠であり、著作者・真正性の証明ではない。
4. 次の優先順位で判定する。
   - 元Scoreの候補バイト列が全くない：**MISSING**。
   - 一致するバイト同一性が1つあり、Scoreの識別子・改訂、参照Track、および必要なPlan／Visit／範囲が規範Profileに従って解決する：**RESOLVED**。
   - ハッシュ一致の候補はあるが、必須の参照先が欠落・矛盾・一意に特定できない：意味上の参照は**AMBIGUOUS**。ハッシュ一致だけでRESOLVEDとはしない。
   - 候補は存在するが一致するハッシュが1つもない：**MISMATCH**。不一致候補が複数あっても、それだけでAMBIGUOUSにしない。
   - 検査後も相異なるハッシュ一致バイト同一性や矛盾する参照解決が残る：**AMBIGUOUS**。恣意的に1件を選ばない。通常のSHA-256同一性の前提では前者は例外的であり、観測済みと主張しない。
5. 関連Profileの参照が整合していると表明できるのは**RESOLVED**のみである。それ以外ではハッシュや識別子を暗黙に書き換えない。明示的な再関連付けは別の権限付き編集であり、必須参照を見直し、Profileが要求する場合は新しい改訂として保存する。未確定または失敗した場合、旧Profileと旧Scoreを維持する。

この優先順位により、通常のファイル探索における`MISMATCH`と`AMBIGUOUS`の混同を防ぐ。4状態は**人間向けの仕様解釈ラベル**であり、必須のJSON列挙値、標準エラーコード、一般的な信頼モデル、動作検証の結果を意味しない。R04/R11/R13/R14およびD01〜D03の採択待ちである。

---

> **Historical editorial snapshot: Draft 0.62 (unratified).** Companion binding resolution states clarified; D01–D05 pending. Runtime tests excluded, not passed.


## Draft 0.62 — Scoreと関連Profileの参照解決状態（未採択の規範案）

Distributed／Productionの関連Profileを開く際、参照元Scoreのハッシュに対して、**RESOLVED**（元Scoreの正確なバイト列が存在しダイジェスト一致）、**MISSING**（元Scoreの実体が存在しない）、**MISMATCH**（候補は存在するがダイジェスト不一致）、**AMBIGUOUS**（候補または同一性が複数あり意図した参照を特定できない）を区別することを推奨する。表示名・ファイルパス・音楽的に等価な書き出しだけではRESOLVEDと判定しない。同一バイト列の複数コピーは同一のバイト同一性であり、曖昧さには該当しない。

RESOLVED以外の状態で最新Scoreやトラック名から参照を**暗黙に付け替えてはならない**。参照未解決のProfileを読み取り専用表示することはできるが、再関連付けはTrack／Plan／Visit／範囲の参照確認を伴う明示的な操作とする。必要な参照が解決していないセットを完全な無損失保存と主張してはならない。これはR04/R11/R13/R14およびD01–D03向けの**未採択案**であり、新しいJSONフィールド、診断メッセージの標準書式、ネットワーク取得許可、実装の動作検証結果を追加するものではない。

---

## Draft 0.61 — 旧Scoreの保持と障害復旧の境界（提案・未承認）

**依存先の保持：** 旧Scoreの正確なバイト列のハッシュを参照するProfileが整合性を維持できるのは、対応する旧Scoreのバイト列も引き続き取得できる場合に限る。Profileだけの保持では十分ではない。新Scoreと旧Scoreを参照する未変更Profileの組を「新バージョンの整合した一式」と表示してはならない。安全な結果は、(i)旧Scoreと旧Profileを対応付けて保持する、(ii)参照先を確認したうえで選択したProfileを明示的に再関連付けする、(iii)参照未解決・分離状態を報告して無損失の一式と主張しない、のいずれかとする。

**部分的な保存失敗：** 一時ファイルへの出力は、それだけではアトミックなトランザクションではない。クラッシュ、リネーム失敗、権限不足、通信中断などでは、実際に確定したScore/Profileのバイト列と未確定・参照未解決のものを区別し、状態が不明なら成功とみなさない。旧Scoreを黙って破棄せず、未確認のハッシュ更新も行わない。ManifestやUIの表示はアトミックな保存の証明ではない。

**新しいJSONプロパティの追加ではない：** 保存場所、確定処理、バックアップ・復旧画面の詳細は実装責任とする。本節はファイルシステムAPIを定義せず、相互運用上の結果を提案する。DistributedとProduction双方に適用する。R04/R11/R13/R14およびD01〜D03の採択は保留中である。

---

## Draft 0.60 — 楽曲編集後の関連Profileのトランザクション的な再関連付け（未採択案）

楽曲の意味が同じでも、書き出したScoreの**元バイト列**が変われば参照先の同一性は変わります。以下は編集ツール向けの提案手順であり、OSTFの新しいJSON命令やファイルシステムの原子的更新を要求するものではありません。

1. 元Scoreのバイト列とハッシュ、参照元のDistributed／Production Profileを、明示的な新Scoreの書き出しが確定するまで変更せず保持する。参照不明のProfileも個別に記録する。
2. 新Scoreの実際の書き出しバイト列からハッシュを算出する。パース後のオブジェクト、空白の正規化、音楽的同等性、Manifestの値で代用しない。
3. 各Profileを「元Scoreを引き続き参照」「新Scoreへ明示的に再関連付け」「不明・未解決」に分類し、利用者が選んでいないものを暗黙に再関連付けしない。トラック名の一致だけで判断しない。
4. 再関連付けするProfileについて、元の参照ハッシュを確認し、新Score上で参照ID・範囲が解決できることを確認する。解決不能ならProfileを変更せず、具体的な不整合を報告する。イベント、オートメーション、歌唱情報を黙って削除しない。
5. 変更対象は確定まで別の出力先へ書き出す。全ファイル一括成功を約束する実装だけが一括ロールバック責任を負う。OSTF自体はファイル／ZIP／ネットワークの原子的トランザクションを提供しない。
6. 新Scoreのハッシュ、Profileごとの判断、未知データの保持、欠落、Asset不足を報告する。一括処理できない場合は元Profileを元Scoreに紐付けたままScoreだけ出力するか、出力を中止する。未解決の組を無損失・整合済みと表明しない。

Sessionでのイベント確定はScoreの変更承認ではなく、Productionのミキサー設定もScoreのMIDI CCを上書きしません。未知データの保持はその内容の解釈を意味しません。再関連付けはプラグイン／ネットワーク／ロボット実行権限を付与しません。R04/R11/R13/R14およびD01〜D03の**未採択**規範候補であり、JSONフィールドの追加はありません。

---

## Draft 0.56 — 操作別の保持責任と明示的な再関連付け（未採択案）

**読込解析・データ保持・編集・実行・音響再現**は異なる能力です。以下の「しなければならない」はD01〜D03での正式採択を前提とした**規範案**であり、版別JSON Schemaには新しい必須項目を追加しません。

- Scoreの読取専用インポートはSessionイベントを確定せず、Production状態を書き換えません。編集可能範囲だけを「対応」と表明できますが、書出しで未対応情報を削除・変換した場合は欠落を開示します。
- Scoreのバイト単位のハッシュが変化した場合、音楽的に同一でもProfileの関連付けを自動移行しません。明示的な確認と再関連付けが必要です。旧Scoreへの参照を保持する選択もできます。
- Sessionのイベント受理・確定は発音、ロボット動作、オーディオ生成の証拠ではありません。同様にProductionのプラグイン記述子は実行可能なプラグインが存在する証拠ではありません。
- URI・ハッシュ・メタデータが残っていても、実際の外部Assetのバイト列がない場合は欠落として申告します。Mixer/Automationを再現するためにScoreのノート・MIDIイベントを暗黙に改変してはいけません。
- 情報欠落の報告には対象のファミリーとバージョン、操作、影響範囲・外部参照、保持／変換／省略／利用不可の区別を含めることを推奨します。これは**OSTF本体外の報告方式**であり、新規の直列化項目ではありません。

必要なデータを保持も欠落申告もできない場合は「完全互換」を主張せず、対応操作の範囲を限定します。詳細は`CONFORMANCE.md`と`PUBLISHER_RELEASE_DECISIONS.md`のR14を参照してください。

# OSTF Distributed Session Profile 0.2 — 日本語規範仕様案（Draft 0.55）

> **現行編集版：Draft 0.59（未採択）。** 下記の古いDraft見出しは、累積した策定経緯を示し、現在のJSON版識別子を変更しません。6件の版別Schemaは不変です。公開判定の正本は [RELEASE_READINESS.md](RELEASE_CHECKLIST.md) とし、D01〜D05はすべて承認待ちです。動作・独立実装検証は判定から除外していますが、完了とは扱いません。

## Draft 0.33 — Sessionイベント受理とScore保存の分離（未採択）

権限・Revision・楽曲同一性を確認してSessionイベントを確定しても、更新対象は**Session状態のみ**です。ScoreのNote、ProductionのMixer/Automation、音響DSPやロボットの物理動作を自動変更しません。拒否・古いRevision・競合を成功した状態変更と報告しないでください。`CONFORMANCE.md`の操作境界表を参照。Schema・通信方式の追加はありません。

---

## Draft 0.32 — Score原本ハッシュと再保存（未採択）

Distributed 0.2の`scoreSha256`は実際に受け取ったScore原本バイトを固定するもので、JSONの意味やURLだけを識別しません。再保存でScoreのバイト列が変われば新しいSHA-256と、既存のRevision規則に従った**明示的な新Session ID**が必要です。既存Session内で確定したイベントの対象を勝手に差し替えてはいけません。`CONFORMANCE.md` Draft 0.32を参照。新しいフィールド・時計プロトコルは追加しません。

---

## Draft 0.29 — 分散セッションのエラー報告と正本の分離（編集案）

`docs/CONFORMANCE.md`のDraft 0.29診断分類を参照。新しいEvent IDを持つ古いbase Revisionの状態変更イベントは拒否し、認証と固定Score/Plan照合を済ませた既承認同一イベントの再送のみ冪等処理できる。承認イベントはSession履歴を変更するがScore Notes/Productionを自動更新しない。各種チェックの結果をロボット実行・安全性の保証に転用しない。この追補は新しいJSONフィールドを追加しない。

---

## OSTF Distributed Session Profile 0.2 — 分散セッション仕様案

**OSTF 4.3 Coreとは別の任意JSONプロファイルです。** 楽曲ファイル `.ostf` にはセッション参加者、リアルタイム位置、通信イベントを入れません。通信手段（HTTP、WebSocket、WebRTC等）や時計同期方式、AIモデル、ロボットの駆動系を指定しません。

## Snapshot（共有状態）

`sessionId`、`documentId`、`revisionId`、`stateRevision`、`participants`、`authorityParticipantId` を持ちます。`position`には楽曲元の`sourceTick`、展開後の`performanceTick`、`visitId`、時計ドメインと観測UTC時刻・不確実性を保持できます。`committedPhrases`は後から参加する演奏者が今後の演奏を再現できるよう、確定した短い演奏フレーズを保持できます。全履歴を再現するには完全なログまたは完全なSnapshotが別途必要です。

参加者IDはTrack IDとは別であり、`assignedTrackIds`の割当てはロボット制御の許可ではありません。参加者の能力は自己申告情報です。実際の物理的な動作・安全性は各ロボットに実装された制御系が独立に判断します。

## Event（共有イベント）

`phraseProposed`、`turnRequested`、`cueIssued`、`performanceObserved`、`participantStatus` は提案・観測・通知にすぎず、確定状態を変更しません。`phraseCommitted`と`sessionStateChanged`だけが承認された状態変更候補です。両者には`resultStateRevision`が必要で、必ず`baseStateRevision + 1`とします。

状態を変更するイベントはSnapshotで指定された権限者の判断でなければなりません。通信の受信順や時計時刻で「最後のものを優先する」といった暗黙ルールはありません。同じ`eventId`の再送は一回だけ扱い、違う内容を同じIDで送信したら競合として報告します。

## Phrase（提案／確定フレーズ）

Profile 0.2の最低限のフレーズ形式は`midi1Notes`です。フレーズ長とノートの開始位置、長さ、音高、ベロシティを整数で表現します。音声合成・歌詞・MPE・ロボットの関節運動・外部音源状態はこの最小表現に含めません。確定したSession Phraseが元のOSTFのNoteを書き換えることはありません。明示的な編集を行って新しいOSTF Revisionへ保存する場合のみ、元の音楽文書が変わります。

## 時間と安全性

共通の音楽Tickを理解できることと、世界各地で同じ瞬間に正確に演奏できることは別です。タイムスタンプだけでは同期できません。時計の校正、通信遅延・揺らぎ、ロボットの準備時間、音の伝搬を実装側で扱います。ネットワークメッセージは運動指令ではなく、ロボットは必ず独立した安全・認証・緊急停止系を維持します。

正確な型とイベント別Payloadは`schema/ostf-distributed-session-0.2.schema.json`、英語の規範的な意味規則は`docs/SESSION_STATE_MACHINE.md`を参照してください。

## Draft 0.4 — Snapshotの状態とイベント同一性

Profile 0.2のSnapshotには`sessionStatus`（`prepared`・`playing`・`stopped`）を必須とします。`playing`のときは`position`が必要です。`prepared`・`stopped`では位置を省略できますが、省略をTick 0と解釈してはいけません。`participantStatus`は個々の参加者の状態報告であり、セッション全体の`sessionStatus`を直接変更する権限はありません。承認済み`sessionStopped`イベントを採用した後のSnapshotは必ず`stopped`となります。Profile 0.2には自動resumeを定義しません。

イベントの重複判定では、`eventId`が同じで**JSON内容が異なる場合**に競合とし、空白やオブジェクト内プロパティ順序だけの違いは競合とみなしません。重複したJSONキーはパース時に不正とします。これはデジタル署名の方式を規定するものではありません。Profile 0.2はあくまでも策定中であり、以前のDraft 0.3のProfile 0.2 Snapshotとの互換性を自動的には保証しません。

## Draft 0.5 — 演奏開始と確定フレーズの範囲

Profile 0.2に`sessionStateChanged`の新しい`changeKind:"sessionStarted"`を追加します。`prepared`から`playing`へ遷移するときは、`payload.position`に演奏Plan・Visit・Source Tick・Performance Tick・時計ドメイン・UTC基準時刻・不確実性を明記し、イベントの`effectivePerformanceTick`と位置Tickを一致させます。`playing`は演奏の時計位置が合意されている状態を意味し、実際の音響やロボット駆動が始まった証拠ではありません。自動の再開・一時停止は定義しません。`sessionStopped`は現在位置の即時の終了であり、将来位置の停止予約ではありません。

`Snapshot.commitmentWindow`は任意の完了範囲宣言です。`startPerformanceTick`から`endPerformanceTick`（半開区間）に交差する、該当State Revisionまでに**確定されたSessionフレーズを全件含む**ことを宣言します。`committedPhrases`が空であれば、その範囲に確定フレーズはないと主張します。省略されれば完全性の保証はありません。別のRevisionで後から確定される内容や、元のOSTF固定ノート、歌詞、ロボットの実行準備までは保証しません。

保存済みの提案を採用する場合は、提案ID・対象Track・フレーズ内容に加えて`effectivePerformanceTick`も一致させます。異なる位置への移動は新規の提案として扱います。詳細は`docs/SESSION_STATE_MACHINE.md`を参照してください。

## Draft 0.6 — 確定Sessionフレーズと演奏Planの整合

`phraseCommitted`で承認できるのは、固定されたOSTFのPerformance Planにおいて対象Trackの`realization`が**明示的に`open`であるVisit**の内部だけです。`fixed`の元ノートに黙って重ねたり、`silent`に音を出したり、`unspecified`を`open`と推測したりしてはいけません。確定フレーズの半開区間全体が一つのVisit内に収まる必要があります。Visitを跨ぐ場合は分割して新規提案します。

**Draft 0.9追補を優先します。** 演奏Planが不明なセッションではフレーズを承認できませんが、現行の未公開Profile 0.2では全Snapshot/Eventにルート`performancePlanId`と`scoreSha256`が必須です。そのため、`prepared`が`position`を省略してもPlanは既に固定されています。`playing`のPositionと`sessionStarted`のPositionはこのルートPlanと一致しなければなりません。Session Phraseは承認後に暗黙の上書き・撤回を行いません。承認済みフレーズの同一Track上での時間重複や、`commitEventId`重複は不正です。実際の権限・時計同期・安全制御は引き続き実装側の責任です。

これらは4.3 Coreに新しいフィールドを加えるものではなく、別冊Session Profile 0.2の**提案中の意味規則**です。`docs/SESSION_STATE_MACHINE.md`のDraft 0.6節を参照してください。

## Draft 0.7 — 楽曲Revision・確定履歴・演奏実績の分離

1つのSessionは同一の楽曲`documentId`・`revisionId`・`performancePlanId`を参照し続けます。Web API側で新しい曲に更新されても、元の確定済みフレーズは自動的に新曲へ移動できません。内容の異なる文書を同じRevisionとして受け取った場合は整合性エラーです。

`phraseCommitted`は**承認されたフレーズの履歴**であり、遠隔ロボットが実際に発音したという証拠ではありません。将来のVisitを飛ばした場合やSessionを停止した場合には、後続の未演奏フレーズを演奏済みとみなさず、承認履歴だけ保持します。演奏中のVisit切替はPerformance Tickが前へ進む場合に限定し、同一Sessionの巻戻し・再開・別Revisionへの切替はProfile 0.2では定義しません。

同一`eventId`かつ内容が同一の再送は、状態Revisionが進んだ後でも二重採用しません。異なる内容の同一IDは競合として拒否します。`assignmentChanged`でも確定済みTrackフレーズを改変・消去しません。将来の確定フレーズを担当する参加者がゼロになる割当変更は、この保守的な策定案では拒否します。各参加者への実際の発音割り当て、認証、機械的安全性はSessionを使う実装側が管理します。

詳しくは英語の`SESSION_STATE_MACHINE.md` Draft 0.7 節を参照してください。JSON Schemaは変更していません。

## Draft 0.8 — 割当変更・イベント再送・フレーズ範囲の規則修正

**未承認の規範案。** Profile 0.2の`sessionStateChanged.payload.changeKind:"assignmentChanged"`は`participantId`と`assignedTrackIds`のみを担当する変更とし、`targetVisitId`または`position`を含めてはいけません。従来のJSON Schema条件式は`position`単独を誤って許していたため、両項目を独立に禁止する`not.anyOf`へ修正しました。新フィールド・新定義は追加していません。**これはDraft 0.8時点の挙動であり、Draft 0.10で置き換えます。** 現在の未公開Draft 0.10では`sessionStarted`と`visitChanged`の両方が`position`を必須とします。`assignmentChanged`では引き続き禁止です。

認証されていない同一イベントIDの受信者へ、過去のイベントが受理されたかを開示してはいけません。**認証・権限・楽曲Revisionの照合が先、同一イベントIDの再送照合が次、未受理イベントに限って状態Revisionの新旧比較**を行います。受理済みと等しい再送はno-op、異なる内容で同じIDは競合です。JSONのオブジェクト内プロパティ順や空白は差異とせず、配列の順番と文字列の実際の文字は区別します。数値は十進数として正確に比較し、`1`と`1.0`は等価ですが真偽値とは異なります。値の精度が保証できない場合は勝手に再送と判定せず不確定として拒否します。

どのSnapshotでも、保存された各`committedPhrases[].phrase.notes[]`の`startTick + durationTicks`は親Phraseの`durationTicks`以下でなければなりません。`commitmentWindow`の有無はこのノート範囲の妥当性に影響しません。停止後やVisitスキップ後に残した過去の確定履歴は、現在の演奏者割当を要求しません。一方、未演奏の未来フレーズの担当者がゼロになる割当変更は、従来の保守的な意味規則どおり拒否します。確定履歴を実際の発音の証拠と解釈してはいけません。

## Draft 0.9 — 演奏PlanとOSTF原本バイト列の固定（未承認の規範案）

これまでのProfile 0.2では`prepared`のSnapshotが`position`を省略すると、どの`performancePlans[].id`を使うか確定できませんでした。また`documentId`と`revisionId`だけでは、同名Revisionで異なるJSONが配信された場合の不一致を確認できません。そこで、**別冊の未公開Distributed Session Profile 0.2に限り**、全Snapshot・Eventでルート直下の`performancePlanId`と`scoreSha256`を必須とします。OSTF 4.3 Core自体のSchemaは変えません。

- `performancePlanId`：参照する4.3楽曲中の有限なPerformance Plan ID。`prepared`/`stopped`の位置情報がないSnapshotでも省略不可です。
- `scoreSha256`：実際に共有するOSTFファイルの**正確なUTF-8バイト列**に対するSHA-256（小文字16進64桁）。HTTPならContent-Encodingを復号した後、JSONパースや書き直しの前の原本バイト列を計算対象にします。原本にBOMが含まれる場合もそのバイトを含めます。JSONの空白だけが違っても別ダイジェストになります。これはJSONの音楽的な同値性ではなく、特定のファイル実体を固定するための値です。
- `position`または`sessionStarted.payload.position`が存在するとき、内側の`performancePlanId`はルートのIDと**必ず一致**します。Visit ID、Source Tick、Performance TickはそのPlanで解決します。位置を省略したことをPlanの省略とみなしてはいけません。
- セッションの固定識別は`sessionId`、`documentId`、`revisionId`、`performancePlanId`、`scoreSha256`の組で行い、イベント再送を受理したかの問い合わせより前に、認証とこの組の照合を行います。同じRevision名でもファイル内容が異なれば拒否します。
- SHA-256はファイルバイト列の照合情報であって、発行者の本人性、署名、所有権、ロボット駆動の安全性を証明しません。これらは引き続きサービスや実機制御側で扱います。
- 旧Draft 0.8のProfile 0.2データには新しい必須フィールドがないため、そのままでは新案に適合しません。使用するPlanと原本バイト列を明示的に再確認して更新します。別バージョンのProfile 0.1を自動で0.2に読み替えません。

**想定診断:** `E-SESSION-PLAN-UNPINNED`、`E-SESSION-POSITION-PLAN-MISMATCH`、`E-SESSION-SCORE-DIGEST`。構造的な整合確認は通信遅延や実機演奏の検証ではありません。

## Draft 0.10 — Visit切替時の時計基準位置を明示する規範案

Profile 0.2の`sessionStateChanged.payload.changeKind:"visitChanged"`では`targetVisitId`に加えて`position`を**必須**とします。`position.visitId`は対象Visitと同一、`performanceTick`はEventの`effectivePerformanceTick`および対象Visitの展開後開始Tickと一致し、`sourceTick`はそのVisitの最初の参照区間の開始Tickを表します。`epochUtc`は受信時刻ではなく、指定された演奏Tickに対応する共有時計の推定時刻です。演奏者側はこの基準位置を使って新しいVisitに移れますが、通信遅延・ロボット動作・同期精度は保証しません。

以前の未公開Draft 0.9のように`visitChanged`がVisit IDだけを持つレコードはDraft 0.10案に適合しません。信用できる時計情報から作者が明示的に更新し、時刻を推測で埋めないものとします。Core 4.3は変更しません。実装・実機検証済みという意味ではありません。

## Draft 0.11 — 時計ドメインの継続性・テンポの正本・停止イベント（未承認の規範案）

- `sessionStarted.payload.position.clockDomainId`で演奏中セッションの音楽時計ドメインIDを確定します。同一Sessionの以後の`playing` Snapshotの`position`と`visitChanged.payload.position`は**同じIDが必須**です。違うIDへの暗黙の変更は不正であり、必要なら新しいSessionを作成します。`prepared`の任意Positionは演奏時計ドメインを確定しません。IDが同じことは通信遅延や時計の精度・本人性を保証しません。
- `position.tempoBpm`は任意の説明情報であり、元のOSTFの`timeline.tempoChanges`から`sourceTick`時点で有効なBPMと**数値的に一致**しなければなりません。source Tickで採用されるのは、その時点以前で最後に明示された段階型Tempoです。Sourceの区間を飛び越したときも元のTempoを再取得します。`tempoBpm`が異なれば`E-SESSION-TEMPO-CONFLICT`として拒否し、省略時には元のOSTFから解釈します。Tempoがソース側にまだ存在しなければ、勝手にテンポを作らず未解決とします。
- `sessionStopped`の`effectivePerformanceTick`は記録上の音楽位置・参考情報であり、将来の停止予約ではありません。承認された停止はただちにSessionを`stopped`にしますが、実際の音やロボット駆動が停止した証拠にはなりません。`prepared`から停止した場合など、再生位置の未確定なケースでTick 0を記録しても物理的な停止時刻を意味しません。

追加フィールドはありません。Core 4.3 Schemaと正式4.2継承部分は変更しません。詳細規則の英語正本案は`SESSION_STATE_MACHINE.md` Draft 0.11であり、実際のWAN・実機・独立パーサー検証は利用者指定のリリース判定条件から除外され、完了とも主張しません。

## Draft 0.12：演奏中の時計基準には元楽曲のテンポが必要（未承認）

`playing`状態のSnapshot、および`sessionStarted`・`visitChanged`の`position`は、音楽時刻とUTC推定時刻を対応させる有効な演奏上の基準位置を主張します。そのため、`sourceTick`において、固定されたOSTF楽曲の`timeline.tempoChanges[]`から有効なBPMを一意に解決できなければなりません。任意の`position.tempoBpm`を省略しても、元楽曲にテンポがなければ`E-SESSION-TEMPO-UNRESOLVED`としてこの時計基準を拒否します。`tempoBpm`が存在する場合は元楽曲の値と一致しなければなりません。

通常のOSTF楽曲に必ずTempoを記載することを要求するものではありません。`prepared` / `stopped` Snapshotの任意のPositionは演奏中の時計基準を宣言しないため、テンポ未解決であっても演奏同期が成立したとは扱いません。演奏開始前に必要なテンポを明示するには、新しいOSTF Revisionを作成して楽曲側に記述します。Profileだけでテンポを捏造・上書きしてはいけません。

1区間の理想的な音楽経過秒数は `60 × Tick数 ÷ (PPQ × BPM)` です。実演奏上の同一Visit内で時計基準から将来Tickを求める場合、元の楽曲のテンポ変更点と参照Section境界で区間を分割し、それぞれのBPMで積算します。省略された元曲の区間は経過時間に加えず、境界をまたいで直前のテンポを流用しません。テンポ未解決区間ではUTC演奏期限を算出できると主張してはいけません。これは楽曲上の理想時刻の数理規則であり、WAN同期精度やロボット駆動時刻を保証しません。

さらにProfile 0.2のSnapshotは少なくとも1名の`participants[]`を持つ必要があります。`authorityParticipantId`がその中の唯一のIDへ解決されるという既存の意味規則を、Schemaの`minItems:1`でも補強しました。これらは正式採択前の編集案です。

## Draft 0.19 — Studio Production Profileとの任意の関連付け

Distributed Session 0.2の`scoreSha256`とProduction Session 0.1/0.2の`score.sha256`を元OSTFの実体バイト列のSHA-256と一致させ、文書ID/RevisionおよびDistributedが指定する有限Plan IDを原本で解決できる場合に限り、同じ曲の二つのProfileとして関連付けられる。ProductionにはルートのPlan IDを勝手に追加しない。Track IDの一致はプラグイン、音声出力、ロボットを自動接続する指示ではない。遠隔の`phraseCommitted`はStudioの録音・Automation・Plugin状態を編集しない。詳しくは`PRODUCTION_SESSION_PROFILE.ja.md`第25節。

## Draft 0.23 — 原本ハッシュと別冊の責任分離（未採用の整理案）

Core Score 4.3そのものに必須のハッシュ値はない。一方、Distributed Session Profile 0.2のルート`scoreSha256`は必須であり、`documentId`、`revisionId`、`performancePlanId`と共に**元ScoreのUTF-8原本バイト列**に固定する。これはJSONの再整形後に計算する標準化ハッシュではない。元Scoreが未入手で両Profileのハッシュが一致しても、元のTrack ID・Plan IDが有効とは確認できない。古いWeb説明の「共通のcanonical JSONハッシュはない」を、別冊0.2の必須`scoreSha256`を無効にするものとして解釈しない。

DistributedのEventが確定しても、ProductionのChannel/Plugin/AudioRegionやCoreのNoteへ無断転記しない。Studio ChannelとSession参加者が同じTrack IDを参照しても、プラグイン起動やロボット駆動の許可は生じない。新JSONパラメーターや通信APIは追加しない。


## Draft 0.24 — データ識別子と旧Revisionイベントの区別（未採択案）

Distributed Profile 0.2のSnapshot/Eventは、ルートに`profile:"OSTF-Distributed-Session-0.2"`および`recordType:"snapshot"`または`"event"`を持ちます。**Production Profileの`profileVersion`フィールドを持ちません。** 旧Distributed 0.1は`profile:"OSTF-Distributed-Session-0.1"`であり、0.2と互換レコードとして自動解釈しません。Production 0.1.0/0.2.0とは`profile`もSchemaも異なります。

すでに承認されているイベントの再送は、セッション/原本/Plan/発信者の認証・照合後に、同一`eventId`と完全に等しいパース済みイベント内容であれば何も再適用しません。同一IDで内容が違う場合は不整合です。**新しい状態変更イベント**が古い`baseStateRevision`を指定していたら拒否します。勝手に`phraseProposed`へ変更したり、最新Revisionとして再承認したりしません。提案・観測・状態報告は確定Revisionを増やしません。根拠となる詳細な英文規範案は`SESSION_STATE_MACHINE.md`です。これらは新規JSONフィールドを定義せず、動作・WAN・ロボットの検証を意味しません。


## Draft 0.70 — 候補集合の探索完了と慎重な参照判定（未採択）

参照の4状態は、**実際に評価できた範囲での判定**であり、インターネット上の全候補を探索した保証ではない。実装は許可された候補の探索範囲、およびその列挙と実体バイト取得の完了・未完了を明示しなければならない。ファイル名、申告されたハッシュ、HTTPヘッダー、音楽的な一致だけでは検証済みとはしない。

1. 許可された候補集合の列挙またはバイト取得が不完全な場合は、外部診断 **NOT_EVALUATED** とする。これはOSTFの新しいJSON値ではない。
2. 候補集合の探索と取得が完了している場合、候補Scoreが0件ならその範囲において **MISSING**、Scoreが1件以上存在しても元バイト列のSHA-256一致がなければ **MISMATCH** とする。世界中に存在しないという意味ではない。
3. ハッシュ一致候補の同一バイト列は重複コピーとしてまとめ、Track／Plan／Visitなど必須参照が欠落または一意に解決できない場合は **AMBIGUOUS** とする。`missing_referent` と `nonunique_referent` はJSONに格納しない診断補足とする。
4. ハッシュと必須参照がすべて整合して初めて **RESOLVED** とする。
5. 許可された候補の列挙または実体バイト取得が一つでも未完了なら、一致候補をすでに観測していても **NOT_EVALUATED** と報告する。部分的・条件付きの **RESOLVED** は認めない。未完了の探索範囲を明示し、候補集合が未完了のままMISSING・MISMATCH・AMBIGUOUS・RESOLVEDを推定してはならない。古いProfileを改訂Scoreへ暗黙に付け替えてはならない。

INVALID／UNSUPPORTEDは形式・バージョンに関する事前エラーであり、4状態とは別扱い。SHA-256だけで著作者の認証やDAW・プラグイン・遠隔AI・ロボットへの実行権限は得られない。本規則はD01〜D03の正式採択前の仕様候補であり、実装検証済みではない。


## Draft 0.76 — 参照判定規則の文書統合（未採択）

上記Draft 0.70の第5項に残っていた部分的`RESOLVED`の例外を撤回し、Draft 0.71／0.73の現行優先規則と一致させた。INVALID／UNSUPPORTEDは参照判定前の形式エラー、許可済み候補の列挙・取得が未完了なら外部診断`NOT_EVALUATED`、探索完了後にのみMISSING／MISMATCH／AMBIGUOUS／RESOLVEDを判定できる。探索完了前に得たハッシュ一致は暫定証拠であり、**RESOLVEDではない**。新しいJSONフィールドやネットワーク探索義務は追加しない。D01〜D03の正式採択前の規範案である。


---

## 5. 5.0で追加・変更した音楽的意味の全差分

# OSTF 5.0 — 意味フィールド・差分リファレンス（Draft 0.9）

この文書は**変更された意味**と**新規形式のフィールド**を列挙する。4.3の全127 Core定義、Production 0.2の14定義、Distributed 0.2の16定義に関する変更しないフィールドの**全項目と意味**は、同梱の採択4.3規範原文を参照する。完全構造索引は`PARAMETER_REFERENCE.md`（5現行Schemaの1,601構造宣言）であり、名前・型・Enumの詳細な一覧を持つ。この索引のみを意味仕様の代用にしない。

## A. 5.0 Core Score

| JSON Pointer | 変更 | 意味 |
|---|---|---|
| `/format` | なし：`OSTF` | Core Score識別子。プロジェクト／Plugin Contextの識別子をここへ入れない |
| `/version` | `4.3.0`→`5.0.0` | 明示的な新版のディスクリミネータ。未知Versionに暗黙フォールバック禁止 |
| `/ppq` | なし | Core MIDI/Timelineの四分音符当たりTick。Host PPQと同一視しない |
| `/song`, `/timeline`, `/harmony`, `/tracks`, `/soundSlots`, `/lyrics`, `/resources` | 形状・意味とも4.3継承 | 定義・制約・時間座標は正式4.3原文参照 |
| `/ensembleInteractions`, `/performancePlans`, `/tracks/*/directions` | 形状・意味とも4.3継承 | IntentはNotes自動変更ではない。Visitは元Scoreの区間投影 |

参照：`adopted-4.3/docs/SPECIFICATION.ja.md`、`adopted-4.3/docs/PARAMETER_REFERENCE.md`。Coreの**各`$defs`は127/127継承**。ルートSchemaのタイトルや`$id`変更は音楽意味の追加ではない。

## B. Production Session 0.3

| フィールド | v0.3における規則 |
|---|---|
| `/profile` | `OSTF-Production-Session`（0.2から継続） |
| `/profileVersion` | 0.3.0（0.2.0文書とは区別） |
| `/score/formatVersion` | **5.0.0固定**。旧4.3用0.2から無条件のラベル変更禁止 |
| `/score/sha256` | Source Score UTF-8**原バイト**SHA-256。装飾や空白のJSON変更でも新Digestが必要 |
| `/score/documentId`, `/score/revisionId` | 存在すれば実際のScoreとの一致必須。推測して採番しない |
| `/channels[]`, `/devices[]`, `/assets[]`, `/audioRegions[]`, `/sidechainConnections[]`, `/hostExtensions[]` | 元0.2の全制約を継承。`asset.byteLength`、`plugin.name`必須など正式0.2原義を保持 |
| `/automation[]` | **v0.3意図的追加制約**：ターゲット別に`valueType`・`points[].value`型／値域を限定 |

Automationターゲット表（`atTick`は各Pointで必須、非負の元Score Tick、Lane内厳密昇順）：

| `target.kind` | `parameter` | `valueType` | `points[].value` | `interpolation` |
|---|---|---|---|---|
| `channel` | `gainDb` | `number` | -120..24 dB | step / linear |
| `channel` | `pan` | `number` | -1..1 | step / linear |
| `channel` | `mute` | `boolean` | true / false | **step** |
| `send` | `gainDb` | `number` | -120..24 dB | step / linear |
| `send` | `enabled` | `boolean` | true / false | **step** |
| `audioRegion` | `gainDb` | `number` | -120..24 dB | step / linear |
| `audioRegion` | `mute` | `boolean` | true / false | **step** |
| `deviceControl` | `enabled`, `bypass` | `boolean` | true / false | **step** |
| `device` | `parameterId`（不透明な文字列） | `number` | 0..1 正規化 | step / linear |

数値にBooleanを渡さない。内部音源のMIDI CC7・CC10・CC11・CC91/93と音声Mixの正本は異なる。スキーマ単体でIDの存在、時刻順、音声グラフ非循環を完全保証したとは主張しない。参照：`adopted-4.3/docs/PRODUCTION_SESSION_PROFILE.ja.md`、`adopted-4.3/docs/PRODUCTION_PARAMETER_REFERENCE.md`、`docs/PRODUCTION_SESSION_0_3.ja.md`。

## C. Distributed Session 0.3

| フィールド | v0.3の規則 |
|---|---|
| `/profile` | `OSTF-Distributed-Session-0.3`。`profileVersion`は**存在しない** |
| `/recordType` | `snapshot`または`event` |
| `/scoreSha256` | Score 5.0原本UTF-8バイトSHA-256、64桁小文字 |
| `/documentId`, `/revisionId` | Score 5.0の実在Document/Revisionへ固定 |
| `/performancePlanId` | Score 5.0の実在有限Planを参照 |
| Snapshot `/participants[]`, `/position`, `/stateRevision` | 0.2における参加者、位置、状態改訂の原義を保持 |
| Event `/kind`, `/payload`, `/baseStateRevision`, `/resultStateRevision` | 0.2の7種類Event／原子改訂・重複イベント規則を継承 |

0.3は**0.2のProfile識別名とScore対象Versionを更新**したもので、Draft0.7の`/score`ネスト、参加者`id`、フレーズ`encoding`等の実験的Wire形状を採用しない。旧Sessionを生きた状態のまま移行せず、5.0 Score用に新Sessionを開始する。参照：`adopted-4.3/docs/SESSION_PROFILE.ja.md`、`adopted-4.3/docs/SESSION_PARAMETER_REFERENCE.md`、`docs/DISTRIBUTED_SESSION_0_3_SPECIFICATION.ja.md`。

## D. OSTFP 1.0：Manifestフィールドと意味

| 場所 | 必須 | 意味 |
|---|---|---|
| `packageFormat`, `packageVersion` | はい | `OSTFP`, `1.0.0` |
| `projectId`, `title` | はい | Project識別と表示名 |
| `score.path` | はい | ZIP内**唯一の**Score原本パス |
| `score.format`, `.version`, `.sha256` | はい | `OSTF`、4.3.0または5.0.0、原本バイトDigest |
| `documents[].id`, `.role`, `.path`, `.family`, `.version`, `.sha256` | Documentを含む場合 | Profile等の別正本識別。`required`は任意Booleanで携帯完備レベルの宣言 |
| `assets[].id`, `.path`, `.purpose`, `.sha256`, `.mediaType`, `.sizeBytes` | Assetを含む場合 | ZIPに**存在する**バイト列の宣言。`license`等は証拠や使用権限ではない |
| `bindings[].documentPath`, `.resourceId`, `.assetId`, `.resourceKind` | Bindingを含む場合 | Core Resource／Production Assetの参照IDを実Assetに結び付ける。内部URIは書き換えない |
| `externalAssets[]` | 任意 | 同梱していないURIを記述するのみ。自動取得・再配布・認証の権限はない |
| `metadata`, `extensions` | 任意 | 表示用・拡張用。Core/Production/Distributedの意味の正本を上書きしない |

制約：先頭`mimetype`は非圧縮ASCII、`manifest.json`は必須、POSIX NFC相対パス・重複なし・ZIP展開先脱出禁止、Manifest非宣言のファイル禁止。ハッシュと存在の静的整合が必要。詳細：`docs/PACKAGE_SPECIFICATION.ja.md`と`docs/PACKAGE_BINDING_RULES.ja.md`。

## E. Plugin Context Exchange 1.0：メッセージ意味

| 場所 | 規則 |
|---|---|
| `protocol`, `protocolVersion` | `OSTF-Plugin-Context`, `1.0.0` |
| `messageId`, `operation` | メッセージIDと `context/editProposal/ack/diagnostic` のいずれか |
| `score.format/version/sha256` | 原本Scoreの識別とバイトSHA。`score.documentId/revisionId`は任意 |
| `scope.startTick/durationTicks`, `trackIds`, `sectionIds` | **部分投影のフィルタ**。データだけで編集権限を与えない |
| `transport.isPlaying/positionTick/hostPpq/scorePpq` | 任意のHost時刻とScore時刻の橋渡し。`positionTick`はHost PPQ上の値 |
| `context.payload.partial/data/unavailableFields` | JSONの部分投影であり保存可能な完全`.ostf`ではない |
| `editProposal.payload.proposalId/baseSha256/mode/changes` | `mode:"atomic"`。HostがSHA、Revision、権限、対象ID、Pointer、Schemaを検証後に**まとめて適用または全拒否** |
| `ack.payload.inReplyTo/status` | `inReplyTo`は`messageId`。`received`は保存成功ではない。`applied`時のみ新SHAと改訂IDを通知可能 |
| `diagnostic.payload.status/paths/detail` | エラー分類と関連JSON Pointer。不明なCore欄を初期値で捏造しない |

VST3・AU・CLAP・Max for Liveは既存のプラグインAPIで動作し、このメッセージ規格自体に**実時間配送・音声DSP・ホスト権限**は含まれない。詳細：`docs/PLUGIN_EXCHANGE_PROTOCOL.ja.md`、`docs/PLUGIN_EXCHANGE_PROTOCOL.ja.md`。

## F. 完全な継承フィールドの見方

- `adopted-4.3/docs/PARAMETER_REFERENCE.md`：Core 127定義の継承元の**全パラメーター・制約**。
- `adopted-4.3/docs/PRODUCTION_PARAMETER_REFERENCE.md`：Production 0.2から継承する14定義の**全パラメーター**。
- `adopted-4.3/docs/SESSION_PARAMETER_REFERENCE.md`：Distributed 0.2から継承する16定義の**全パラメーター**。
- `PARAMETER_REFERENCE.md`：5現行Schemaの条件、Union、プロパティ宣言の**構造索引**。

この4資料と本リファレンスを組み合わせたものを、**Draft0.9の全フィールド参照体系**とする。ただし実機動作同一性を意味しない。


---

## 6. Production Session 0.3の意味規則

# OSTF 5 Production Session 0.3 — 相互運用意味規則（Draft 0.10）

**Production 0.3はバイト照合済の採択4.3 Production 0.2を継承する5.0用規範です。正式な継承原文は `adopted-4.3/docs/PRODUCTION_SESSION_PROFILE.ja.md` に収録しています。** 構造の正本は`schema/ostf-production-session-0.3.schema.json`、宣言可能なProfileは`profile:"OSTF-Production-Session"`、`profileVersion:"0.3.0"`です。`score.formatVersion`は`5.0.0`固定。各実装はCore Score原文のUTF-8バイト列のSHA-256を照合する必要があります。未知のScore版、旧Profileとの不一致を自動変換してはなりません。

## 1. チャンネル・音源・接続の参照

* `channels[].id`、`devices[].id`、`assets[].id`、`audioRegions[].id`、`automation[].id`、全チャンネルを横断した`channels[].sends[].id`、`sidechainConnections[].id`はそれぞれの名前空間で一意。IDは表示名で代用しません。
* `master` Channelはちょうど1件。`track` Channelだけが実在Core Trackに対応し`trackId`を持つ。`audioTrack`はCore Trackを増やさず、`bus/master`はTrack参照を持ちません。Core Trackが複数Channelから参照される場合、意図的な重複出力として誤って扱わず、実装が必要な多重マッピング規則を提供しない限り拒否します。
* それぞれの`deviceIds[]`は同一Profileに存在するDeviceを処理順に列挙します。1 Deviceを2 Channelで所有させない。`instrument`はCore Track Channelの最初のSlotに最大1個、Bus/MasterはInstrumentを含まない。未知のPlugin識別子・状態は参照として保持します。
* 非Master Channelの`outputChannelId`は他Channelに解決しなければなりません。`send.targetChannelId`はBusに、`sidechain.targetDeviceId`は別Channelに属するEffectに解決しなければなりません。`sourceChannelId`はMasterにできません。Sidechain `(targetDeviceId,targetPortId)`は同じProfileで二重に定義しない。
* Output、Send、Sidechainで作られたChannel依存の有向グラフは循環禁止。Source→Destinationを辺とし、SidechainではTarget Deviceの所有ChannelをDestinationとします。存在しない参照や循環を無音で補正せず、明確に拒否・診断します。

## 2. 素材・Audio Regionの一致

* `stateAssetId`は`purpose:"pluginState"`のAssetだけを参照する。`audioRegions[].sourceAssetId`は`purpose:"audioSource"`のAssetだけを参照する。用途違いは拒否します。URIは自動ダウンロードやインストール権限ではありません。
* `sourceStartFrame >= 0`、`sourceFrameCount > 0`、`sourceStartFrame + sourceFrameCount <= asset.frameCount`。`fadeInTicks + fadeOutTicks <= durationTicks`。`startTick`はScore元のグローバルTickです。
* `native`は指定された音声Frameを元のTempo Mapの実時間で再生し、勝手にループ・伸縮しない。`fit`はRegion時間と指定Frame区間の等比例関係を意図し、音高の扱いを`pitchPolicy:preserve|followRate`に明示する。アルゴリズムの違いは音響一致を保証しません。
* 音声Regionは`track`または`audioTrack` Channelに置く。Bus/Master上のAudio Regionは不正。重なりは加算であり、自動Crossfade、正規化、補完サンプルの挿入を行わない。

## 3. Automationの正本・値域・競合

* 全`automation[].points`は非負の**元Score Tick**の厳密昇順で、同Tick重複禁止。複数Visitが同じ元区間を通る場合、元座標の自動化をそれぞれ再適用します。
* 同じ`(target.kind,参照ID,parameter/parameterId)`へ複数Laneを宣言しない。サポートされないLaneを他のパラメータへ暗黙変換しません。
* Boolean対象は`channel.mute`、`send.enabled`、`audioRegion.mute`、`deviceControl.enabled/bypass`のみ。`valueType:boolean`と`interpolation:step`を必須にし、`points[].value`はBooleanです。**Boolean Pointは`atTick`と`value`の両方が必須です。**
* `channel.gainDb/send.gainDb/audioRegion.gainDb`は数値dB、`channel.pan`は-1..1、`device.parameterId`は原則0..1の正規化数値。`deviceControl`は内部VSTパラメータではありません。値域外や異なる型を暗黙に丸めず、診断します。
* 同じ時刻の異種Laneの効果とMIDI CC間の処理順は明示された責務だけに限る。MIDI CC7/10/11/91/93をMixer Gain/Pan/Sendと同じ正本として合成・上書きしません。
* 初回Point前はChannel/Device静的値、最終Point後は最後のPoint値を保持。`step`は直前値、`linear`は対象の数値領域で線形補間します。1つの対象について異なるLaneが競合したら曖昧なlast-writer-winsを採用しません。

## 4. 情報損失と受け渡し

* Score編集で元バイトSHAが変わった場合、Productionの旧`score.sha256`をそのまま引用しません。ユーザーが明示的にProductionを新Scoreへ再関連付けするか、旧Profileを歴史資料として保持します。Plugin Contextの`ack`だけで制作環境のSHAを更新しません。
* `.ostfp`内に素材が存在しても、Pluginプログラム・License・Voicebankが利用可能だと保証しません。未対応Hostは識別子・順序・State記述子と実際に受領したBytesを可能な限り保持するか、損失範囲を示して破壊的保存を拒否します。
* 本規格はDAW/プラグインの演奏・DSPアルゴリズム、Multi-take Comp、複雑なWarp、Surround、並列Rack、物理I/Oの同一性を標準化しません。

**公開版の規範範囲**：上記はProduction 0.3の正式な意味規則です。参照整合、音楽時間、循環禁止等はJSON Schema単独で検証できないため、実装が別途評価します。実装・DSP・DAWでの可聴互換性はこの文書の保証対象ではありません。

## Automation Target の型と値域（規範）

Production Session 0.3では、以前の開発Schemaに存在した数値ターゲットへBooleanを与えられる構造上の抜けを修正する。Score 5.0 Core、旧4.3 Production 0.2、Distributed Sessionを変更しない。

| `target.kind` | `parameter` | `valueType` | `points[].value` | 補足 |
|---|---|---|---|---|
| `channel` | `gainDb` | `number` | -120～+24 dB | チャンネルの音声Gain。MIDI CC7と独立 |
| `channel` | `pan` | `number` | -1～+1 | 音声Pan。MIDI CC10と独立 |
| `channel` | `mute` | `boolean` | `true` / `false` | `interpolation:step`のみ |
| `send` | `gainDb` | `number` | -120～+24 dB | 対象Sendの音声Gain |
| `send` | `enabled` | `boolean` | `true` / `false` | `interpolation:step`のみ |
| `audioRegion` | `gainDb` | `number` | -120～+24 dB | Region段階の音声Gain |
| `audioRegion` | `mute` | `boolean` | `true` / `false` | `interpolation:step`のみ |
| `deviceControl` | `enabled`、`bypass` | `boolean` | `true` / `false` | Plugin内部Parameterではない |
| `device` | `parameterId` | `number` | 0～1 | 正規化された不透明Parameter値、実パラメータの尺度はホスト依存 |

**必須意味規則：** 各Laneは`points[]`を1件以上持ち、`atTick`を元ScoreのGlobal Tickで**厳密昇順・重複なし**に並べる。Scopeは元ScoreのTickであり、Performance PlanのVisitが再訪する場合も元位置のAutomationを再適用する。複数の同じ`target.kind`+ID+Parameterがある場合、配列後勝ちにせず不正とする。数値には`step`と`linear`を許し、Booleanには`step`のみ。最初のPoint以前は各静的Channel/Send/Device/Region値、最後のPoint以降は最後のPoint値とする。未存在ID、未対応Parameter、型・値域外を黙って補正せず、保存拒否またはLoss報告を行う。

**構造上の保証範囲：** 0.3 Schemaではターゲットごとの型・値域まで確認できる。ただし参照先IDの存在・重複Lane・時刻の昇順・音声グラフの循環禁止をJSON Schema 2020-12の単一文書構造ルールのみで完結させたとは主張しない。実機の音質・再生・プラグイン相互運用は未検証。

**サンプル：** 配布の`examples/production/03-boolean-and-device-automation-03.json`はBooleanおよびDevice操作を示す。`true`を`gainDb`に与える場合、0〜1以外を`device`パラメータに与える場合などは**不正例**であり、正規サンプルに含めない。


### 正式4.3原本継承の注意

正式採択4.3 Production0.2 Schemaの14 `$defs`全てを再採用した。`channel.name`、`plugin.name`（必須）、`plugin.namespace`、`asset.purpose=renderedAudio`、`asset.byteLength`、`hostExtension.namespace`のパターン等は正式0.2の原義のまま保持する。以前の未公開案にあった`assets[].sizeBytes`という便宜項目は**ProductionではなくPackage Manifest内のsizeBytes**としてのみ使用する。0.3では`profileVersion`とScore 5.0 pinを変更し、Automation数値型制約を追加。詳細は`PROVENANCE.md`参照。


---

## 7. Distributed Session 0.3の意味規則

# OSTF 5.0.0 — Distributed Session 0.3 正式規範仕様

**この版は2026-11-16正式採択4.3 Distributed Session0.2（SHA照合済）を元にした5.0版。** 規範Schema: `schema/ostf-distributed-session-0.3.schema.json`。Core/Production/Plugin Contextとは別のJSON文書。通信・WAN同期・音源・ロボットの実行権限を与えない。

## 文書識別・原本へのピン

`profile:"OSTF-Distributed-Session-0.3"`と`recordType:"snapshot"|"event"`を両文書で使用する。`profileVersion`やネストした`score`は**使用しない**。`sessionId`、`documentId`、`revisionId`、`performancePlanId`、`scoreSha256`（元Score5のraw UTF-8バイトSHA-256、64桁小文字）は共通必須。PlanはScore5の既存かつ有限な`performancePlans[]`を参照する。参照の同一性は外部に現物Scoreが存在してはじめて確認できる。

## Snapshot

`sessionStatus: prepared|playing|stopped`、`stateRevision`非負整数、`authorityParticipantId`、1件以上の`participants[]`が必須。各Participantは`participantId`, `kind:human|softwareAgent|physicalRobot`, `assignedTrackIds[]`を必須とする。`playing`には`position`必須、`prepared/stopped`では任意。`committedPhrases[]`、`commitmentWindow`は任意であり、既存の意味を継承。

`commitmentWindow`は`startPerformanceTick`と`endPerformanceTick`の半開区間で、`start<end`。窓を与える場合はplayingで`position`と`committedPhrases`が必須であり、**窓と交差する確定フレーズが全て含まれるという宣言**になる。不完全な窓に暗黙の`coverage:partial`を付けることは認めない。窓を省略して部分抜粋を保持できる。

## Event

`eventId`, `issuerParticipantId`, `baseStateRevision`, `effectivePerformanceTick`, `kind`, `payload`が必須。7種類：`phraseProposed`, `phraseCommitted`, `turnRequested`, `cueIssued`, `performanceObserved`, `participantStatus`, `sessionStateChanged`。`phraseCommitted`と`sessionStateChanged`では`resultStateRevision`が必須であり、受理時に必ず`base+1`。それ以外はこのフィールド禁止。イベント重複の冪等性、StateRevision競合・順序・権限は採択版0.2の意味を継承。

`phrase`は`representation:"midi1Notes"`, `durationTicks>0`, `notes[]`（pitch 0..127, velocity 1..127）の構造。確定フレーズは`commitEventId`で識別し、CoreのNotesへの自動編集や実DSP/ロボット制御ではない。

`sessionStateChanged.payload.changeKind`は`sessionStarted`, `visitChanged`, `assignmentChanged`, `sessionStopped`の4種類。時計Anchor (`position`: performancePlanId/visitId/sourceTick/performanceTick/clockDomainId/epochUtc/uncertaintyMs) は開始・Visit移動で必須。Assignment変更ではTrack集合のみ。Stopped後の同一Session再開は定義せず、別Sessionが必要。

## Score 5と旧0.2の分離

同名の意味を持つフィールドでも、正式0.2は4.3 Score専用、0.3は5.0 Score専用。4.3から5.0にScoreを改訂した時は新Sessionを明示的に作る。単に`profile`だけ差し替えたり、過去Eventの権限・参加者・clockを自動引き継いだりしない。Schema構造の妥当性は実ネットワーク・機材動作の証明ではない。

**過去の未公開草案からの修正履歴**：旧ネスト`score`、`participant.id`、`phrase.encoding`、`committedPhrase.eventId`、`commitmentWindow.coverage`を正式0.2由来のwireフィールドへ修正。旧草案例は新Schemaに対応した新しいExampleへ書き直した。


---

## 8. OSTFP：ZIP、資産、参照および安全対策

# OSTF Project Package 1.0 — OSTF 5.0用規範案（Draft 0.10）

## 1. 目的とファイル表現

OSTF TEXT（`.ostf`）は従来どおり独立したUTF-8 JSONの楽曲Scoreです。OSTF PROJECT（`.ostfp`）は、正本Scoreを**必ず1件**、制作／分散Session JSONや実体Assetを任意で同梱する**ZIP輸送形式**です。Scoreと制作情報の正本を混合しません。Project Directoryは同じ論理構造を持つ**展開・編集中のフォルダ表現**であり、第3の交換用拡張子ではありません。単なるPack/Unpackで元のScore等のバイト列を書き換えてはいけません。

## 2. ZIP構造と識別子

1. ZIP最初のメンバーは`mimetype`、圧縮方式`Stored`、内容はASCIIの`application/vnd.ostf-project+zip`**完全一致**（BOM・改行・空白なし）を必須とします。このメディアタイプは**提案上の未登録値**であり、IANA登録済みとは表記しません。
2. 2番目は暗号化されていないUTF-8 JSONの`manifest.json`です。構造は`schema/ostf-package-manifest-1.0.schema.json`に従います。
3. 残りはManifestで宣言したScore1件、任意のJSONとBinaryです。ZIPの`Stored`/`Deflate`およびZIP64を認めます。空ディレクトリエントリを必須とはせず、実体素材には数えません。暗号化されたZIPや実行可能ファイルのインストールを規格化しません。
4. 各パスはNFC正規化済みPOSIX相対パスです。絶対／ドライブパス、バックスラッシュ、`.`/`..`、制御文字、ルート脱出、予約名との衝突を禁止します。大文字小文字同一視による衝突も拒否します。Symlinkなどを使った展開先の迂回は拒否します。

受信アプリはZIPを信頼できない入力として扱い、重複名、Zip Slip、圧縮爆弾、巨大展開、パス衝突、Symlink経由の脱出や不完全保存を防ぎます。同梱`tools/ostfp.py`は独自上限を持つ参考試作であり、セキュリティ認証済み実装や共通上限値ではありません。

## 3. Manifestと原本SHA

必須キーは`packageFormat:"OSTFP"`、`packageVersion:"1.0.0"`、`projectId`、`title`、`score`、`documents[]`、`assets[]`、`bindings[]`です。

- `score`：`path`, `format:"OSTF"`, `version:"4.3.0"|"5.0.0"`, `sha256`。正本は必ず1件です。
- `documents[]`：`id/role/path/family/version/sha256`、任意`required`。各JSONは独立した正確な版で識別します。
- `assets[]`：`id/path/purpose/sha256/mediaType/sizeBytes`、任意の権利表示。`sizeBytes`は実体のバイト数です。
- `externalAssets[]`、`metadata`、`extensions`：任意・非権威の補助データです。

ハッシュはZIP圧縮後のバイトや整形JSONではなく、**各ファイルの非圧縮・元バイトSHA-256**です。Manifest自身は自己ハッシュしません。`mimetype`と`manifest.json`以外の全実体をScore、documents、assetsのいずれか**ちょうど一つ**に記載します。未記載・二重宣言・実体欠損は不正です。補助JSONを第2の正本Scoreにしてはいけません。

## 4. ScoreとProfileの組合せ

| Score | Production | Distributed | Manifest内のfamily/version |
|---|---|---|---|
| OSTF 4.3.0 | Production 0.2.0（任意） | Distributed 0.2（任意） | Production `OSTF-Production-Session` / `0.2.0`、Distributed `OSTF-Distributed-Session-0.2` / `0.2` |
| OSTF 5.0.0 | Production 0.3.0（任意） | Distributed 0.3（任意） | Production `OSTF-Production-Session` / `0.3.0`、Distributed `OSTF-Distributed-Session-0.3` / `0.3` |

Productionの本文は`profile`、`profileVersion`、`score.formatVersion`、`score.sha256`を実際のScoreと一致させます。任意の`score.documentId/revisionId`もScoreのDocument識別子と一致させます。Distributedの本文では`profile`、`recordType:"snapshot"|"event"`と、正しいScore/Plan参照を確認します。**Distributed 0.3にはネストした`score`オブジェクトも`profileVersion`も存在せず、ルートの`scoreSha256`、`documentId`、`revisionId`、`performancePlanId`を照合します。** これらは正本の実バイトSHA、Document、Revision、有限のPerformance Planに対応します。旧Distributed 0.2も採択された旧規範に従って照合します。旧SessionのVersionだけ置き換えて再利用してはいけません。

`documents[].role:"supplement"|"metadata"`はCore／Profileの正本権限を生みません。Plugin Contextメッセージを補助資料として保存しても編集実行権限にはなりません。

## 5. AssetのBinding

`bindings[]`は`(documentPath,resourceKind,resourceId)`から同梱された1件の`assets[].id`への対応です。`coreResource`は**正本Score**の`resources[].id`、`productionAsset`は**指定Production文書**の`assets[].id`（Plugin Stateを含む）に解決します。パスは参照文書の場所ではなく**Project Root基準**です。曖昧な重複Binding、存在しないID、実体SHAの矛盾、用途／MIMEの不一致を拒否します。**同梱のために元JSONのURIやScoreを変更しません。** `PACKAGE_BINDING_RULES.ja.md`も参照してください。

`externalAssets[]`は非同梱参照であり、HTTPSの自動取得・ファイル読取権限を与えません。参照があっても音声素材、プラグイン本体、ライセンス、実音再現が確保されたとは主張できません。

## 6. Project Directory・保存・部分Export

Project Directoryは`mimetype`と`manifest.json`、Manifestで宣言した実体を、`.ostfp`と同じルート相対パスで保持します。Pack/Unpackは元のScore/Profile/Assetバイトを保持します。ZIPメタデータ・圧縮結果のSHAまで同一にする必要はありません。保存では一時領域で全実体とManifestを構築して一貫した世代を公開することを推奨しますが、複数ファイルのOSレベル原子的保存は保証しません。Scoreを変更したら別ProfileのSHAを暗黙更新せず、明示的な再関連付け／新Sessionが必要です。Scoreだけの`.ostfp`は合法ですが、制作情報・音声実体を受領したのに省略した場合は「プロジェクト全体が無損失」と表現せずLossを報告します。`MIGRATION_MATRIX.ja.md`を参照してください。

## 7. 保証しない事項

構造Schema合格、参照意味の成立、元バイトの一致、ZIPの安全処理、DAW・プラグイン実機互換性は別の機能です。`.ostfp`は実行ファイル／音源インストーラー、認証済み遠隔Session、著作権許諾、音響レンダリング保証ではありません。実装は`CONFORMANCE.ja.md`で機能別の対応範囲を宣言します。


---

## 9. Plugin ContextとHost権限・編集・ACK

# OSTF Plugin Context Exchange 1.0 — 規範案（Draft 0.10）

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


---

## 10. 互換性・移行・Loss報告

# OSTF 4.3 ⇄ 5.0：移行・関連付け・情報損失規則（Draft 0.10）

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


---

## 11. 第三者開発者の能力別適合と制限

# OSTF 5.0 — 機能別適合宣言（Draft 0.10）

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


---

## 12. バージョン／文書ファミリーのレジストリ

# OSTF 5.0 — ファイル識別と提案識別子（Draft 0.10）

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


---

## 13. ファイルサンプルを使った実装の順序

1. `schema/ostf-5.0.0.schema.json`と`examples/score/*.ostf`で楽曲テキストの必須構造を確認します。
2. オーディオやプラグイン状態を扱う場合はProduction0.3のJSONと`examples/ostfp/`の素材を読みます。
3. AI・遠隔セッションではDistributed0.3のSnapshot/EventとScore SHA、改訂番号を対応付けます。
4. VST3/AU/CLAPはPlugin Contextの`context`と`editProposal`を区別し、Host権限がある場合のみScoreを改訂します。
5. `.ostfp` ZIPの`mimetype`、`manifest.json`、各メンバーの原本ハッシュを確認します。
6. 実行・再生・音色一致・プラグイン互換性は実装側の責任であり、本規格は一律に保証しません。
