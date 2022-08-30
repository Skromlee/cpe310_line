from flask import Flask, request, make_response, jsonify
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dateutil.parser import parse
import os

cred = credentials.Certificate('./kl888-88f79-firebase-adminsdk-7vr01-7101c2a832.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
log = app.logger

@app.route("/", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    # Action Switcher
    if action == 'reservation.reservation-yes':
        res = create_reservation(req)
    if action == 'view-set':
        res = view_set(req)
    else:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))


def create_reservation(req):
    parameters = req.get('queryResult').get('parameters')
    name = parameters.get('name')
    pro_id = parameters.get('pro_id')
    time = parse(parameters.get('time'))
    date = parse(parameters.get('date'))

    date_ref = db.collection(u'date').document(str(date.date()))
    date_ref.collection(u'reservations').add({
        u'name': name,
        u'pro_id': pro_id,
        u'time': date.replace(hour=time.hour, minute=time.minute)
    })
    return 'เรียบร้อยละค่า ขอบคุณนะคะที่ให้ความสำคัญกับเรา เดี๋ยวจะมีฝ่ายประชาสัมพันธติดต่อกลับไปนะครับ'

combo_set_resp = {
    "type-a": "บ้านประเภท A จะมีราคาประมาณ 7 - 11 ล้านบาท โดยจะมีพื้นที่ใข้สอยโดยประมาณอยู่ที่ 300 ตร.ม. โดยเมื่อซื้อกับเราจะแถม แอร์ทุกห้อง รวมทั้ง ฟรีค่าโอน และ จดจำนอง",
    "type-b": "บ้านประเภท B จะมีราคาประมาณ 1 - 3 ล้านบาท โดยจะมีพื้นที่ใข้สอยโดยประมาณอยู่ที่ 110 - 130 ตร.ม. โดยเมื่อซื้อกับเราจะแถม แอร์ทุกห้อง รวมทั้ง ฟรีค่าโอน และ จดจำนอง",
    "type-c": "บ้านประเภท C จะมีราคาประมาณ 4 - 7 ล้านบ้าน โดยจะมีพื้นที่ใข้สอยโดยประมาณอยู่ที่ 180 - 220 ตร.ม. โดยเมื่อซื้อกับเราจะแถม แอร์ทุกห้อง รวมทั้ง ฟรีค่าโอน และ จดจำนอง"
}

def view_set(req):
    parameters = req.get('queryResult').get('parameters')
    combo_set = parameters.get('combo-set')
    return combo_set_resp[combo_set]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))