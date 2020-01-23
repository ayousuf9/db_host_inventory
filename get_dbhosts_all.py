#!/usr/bin/env python

import json
import requests
import argparse

"""
This script lists all the db hosts in inventory service api json output.
It also separates the list as primary and DR.
Input:
    None
Output:
    Primary and DR hosts
"""

url = 'https://heimdall.eng.sfdc.net/pcs-inventory/v1/dbHosts'

r = requests.get(url, timeout=10)
if r.ok:
    json_data = r.text
    dic_data = json.loads(json_data)
    # Returns a list of name and isDR value.  Example: ['eu1-db-1-frf', 'False']
    host_list = [[h.get(x) for x in ['name', 'isDR']] for h in dic_data['hostList']]
    #Sort by 3rd field, delimited by -, which is a number and sort as integer not as a string
        #Example: eu1-db1-2-frf.  Third field is 2.
    host_list.sort(key=lambda x: int(x[0].split('-')[2]))
    # Sort by 4th field which is dc or data center.
    host_list.sort(key=lambda x: x[0].split('-')[3])
    # Sort by 2nd field which is db type.  Example: db1 or dgdb1
    host_list.sort(key=lambda x: x[0].split('-')[1])
    # Sort by 1st field which is pod name.  Example: na67
    host_list.sort(key=lambda x: x[0].split('-')[0])
    pri_hosts = []
    dr_hosts = []
    for h_info in host_list:
        if h_info[1] == False:
            pri_hosts.append(h_info[0])
        else:
            dr_hosts.append(h_info[0])

print('=== Primary ===')
for pri_host in pri_hosts:
    print(pri_host)
print('\n')
print('=== DR ===')
for dr_host in dr_hosts:
    print(dr_host)
print('\n')

print('Total Number of hosts: {}'.format(len(dic_data['hostList'])))
print('Total Primary: {}'.format(len(pri_hosts)))
print('Total DR: {}'.format(len(dr_hosts)))
