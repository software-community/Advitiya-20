import requests
import os
from firebase_admin import credentials

try:
    cred = credentials.Certificate("service-account.json")
    access_token_info = cred.get_access_token().access_token
except:
    access_token_info = ''

def sendNotification(title, message):
    headers = {'Content-type': 'application/json',
               'Authorization': 'Bearer ' + access_token_info}
    postdata = {
        "message": {
            "condition": "!('anytopicyoudontwanttouse' in topics)",
            "notification": {
                "title": title,
                "body": message
            },
            "data":
            {
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            },
            "webpush": {
                "fcm_options": {
                    "link": "https://play.google.com/store/apps/details?id=com.softcom.advitiya"
                }
            }
        }
    }
    r = requests.post('https://fcm.googleapis.com//v1/projects/advitiya2020-719da/messages:send',
                      json=postdata, headers=headers)
