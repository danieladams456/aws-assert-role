package verifier_test

import (
	"errors"
	"os"
	"testing"

	"github.com/danieladams456/kmsverifier/verifier"
)

func Test_verifyJWT(t *testing.T) {
	token, ok := os.LookupEnv("ROLE_ASSERTION")
	if !ok {
		t.Error(errors.New("must provide token in ROLE_ASSERTION env var"))
	}

	verifier := verifier.Verifier{}
	verifier.LoadPubKeys()

	_, err := verifier.VerifyJWT(token)
	if err != nil {
		t.Error(err)
	}
}
