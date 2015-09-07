from configs import config
key = {

    'intro-video-request':{
         'title': 'You are in demand!',
         'text': '<requester_name> just asked you for an intro video.',
         'url': config.WEB_URL + '/u/   %s',
         'day-limit': 1,
         'label_one':'',
         'label_two': ''
    }
}




def user_profile_request(requester_name):
    text = key['intro-video-request']['text']
    return text.replace('<requester_name>', requester_name)

