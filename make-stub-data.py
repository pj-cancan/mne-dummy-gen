"""

# make-stub-data

* スタブ用のデータを作成

## 概要
* sqliteに格納したデータからスタブデータの作成を行う
* 作成するデータは２種類
  * 座標データ
  * 属性データ
* タイムスタンプ/shadow_idのグループ単位でデータを作成


### データ形式

* 座標データ
 * shadow_id
 * seq_no
 * lat
 * lng
 * alt


"""

SQL_SELECT = """select timestamp_id,seq_no,shadow_id,lat,lng,alt,attributes from traffic_data order by timestamp_id,seq_no,shadow_id"""

import json
import sqlite3
import time
import yaml
from collections import OrderedDict
from contextlib import closing
from datetime import datetime
import random


def get_epoc_time(str_dt: str):
    dt = datetime.strptime(str_dt, '%Y/%m/%d %H:%M:%S')
    return int(time.mktime(dt.timetuple())) * 1000


def get_attributes_by_random(item_count: int):
    attr = {}
    for x in range(1, item_count + 1):
        key = "item%03d" % x
        attr[key] = random.uniform(1.0, 100.0)
    return attr


def make_coordinate(cursor, file_path):
    # 座標値のみのYamlを生成
    pos_yaml = OrderedDict()
    pos_yaml["response"] = OrderedDict()
    pos_yaml["response"]["mode"] = "cyclic"
    pos_yaml["response"]["bodies"] = []

    old_timestamp = ""
    bodies = []
    body = OrderedDict()
    for row in cursor.execute(SQL_SELECT):
        # print(row)
        if row[0] != old_timestamp:
            if len(body) != 0:
                bodies.append(body)
            body = OrderedDict()
            body["label"] = row[1]
            body["code"] = 200
            body["content_type"] = "application/json"
            body["body"] = []

            old_timestamp = row[0]

        rec = OrderedDict()
        rec["timestamp"] = get_epoc_time(row[0])
        rec["seq_no"] = row[1]
        rec["shadow_id"] = row[2]
        rec["mobility_id"] = row[2]
        rec["lat"] = row[3]
        rec["lng"] = row[4]
        rec["alt"] = row[5]
        rec["attributes"] = get_attributes_by_random(100)

        body["body"].append(rec)
    bodies.append(body)

    pos_yaml["response"]["bodies"] = bodies

    with open(file_path, "w") as file:
        file.write(yaml.dump(pos_yaml, default_flow_style=False))


def make_attributes(cursor, file_path):
    # 座標値のみのYamlを生成
    pos_yaml = OrderedDict()
    pos_yaml["response"] = OrderedDict()
    pos_yaml["response"]["mode"] = "default"
    pos_yaml["response"]["bodies"] = []

    old_timestamp = ""
    bodies = []
    default_body = OrderedDict()
    default_body["label"] = "default"
    default_body["code"] = 200
    default_body["content_type"] = "script/python"
    default_body["body"] = """    
#print(request.json["shadowes"])
keys = [ (shadow["shadow_id"],shadow["seq_no"]) for shadow in request.json["ids"] ]
print(keys)
if len(keys) > 0:
  seq_no = str(keys[0][1])
  #print("seq_no",seq_no)
  (_code,_content_type,_body) = get_label_data(label=seq_no)
  #print("body=>",_body)
  
  # get shadows
  new_body = []
  for b in _body:
    if (b["shadow_id"],seq_no) in keys:
      new_body.append(b)
                                
  #print("new_body=>",new_body)
  body = new_body
else:
  (code,content_type,body) = get_label_data(label="0")   
    """
    bodies.append(default_body)

    body = OrderedDict()
    for row in cursor.execute(SQL_SELECT):
        # print(row)
        if row[0] != old_timestamp:
            if len(body) != 0:
                bodies.append(body)
            body = OrderedDict()
            body["label"] = row[1]
            body["code"] = 200
            body["content_type"] = "application/json"
            body["body"] = []

            old_timestamp = row[0]

        rec = OrderedDict()
        rec["timestamp"] = get_epoc_time(row[0])
        rec["seq_no"] = row[1]
        rec["shadow_id"] = row[2]
        rec["mobility_id"] = row[2]
        rec["lat"] = row[3]
        rec["lng"] = row[4]
        rec["alt"] = row[5]
        #rec["attributes"] = json.loads(row[6])
        rec["attributes"] = get_attributes_by_random(100)


        body["body"].append(rec)
    bodies.append(body)

    pos_yaml["response"]["bodies"] = bodies

    with open(file_path, "w") as file:
        file.write(yaml.dump(pos_yaml, default_flow_style=False))


def main(args):
    global SQL_SELECT
    print(args)
    # データベースを作成
    with closing(sqlite3.connect(args.db)) as db:
        cursor = db.cursor()
        make_coordinate(cursor, args.coordinate)
        make_attributes(cursor, args.attributes)


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--coordinate", default="/tmp/coordinate.dat",
                        help="座標データ(default = /tmp/coordinate.yml)", type=str)
    parser.add_argument("-a", "--attributes", default="/tmp/attributes.dat",
                        help="属性データ(default = /tmp/attributes.yml)", type=str)
    parser.add_argument("-d", "--db", default="/tmp/merge.dat", help="データベースファイル名(default = /tmp/merge.dat)", type=str)
    args = parser.parse_args()

    yaml.add_representer(OrderedDict, represent_ordereddict)

    main(args)
