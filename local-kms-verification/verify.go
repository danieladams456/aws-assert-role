package main

import (
	"crypto"
	"crypto/rsa"
	"crypto/sha512"
	"crypto/x509"
	"encoding/base64"
	"errors"
	"fmt"

	"github.com/form3tech-oss/jwt-go"
)

func verifySignature(message, signature string, pubKey *rsa.PublicKey) error {
	sigBytes, err := base64.StdEncoding.DecodeString(signature)
	if err != nil {
		return fmt.Errorf("error decoding signature: %s", err)
	}
	hashed := sha512.Sum512([]byte(message))
	return rsa.VerifyPKCS1v15(pubKey, crypto.SHA512, hashed[:], sigBytes)
}

var keys = map[string]string{
	"d1583b11-f7f7-49b6-a3c7-01fbae56915f": "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAo009XAA3N0XFKrrWda1gTc0ehoXmxWsL6/THCTMKWZt82uENiYXoSVoekjd7WYb5Er5oN59W36YEL65hH402I0Frw5YEDsM0epum9eJgyuZ/2bmH/DA7ncwpRXggkOfzoqjXzubCqQYVnsb9ErDzgBPlug3LjyL8ju/Oe/P9dFIXie/egdRYr3QXbRYMl3UuebtdMNbRdFaCkv8IMeYGPvrrDXE78w4o6dvsnnBDr7aHMTprCt4Yzttbigg69OpmjA4qBz4+33YHXKNtNcUb9CuVlBla2ZZkfU7BQ4TEi/87kAorXuUZDnV1atUBiwwlTxlQeZhcVrM5sFtjKDsJGij6rxvyTrsXTjSH/UhCHr4e2tbDutVdvuG+NVjAWhlMHGJGbjphxwAbB7KX5JqSMpYsKFfp5QTHA4Hbiu5xaBSi8jzDanDfzufHXQvuf1cpkShxjSc2gyiYaflodjxiQ2OJr3MtzRxm977aOyJmytEuY7Zpya9lmwzAv/6uIrmAu+iFq5cje46kwES16dsGYI8v1YSSc9vIGAzhl27qNTjEnjmYPcyLeL5MiuGk+3eh4asRAZMvZ+vvIAnuhM9N3cCmK4Tn0L6vAwmosQrOf3H11QxXD3KQGP8sJXAxxTJ7pb4GKYITZW2sJ3Jaifi/04MBtm0n4N8xCGUxO4tiXDkCAwEAAQ==",
}

// in runtime, the parsing would be done ahead of time and lookup map[string]*rsa.PublicKey
func lookupKey(input *jwt.Token) (interface{}, error) {
	kid, ok := input.Header["kid"].(string)
	if !ok {
		return nil, errors.New("kid header missing or not string")
	}
	pubKeyStr, ok := keys[kid]
	if !ok {
		return nil, fmt.Errorf("could not find public key: %s", kid)
	}

	pubKeyBytes, err := base64.StdEncoding.DecodeString(pubKeyStr)
	if err != nil {
		return nil, err
	}
	return x509.ParsePKIXPublicKey(pubKeyBytes)
}

func verifyJWT(token string) (*jwt.Token, error) {
	return jwt.Parse(token, lookupKey)
}
