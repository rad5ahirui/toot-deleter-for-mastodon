#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import requests

base_url = 'https://mstdn.jp' # Set your instance's URL.

def get_access_token(filename):
    with open(filename) as f:
        access_token = f.readline().rstrip()
    return access_token

def get_user_toots(session, user_id):
    r = session.get(f'{base_url}/api/v1/accounts/{user_id}/statuses')
    r.raise_for_status()
    return r.json()

def delete_status(session, status_id):
    r = session.delete(f'{base_url}/api/v1/statuses/{status_id}')
    r.raise_for_status()

def main():
    user_id = '12345' # Set your user id.
    access_token = get_access_token('access_token.txt')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'curl/7.67.0'
    }
    session = requests.Session()
    session.headers.update(headers)
    interval = 62
    while True:
        statuses = get_user_toots(session, user_id)
        if len(statuses) == 0:
            break
        print(f'{len(statuses)} statuses retrieved')
        time.sleep(2)
        for status in statuses:
            status_id = status['id']
            print(f"Deleting {status_id}: {status['content']}")
            delete_status(session, status_id)
            time.sleep(interval)
        print(f'{len(statuses)} statuses deleted')
    print('Done')

if __name__ == '__main__':
    main()
