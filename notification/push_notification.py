import helper
import gcm
import random
import time
import datetime
import notification_decision

key = helper.key


def send(notification_id, user_id, k=None, source='application'):

    devices = get_active_mobile_devices(user_id)

    should_push = notification_decision.count_of_push_notifications_sent(user_id=user_id) \
                                     <= config.GLOBAL_PUSH_NOTIFICATION_DAY_LIMIT

    notification = Notification.query.get(notification_id)



    ''' Only if the user has valid devices to be pushed to and is
    under global limit for the same'''

    if len(devices) and should_push:
        print 'Still under limits for number of daily notifications'
        k = key[notification.type] if k is None else k

        group_id = '-'.join([str(notification.type), str(notification.object_id)])
        from controllers import get_item_id

        for device in devices:
            print 'Found valid devices for push notifications'


            user_push_notification = UserPushNotification(notification_id=notification_id,
                                                              user_id=user_id,
                                                              device_id=device.device_id,
                                                              push_id=device.push_id,
                                                              added_at=datetime.datetime.now(),
                                                              pushed_at=datetime.datetime.now(),
                                                              clicked_at=None,
                                                              source=source,
                                                              cancelled=False,
                                                              result=None,
                                                              id=get_item_id())
            db.session.add(user_push_notification)
            db.session.commit()
            payload = {
                            "user_to": user_id,
                            "type": 1,
                            "id": user_push_notification.id,
                            "notification_id": notification.id,
                            "heading": k['title'],
                            "text": notification.text.replace('<b>', '').replace('</b>', ''),
                            "styled_text": notification.text,
                            "icon_url": notification.icon,
                            "cover_image": None,
                            "group_id": group_id,
                            "link": notification.link,
                            "deeplink": notification.link,
                            "timestamp": int(time.mktime(user_push_notification.added_at.timetuple())),
                            "seen": False,
                            "label_one": k['label_one'],
                            "label_two": k['label_two']
                        }

            print 'pushing gcm for android'
            gcm_sender = GCM()
            gcm_sender.send_message([device.push_id], payload)




def get_active_mobile_devices(user_id):

    devices = AccessToken.query.filter(AccessToken.user == user_id, AccessToken.active==True,
                             AccessToken.push_id != None).all()
    return devices





class GCM():

    def __init__(self, api_key=config.GCM_API_KEY):
        self.gcm = gcm.GCM(api_key)

    def send_message(self, gcm_ids, data):
        self.gcm.json_request(registration_ids=gcm_ids, data=data)


