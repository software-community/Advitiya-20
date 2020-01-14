import requests
import os

def sendNotification(title, message):
    headers = {'Content-type': 'application/json',
               'Authorization': 'key=' + os.environ.get('FCM_APIKEY', '')}
    postdata = {
        
            "notification":
            {
                "body": message,
                "title": title
            },
            "priority": "high",
            "data":
            {
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            },
            "condition": "!('anytopicyoudontwanttouse' in topics)"
        
    }
    r = requests.post('https://fcm.googleapis.com/fcm/send', json = postdata, headers = headers)