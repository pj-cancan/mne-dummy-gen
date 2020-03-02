
apikey=AIzaSyAtC_LFnW80qN4Lw8tTRMuVIEsZEpGFbog
duration=300
cars=10

python dummy-gen.py --out /mnt/ramdisk/test1.yml --duration ${duration} --speed 40 --random 10 \
  --timestamp "2000/01/01 00:00:00" --apikey ${apikey} --routes ${cars} --interval 1                 --title A --idnames shadow_id \
  --locations "刈谷市" "デンソー　本社" "東海市"  "大府市" "高浜市" "安城市" "豊明市" "岡崎市" "西尾市" "豊田市" \
  --endless true

python dummy-gen.py --out /mnt/ramdisk/test2.yml --duration ${duration} --speed 40 --random 10 \
  --timestamp "2000/01/01 00:00:00" --apikey ${apikey} --routes ${cars} --interval 5 --filldown True --title B --idnames shadow_id \
  --locations "札幌駅" "すすきの駅" "ニトリ麻生店" "札幌グランドホテル" "札幌市立明園中" "札幌市 北区役所" \
  --endless true

python data-merge.py --db /tmp/merge.dat --files /mnt/ramdisk/test1.yml /mnt/ramdisk/test2.yml

python make-stub-data.py --db /tmp/merge.dat --coordinate /mnt/ramdisk/coordinate.yml --attributes /mnt/ramdisk/attributes.yml

cp /mnt/ramdisk/coordinate.yml /mnt/pcie/workspaces/workspace-pycharm/gw_stub/response/
cp /mnt/ramdisk/attributes.yml /mnt/pcie/workspaces/workspace-pycharm/gw_stub/response/