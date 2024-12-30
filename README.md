# Hypershade_FileTool_v1.2  
  
  
このスクリプトはテクスチャのリロードをワンタッチでできるようにするために作ったのが始まりです。  
アップデートで新たな機能を追加しました。
難しい機能はないため、感覚で使えれると思います。
  
  
《ダウンロード》  
CodeをクリックしてDownload ZIPからダウンロードできます。  

《アップデート》  
新しい「Hypershade_FileTool」フォルダーと「Hypershade_FileTool_im.py」のファイルを上書き保存するだけです。  　
  
  
《主な機能》  
【Hypershade_FileTool.py】  
・選択したテクスチャを再読み込み  
・全てのテクスチャを再読み込み  
・テクスチャのプレビュー表示  
・読み込み先フォルダ開く  
・トゥーンマテリアルノードを生成  
  
【Hypershade_materialTool.py】  
・選択したマテリアルをリストに追加します。  
・リストのマテリアルを選択した状態で「リストで選択しているマテリアルをHypershadeで選択」を  
クリックすると、選択したマテリアルが選択された状態でHypershadeが起動します。  
・選択しているメッシュまたはフェイスを一時保存してリストで選択しているマテリアルを適用できます。  
1.選択しているメッシュまたはフェイスを保存 → 2.メッシュまたはフェイスにリストで選択しているマテリアルを適用  
の順番でボタンをクリックします。  

・マテリアルを新たに作成して適用できます。また色も設定できます。  
  
《更新内容》  
「Hypershade_FileTool.py」のテクスチャのプレビュー表示のコードの  
「cmds.iconTextButton」から「cmds.image」に変更しました。  


「Hypershade_materialTool.py」に  
・開いたscene名.iniでマテリアルの名前リストが「userdata」フォルダに保存され  
開いたscene名とiniファイル名が同じファイルがロードされる機能が追加されました。  
これにより、それぞれのsceneで追加したマテリアル名を表示することができるようになりました。  
また、iniファイルをユーザーが選んでロードすることもできます。  
・選択したオブジェクトからマテリアル名を取得してリストに追加する機能を追加しました。  
・選択項目の分離機能も追加しました。  
  
  
《導入方法》  
英語版をお使いの方は「Hypershade_FileTool」のフォルダーと「Hypershade_FileTool_in.py」を  
"C:\Users\{名前}\Documents\maya\2023\scripts"に入れてください。  
ファイル名を指定して実行で
```
%USERPROFILE%\Documents\maya\2023\scripts
```
を入力すると一発でフォルダーが開きます。  
Mayaのスプリクトエディターを起動して「Hypershade_FileTool_in.py」登録して実行するとGUIが表示されます。  
  
日本語版の方は"C:\Users\{名前}\Documents\maya\2023\ja_JP\scripts"に入れると起動できるはずです。  

  
《使い方》  
起動するとファイル(File)テクスチャノードを読み込みます。  
ない場合は"Fileノードがありません"と表示されます。  
おまけの中に「Hypershade_materialTool」と「Toon auto-create tool」のボタンがあります。  
  
作成:mirumoru,GPT-4o  
※AIを使用して作成いています。  
  
トゥーンマテリアルノード[参考先](https://x.com/tajiman_vrc/status/1568527678554406913)  
  
  
《更新履歴》  
2024年10月5日 v1.0(配布用) 公開  
2024年11月4日 v1.1(配布用) 公開  
2024年12月30日 v1.2(配布用) 公開  
―――――――――――――――――――――――――――――――  
《License》  
Copyright (c) 2024 mirumoru  
Released under the MIT license  
https://opensource.org/licenses/mit-license.php  
