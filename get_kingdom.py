#!/usr/bin/env python

import json
import requests

url = 'https://heimdall.eng.sfdc.net/pcs-inventory/v1/kingdoms'

r = requests.get(url, timeout=10)
if r.ok:
    json_data = r.text
    dic_data = json.loads(json_data)
    for kingdom in dic_data['kingdoms']:
        print(kingdom)
    print('Total Number of kingdoms: {}'.format(len(dic_data['kingdoms'])))
