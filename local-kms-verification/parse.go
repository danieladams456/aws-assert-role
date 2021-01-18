package main

import (
	"crypto/rsa"
	"crypto/x509"
	"encoding/base64"
	"errors"
)

// parses base64 string into rsa public key
func parsePublicKey(base64PubKey string) (*rsa.PublicKey, error) {
	pubKeyBytes, err := base64.StdEncoding.DecodeString(base64PubKey)
	if err != nil {
		return nil, err
	}
	pubKey, err := x509.ParsePKIXPublicKey(pubKeyBytes)
	if err != nil {
		return nil, err
	}
	rsaPubKey, ok := pubKey.(*rsa.PublicKey)
	if !ok {
		return nil, errors.New("could not cast to *rsa.PublicKey")
	}
	return rsaPubKey, nil
}
