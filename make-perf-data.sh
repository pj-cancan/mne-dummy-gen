
apikey=AIzaSyAtC_LFnW80qN4Lw8tTRMuVIEsZEpGFbog
duration=30
cars=$1
if [ "$cars" = "" ] ; then
    echo 生成台数を第1引数に指定してください
    exit
fi

python dummy-gen.py --out /mnt/ramdisk/kariya-${cars}.json --duration ${duration} --speed 40 --random 10 \
  --timestamp "2000/01/01 00:00:00" --apikey ${apikey} --routes ${cars} --interval 1                 --title A --idnames shadow_id \
  --locations "刈谷市" "デンソー　本社" "東海市"  "大府市" "高浜市" "安城市" "豊明市" "岡崎市" "西尾市" "豊田市" \
  --endless true

exit

python dummy-gen.py --out /mnt/ramdisk/sapporo-${cars}.yml --duration ${duration} --speed 100 --random 10 \
  --timestamp "2000/01/01 00:00:00" --apikey ${apikey} --routes ${cars} --title B --idnames shadow_id \
  --locations "札幌駅" "すすきの駅" "ニトリ麻生店" "札幌グランドホテル" "札幌市立明園中" "札幌市 北区役所" \
  --endless true

# データをマージするためにsqliteに格納する
python data-merge.py --db /tmp/merge-${cars}.dat --files /mnt/ramdisk/kariya-${cars}.yml /mnt/ramdisk/sapporo-${cars}.yml

# データを作成する
python make-stub-data.py --db /tmp/merge.dat --coordinate /mnt/ramdisk/coordinate.yml --attributes /mnt/ramdisk/attributes.yml

#cp /mnt/ramdisk/coordinate.yml /mnt/pcie/workspaces/workspace-pycharm/gw_stub/response/
#cp /mnt/ramdisk/attributes.yml /mnt/pcie/workspaces/workspace-pycharm/gw_stub/response/