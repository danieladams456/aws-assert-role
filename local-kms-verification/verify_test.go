package main

import (
	"errors"
	"os"
	"testing"
)

func Test_verifyJWT(t *testing.T) {
	token, ok := os.LookupEnv("ROLE_ASSERTION")
	if !ok {
		t.Error(errors.New("must provide token in ROLE_ASSERTION env var"))
	}
	_, err := verifyJWT(token)
	if err != nil {
		t.Error(err)
	}
}
