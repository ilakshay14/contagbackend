import urllib2
import urllib


class SMS():
    def send(self, mobile_number, sms_text):
        url_parameters = urllib.urlencode({

            "pass": "password",
            "sender": "contag",
            "priority": "ndnd",
            "phone": mobile_number,
            "text": sms_text
        })

        url = "http://bhashsms.com/api/sendmsg.php?user=sms@contag&"

        url += url_parameters

        print url

        response = urllib2.urlopen(url).read()

        return response
