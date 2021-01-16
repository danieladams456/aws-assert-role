#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import requests
import boto3
from base64 import b64encode

kms = boto3.client('kms')
KEY_ID = 'alias/identity-assertion-signing'
SIGNING_ALGORITHM = 'RSASSA_PKCS1_V1_5_SHA_512'


def main():
    with open('../request.json') as infile:
        presigned = json.load(infile)

    # send presigned request
    res = requests.post(
        presigned['url'], headers=presigned['headers'], data=presigned['body'])
    res.raise_for_status()
    print(res.text)

    # parse result for role session arn
    root = ET.fromstring(res.text)
    arn = root.find(
        './{https://sts.amazonaws.com/doc/2011-06-15/}GetCallerIdentityResult/{https://sts.amazonaws.com/doc/2011-06-15/}Arn').text
    print('role session arn')
    print(arn)

    # pull public key for informational reasons
    public_key = kms.get_public_key(KeyId=KEY_ID)['PublicKey']
    print('\npublic key')
    print(b64encode(public_key).decode())

    # sign by sending full bytes object to KMS
    sign_res = kms.sign(
        KeyId=KEY_ID,
        SigningAlgorithm=SIGNING_ALGORITHM,
        Message=arn.encode(),
    )
    signature = sign_res['Signature']
    print('\nsignature')
    print(b64encode(signature).decode())

    # verify
    verify_res = kms.verify(
        KeyId=KEY_ID,
        SigningAlgorithm=SIGNING_ALGORITHM,
        Message=arn.encode(),
        Signature=sign_res['Signature'],
    )
    print('\nsignature valid:', verify_res['SignatureValid'])


if __name__ == '__main__':
    main()
