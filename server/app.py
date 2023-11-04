from flask import Flask, request
import pysondb

db = pysondb.getDb('../db/data.json')

most_used_device = '' 
most_used_device_count = 0
latest_used_device=''

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all_links():
    return 200

@app.route('/data', methods=['POST'])
def post_data():

    body = request.form

    timestamp = body['timestamp']
    deviceId = body['deviceId']
    print('....>.................................................................')

    latest_used_device = deviceId
    try:
        device = db.getByQuery(query={"deviceId": deviceId})
        device['timestamps'].append(timestamp)

        db.update(device)
    except:
        db.add({"deviceId": deviceId, "timestamps":[timestamp]})
    return 'success'



@app.route('/data/<motion_sensor_id>')
def get_sensor_values(motion_sensor_id):
    entries = db.getAll({'deviceId': motion_sensor_id})
    print(entries)
    pass

#last activated, most actived, least activated
@app.route('/stats')
def get_sensors_stats():
    sensors = db.getAll()
    last_activated = sensors[len(sensors)-1]

    most_activated = db
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)