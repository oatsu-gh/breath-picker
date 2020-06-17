# breath picker

 歌唱DBからブレス音声を切り出す



## 開発環境

Window10 Education 2004, Python3.8.3



## 使用ライブラリ

- Pydub（標準ライブラリだと思う。たぶん。）

- [utaupy](https://github.com/oatsu-gh/utaupy)（UTAUや歌唱データベース用の自作ライブラリです。）

## 使い方

- PowerShellとかから `python breath_picker.py` で起動してがんばってください。切り出したファイルは (currentdirectory)/out 以下に保存されます。 
- 「東北きりたん歌唱データベース」形式のモノフォンラベルは、[こちら](https://github.com/oatsu-gh/oto2lab/blob/master/tool/convert_label_time_unit.py)のツールで単位換算してから本ツールで使ってください。
- 歌唱データベースの音声そのものをDTMなどの素材として使うことは、規約で制限されていることが多いです。
- 本ツールで生成したファイルをDTMなどに使いたい場合は、各歌唱データベースの規約に準拠しているか必ず確認してください。きりたんはNGだと思います。
