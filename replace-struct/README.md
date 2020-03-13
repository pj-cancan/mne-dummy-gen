# Replace Struct

## Abstruct
`dummmy-gen.py` で生成されたJSONファイルの構造体を以下のように変換，修正する

|修正前|修正後|説明|
|:----|:------|:--|
|mobility_id|device_id|車情報|
|lat|latitude|緯度|
|lng|longitude|経度|
|timestamp|date|日時|
|spd|speed|速度|
|-|direction|目的地？|
|-|acceleration_x|加速度|
|-|acceleration_y|加速度|
|-|acceleration_z|加速度|
|seq_no|-|？|
|alt|-|？|
|drv_time|-|？|

* 各加速度は-0.5~0.5のランダムな値をとるが，0.1%の確率で大きく負の値も取る


## Usage
* 第一引数に読み取るjsonファイル指定
* 第二引数に出力先指定

## Example

```
go run main.go ./input.json ./output.json 
```