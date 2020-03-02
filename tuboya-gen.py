# -*- coding:utf8 -*-

import json, datetime
from collections import OrderedDict
import pprint
import math, random
import argparse
from typing import *
import googlemaps
import sys
import polyline
import math
from collections import namedtuple

# 定数の定義
rad = 3.1415926535897932384626433832795028841971 / 180.0
RX = 6378137.000000
RY = 6356752.314140
e = math.sqrt((RX * RX - (RY * RY)) / (RX * RX))

SectionInfo = namedtuple('SectionInfo', (
    'bgn',
    'end',
    'distance',
    'delta',
    'bgn_distance',
    'end_distance'
))


class Vehicle:
    def __init__(self, fr: str, to: str, start_time: int, speed: int, response) -> None:
        print()


class BaseLatLng:
    def __init__(self, lat: float, lng: float) -> None:
        self.lat = lat
        self.lng = lng

    def to_tuple(self) -> Tuple[float, float]:
        return (self.lat, self.lng)

    def __str__(self) -> str:
        return "(%f,%f)" % (self.lat, self.lng)


class LatLng(BaseLatLng):
    def __init__(self, lat: float, lng: float) -> None:
        super().__init__(lat, lng)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseLatLng):
            other2: BaseLatLng = other
            return self.lat == other2.lat and self.lng == other2.lng
        else:
            return False

    def __add__(self, other: BaseLatLng) -> BaseLatLng:
        return LatLng(self.lat + other.lat, self.lng + other.lng)

    def __sub__(self, other: BaseLatLng) -> BaseLatLng:
        return LatLng(self.lat - other.lat, self.lng - other.lng)

    def __mul__(self, other: float) -> BaseLatLng:
        return LatLng(self.lat * other, self.lng * other)


def calc_distance(bgn_point: LatLng, end_point: LatLng) -> float:
    # 距離計算関数
    # 極半径
    # ベッセル楕円体 ( 旧日本測地系 ) <- 以前の日本での標準
    # const RX = 6377397.155000  // 赤道半径
    # const RY = 6356079.000000  // 極半径
    # WGS84 ( GPS ) <- Google はこの測地系
    # const RX = 6378137.000000  // 赤道半径
    # const RY = 6356752.314245  // 極半径
    # 2点の経度の差を計算 ( ラジアン )

    (lat_1, lng_1) = bgn_point.to_tuple()
    (lat_2, lng_2) = end_point.to_tuple()

    a_x = lng_1 * rad - (lng_2 * rad)
    # 2点の緯度の差を計算 ( ラジアン )
    a_y = lat_1 * rad - (lat_2 * rad)
    # 2点の緯度の平均を計算
    p = (lat_1 * rad + lat_2 * rad) / 2
    # 離心率を計算

    # 子午線・卯酉線曲率半径の分母Wを計算
    w = math.sqrt(1 - (e * e * math.sin(p) * math.sin(p)))
    # 子午線曲率半径を計算
    m = RX * (1 - (e * e)) / (w * w * w)
    # 卯酉線曲率半径を計算
    n = RX / w
    # 距離を計算
    x = (a_y * m)
    y = (a_x * n * math.cos(p))
    d = x * x + y * y
    d = math.sqrt(d)
    return d


def get_route(api_key: str, start: Union[str, tuple], end: str, start_time: str, speed: int,
              output_interval: int) -> Tuple[datetime.datetime, LatLng]:
    google_client = googlemaps.Client(api_key)

    today: datetime.datetime = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M')

    response: List = []
    try:
        response = google_client.directions(
            origin=start,
            destination=end,
            language="ja",
            mode="driving",
            avoid=["indoor"])
    except Exception as ex:
        print(sys.exc_info(), ex)
        return today, LatLng(0, 0)

    # 経路情報を取得
    steps: List = response[0]["legs"][0]["steps"]

    # パスを構築する
    path_points = []
    for stp in steps:
        points: str = stp["polyline"]["points"]
        lat_lngs = polyline.decode(points)
        for lat_lng in lat_lngs:
            # 緯度・経度のタプル
            path_points.append(LatLng(*lat_lng))

    # 区間を構築
    new_steps = []
    length = len(path_points)
    distance = 0.0
    # 次のポイントと組み合わせて区間を構築
    for i in range(0, length - 1):
        bgn_point = path_points[i]
        end_point = path_points[i + 1]

        # ２点間の距離・差分などを計算
        section_distance = calc_distance(bgn_point, end_point)
        end_distance = distance + section_distance
        # 名前付きタプルを構築
        obj = SectionInfo(
            bgn_point,
            end_point,
            section_distance,
            end_point - bgn_point,
            distance,
            end_distance
        )

        new_steps.append(obj)
        # 全走行距離を計算
        distance += section_distance

    # シミュレート開始

    # 時速何km/hが秒速で何m進むか
    car_speed = (speed * 1000.0) / 3600.0

    # 全行程距離(m)を所定の秒速なら何秒で終了するか
    loop_count: int = int(distance / car_speed)

    # 車の位置
    car_pos: float = 0.0

    time_delta: datetime.timedelta = datetime.timedelta(seconds=1)

    new_car_pos: LatLng = new_steps[0].end

    # ループ開始(分解能は１秒)
    for x in range(0, loop_count):

        for i in range(0, len(new_steps)):
            step: SectionInfo = new_steps[i]
            # 現在車の距離がどの区間にあるのか判定する
            if step.bgn_distance <= car_pos <= step.end_distance:
                # 区間の距離
                section_distance = step.distance

                # 区間の開始位置から車の距離
                car_pos_from_bgn = car_pos - step.bgn_distance

                # 区間内において、車の位置が何％の位置にあるのかを計算
                car_progres_per = car_pos_from_bgn / section_distance

                # 開始・終点の傾き * 区間内の位置
                new_car_pos = step.bgn + step.delta * car_progres_per

                # 3秒単位で出力
                if x % output_interval == 0:
                    print('%s,%3.32f,%3.32f,%d,"%s","%s"' % (
                        today.strftime('%Y/%m/%d %H:%M:%S'), new_car_pos.lat,
                        new_car_pos.lng, speed, start, end))
                break

        today += time_delta
        # 車の移動
        car_pos += car_speed

    # print("全長", distance)
    return today, new_car_pos


def main(output_interval: int) -> None:
    # ヘッダー出力
    print("date_time,lat,lng,speed,from,to")
    api_key = "AIzaSyAtC_LFnW80qN4Lw8tTRMuVIEsZEpGFbog"

    # routes:[]
    #   src: 移動元
    #   dst: 移動先
    #   speed: スピード(km/h)
    #   rest: 移動先に到着後に停止する時間

    step1 = {
        "start_datetime": "2018/6/30 08:00",
        "routes": [
            {"src": "大崎", "dst": "海ほたるパーキングエリア", "speed": 50, "rest": 15},
            {"src": "海ほたるパーキングエリア", "dst": "中の島大橋", "speed": 35, "rest": 10},
            {"src": "中の島大橋", "dst": "イオンモール木更津", "speed": 35, "rest": 45},
            {"src": "イオンモール木更津", "dst": "富津公園キャンプ場着", "speed": 20, "rest": 0},
        ]
    }

    step2 = {
        "start_datetime": "2018/6/30 15:00",
        "routes": [
            {"src": "富津公園キャンプ場着", "dst": "海ほたるパーキングエリア", "speed": 50, "rest": 15},
            {"src": "海ほたるパーキングエリア", "dst": "スーパーバリュー 品川八潮店", "speed": 35, "rest": 45},
            {"src": "スーパーバリュー 品川八潮店", "dst": "大崎", "speed": 35, "rest": 35},
        ]
    }

    for step in [step1, step2]:
        start_time: str = str(step["start_datetime"])
        arrived_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M')
        routes: List[Dict] = []
        if isinstance(step["routes"], list):
            routes = list(step["routes"])
        for route in routes:
            (arrived_time, car_latlng) = get_route(
                api_key,
                route["src"],
                route["dst"],
                arrived_time.strftime('%Y/%m/%d %H:%M'),
                route["speed"],
                output_interval
            )
            arrived_time += datetime.timedelta(minutes=route["rest"])


if __name__ == '__main__':
    main(60)
    # main(int(sys.argv[1]))
