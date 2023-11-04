import requests

import threading
import time

_SERVER_PORT = 3000
_NUM_THREADS = 10

def monitor_data(identifier: str) -> None:
    request_data: dict = {       \
        'timestamp': 0,          \
        'deviceId': identifier, \
    }

    while True:
        request_data['timestamp'] = int(time.time())
        # NOTE: potentially might need to check if the data submit was successful
        requests.post(f'https://localhost:{_SERVER_PORT}/data', data=request_data)
        time.sleep(10)

if __name__ == '__main__':
    threads: list = []

    for i in range(_NUM_THREADS):
        identifier: str = f'monitor_device_{i+1}'
        threads.append( \
                threading.Thread(target=monitor_data, args=[identifier]) \
            ) 

    for t in threads:
        t.start()
