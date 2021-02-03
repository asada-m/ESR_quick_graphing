# ESR_quick_graphing Readme
Quick graphing for ESR data  

ESRスペクトルを50秒以内に作図するプログラム  
ver.1.06 (2021/02/03)

・BrukerのESRデータを素早く作図するのに特化したプログラムです。  
・Matlab easyspin の eprload 関数を参考に作成しています。

★このプログラムはあくまで測定データの確認用です！  
★論文用の図はちゃんとしたグラフソフトで、  
　計算に使用する値をよく確認して作成することをおすすめします！！  

### ■インストール方法
１．Python3.8以降(64bit)をダウンロードしてください。パスを追加すると便利です。  
２．コマンドプロンプトで下記コマンドを実行して、必要なモジュールをインストールしてください。  

python -m pip install  
python -m pip install numpy  
python -m pip install matplotlib  
python -m pip install PySimpleGUI  

３．ESR_graph_main.py　を実行すると起動します。  
４．exeファイルを作成したい場合は、PyInstallerを別途使ってパッケージしてください。  
(matplotlibのバージョンが新しいとexe化に失敗してしまうので、3.2.2を使ってください)  
実行ファイルは数十MBくらいのサイズになります。  

python -m pip install PyInstaller  
pip install matplotlib==3.2.2  
pyinstaller -wF ESR_graph_main.py  

・exeファイルはdistフォルダ内に作成されます。  
・exeは単体で動作できますが、同じフォルダにいくつかファイルを出力するので、  
　置き場所にご注意ください。  
・Windows以外のOSで使いたい場合は、それぞれの環境でexeを作成してください。  

### ■作図可能なデータの種類
・Bruker BES3T  
・拡張子.datのASCIIデータ  
  
### ■今後追加したい機能
・2D sliceモード  
・列数の異なるdatデータをプロットすると強制終了するのを修正したい  
・軸単位変換  

### ■今のところ追加予定のない機能
・par,spc形式のデータの取り扱い  
　→　datに変換してから作図してください。  
・むずかしい作図設定  
　→　スクリプトを改造するか、別の作図ソフトウェアを使用してください。  
  
### ■更新履歴
ver.0.1 (2021/01/12)   - 1D データを作図できる最低限の機能  
ver.0.2 (2021/01/12)   - オプションを保存できるようになった  
ver.0.3-0.5   - カンブリア爆発  
ver.1.0 (2021/01/17)   - 公開版 Imaginary以外のDTAデータはだいたい作図可能  
ver.1.02 (2021/01/17)   - link修正、ソースファイルの日本語でエラーが出る？？のでASCIIに変更  
ver.1.03 (2021/01/18)   - datが表示できなかったのを修正  
ver.1.04 (2021/01/19)   - exe化が全然うまくいってなかったのを修正  
ver.1.05 (2021/01/26)   - Imaginary、複数列dat、キャプション位置調整、Normalize計算修正  
ver.1.06 (2021/02/03)   - 便利機能をいろいろ追加  

### ■使用ソフトウェア
Python  
Numpy  
PySimpleGUI  
Matplotlib  

### ■Licences
MIT licence  
Copyright © 2021 AsadaMizue; All Rights Reserved  
