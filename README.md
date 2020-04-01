# Abstruct
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

## Run

```
# 100秒間 大崎から品川への走行のダミーデータを作成します
python  dummy-gen.py --duration 100 --apikey xxxxxxxxxxxxxxxxxxxxxx --location "大崎" "品川"

# ヘルプを表示
python dummy-gen.py -h
['dummy-gen.py', '-h']
usage: dummy-gen.py [-h] [-d DURATION] [-o OUT]
                    [-lo LOCATIONS [LOCATIONS ...]] [-r ROUTES] [-w WAYPOINTS]
                    [-s SPEED] [-sr SPEEDRANDOM] [--idtitle IDTITLE]
                    [-t TIMESTAMP] [-lp LOOP] [-rr ROUTERANDOM] [-k APIKEY]
                    [--idnum IDNUM] [--idnames IDNAMES [IDNAMES ...]]
                    [-u UNITIME]

optional arguments:
  -h, --help            show this help message and exit
  -d DURATION, --duration DURATION
                        sample duration(default = 600)
  -o OUT, --out OUT     output filename(default = sample.json)
  -lo LOCATIONS [LOCATIONS ...], --locations LOCATIONS [LOCATIONS ...]
                        locations (default = "大崎" "お台場" "品川" "羽田空港")
  -r ROUTES, --routes ROUTES
                        route size(default = 1)
  -w WAYPOINTS, --waypoints WAYPOINTS
                        waypoints(default = 2)
  -s SPEED, --speed SPEED
                        speed(default = 36(km/h))
  -sr SPEEDRANDOM, --speedrandom SPEEDRANDOM
                        speed random facor(default = 0persent)
  --idtitle IDTITLE, --idtitle IDTITLE
                        device_id = idtitle + sequential num(default = DUMMY)
  -t TIMESTAMP, --timestamp TIMESTAMP
                        start time(default = 2020/01/01 00:00:00.000)
  -lp LOOP, --loop LOOP
                        loop among waypoints(default = False)
  -rr ROUTERANDOM, --routerandom ROUTERANDOM
                        if True, make route with all locations(default =
                        False)
  -k APIKEY, --apikey APIKEY
                        Google Duration APIのキーを指定して下さい
  --idnum IDNUM, --idnum IDNUM
                        IDの開始番号(default = 0)
  --idnames IDNAMES [IDNAMES ...], --idnames IDNAMES [IDNAMES ...]
                        IDのキー名 スペース区切りで複数指定できます
  -u UNITIME, --unitime UNITIME
                        タイムスタンプ間隔を指定します(default = 1.0 sec)
```


## Options
| flag        | type   | description                                                    | default                              |
|-------------|--------|----------------------------------------------------------------|--------------------------------------|
| apikey      | string | Google Map api の Duration api key                             | -                                    |
| duration    | int    | 走行時間（sec）                                                 | 600                                  |
| out         | string | 出力ファイル名　拡張子jsonまたはymlで指定してください              | sample.json                          |
| locations   | string | 出発地と目的地（複数）                                           | ["大崎", "お台場", "品川", "羽田空港"] |
| routes      | int    | 同時走行車数                                                    | 1                                    |
| waypoints   | int    | 目的地までに経由する場所の数                                      | 2                                    |
| speed       | float  | 走行速度（km/h）                                                | 36                                   |
| speedrandom | int    | 速度変化のランダム割合(%)                                        | 0                                    |
| idtitle     | string | 車両IDタイトル                                                  | DUMMY                                |
| idnum       | int    | 車両ID番号                                                      | 0000000                              |
| timestamp   | time   | 走行開始時刻（YYYY/MM/DD HH/MM/SS.fff）                          | 2020/01/01 0:00:00.000               |
| loop        | bool   | 目的地に到着した時点で終了する　Trueの場合，出発地と目的地を往復する | False                                |
| routerandom | bool   | 入力locationをランダムに回る                                     | True                                 |
| unitime     | float  | データ記録を行うタイムスタンプの間隔(sec)                         | 1                                    |
| idnames     | string | 車両IDのKey名                                                   | device_id                            |

# Example

## データ生成例1
 
- 東京周辺を走行する，1時間(3600秒)のデータを5件生成
- 平均速度は36km/h, 速度のランダムさは20%, 車両IDは"DEMO000000", 時間は2017/08/16 09:00:00から1秒刻み
- `location`からランダムに3点を選択し，それらの都市間を回り続ける．

```
python dummy-gen.py \
--duration 3600 \
--apikey xxxxxxx \
--location "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" \
--routes 5 \
--unitime 1 \
--waypoints 2 \
--speed 36 \
--speedrandom 20 \
--idtitle DEMO \
--loop True \
--timestamp "2017/08/16 09:00:00.000"
```

### Output
```
{
        "device_id": "DEMO000000",
        "date": "2017-08-16T09:00:01.000000+09:00",
        "seq_no": 0,
        "latitude": 34.9551073,
        "longitude": 137.1731918,
        "speed": 39.966776630358495
}
```


## データ生成例2

- 品川から大崎へ向かう60秒間のデータを10秒毎に出力する． 
- 出力件数は6件となる
```
python dummy-gen.py \
--duration 60 \
--apikey xxxxxxx \
--location "品川" "大崎"
--unitime 10
```

### Output
```
{
        "device_id": "DUMMY000000",
        "date": "2020-01-01T00:00:10.000000+09:00",
        "seq_no": 0,
        "latitude": 35.6203897,
        "longitude": 139.7255799,
        "speed": 36.0
}
```

## データ生成例3
 
- 東京駅周辺を走行する，100分間(6000秒)のデータを生成
- 時間は2020/01/01 00:00:00.000から 1分刻み
- 入力 location を順番に向かって走行する．

```
python dummy-gen.py \
--duration 6000 \
--apikey xxxxxxx \
--location "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" \
--unitime 60 \
--timestamp "2020/01/01 00:00:00.000" \
--routerandom false
```
### Output
```
{
        "vehicleID": "DEMO001234",
        "date": "2020-01-01T00:10:00.000000+09:00",
        "seq_no": 0,
        "latitude": 35.6773514,
        "longitude": 139.7655863,
        "speed": 36.0
}
```

## データ生成例4
 
- 東京駅周辺を走行する，10分間(600秒)のデータを生成
- 時間は2020/01/01 00:00:00.000から0.1秒刻み
- 入力 location からランダムに3点選んで走行
- device_idのKey名を`vehicleID`としてID名を`DEMO001234`にする

```
python dummy-gen.py \
--duration 600 \
--apikey xxxxxxx \
--location "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" \
--unitime 0.1 \
--timestamp "2020/01/01 00:00:00.000" \
--idtitle DEMO \
--idnum 1234
--idnames vehicleID
```
### Output
```
{
        "vehicleID": "DEMO001234",
        "date": "2020-01-01T00:00:00.100000+09:00",
        "seq_no": 0,
        "latitude": 35.6773514,
        "longitude": 139.7655863,
        "speed": 36.0
}
```

## データ生成例5
 
- 生成例4 と同じ形式でデータ生成するが，目的地に到着してもdurationを経過するまで出発地と目的地を巡回する  
  すなわち6000レコード生成する

```
python dummy-gen.py \
--duration 600 \
--apikey xxxxxxx \
--location "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" \
--unitime 0.1 \
--timestamp "2020/01/01 00:00:00.000" \
--idtitle DEMO \
--idnum 1234
--idnames vehicleID
--loop true
```

### Output
```
{
        "vehicleID": "DEMO001234",
        "date": "2020-01-01T00:00:00.100000+09:00",
        "seq_no": 0,
        "latitude": 35.6773514,
        "longitude": 139.7655863,
        "speed": 36.0
}
```

## データ生成例6
 
- 生成例4 と同じ形式でデータ生成  
  車両名のキーを`vehicle_key1`，`vehicle_key2`の 2つ持たせる

```
python dummy-gen.py \
--duration 600 \
--apikey xxxxxxx \
--location "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" \
--unitime 1.0 \
--timestamp "2020/01/01 00:00:00.000" \
--idnames vehicle_id1 vehicle_id2  
```

### Output
```
{
        "vehicle_id1": "DUMMY000000",
        "vehicle_id2": "DUMMY000000",
        "date": "2020-01-01T00:00:01.000000+09:00",
        "seq_no": 0,
        "latitude": 35.6648142,
        "longitude": 139.7563172,
        "speed": 36.0
}
```