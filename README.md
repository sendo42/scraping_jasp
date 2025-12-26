# やること

1,一通り動くようにする
2,input dirにあるファイルを全ていれる。
3,個別でいれてoutput dirに出力をする。
4,保存

while
{
    個別でいれる。
    output dirに出力する。
}

# 前処理

最初の前処理のコマンド、
cat Downloads/zzSCUSDT.csv | cut -d ' ' -f 2 > Downloads/test.csv

これでもいいけど、awkの方が便利かなあ
cat *.csv | awk -F" " '{print $2} > aiueo.csv

# クリックしてる場所と要素

## 解析 -> 

//*[@id="page_menu"]/li[2]/a

/html/body/div[3]/aside/section/ul/ul/li[2]/a


## データ入力の中のデータ選択 サンプルデータ

//*[@id="tab-9017-1"]/div[1]/div/div/div/div[1]
生成されるidはランダムになる。だから絶対パスで指定する必要がある。面倒だけど一つ一つ追えば必ず同じやつになるはず。

/html/body/div[3]/div/section/div/div/div[2]/div/div[1]/form/div/div/div[1]/div[1]/div/div/div/div[1]


## ファイル読み込み = CSVを選ぶ
/html/body/div[3]/div/section/div/div/div[2]/div/div[1]/form/div/div/div[1]/div[1]/div/div/div/div[2]


## 次へ

id
dataApply

## ファイルを選択

id
file1

## ファイルを送信

これはsend_keysってやつでイベントを発火させるしかない。

## Decomp 色々、ここでオプションとか指定できる
周期 id period1-selectized


## 実行ボタン （送ったデータをブラウザで読み込み）

id
do

## さらに実行ボタン (周期やトレンド時数を設定したもの)

id
run1



## プロットをダウンロード

id
downloadPDF1


