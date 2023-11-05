#!/usr/local/bin/python3.10
import requests

import random
import threading
import time

SERVER_PORT = 3000
NUM_THREADS = 100

# a debug logger
def dbg(timestamp: str, device_id: str) -> None:
    _yellow = '\u001b[33m'
    _cyan   = '\u001b[36m'
    _end    = '\u001b[0m'
    print(f'{_yellow}POST{_end} server:3000{_cyan}/data{_end}] timestamp: {timestamp}, device_id: {device_id}')

def monitor_data(identifier: str) -> None:
    request_data: dict = {      \
        'timestamp': 0,         \
        'deviceId': identifier, \
    }

    while True:
        request_data['timestamp'] = int(time.time())
        # NOTE: could check if the data submit was successful
        requests.post(f'http://server:{SERVER_PORT}/data', json=request_data)
        time.sleep(random.randint(5, 15))
        
        dbg(request_data['timestamp'], request_data['deviceId'])

if __name__ == '__main__':
    threads: list = []
    # wait so the server can start during deployment
    time.sleep(5)

    for i in range(NUM_THREADS):
        identifier: str = f'monitor_device_{i+1}'
        threads.append( \
                threading.Thread(target=monitor_data, args=[identifier]) \
            ) 

    for t in threads:
        t.start()
        time.sleep(0.25)
