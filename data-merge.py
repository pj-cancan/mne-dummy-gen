"""
データマージプログラム

複数出力されたデータをsqlite3のデータベースに格納する

-- 移動データ
create table traffic_data (
  shadow_id text
  timestamp text
  lat REAL
  lng REAL
  attributes text
)

-- タイムスタンプ一覧を保持
create table timestamp_list(
  timestamp text
)

-- 車(shadow_id)一覧を保持
create table mobilities (
  shadow_id text
)

### 仕様等
・実行時にデータベースを新規に作成する
・データベースファイルを指定する
・取込み(マージ)するデータを複数指定する


"""
import sys
import os
import os.path
import sqlite3
import argparse
import json
import yaml
from contextlib import closing

CREATE_TABLES = """
-- 移動データ
create table traffic_data (
  shadow_id text,
  seq_no integer,
  timestamp_id text,
  lat REAL,
  lng REAL,
  alt REAL,
  attributes text
)
;
-- タイムスタンプ一覧を保持
create table timestamp_list(
  timestamp text
)
;
-- 車(shadow_id)一覧を保持
create table mobilities (
  shadow_id text
)
"""

INSERT_SQL = "insert into traffic_data(shadow_id,seq_no,timestamp_id,lat,lng,alt,attributes) values(?,?,?,?,?,?,?)"

AFTER_SQL = """
insert into timestamp_list as select timestamp_id from traffic_data group by timestamp_id order by timestamp_id
;
insert into mobilities as select shadow_id from traffic_data group by shadow_id order by shadow_id


"""


def create_db(file_path):
    # データベースを作成する
    if os.path.exists(file_path):
        os.remove(file_path)

    # DB作成
    conn = sqlite3.connect(file_path)
    insert_cursor = conn.cursor()

    # テーブル作成
    for sql in CREATE_TABLES.split(";"):
        insert_cursor.execute(sql)

    return conn


def read_data(file, rows):
    # ファイルを読み込む

    if not os.path.exists(file):
        return False
    print("read file [%s]" % file)
    f = open(file, "r")

    if file.endswith(".json"):
        rows += json.load(f)
    elif file.endswith(".yaml") or file.endswith(".yml"):
        rows += yaml.load(f)

    print("read done [%s]" % file)

    return True


def insert_rows(cursor, rows):
    length = len(rows)
    counter = 1
    for row in rows:
        param = (
            row["shadow_id"],
            row["seq_no"],
            row["timestamp"],
            row["lat"],
            row["lng"],
            row["alt"],
            json.dumps(row, separators=(',', ':'))
        )

        cursor.execute(INSERT_SQL, param)
        print("insert record (%d/%d)" % (counter, length))
        counter += 1


def main(args):
    # メイン処理

    # データベースを作成
    with closing(create_db(args.db)) as db:
        cursor = db.cursor()

        # ファイルを読み込む
        for file in args.files:
            rows = []
            if not read_data(file, rows):
                return -1
            # データをSQLに格納
            insert_rows(cursor, rows)

        # 終了(コミット)
        db.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--db", default="/tmp/merge.dat", help="データベースファイル名(default = /tmp/merge.dat)", type=str)
    parser.add_argument("-", '--files', default=[],
                        help="locations (default = []", nargs='+')
    args = parser.parse_args()

    main(args)
