#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import requests


def main():
    with open('request.json') as infile:
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
    print('role session arn', arn)


if __name__ == '__main__':
    main()
