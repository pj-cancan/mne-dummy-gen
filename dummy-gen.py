# -*- coding: UTF-8 -*-

import json, datetime
from collections import OrderedDict
import pprint
import math, random
import argparse
import googlemaps
import sys
import copy
from distutils.util import strtobool

# 定数 ###############################
# 緯度 35度と仮定(経度１度の距離は経度によって決まるため、tokyo(北緯35度)とする)
# 1mあたりの緯度は 0.0000090133729745762
# 例えば現在地の緯度から 10m 南の緯度を求めるには、この値に 10 を掛けたものを現在地の緯度からマイナスすれば求まる．北ならプラスする
lat_per_1m = 0.000009
# 1mあたりの経度は 0.000010966404715491394 度
# 例えば現在地の経度から 10m 西の経度を求めるには、この値に 10 を掛けたものを現在地の経度からマイナスすれば求まる．東ならプラスする
lng_per_1m = 0.000011



# 車両系定数 #########################
curvature = 0
diag = False
gas = 100
height = 0
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
wiper = 0
passengers = 1
# シフト情報(固定)
shift_type = "D3"
# １秒あたりに変化するスピード値の上限
speed_change_max = 3.0
# 開度のMAX
acc_brk_max = 25.0

gas_max = 40

air_min = 2
air_max = 2.4

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--duration", default=600, help="sample duration(default = 600)", type=int)
parser.add_argument("-o", "--out", default="sample.json", help="output filename(default = sample.json)", type=str)
parser.add_argument("-lo", '--locations', default=["大崎", "お台場", "品川", "羽田空港"], help="locations (default = \"大崎\" \"お台場\" \"品川\" \"羽田空港\")", nargs='+')
parser.add_argument("-r", "--routes", default=1, help="route size(default = 1)", type=int)
parser.add_argument("-w", "--waypoints", default=2, help="waypoints(default = 2)", type=int)
parser.add_argument("-s", "--speed", default=36, help="speed(default = 36(km/h))", type=float)
parser.add_argument("-sr", "--speedrandom", default=0, help="speed random facor(default = 0persent)", type=int)
parser.add_argument("--idtitle", "--idtitle", default="DUMMY", help="device_id = idtitle + sequential num(default = DUMMY)", type=str)
parser.add_argument("-t", "--timestamp", default="2020/01/01 00:00:00.000", help="start time(default = 2020/01/01 00:00:00.000)")
parser.add_argument("-lp", "--loop", default=False, help="loop among waypoints(default = False)", type=strtobool)
parser.add_argument("-rr", "--routerandom", default=True, help="if True, make route with all locations(default = False)", type=strtobool)
parser.add_argument("-k", "--apikey", default=False, help="Google Duration APIのキーを指定して下さい", type=str)
parser.add_argument("--idnum", "--idnum", default=0, help="IDの開始番号(default = 0)", type=int)
parser.add_argument("--idnames", "--idnames", default = ["device_id"] , help="IDのキー名 スペース区切りで複数指定できます", nargs='+')
parser.add_argument("-u", "--unitime", default=1, help="タイムスタンプ間隔を指定します(default = 1.0 sec)", type=float)

print(sys.argv)

args = parser.parse_args()
waypoints = args.waypoints
unit_time = args.unitime
routerandom = args.routerandom


if args.apikey is not None:
    api_key = args.apikey

if not routerandom:
    waypoints = len(args.locations)
    
if waypoints < 2:
    waypoints = 2




def create_sample(cars, start_time, duration):
    sample_data = []
    for car in cars:
        car_record = gen_rand(car, start_time, duration)
        sample_data.extend(car_record)
        print(str(len(sample_data)) + " data generated")
    return sample_data

def gen_rand(car, start_time, duration):
    v_id = car['v_id']
    drv_time = random.randint(0, 2400)

    # ± random % の速度増減をさせる
    speed = car['speed'] * (1.0 + random.randint(-args.speedrandom, args.speedrandom) / 100.0)
    max_speed = speed * (1.0 + args.speedrandom / 100.0)
    min_speed = speed * (1.0 - args.speedrandom / 100.0)
    
    brake_level = 0
    acceleration_level = 0
    brake_level = 0
    steering = 0
    gas = random.randint(gas_max * 0.2, gas_max)
    wheel_air_fl = random.uniform(air_min, air_max)
    wheel_air_fr = random.uniform(air_min, air_max)
    wheel_air_rl = random.uniform(air_min, air_max)
    wheel_air_rr = random.uniform(air_min, air_max)
    
    lat = car['coordinates'][0][0] # start lat
    lng = car['coordinates'][0][1] # start lng
    tgt_lat = car['coordinates'][1][0]  # target lat
    tgt_lng = car['coordinates'][1][1]  # target lng

    coordinates = iter(car['coordinates'][1:])
    tgt_coordinates = next(coordinates)
    last_record = {}

    rand_data = []
    for i in range(0, duration):
        record = OrderedDict()
        # unitimeごとにタイムスタンプを刻む
        start_time = start_time + datetime.timedelta(0, unit_time)
        
        for idname in args.idnames:
            record[idname] = v_id

        # speed random change
        speed_diff = random.uniform(-speed_change_max, speed_change_max)
        speed += speed_diff

        if speed > max_speed:
            speed_diff += max_speed - speed
            speed = max_speed
        if speed < min_speed:
            speed_diff += min_speed - speed
            speed = min_speed

        # acc brk change
        if (speed_diff + speed_change_max / 3) > 0:
            acceleration_level = (int)((speed_diff + speed_change_max / 3) / speed_change_max * acc_brk_max)
            brake_level = 0
        else:
            acceleration_level = 0
            brake_level = (int)(-(speed_diff + speed_change_max / 3) / speed_change_max * acc_brk_max)

        # 変数
        # 方位角(ラジアン)
        azimuth = math.atan2((tgt_lat - lat), (tgt_lng - lng)) * 180 / math.pi
        if azimuth < 0:
            azimuth += 360
        # 現地点と次地点との距離
        distance = math.hypot(tgt_lng - lng, tgt_lat - lat)

        # 1イテレーション(unit time)あたりに進む距離(m)
        speed_per_iter = int(speed / 3.6 * unit_time)

        # 1イテレーションあたりに進むlat,lng
        lat_delta = math.sin(azimuth / 180.0 * math.pi) * lat_per_1m * speed_per_iter
        lng_delta = math.cos(azimuth / 180.0 * math.pi) * lng_per_1m * speed_per_iter

        delta = math.hypot(lng_delta, lat_delta)

        # 出力の定義
        record['date'] = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f'+'+09:00')
        record['seq_no'] = i
        record['latitude'] = lat
        record['longitude'] = lng
        record['speed'] = speed
        
        # 任意でコメントアウトを外して使用してください
        # record['direction'] = azimuth
        # record['acc_lv'] = acceleration_level
        # record['emergency_cd'] = "0"
        # record['alt'] = height
        # record['drv_time'] = drv_time
        # record['brk_lv'] = brake_level
        # record['steering'] = steering
        # record['wl_spd_fr'] = int(speed)
        # record['wl_spd_fl'] = int(speed)
        # record['wl_spd_rr'] = int(speed)
        # record['wl_spd_rl'] = int(speed)

        # 定数
        # record['curv'] = curvature
        # record['diag'] = diag
        # record['gas'] = gas
        # record['wl_air_fl'] = int(wheel_air_fl)
        # record['wl_air_fr'] = int(wheel_air_fr)
        # record['wl_air_rr'] = int(wheel_air_rr)
        # record['wl_air_rl'] = int(wheel_air_rl)
        # record['battery'] = battery
        # record['light'] = light
        # record['wiper'] = wiper
        # record['passengers'] = passengers
        # record['shift_type'] = shift_type

        if distance > delta:
            lat = lat + lat_delta
            lng = lng + lng_delta
        else:
            lat = tgt_lat
            lng = tgt_lng
            try: # 次の巡回地点へ
                tgt_coordinates = next(coordinates)
                tgt_lat = tgt_coordinates[0]
                tgt_lng = tgt_coordinates[1]
            except Exception:
                if args.loop:
                    coordinates = iter(car['coordinates'][1:])
                    tgt_coordinates = next(coordinates)
                    tgt_lat = tgt_coordinates[0]
                    tgt_lng = tgt_coordinates[1]
                else:
                    break

        # データ格納
        rand_data.append(record)

        drv_time = drv_time + 1

    return rand_data


class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


# 巡回経路の緯度経度の作成
def create_sample_path(car_id, speed, start, end):
    # https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/directions.py

    googleClient = googlemaps.Client(api_key)
    legs = []
    try:
        response = googleClient.directions(
            origin=start,
            destination=end,
            language="ja",
            mode="walking",
            avoid=["trolls", "highways", "indoor"])
        legs = response[0]["legs"][0]
    except Exception as e:
        print(sys.exc_info())
        return

    # MyPrettyPrinter().pprint(legs)

    start_location = [legs["start_location"]["lat"], legs["start_location"]["lng"]]
    car = OrderedDict()
    car["v_id"] = car_id
    car["speed"] = speed

    coordinates = [start_location]
    for step in legs["steps"]:
        coordinate = [
            step["end_location"]["lat"],
            step["end_location"]["lng"]
        ]
        coordinates.append(coordinate)
    car["coordinates"] = coordinates
    return car

# 巡回路の作成
def routes():
    locations = args.locations
    print("Location list(len:%d):" % (len(locations)))
    # print(str(locations).decode("unicode_escape"))

    routes = []
    # no random mode
    # 入力順に回る
    if not args.routerandom:
        route = []
        for loc in locations:
            route.append(loc)
        routes.append(route)
        return routes

    # random mode
    # スタート，経由地，目的地をランダムに生成
    for i in range(args.routes):
        start_index = random.randint(0, len(locations) - 1)
        route = [locations[start_index]]
        # routeからランダムにwaypoints個の経由地を選択
        for num in range(args.waypoints):
            while True:
                end_index = random.randint(0, len(locations) - 1)
                if start_index != end_index:
                    start_index = end_index
                    break
            route.append(locations[end_index])
        if args.loop:
            route.append(route[0])
        routes.append(route)
    return routes


def main():
    global args

    rts = routes()
    print("Routes list(%d * %d waypoints):" % (len(rts), waypoints))
    # print(str(rts).decode("unicode_escape"))

    cars = []
    car_id = 0
    for i, locations in enumerate(rts):
        # locations :=巡回路
        car_id = args.idtitle + ('%06d' % (i + args.idnum))
        # car:=start->endまでの緯度経度を保有
        car = []
        print("processing:", len(rts) - i)
        for j, location in enumerate(locations):
            if j == len(locations) - 1:
                break
            temp_car = create_sample_path(car_id, args.speed, locations[j], locations[j + 1])
            if temp_car is None:
                continue
            if len(car) == 0:
                car = temp_car
            else:
                car['coordinates'] = car['coordinates'][:-1]
                car['coordinates'].extend(temp_car['coordinates'][1:])
        if car is not None:
            cars.append(car)


    start_time = datetime.datetime.strptime(args.timestamp, "%Y/%m/%d %H:%M:%S.%f")

    sample_json = create_sample(cars, start_time, (int)(args.duration/unit_time))

    # ファイル出力
    if args.out.endswith(".json"):
        with open(args.out, "w") as file:
            json.dump(sample_json, file, indent=4)
    
    elif args.out.endswith(".yml") or args.out.endswith(".yaml"):
        import yaml
        output_data = []
        for x in sample_json:
            row = {}
            for y in x.keys():
                row[y] = x[y]
            output_data.append(row)
        with open(args.out, "w") as file:
            file.write(yaml.dump(output_data, default_flow_style=False))

    print("%d records are generated as %s" % (len(sample_json), args.out))



if __name__ == "__main__":

    main()
