#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import requests
import boto3
import ssl
import base64

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
    ARN_XPATH = './{https://sts.amazonaws.com/doc/2011-06-15/}GetCallerIdentityResult/{https://sts.amazonaws.com/doc/2011-06-15/}Arn'
    arn = root.find(ARN_XPATH).text
    print('role session arn')
    print(arn)

    # pull public key for informational reasons
    der_public_key = kms.get_public_key(KeyId=KEY_ID)['PublicKey']
    pem_public_key = ssl.DER_cert_to_PEM_cert(
        der_public_key).replace('CERTIFICATE', 'PUBLIC KEY')
    print(f'\npublic key\n{pem_public_key}')

    # sign by sending full bytes object to KMS
    sign_res = kms.sign(
        KeyId=KEY_ID,
        SigningAlgorithm=SIGNING_ALGORITHM,
        Message=arn.encode(),
    )
    signature = base64.urlsafe_b64encode(sign_res['Signature']).decode()
    print(f'\nsignature\n{signature}')

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
