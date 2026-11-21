# Open Song Timeline Format (OSTF) 5.0.0 — 正式公開版

**規格バージョン：5.0.0／2026年11月22日**  
**2形式：OSTF TEXT（`.ostf`）とOSTF PROJECT（`.ostfp`）**

OSTFは作曲、コード進行、メロディ、MIDI、歌詞、歌唱、演奏表現などをテキストで共有するためのオープン規格です。5.0では**4.3の音楽Coreをそのまま継承**しつつ、音声素材・プラグイン状態などをまとめてやり取りするプロジェクトZIP形式を正式に追加します。サードパーティー製DAW、VST3・AU・CLAP、Max for Live、AI作曲ソフトは**必要な機能だけ**実装できます。

## ファイル形式

- **`.ostf`／OSTF TEXT**：BOMなしUTF-8のJSONテキスト。AIとの貼り付け・編集・音楽情報交換に適しています。音声を必須としません。
- **`.ostfp`／OSTF PROJECT**：1曲のScore、任意のProduction/Distributed JSON、オーディオ・プリセット等を`manifest.json`と一緒に格納するZIP。解凍すればOSTF TEXTを元のバイト列のまま取り出せます。
- **制作中のフォルダ形式**：OSTFPと同じメンバー構造を展開して使える表現。別の必須拡張子は追加しません。

## 完全なマニュアルとリファレンス

- **[全網羅マニュアル（日本語）](docs/COMPLETE_MANUAL.ja.md)**：音楽Core、Production、Distributed、OSTFP、Plugin Contextを一冊に収録。
- **[全網羅パラメーターリファレンス（日本語）](docs/PARAMETER_REFERENCE.ja.md)**：現行Schemaの**1,601構造宣言**と旧Core意味規則・5.0差分。
- [英語・全網羅マニュアル](docs/COMPLETE_MANUAL.md)／[英語・全網羅リファレンス](docs/PARAMETER_REFERENCE.md)
- [正式仕様](docs/SPECIFICATION.ja.md)／[OSTFP仕様](docs/PACKAGE_SPECIFICATION.ja.md)／[VST等プラグイン連携](docs/PLUGIN_EXCHANGE_PROTOCOL.ja.md)
- [Production Session](docs/PRODUCTION_SESSION_0_3.ja.md)／[Distributed Session](docs/DISTRIBUTED_SESSION_0_3_SPECIFICATION.ja.md)
- [4.3互換・移行](docs/MIGRATION_MATRIX.ja.md)／[サードパーティー適合](docs/CONFORMANCE.ja.md)／[安全性](docs/SECURITY.ja.md)

## 全網羅サンプル

- [`examples/score/`](examples/score/)：**25件の`.ostf`**。最小構造、ジャズ、テクノ、ギター、AABA、歌唱、複数声部、フレーズ、AI向け演奏指示など。
- [`examples/ostfp/`](examples/ostfp/)：**11件の`.ostfp`**。音声素材、録音Session、架空のプラグイン状態、分散Session、旧4.3互換、制作・分散同梱など。
- `examples/production/`、`examples/distributed/`、`examples/plugin/`：制作・共同演奏・プラグイン読取／編集提案のJSON例。
- **[全サンプルの機能別一覧](docs/EXAMPLES_GUIDE.ja.md)**。

## 開発者の使い方

```bash
python -m pip install jsonschema
python tools/validate_examples.py
python tools/ostfp.py validate examples/ostfp/11-combined-production-distributed.ostfp
```

ZIPのSchemaとSHAを確認する静的ツールを同梱。**動作検証・独立DAW/VST3/AU/CLAP/M4L実装検証・実機オーディオ再現性・個別承認は、今回の文書リリース条件から除外**しました。これらを実施済み・合格済みとは記載しません。JSONの有効性が第三者プラグインや素材の利用権限を与えることもありません。

## 既存規格との互換性

4.3のScore・Production 0.2・Distributed 0.2を元の版のまま参照・保管できます。Production 0.3はScore5の原本SHAを参照し、Distributed 0.3は別文書として状態・Revision・Sessionを管理します。プラグインの`editProposal`は未信頼の提案であり、Hostによる実保存成功後でなければ`applied`とはなりません。

規格文章・自作サンプルのライセンスはCC0、参考ツールのコードはMITです。ライセンス範囲は[LICENSE-POLICY](LICENSE-POLICY.md)と[NOTICE](NOTICE.md)、継承元は[PROVENANCE](docs/PROVENANCE.md)を参照してください。未登録のパッケージMIMEとSchema URIには登録・配信保証はありません。

**本ZIPはGitHubへアップロードできる正式仕様の配布物です。** GitHubへの実際のアップロード・Release Tagの作成は別操作です。
