# -*- coding: UTF-8 -*-

import argparse
import pprint
import json
import copy
import time
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", default = "input.json", help = "input filename(default = input.json)", type = str)
parser.add_argument("-o","--out", default = "out.json", help = "output filename(default = out.json)", type = str)
parser.add_argument("-t","--title", default = "A", help = "title(default = A)", type = str)
parser.add_argument("--date", default = "2017/08/02", help = "date(default = 2017/08/02)", type = str)
parser.add_argument("--datetime", default = None, help = "datetime(default = None)", type = str)
parser.add_argument("--duration", default = 600, help = "duration(default = 600)", type = int)
parser.add_argument("-r","--replicate", default = 1, help = "replicate(default = 1)", type = int)
args = parser.parse_args()

duration = args.duration

def load_json(filename):
    json_file = {}
    with open(filename, "r") as file:
        json_file = json.load(file)
    return json_file

def write_json(filename,json_filen):
    with open(filename, "w") as file:
        json.dump(json_filen,file,indent=4)

def replicate_with_datetime(before_json):
    after_json = []
    for i in range(0, args.replicate):
        dt = datetime.datetime.strptime(args.datetime, '%Y/%m/%d %H:%M:%S')
        for j,record in enumerate(before_json):
            if duration == j:
                break
            record['vehicle_id'] = args.title + ('%06d' % i)
            record['timestamp'] = dt.strftime('%Y/%m/%d %H:%M:%S')# time.strftime('%H:%M:%S',time.gmtime(j))
            tmp_record = copy.deepcopy(record)
            after_json.append(tmp_record)
            dt = dt + datetime.timedelta(seconds=1)
    return after_json

def replicate_with_date(before_json):
    after_json = []
    for i in range(0, args.replicate):
        for j,record in enumerate(before_json):
            if duration == j:
                break
            record['vehicle_id'] = args.title + ('%06d' % i)
            record['timestamp'] = args.date + " " + time.strftime('%H:%M:%S',time.gmtime(j))
            tmp_record = copy.deepcopy(record)
            after_json.append(tmp_record)
    return after_json

def replicate(input_json):
    after_json = {}
    if args.datetime is not None:
        after_json = replicate_with_datetime(input_json)
    else:
        after_json = replicate_with_date(input_json)
    return after_json

def main():
    input_json = load_json(args.input)
    if len(input_json) < duration:
        print("input array is too short:", len(input_json), " < ",duration)
        sys.exit()
    after_json = replicate(input_json)
    write_json(args.out,after_json)

if __name__ == '__main__':
    main()
