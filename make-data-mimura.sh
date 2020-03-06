
#count=1
apikey=AIzaSyAEnTH19QPx0aqS3eipPnCKLo-cuH8tuSc

for count in $(seq 1124 2000);do count=`printf %06d $count`

python3 dummy-gen.py -d 6000 -o ../dummy-2000-data/DUMMY$count.json --apikey $apikey -l "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" -r 1 -w 4 -s 36.0 -m 20  -e True -p  "2020/03/06 09:00:00.000" -i 0.1 --idoffset $count
done
