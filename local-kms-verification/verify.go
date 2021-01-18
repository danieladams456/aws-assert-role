package kmsverifier

import (
	"crypto"
	"crypto/rsa"
	"crypto/sha512"
	"encoding/base64"
	"errors"
	"fmt"
)

func verifySignature(message, signature string, pubKey *rsa.PublicKey) error {
	sigBytes, err := base64.StdEncoding.DecodeString(signature)
	if err != nil {
		return fmt.Errorf("error decoding signature: %s", err)
	}
	hashed := sha512.Sum512([]byte(message))
	return rsa.VerifyPKCS1v15(pubKey, crypto.SHA512, hashed[:], sigBytes)
}

func verifyJWT(jwt string, pubKey *rsa.PublicKey) error {
	return errors.New("not implemented")
}
