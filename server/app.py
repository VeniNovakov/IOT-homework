from flask import Flask, request
import pysondb

db = pysondb.getDb('db/data.json')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all_links():
    return [
            {
                'path': '/',
                'method': 'GET',
                'description': 'get app link map'
                },
            {
                'path': '/data', 
                'method': 'POST', 
                'description': 'post an entry of detected motion {"timestamp": integer unix time, "deviceId": integer}'
                },
            {
                'path': '/data/{device-id}', 
                'method': 'GET',
                'description': 'get information for the device with given device-id'
                },
            {
                'path': '/stats', 
                'method': 'GET',
                'description': 'get the last activated sensor, the most activated sensor and the sensor with most time since activation'
                },
        ] 

@app.route('/data', methods=['POST'])
def post_data():

    body = request.get_json(force=True)

    timestamp = body['timestamp']
    deviceId = body['deviceId']

    _yellow = '\u001b[33m'
    _cyan   = '\u001b[36m'
    _end    = '\u001b[0m'
    print(f'{_yellow}POST{_end} localhost:3000{_cyan}/data{_end}] timestamp: {timestamp}, deviceId: {deviceId}')

    if device := db.getByQuery(query={"deviceId": deviceId}):
        device[0]['timestamps'].append(timestamp)
        device[0]['timestamps'] = sorted(device[0]['timestamps'], reverse = True)

        db.updateById(pk=device[0]['id'], new_data={"deviceId": device[0]['deviceId'], "timestamps": device[0]['timestamps']})
    else:
        db.add({"deviceId": deviceId, "timestamps": [timestamp]})
    
    return 'success'



@app.route('/data/<motion_sensor_id>')
def get_sensor_values(motion_sensor_id):
    return db.getByQuery(query={"deviceId": motion_sensor_id})

@app.route('/stats')
def get_sensors_stats():
    devices = db.getAll()
    
    if len(devices) == 0:
        return 'No devices in the database', 400

    last_activated = devices[0]
    most_activated = devices[0]
    most_time_since_activation = devices[0]

    for i in devices:
        if last_activated['timestamps'][0] < i['timestamps'][0]:
            last_activated = i
        if len(most_activated['timestamps']) < len(i['timestamps']):
            most_activated = i
        if most_time_since_activation['timestamps'][0] > i['timestamps'][0]:
            most_time_since_activation = i
  
    return {
        "last activated": last_activated,   
        "most activated": most_activated,    
        "most time since activation": most_time_since_activation
    }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
