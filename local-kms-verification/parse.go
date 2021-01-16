package localkmsverifier

import (
	"crypto/rsa"
	"crypto/x509"
	"encoding/base64"
)

// parses base64 string into rsa public key
func parsePublicKey(base64PubKey string) (*rsa.PublicKey, error) {
	pubKeyBytes, err := base64.StdEncoding.DecodeString(base64PubKey)
	if err != nil {
		return nil, err
	}
	return x509.ParsePKCS1PublicKey(pubKeyBytes)
}
