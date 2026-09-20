# Tap on KOTOBA — 大きな文字で遊ぶ、四字熟語・ことわざの穴うめパズル

インストール不要・通信なし・依存ライブラリなしのことばパズルです。
`app/index.html` をブラウザで開くだけで遊べます。ファイルをローカルに置いたまま（`file://`）でも、
静的ホスティングに置いても動きます。

- 紹介ページ: <https://pikaring.github.io/tap-on-kotoba/>
- ゲーム本体: <https://pikaring.github.io/tap-on-kotoba/app/>
- 1 ファイル版: [`app/standalone.html`](app/standalone.html)（約 35 KB。これ 1 つで配布できます）

「一石□鳥」「棚から□」の□に入ることばを、4 つのタイルから選びます。全 100 問
（四字熟語 50 問・ことわざ 50 問）から毎回 10 問。**高齢の方が遊ぶことを前提**に、
画面いっぱいの大きな文字、タップだけの操作、時間制限も減点もない進行にしています。

名前は、タップ（tap）するだけで遊べることば（KOTOBA）のパズルだから。
アイコンは選択肢のタイルと、空欄の「？」です。

## English

**Tap on KOTOBA** is a Japanese word puzzle that runs entirely in the browser.
No install, no sign-up, no network traffic, no dependencies. Open `app/index.html` and play,
or grab the single-file build `app/standalone.html` (~35 KB) and play offline.

- Play now: <https://pikaring.github.io/tap-on-kotoba/app/>
- Fill the blank in a four-character idiom (四字熟語) or a proverb (ことわざ) by tapping one of four tiles.
- 100 questions (50 idioms, 50 proverbs); 10 random ones per round. Reading and meaning are shown after each correct answer.
- Built for older players: type scales with the viewport (up to 96px), tap-only input, no timer, no penalty, no game over.
- Works in both landscape and portrait; the layout switches when you rotate the device.
- The UI and all content are in Japanese.

```
tap-on-kotoba/
├── index.html        紹介ページ（GitHub Pages のトップ）
├── assets/           紹介ページ用（site.css・アイコン・OGP画像）
├── make_icon.py      アイコンの生成スクリプト
├── make_og.py        OGP画像の生成スクリプト
└── app/              ゲーム本体（ここが実体）
    ├── index.html        これを開く
    ├── questions.js      問題データ（100問）
    ├── standalone.html   1 ファイル版（build.js が生成）
    └── build.js          index.html に JS を埋め込むビルドスクリプト
```

## 遊び方

1 問ごとに 1 か所が空欄になっています。下に並ぶ 4 つのタイルから、当てはまることばをタップします。

- **時間制限なし・減点なし**。間違えたタイルには ✕ が付き、何度でも選び直せます
- 正解すると読みと意味を大きな文字で表示し、「つぎへ」で次の問題へ
- 「ヒント」で選択肢を 2 つに絞れます（1 問 1 回）
- 上部の帯が進み具合。一度で正解した問題は緑、選び直した問題は黄色
- 「♪ 音あり / 音なし」で効果音を切り替え（音が出せない端末では自動的に無効）
- 最後に「一度で正解した数」を★で表示。順位も記録も残しません

## 高齢者向けに意図した設計

| 項目 | 方針 |
|---|---|
| 操作 | **タップのみ**。ドラッグ&ドロップは指が離れて失敗しやすいため使わない |
| 書体 | ゴシック体。`Meiryo`（メイリオ）を先頭に、iOS/Mac は ヒラギノ角ゴ、Android は Noto Sans JP、新しい Windows は 游ゴシックへ順に落ちる。Web フォントは読み込まないのでオフラインでも同じ見た目 |
| 文字の大きさ | 画面の高さ・幅に比例（`clamp` + はみ出し時の自動縮小）。問題文は横向きで約 57〜80px、縦向きで約 58〜96px。正解後の意味の文は 22〜37px |
| 画面構成 | `100dvh` に収めスクロールなし。1 画面 1 タスク |
| 横向き | 問題は 1 行に収め、選択肢は横一列に 4 つ。正解後は意味の文とボタンを左右に並べる |
| 縦向き | 問題は折り返して大きく表示し、選択肢は 2×2。正解後は意味の文の下に幅いっぱいのボタン |
| タップ領域 | 選択肢タイルは高さ 54px 以上（縦向きは 64px 以上）。指の届く画面下部に配置 |
| 失敗の扱い | ペナルティ・時間切れ・ゲームオーバーなし。「おしい！もう一度」だけ |
| 色 | 本文のコントラスト比 15:1 以上。正誤は色に加えて ○ / ✕ の記号でも示す |
| その他 | ピンチズーム可（`user-scalable` を止めていない）、セーフエリア対応、`prefers-reduced-motion` 対応 |

## 問題の追加・変更

`app/questions.js` の `QUESTIONS` 配列に足すだけです（現在 100 問）。

```js
{ t:"k",                       // "y"=四字熟語 / "k"=ことわざ（見出しの表示が変わる）
  q:"猿も_から落ちる",          // "_" が空欄の位置
  a:"木",                      // 正解
  c:["木","枝","山","屋根"],    // 選択肢4つ（正解を含む。表示順はシャッフルされる）
  yomi:"さるも きからおちる",
  imi:"どんな名人でも、ときには失敗することがある。" }
```

選択肢は 4 つ前提（横向きは 1 列に 4 つ、縦向きは 2×2）。増やす場合は `app/index.html` の
`.choices` の `grid-template-columns` も調整してください。1 回の出題数は同ファイルの
`PER_GAME`（既定 10）で変えられます。

問題を足したら 1 ファイル版を作り直します。

```sh
cd app && node build.js      # → app/standalone.html
```

## ローカルで動かす

```sh
cd tap-on-kotoba
python3 -m http.server 8000   # http://localhost:8000/     … 紹介ページ
                              # http://localhost:8000/app/ … ゲーム本体
```

`file://` で `app/index.html` を直接開いても動きます。

## 公開する（GitHub Pages）

ビルド不要の静的サイトなので、このリポジトリをそのまま公開できます。
Settings → Pages → Source を「Deploy from a branch」、Branch を `main` / `/ (root)` に設定します。

## アイコン・OGP画像の作り直し

```sh
pip install Pillow
python3 make_icon.py   # → assets/icon.png, assets/favicon.ico, icon_preview.png（確認用）
python3 make_og.py     # → assets/og.png
```

日本語フォントは Windows（メイリオ等）→ Linux（IPAゴシック等）の順に探します。

## 動作確認

Playwright で 6 サイズ（横向き 844×390 / 667×375 / 1024×600、縦向き 390×844 /
360×640 / 768×1024）について、縦横スクロールが発生しないこと・問題文と選択肢が
枠からはみ出さないこと・最も長い解説を表示しても画面が押し出されないこと・
1 問の正誤〜結果画面まで進めること・JS エラーが出ないことを確認しています。

あわせて全 100 問を 1 問ずつ実際に描画し、問題文の重複がないこと、選択肢が 4 つで
重複がなく正解を含むこと、空欄が 1 つであること、自動縮小がかかっても文字が小さく
なりすぎないこと（最も長い「井の中の蛙□を知らず」でも横 844×390 で 70px、
横 667×375 で 57px）を確認しています。

## ライセンス

MIT License。問題文・解説文を含め、自由に使えます。
公民館・デイサービス・学校などでの利用もどうぞ。
