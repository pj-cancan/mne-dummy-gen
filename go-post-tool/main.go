package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

//☆入力jsonファイルに応じて構造体を定義
type data struct {
	Name string `json:"Name"`
	Age  int    `json:"Age"`
}

func main() {
	const url = "http://127.0.0.1:9999/hello"//☆post先URL
	flag.Parse()
	filePath := flag.Arg(0) //入力json

	if len(filePath) == 0 {
		log.Fatal("Please specify json file path")
	}

	readFile, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatal(err)
	}

	var datas []data
	if err := json.Unmarshal(readFile, &datas); err != nil {
		log.Fatal(err)
	}

	for _, data := range datas { //サーバへpost
		byte, _ := json.Marshal(data)
		resp, err := http.Post(url, "application/json", bytes.NewBuffer(byte))
		if err != nil {
			log.Fatal(err)
		}

		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}

		if resp.StatusCode != http.StatusOK {
			fmt.Printf("%s", body)
			return
		}

		fmt.Printf("%v\n", string(body))
	}
}
