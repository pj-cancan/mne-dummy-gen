# -*- coding: UTF-8 -*-

import argparse
import pprint
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", default = "input.json", help = "input filename(default = input.json)", type = str)
parser.add_argument("-o","--out", default = "out.json", help = "output filename(default = out.json)", type = str)
parser.add_argument("-t","--title", default = "A", help = "title(default = A)", type = str)
#parser.add_argument("--date", default = "2017/08/02", help = "date(default = 2017/08/02)", type = str)
parser.add_argument("--duration", default = 600, help = "duration(default = 600)", type = int)
args = parser.parse_args()

def load_json(filename):
    json_file = {}
    with open(filename, "r") as file:
        json_file = json.load(file)
    return json_file

def write_json(filename,json_filen):
    with open(filename, "w") as file:
        json.dump(json_filen,file,indent=4)

def replace(before_json):
    after_json = []
    for i,record in enumerate(before_json):
        if args.duration == i:
            break
        record['vehicle_id'] = args.title + record['vehicle_id'][1:]
        record['timestamp'] = args.date + record['timestamp'][10:]
        after_json.append(record)
    return after_json

def main():
    input_json = load_json(args.input)
    after_json = replace(input_json)
    write_json(args.out,after_json)

if __name__ == '__main__':
    main()
