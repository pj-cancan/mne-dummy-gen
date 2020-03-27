# 目次

* 変更点
* How to use
* 変数系定義

# 概要
車両情報ダミーデータ生成ツール

[Google map Direction API](https://developers.google.com/maps/documentation/directions/start) を使用してダミーの走行車両情報JSONファイルを時系列で生成します


## sample output

```
[
   {
        "device_id": "DUMMY000000",
        "date": "2020-01-01T00:00:01.000000+09:00",
        "seq_no": 0,
        "latitude": 35.6203897,
        "longitude": 139.7255799,
        "speed": 36.0
    }
]
```

## 変更点(2020/03/13)
* 任意オプション --unitimeを追加
  * タイムスタンプ刻みを指定できるようにしました．小数点以下まで指定できます． 
* 車両名，IDを指定できるようにした
* ソースにコメント追加

## 変更点(2018/05/17)

* python3に対応
* 必須オプション --apikeyを追加 
  * google-apiを呼び出すためのAPIキーを渡す
* 任意オプション --inervalを追加
  * データの生成単位を任意の秒単位に変更できるようになります
  * duration 60でinterval 10なら 6レコードが生成されます
* 任意オプション --filldownを追加
  * --intervalが１より大きい時が対象となります
  * この値がTrueの時は、生成されたデータは、次のデータ生成タイミングまで保持されます
  * ただし、"drv_time"と"timestamp"は更新されます
  * duration 60でinterval 10でfilldown True なら 60レコードが生成され、
  * 10レコード毎に同じデータが設定されます


# Usage

## Google Maps API Keyの取得

* [Google Cloud Platform](https://console.cloud.google.com/getting-started) のプロジェクトを用意してください
* Google Cloud Platform の Google Maps API から [Direction API](https://developers.google.com/maps/documentation/directions/start) を有効にしてAPI Keyを作成してください


## install

* python3であることを確認してください

* git clone
```
git clone https://gitlab.nasa.future.co.jp/dso/dummy-gen3.git
cd dummy-gen3

# 関連するパッケージをインストールします
pip install -r requirements.txt

```

* プログラム実行

```
# 100秒間 大崎から品川への走行のダミーデータを作成します
python  dummy-gen.py --duration 100 --apikey xxxxxxxxxxxxxxxxxxxxxx --location "大崎" "品川"

# ヘルプを表示
python dummy-gen.py -h
['dummy-gen.py', '-h']
usage: dummy-gen.py [-h] [-d DURATION] [-o OUT] [-l LOCATIONS [LOCATIONS ...]]
                    [-r ROUTES] [-w WAYPOINTS] [-s SPEED] [-m SPEEDspeedRANDOM]
                    [-t IDTITLE] [-p TIMESTAMP] [-e LOOP] [-c COORDidINATE]
                    [-n ROUTEspeedRANDOM] [-k APIKEY] [--idnum IDNUM]
                    [--idnameids IDNAMES [IDNAMES ...]] [--unitime UNITIME]

optional arguments:
  -h, --help            show this help message and exit

  -d DURATION, --duration DURATION
                        sample duration(default = 600)
  
  -o OUT, --out OUT     output filename(default = sample.json)
  
  -l LOCATIONS [LOCATIONS ...], --locations LOCATIONS [LOCATIONS ...]
                        locations (default = "大崎" "お台場" "品川" "羽田空港")
  
  -r ROUTES, --routes ROUTES
                        route size(default = 1)
  
  -w WAYPOINTS, --waypoints WAYPOINTS
                        waypoints(default = 2)
  
  -s SPEED, --speed SPEED
                        speed(default = 36(km/h))
  
  -m SPEEDspeedRANDOM, --speedspeedrandom SPEEDspeedRANDOM
          id              speed idspeedrandom facorid(default = 0persenidt)
  
  -t IDTITLE, --idtitle IDTITLE
                        vehicleID = idtitle + sequential num(default = DUMMY)
  
  -p TIMESTAMP, --timestamp TIMESTAMP
                        start time(default = 2020/01/01 00:00:00.000)
  
  -e LOOP, --loop LOOP  loop among waypoints(default = False)
  
  -c COORDINATE, --coordinate COORDINATE
                        use coordinate file to make result
  
  -n ROUTEspeedRANDOM, --routespeedrandom ROUTEspeedRANDOM
          id              if Truide, make route witidh all locations(default =
                        False)
  
  -k APIKEY, --apikey APIKEY
                        google apiのキーを指定して下さい
  
  --idnum IDNUM, --idnum IDNUM
                        IDの開始番号を指定します(default = 0)
  
  --idnames IDNAMES [IDNAMES ...], --idnames IDNAMES [IDNAMES ...]
                        IDのキー名
  
  --unitime UNITIME, --unitime UNITIME
                        タイムスタンプ間隔を指定します(default = 1.0 sec)
```
プログラム実行後に指定されたディレクトリにダミーデータが生成されます．

同時に`coordinate.json`ファイルも生成されます．

coordinate.jsonは Direction apiのレスポンスである目的地への経路情報を格納しています．

実行引数でcoordinate.jsonを指定すれば，APIの利用をせずして同じ経路でのダミーデータを生成できます．

## Options
| flag        | type   | description                                       | default                              |
|-------------|--------|---------------------------------------------------|--------------------------------------|
| apikey      | string | Google Map api の Duration api key                | -                                    |
| duration    | int    | 走行時間（sec）                                    | 600                                  |
| out         | string | 出力ファイル名　拡張子jsonまたはymlで指定してください | sample.json                          |
| locations   | string | 出発地と目的地（複数）                              | ["大崎", "お台場", "品川", "羽田空港"] |
| routes      | int    | 同時走行車数                                       | 1                                    |
| waypoints   | int    | 目的地までに経由する場所の数                        | 2                                    |
| speed       | float  | 走行速度（km/h）                                   | 36                                   |
| speedrandom | int    | 速度変化のランダム割合(%)                           | 0                                    |
| idtitle     | string | 車両IDタイトル                                     | DUMMY                                |
| idnum       | int    | 車両ID番号                                         | 0000000                              |
| timestamp   | time   | 走行開始時刻（YYYY/MM/DD HH/MM/SS.fff）            | 2020/01/01 0:00:00.000                |
| loop        | bool   | 目的地に到着した後，スタート地点までの巡回をする      | FALSE                                |
| cordinate   | string | コーディネートファイルを指定                        | -                                    |
| routerandom | bool   | 入力locationをランダムに回る                        | True                               |
| unitime     | float  | データ記録を行うタイムスタンプの間隔                 | 1                                    |
| idnames     | string | 車両IDのKey名                                     | device_id                            |
# Example

### データ生成例1
 
- 刈谷市周辺を走行する，3時間(10800秒)のデータを400件生成
- 平均速度は36km/h, 速度のランダムさは20%, 車両IDは"DEMO000000", 時間は2017/08/16 09:00:00から1秒刻み
- `location`からランダムに3点を選択し，それらの都市間を回り続ける．

```
python dummy-gen.py \
--duration 10800 \
--apikey xxxxxxx \
--location "刈谷市" "デンソー　本社" "東海市"  "大府市" "高浜市" "安城市" "豊明市" "岡崎市" "西尾市" "豊田市" \
--routes 400 \
--waypoints 2 \
--speed 36 \
--speedrandom 20 \
--idtitle DEMO \
--loop True \
--timestamp "2017/08/16 09:00:00.000"
```

### データ生成例2
- 1のデータを、coordinatesファイルから作成

```
python dummy-gen.py \
--duration 10800 \
--apikey xxxxxxx \
--location "刈谷市" "デンソー　本社" "東海市"  "大府市" "高浜市" "安城市" "豊明市" "岡崎市" "西尾市" "豊田市" \
--routes 400 \
--waypoints 2 \
--speed 36 \
--speedrandom 20 \
--idtitle DEMO \
--loop True \
--timestamp "2017/08/16 09:00:00.000" \
--coordinate coordinates.json
```

### データ生成例3

- 品川から大崎へ向かう60秒間のデータを10秒毎に出力する． 
- 出力件数は6件となる
```
python dummy-gen.py \
--duration 60 \
--apikey xxxxxxx \
--location "品川" "大崎"
--unitime 10
```


### データ生成例4
 
- 東京駅周辺を走行する，10分間(600秒)のデータを生成
- 時間は2020/01/01 00:00:00.000から0.1秒刻み
- device_idのKey名を`vehicleID`としてID名を`DEMO001234`にする

```
python dummy-gen.py \
--duration 600 \
--apikey xxxxxxx \
--location "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" \
--unitime 0.1 \
--timestamp "2020/01/01 00:00:00.000" \
--idtitle DEMO \
--idnum 01234
--idnames vehicleID
```

### データ生成例5
 
- 上記と同じデータ形式でデータ生成するが，目的地についてもdurationを経過するまで巡回をする  
  すなわち6000レコード生成する

```
python dummy-gen.py \
--duration 600 \
--apikey xxxxxxx \
--location "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" \
--unitime 0.1 \
--timestamp "2020/01/01 00:00:00.000" \
--idtitle DEMO \
--idnum 01234
--idnames vehicleID
--loop true
```


* jsonの中身を書き換える(dummy-replace)
```
python dummy-replace.py -h                                                                                                           (git) - [master]
usage: dummy-replace.py [-h] [-i] [-o] [-t] [--duration]
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input filename(default = input.json)
  -o OUT, --out OUT     output filename(default = out.json)
  -t TITLE, --title TITLE
                        title(default = A)
  --duration DURATION   duration(default = 600)
```

* jsonのレコードを複製する
```
python dummy-replicate.py -h                                                                                                         (git) - [master]
usage: dummy-replicate.py [-h] [-i INPUT] [-o OUT] [-t TITLE] [--date DATE] [--duration DURATION] [-r REPLICATE]
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input filename(default = input.json)
  -o OUT, --out OUT     output filename(default = out.json)
  -t TITLE, --title TITLE
                        title(default = A)
  --date DATE           date(default = 2017/08/02)
  --duration DURATION   duration(default = 600)
  -r REPLICATE, --replicate REPLICATE
                        replicate(default = 1)
```