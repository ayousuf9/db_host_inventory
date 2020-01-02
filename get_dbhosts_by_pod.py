#!/usr/bin/env python

import json
import requests
import argparse

"""
This script takes one or more pod names, separated by comma, and returns all the hosts that matches the pod
    name in inventory service api json output.  It also separates the list as primary and DR.
Input:
    Pod Name(s): Example: cs3 or cs3,eu1,..
Output:
    Primary and DR hosts
"""

def process_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pod_name', required=True,
         help='One or more Pod Names.  Examples: cs3 or cs3,eu1,..')
    args = parser.parse_args()
    return args

args = process_arguments()

# pn = pod name
for pn in args.pod_name.split(','):
    url = 'https://heimdall.eng.sfdc.net/pcs-inventory/v1/dbHosts?pod=' + pn

    r = requests.get(url, timeout=10)
    if r.ok:
        json_data = r.text
        dic_data = json.loads(json_data)
        '''
        {"hostList":[{"name":"eu1-db1-9-lon","kingdom":"LON","pod":"EU1","superPod":"LON-SP9","coolanID":"59e8f7b396b57c4a80bcd0be","coolanStatus":"ACTIVE","cpuModel":"Intel(R) Xeon(R) CPU E5-2699 v3 @ 2.30GHz","role":"db","status":"Active","statusSource":"iDB/AFD/Tech Asset","model":"HEWLETT PACKARD - PROLIANT - DL380 Gen9 2699V3 - 17.1 DB SKU 8SFF","isDR":false,"isVM":false,"osName":"Oracle Linux Server","osMajorVersion":"6","osPatchVersion":"10","kernelVersion":"4.1.12-124.24.1.el6uek.x86_64","macAddress":"5CB901D44BF8","serialNumber":"CZ36114C55","sfdcReleaseVersion":"2019.0825","estatesRole":"","ipAddress":"","puppetReleaseVersion":"20191107070721891"},{"name":"eu1-db1-5-frf","kingdom":"FRF","pod":"EU1","superPod":"FRF-SP1","coolanID":"58ef68141a9648051dd686ee","coolanStatus":"ACTIVE","cpuModel":"Intel(R) Xeon(R) CPU E5-2699 v3 @ 2.30GHz","role":"db","status":"Active","statusSource":"iDB/AFD/Tech Asset","model":"HEWLETT PACKARD - PROLIANT - DL380 Gen9 2699V3 - 17.1 DB SKU 8SFF","isDR":false,"isVM":false,"osName":"Oracle Linux Server","osMajorVersion":"6","osPatchVersion":"10","kernelVersion":"4.1.12-124.24.1.el6uek.x86_64","macAddress":"5CB901D92EC0","serialNumber":"CZ36114BRY","sfdcReleaseVersion":"2019.0825","estatesRole":"db","ipAddress":"10.248.156.8","puppetReleaseVersion":"20191107070721891"},
        '''
        # Returns a list of name and isDR value.  Example: ['eu1-db-1-frf', 'False']
        host_list = [[h.get(x) for x in ['name', 'isDR']] for h in dic_data['hostList']]
        #Sort by 3rd field, delimited by -, which is a number and sort as integer not as a string
            #Example: eu1-db1-2-frf.  Third field is 2.
        host_list.sort(key=lambda x: int(x[0].split('-')[2]))
        # Sort by 4th field which is dc or data center.
        host_list.sort(key=lambda x: x[0].split('-')[3])
        # Sort by 2nd field which is db type.  Example: db1 or dgdb1
        host_list.sort(key=lambda x: x[0].split('-')[1])
        pri_hosts = []
        dr_hosts = []
        for h_info in host_list:
            if h_info[1] == False:
                pri_hosts.append(h_info[0])
            else:
                dr_hosts.append(h_info[0])

    print('-' * 80)
    print('=== Primary for {} ==='.format(pn))
    for pri_host in pri_hosts:
        print(pri_host)
    print('\n')
    print('=== DR for {} ==='.format(pn))
    for dr_host in dr_hosts:
        print(dr_host)
    print('\n')

    print('=== Total Number of hosts for {}: {} ==='.format(pn, len(dic_data['hostList'])))
    print('=== Total Primary hosts for {}: {} ==='.format(pn, len(pri_hosts)))
    print('=== Total DR hosts for {}: {} ===\n'.format(pn, len(dr_hosts)))
