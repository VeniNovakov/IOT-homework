from flask import Flask, request
import pysondb

db = pysondb.getDb('../db/data.json')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all_links():

    print('GET / -> get refs within the site'+'\n'
    'POST /data -> post an entry of detected motion {"timestamp": integer unix time, "deviceId": integer}'+'\n'+
    'GET /data/<motion_sensor_id> -> get info of a device with deviceId motion_sensor_id'+'\n'+
    'GET /stats -> get the last device that has detected motion, the most activated sensor and the device with most time since activation'+'\n')
    return 'success'

@app.route('/data', methods=['POST'])
def post_data():

    body = request.get_json(force=True)

    timestamp = body['timestamp']
    deviceId = body['deviceId']

    if device := db.getByQuery(query={"deviceId": deviceId}):
        device[0]['timestamps'].append(timestamp)
        device[0]['timestamps'] = sorted(device[0]['timestamps'], reverse=True)

        db.updateById(pk=device[0]['id'], new_data={"deviceId": device[0]['deviceId'], "timestamps":device[0]['timestamps']})
    else:
        db.add({"deviceId": deviceId, "timestamps":[timestamp]})
    
    return 'success'



@app.route('/data/<motion_sensor_id>')
def get_sensor_values(motion_sensor_id):
    motion_sensor_id = int(motion_sensor_id)
    device = db.getByQuery(query={"deviceId": motion_sensor_id})

    return 'success'

#last activated, most actived, least activated
@app.route('/stats')
def get_sensors_stats():
    devices = db.getAll()
    last_activated = devices[0]
    most_activated = devices[0]
    naj_mnogo_vreme_neaktiviran = devices[0]
    for i in devices:
        if last_activated['timestamps'][0] < i['timestamps'][0]:
            last_activated = i
        if len(most_activated['timestamps']) < len(i['timestamps']):
            most_activated = i
        if naj_mnogo_vreme_neaktiviran['timestamps'][0] > i['timestamps'][0]:
            naj_mnogo_vreme_neaktiviran = i
        
    print("last activated: ",last_activated)    
    print("most activated: ", most_activated)    
    print("most time since activation: ", naj_mnogo_vreme_neaktiviran)    
    return 'success'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)