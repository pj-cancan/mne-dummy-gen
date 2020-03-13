package main

import (
	"encoding/json"
	"flag"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
	"time"
)

type Input struct {
	MobilityID string  `json:"mobility_id"`
	SeqNo      int     `json:"seq_no"`
	Latitude        float64 `json:"latitude"`
	Longitude        float64 `json:"longitude"`
	Alt        int     `json:"alt"`
	DrvTime    int     `json:"drv_time"`
	Date  string  `json:"date"`
	Speed        float64 `json:"speed"`
}

type Output struct {
	DeviceID      string    `json:"device_id"`
	Date          time.Time `json:"date"`
	Latitude      float64   `json:"latitude"`
	Longitude     float64   `json:"longitude"`
	Speed         float64   `json:"speed"`
	Direction     float64   `json:"direction"`
	AccelerationX float64   `json:"acceleration_x"`
	AccelerationY float64   `json:"acceleration_y"`
	AccelerationZ float64   `json:"acceleration_z"`
}

//-0.5 ~ 0.5の乱数を生成
//0.1%の確率で-0.5を下回る外れ値を生成
func randAcceleration() float64 {
	var number float64
	probability := rand.Float64()
	if probability < 0.001 {
		number = -0.5 - rand.Float64()
	} else {
		number = rand.Float64() - 0.5
	}
	return number
}

//time stampを変換
func timeStampParse(value string) time.Time {
	loc, _ := time.LoadLocation("Asia/Tokyo")
	layout := "2006/01/02 03:04:05.000000"
	date, _ := time.ParseInLocation(layout, value, loc)

	return date
}

//ファイル出力
func writeFile(filename string, bytes []byte) {
	ioutil.WriteFile(filename, bytes, os.ModePerm)
}

func main() {
	rand.Seed(time.Now().UnixNano())
	flag.Parse()
	inputName := flag.Arg(0)  //inputJSONファイル
	outputName := flag.Arg(1) //出力JSONファイル名
	count := flag.Arg(2)      //イテレーション

	if count==""{
		log.Printf("Processing...\n")
	}else{
		log.Printf("Processing... %s/2000\n", count)
	}
	

	bytes, err := ioutil.ReadFile(inputName)
	if err != nil {
		log.Fatal(err)
	}
	var inputData []Input
	var outputData []Output
	json.Unmarshal(bytes, &inputData)

	for _, data := range inputData {
		var out Output
		out.DeviceID = data.MobilityID
		out.Date = timeStampParse(data.Date)
		out.Latitude = data.Latitude
		out.Longitude = data.Longitude
		out.Speed = data.Speed
		out.Direction = 123.45 //適当な値
		out.AccelerationX = randAcceleration()
		out.AccelerationY = randAcceleration()
		out.AccelerationZ = randAcceleration()
		outputData = append(outputData, out)
	}
	outputJson, err := json.MarshalIndent(outputData, "", "    ")
	if err != nil {
		log.Fatal(err)
	}
	writeFile(outputName, outputJson)

}
