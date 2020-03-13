
#count=1
apikey=AIzaSyAEnTH19QPx0aqS3eipPnCKLo-cuH8tuSc

for count in $(seq 1 2000);do count=`printf %06d $count`

python3 dummy-gen.py -d 6000 -o ../2020-03-10-dummy-data/DUMMY$count.json --apikey $apikey -e True --unitime 0.1 -r 1 -m 10 -d 6000 -l  "東京駅" "汐留" "有楽町" "新橋" "銀座" "日比谷" -w 4 -s 36 --idoffset $count
done

