from flask import Flask, request
import pysondb

db = pysondb.getDb('../db/data.json')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all_links():
    paths = ['/', '/data', '/data/<motion_sensor_id>', '/stats']
    methods = ['GET', 'POST', 'GET', 'GET']
    description = ['get refs within the site',
                    'post an entry of detected motion {"timestamp": integer unix time, "deviceId": integer}',
                    'get info of a device with deviceId motion_sensor_id',
                    'get the last device that has detected motion, the most activated sensor and the device with most time since activation'
                    ]
    json=[]

    for i in range(len(paths)):
        json.append({'path': paths[i], 'method': methods[i], 'description': description[i]})

    return json

@app.route('/data', methods=['POST'])
def post_data():

    body = request.get_json(force=True)

    timestamp = body['timestamp']
    deviceId = body['deviceId']

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