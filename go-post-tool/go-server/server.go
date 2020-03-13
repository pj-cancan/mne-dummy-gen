package main

import (
    "log"
    "net/http"

    "github.com/ant0ine/go-json-rest/rest"
)

type postHelloInput struct {
    Name string
    Age int
}

type postHelloOutput struct {
    Result string
}

func postHello(w rest.ResponseWriter, req *rest.Request) {
    input := postHelloInput{}
    err := req.DecodeJsonPayload(&input)

    if err != nil {
        rest.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    if input.Name == "" {
        rest.Error(w, "Name is required", 400)
    }

    log.Printf("%#v", input)

    w.WriteJson(&postHelloOutput{
        "Your input is" + input.Name,
    })
}

func main() {
    api := rest.NewApi()
    api.Use(rest.DefaultDevStack...)
    router, err := rest.MakeRouter(
        rest.Post("/hello", postHello),
    )

    if err != nil {
        log.Fatal(err)
    }
    log.Printf("Server started.")
    api.SetApp(router)
    log.Fatal(http.ListenAndServe(":9999", api.MakeHandler()))
}