import { HttpRequest } from "@aws-sdk/protocol-http";
import { Sha256 } from "@aws-crypto/sha256-js";
const { SignatureV4 } = require("@aws-sdk/signature-v4");

const minimalRequest = new HttpRequest({
  method: "POST",
  protocol: "https:",
  path: "/",
  headers: {
    host: "foo.us-bar-1.amazonaws.com",
  },
  hostname: "foo.us-bar-1.amazonaws.com",
});

const credentials = {
  accessKeyId: "foo",
  secretAccessKey: "bar",
};
const signerInit = {
  service: "foo",
  region: "us-bar-1",
  sha256: Sha256,
  credentials,
};

const signer = new SignatureV4(signerInit);
const signed = await signer.presign(minimalRequest, {
  signingDate: new Date("2000-01-01T00:00:00.000Z"),
});

console.log(signed);
