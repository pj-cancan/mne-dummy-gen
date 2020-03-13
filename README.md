# 目次

* 変更点
* How to use
* 変数系定義

## 概要
ダミーデータ生成ツール  
[Google map Direction API](https://developers.google.com/maps/documentation/directions/start) を使用してダミーの車両情報を時系列で生成する

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


## google maps APIの取得
* Google Cloud Platform のプロジェクトを作成しておく
* Google Cloud Platform の Google Maps API から Direction API を有効にしてAPI Keyを作成


## How to use

* python3であることを確認してください

* git clone
```
git clone https://gitlab.nasa.future.co.jp/dso/dummy-gen3.git
cd dummy-gen3

# 関連するパッケージをインストールする
pip install -r requirements.txt

```

* ルートを決める

``` dummy-gen.py
# [[出発地,目的地],]
def execute():
    locations = [["大崎","お台場"],["品川","羽田空港"]]
```

* プログラム実行

```
# 100秒 * ルート分のダミーデータを作成する
python  dummy-gen.py --duration 100 --apikey xxxxxxxxxxxxxxxxxxxxxx

# ヘルプを表示
python dummy-gen.py -h
usage: dummy-gen.py [-h] [-d DURATION] [-o OUT] [-l LOCATIONS [LOCATIONS ...]]
                    [-r ROUTES] [-w WAYPOINTS] [-s SPEED] [-m RANDOM]
                    [-t TITLE] [-p TIMESTAMP] [-e ENDLESS] [-c COORDINATE]
                    [-n NONRANDOM] [-k APIKEY] [-i INTERVAL] [-f FILLDOWN]
                    [--idoffset IDOFFSET] [--idnames IDNAMES [IDNAMES ...]]
                    [--unitime UNITIME]

optional arguments:
  -h, --help            show this help message and exit  

  -d DURATION, --duration DURATION
                        Driving time(sec) (default = 600 sec)

  -o OUT, --out OUT     output filename(default = sample.json)
                        .yaml or .json can be specified  

  -l LOCATIONS [LOCATIONS ...], --locations LOCATIONS [LOCATIONS ...]
                        locations (default = "大崎" "お台場" "品川" "羽田空港")

  -r ROUTES, --routes ROUTES
                        route size(default = 2)

  -w WAYPOINTS, --waypoints WAYPOINTS
                        waypoints(default = 5)

  -s SPEED, --speed SPEED
                        speed(default = 36(km/h))

  -m RANDOM, --random RANDOM
                        Speed ​​change random rate(default = 0persent)

  -t TITLE, --title TITLE
                        vehicleID = title + sequential num(default = A)

  -p TIMESTAMP, --timestamp TIMESTAMP
                        start time(default = 2020/01/01 00:00:00.000000)

  -e ENDLESS, --endless ENDLESS
                        loop among waypoints(default = False)

  -c COORDINATE, --coordinate COORDINATE
                        use coordinate file to make result

  -n NONRANDOM, --nonrandom NONRANDOM
                        if True, make route with all locations(default = False)

  -k APIKEY, --apikey APIKEY
                        Directioni APIのキーを指定

  -i INTERVAL, --interval INTERVAL
                        データ生成インターバルを指定します(default = 1)

  -f FILLDOWN, --filldown FILLDOWN
                        データ生成インターバル時のデータの振りおろしを行います

  --idoffset, IDOFFSET  
                        車両IDの番号を指定します(default = 0)

  --idnames, IDNAMES
                        車両ID名を指定します(default = ["device_id"]) 複数のID名を付けられます

  --unitime, UNITIME
                        タイムスタンプ間隔を指定します(default = 1.0 sec)
```

## Example

### データ生成例1
 
- 刈谷市周辺を走行する，3時間(10800秒)のデータを400件生成
- 平均速度は36km/h, 速度のランダムさは20%, 車両IDは"DEMO000000", 時間は2017/08/16 09:00:00から
- `location`からランダムに3点を選択し，それらの都市間を回り続ける．

```
python dummy-gen.py \
--duration 10800 \
--apikey xxxxxxx \
--location "刈谷市" "デンソー　本社" "東海市"  "大府市" "高浜市" "安城市" "豊明市" "岡崎市" "西尾市" "豊田市" \
--routes 400 \
--waypoints 2 \
--speed 36 \
--random 20 \
--title DEMO \
--endless True \
--timestamp "2017/08/16 09:00:00"
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
--random 20 \
--title DEMO \
--endless True \
--timestamp "2017/08/16 09:00:00" \
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
--interval 10
```

### データ生成例4

品川から大崎へ向かう60秒間のデータのうち，10秒毎にデータ更新．その間のデータは前のデータを引き継ぐ．  
出力件数は60件となる

```
python  dummy-gen.py \
--duration 60 \
--apikey xxxxxxx \
--location "品川" "大崎"
--interval 10 \
--filldown True
```

### データ生成例5
 
- 東京駅周辺を走行する，10分間(600秒)のデータを生成
- 時間は2020/01/01 00:00:00.000から0.1秒刻み
- device_idは`DEMO01234`

```
python dummy-gen.py \
--duration 600 \
--apikey xxxxxxx \
--location "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" \
--routes 1 \
--waypoints 4 \
--endless True \
--unitime 0.1 \
--timestamp "2020/01/01 00:00:00.000" \
--title DEMO \
--idoffset 01234
```

### sample output

```
[
    {
       "device_id": "A000001",
        "date": "2020-01-01T00:00:00.100000+09:00",
        "latitude": 35.6746554,
        "longitude": 139.7620339,
        "speed": 35.52413667069178,
        "direction": 167.1427506900309,
        "emergency_cd": "0",
    },
]
```

## 変数系定義

* 車両系定数
```
curvature = 0
diag = False
gas = 100
wheel_air_fr = 100
wheel_air_fl = 100
wheel_air_rr = 100
wheel_air_rl = 100
wheel_speed_fr = 100
wheel_speed_fl = 100
wheel_speed_rr = 100
wheel_speed_rl = 100
battery = 100
light = False
wiper = False
passengers = 1
# シフト情報
shift_type = "4"
```

* 車両系変数
```
# m/s
speed = 10
# brake (0 - 100)
brake_level = 0
# 加速レベル (0 - 100)
acceleration_level = 0
brake_level = 0
steering = 0
wheel_speed_fr = 100
wheel_speed_fl = 100
wheel_speed_rr = 100
wheel_speed_rl = 100
# 運転時間(秒)
driving_time = 0
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