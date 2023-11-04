import requests

import random
import threading
import time

SERVER_PORT = 3000
NUM_THREADS = 10

def monitor_data(identifier: str) -> None:
    request_data: dict = {      \
        'timestamp': 0,         \
        'deviceId': identifier, \
    }

    while True:
        request_data['timestamp'] = int(time.time())
        # NOTE: potentially might need to check if the data submit was successful
        requests.post(f'http://localhost:{SERVER_PORT}/data', json=request_data)
        time.sleep(random.randint(5, 15))

if __name__ == '__main__':
    threads: list = []

    for i in range(NUM_THREADS):
        identifier: str = f'monitor_device_{i+1}'
        threads.append( \
                threading.Thread(target=monitor_data, args=[identifier]) \
            ) 

    for t in threads:
        t.start()
        time.sleep(0.25)
