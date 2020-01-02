#!/usr/bin/env python

import json
import requests

url = 'https://heimdall.eng.sfdc.net/pcs-inventory/v1/pods'

r = requests.get(url, timeout=10)
if r.ok:
    json_data = r.text
    dic_data = json.loads(json_data)
    for pod in dic_data['pods']:
        print(pod)
    print('Total Number of pods: {}'.format(len(dic_data['pods'])))
