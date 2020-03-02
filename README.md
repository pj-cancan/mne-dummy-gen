# 目次

* 変更点
* How to use
* 変数系定義

## 概要
ダミーデータ生成ツール  
Google map Direction APIを使用して車両情報を時系列で生成する

## 変更点(2018/05/17)

* python3に対応
* 必須オプション --apikeyを追加 
  * google-apiを呼び出すためのAPIキーを渡す
* 任意オプション --inervalを追加
  * データの生成単位を任意の秒単位に変更できるようになります
  * duration 60でinterval 10なら 6レコードが生成されます
* 任意オプション --filldownを追加
  * --intervalが１より大きい時が対象となります
  * この値がTrueの時は、生成されたデータは、次のデータ生成タイミングまで保持されます。
  * ただし、"drv_time"と"timestamp"は更新されます
  * duration 60でinterval 10でfilldown True なら 60レコードが生成され、
  * 10レコード毎に同じデータが設定されます


## google maps APIの取得
* Google Cloud Platform の Google Maps API から Direction API を有効にしてAPI Keyを作成しておく


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
                    [-n NONRANDOM] [-k APIKEY] [-i INTERVAL]

optional arguments:
  -h, --help            show this help message and exit  

  -d DURATION, --duration DURATION
                        sample duration(default = 10)

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
                        speed random facor(default = 0persent)

  -t TITLE, --title TITLE
                        vehicleID = title + sequential num(default = A)

  -p TIMESTAMP, --timestamp TIMESTAMP
                        start time(default = 2017/08/02 00:00:00)

  -e ENDLESS, --endless ENDLESS
                        loop among waypoints(default = False)

  -c COORDINATE, --coordinate COORDINATE
                        use coordinate file to make result

  -n NONRANDOM, --nonrandom NONRANDOM
                        if True, make route with all locations(default =
                        False)

  -k APIKEY, --apikey APIKEY
                        Directioni APIのキーを指定

  -i INTERVAL, --interval INTERVAL
                        データ生成インターバル(秒)を指定します(default = 1)

  -f FILLDOWN, --filldown FILLDOWN
                        データ生成インターバル時のデータの振りおろしを行います
```

## Example

### データ生成例1
 
- 刈谷市周辺を走行する，3時間(10800秒)のデータを400件生成。
- 平均速度は36km/h, 速度のランダムさは20%, 車両IDは"DEMO000000", 時間は2017/08/16 09:00:00から。
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
--timestanp "2017/08/16 09:00:00"
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
--timestanp "2017/08/16 09:00:00" \
--coordinate coordinates.json \
--timestanp "2017/08/16 09:00:00“
```

### データ生成例3

60秒間のデータを10秒毎にデータ出力する． 出力件数は6件となる

```
python dummy-gen.py \
--duration 60 \
--apikey xxxxxxx \
--interval 10
```

### データ生成例4

60秒間のデータのうち，10秒毎にデータ更新．その間のデータは前のデータを引き継ぐ．  
出力件数は60件となる

```
python  dummy-gen.py \
--duration 60 \
--apikey xxxxxxx \
--interval 10 \
--filldown True
```

### sample output

```
[
    {
        "v_id": "0", 
        "lat": 35.62636, 
        "lng": 139.7792279, 
        "drv_time": 2066, 
        "height": 0,
        "timestamp": "2017/08/02 00:12:37", 
        "spd": 10, 
        "acc_lv": 0, 
        "brk_lv": 0, 
        "steering": 0, 
        "wl_spd_fr": 100, 
        "wl_spd_fl": 100, 
        "wl_spd_rr": 100, 
        "wl_spd_rl": 100, 
        "curv": 0, 
        "diag": false, 
        "gas": 100, 
        "wl": 100, 
        "wl_air_fl": 100, 
        "wl_air_fr": 100, 
        "wl_air_rr": 100, 
        "wl_air_rl": 100, 
        "battery": 100, 
        "light": false, 
        "wiper": 1, 
        "passengers": 1, 
        "shift_type": "4"
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