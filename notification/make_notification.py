from models import User, Question, Notification, Post, Upvote, \
                   Follow, UserNotificationInfo, Comment
from database import get_item_id
from app import db
from configs import config
from notification import helper, user_notification as un, notification_decision
from sqlalchemy.orm.exc import NoResultFound

import datetime

key = helper.key


def notification_logger(nobject, for_users, manual=False, created_at=datetime.datetime.now(),
                        list_type='me', push_at=None,k=None):

    notification = Notification(type=nobject['notification_type'], text=nobject['text'],
                                link=nobject['link'], object_id=nobject['object_id'],
                                icon=nobject['icon'], created_at=created_at,
                                manual=manual, id=get_item_id())
    db.session.add(notification)
    db.session.commit()

    un.add_notification_for_user(notification_id=notification.id, for_users=for_users,
                                 list_type=list_type,
                                 push_at=push_at,k=k)
    return notification




def user_profile_request(user_id, request_for, request_id, request_type=config.REQUEST_TYPE):


    users = User.query.filter(User.id.in_([user_id, request_for])).all()

    for u in users:
        if u.id == user_id:
            request_by = u
        if u.id == request_for:
            requested = u

    k = key[request_type]

    nobject = {
        'notification_type': request_type,
        'text': helper.user_profile_request(requester_name=request_by.first_name),
        'icon': request_by.profile_picture,
        'link': k['url'] % request_for,
        'object_id': request_id
    }


    notification_logger(nobject=nobject, for_users=[requested.id], push_at=datetime.datetime.now())

