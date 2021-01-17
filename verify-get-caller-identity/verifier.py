#!/usr/bin/env python3
import time
import xml.etree.ElementTree as ET
import json
import requests
import boto3
import ssl
import base64

kms = boto3.client('kms')
KEY_ID = 'alias/identity-assertion-signing'
SIGNING_ALGORITHM = 'RSASSA_PKCS1_V1_5_SHA_256'
JWT_VALID_DURATION = 3600


def jwt_serialize_part(part_dict):
    return base64.urlsafe_b64encode(json.dumps(part_dict).encode()).strip(b'=')


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
    pubkey_res = kms.get_public_key(KeyId=KEY_ID)
    kid = pubkey_res['KeyId'].split('key/')[1]  # actual guid, not alias
    der_public_key = pubkey_res['PublicKey']
    pem_public_key = ssl.DER_cert_to_PEM_cert(
        der_public_key).replace('CERTIFICATE', 'PUBLIC KEY')
    print(f'\npublic key\n{pem_public_key}')

    # construct JWT object for KMS to sign
    header_dict = {
        'typ': 'JWT',
        'alg': 'RS256',
        'kid': kid
    }
    header = jwt_serialize_part(header_dict)

    current_time = int(time.time())
    body_dict = {
        'iat': current_time,
        'exp': current_time + JWT_VALID_DURATION,
        'arn': arn,
    }
    body = jwt_serialize_part(body_dict)
    message = header + b'.' + body
    print(f'jwt header + body to be signed\n{message.decode()}')

    # sign by sending full bytes object to KMS
    sign_res = kms.sign(
        KeyId=KEY_ID,
        SigningAlgorithm=SIGNING_ALGORITHM,
        Message=message,
    )

    # verify
    verify_res = kms.verify(
        KeyId=KEY_ID,
        SigningAlgorithm=SIGNING_ALGORITHM,
        Message=message,
        Signature=sign_res['Signature'],
    )
    print('\nsignature valid via KMS API call:', verify_res['SignatureValid'])

    # verify locally using JWT library
    signature = base64.urlsafe_b64encode(sign_res['Signature']).strip(b'=')
    print(f'\nsignature for local verification\n{signature.decode()}')

    jwt = message + b'.' + signature
    print(f'\nfull JWT\n{jwt.decode()}')


if __name__ == '__main__':
    main()
