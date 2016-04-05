package main

import (
	"fmt"
	"os"

	. "./builder"
	. "./role"
	. "./ssh"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Println("how to use : go run bootstrapping.go [base|rails]")
		return
	}

	role := NewRole(os.Args[1])
	handle(role)
}

func handle(role Role) {
	switch role {
	case BASE:
		Builder{
			Role: BASE,
			Ssh: Ssh{
				Key:            os.Getenv("SSH_INITIALIZE_KEY_PATH"),
				ItamaePort:     "22",
				ServerspecPort: os.Getenv("SSH_PORT"),
			},
		}.Build()
	case RAILS:
		Builder{
			Role: RAILS,
			Ssh: Ssh{
				Key:            os.Getenv("SSH_INITIALIZE_KEY_PATH"),
				ItamaePort:     os.Getenv("SSH_PORT"),
				ServerspecPort: os.Getenv("SSH_PORT"),
			},
		}.Build()
	default:
		fmt.Println("invalid argument, please input [ base, rails ]")
	}
}
