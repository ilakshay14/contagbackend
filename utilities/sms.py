import urllib2
import urllib


class SMS():

    def send(self, mobile_number, sms_text):
        url_parameters = urllib.urlencode({

            "pass": "Revolution",
            "sender": "Contag",
            "priority": "ndnd",
            "phone": mobile_number,
            "text": sms_text
        })

        url = "http://bhashsms.com/api/sendmsg.php?user=pitstop&"

        url += url_parameters

        print url

        response = urllib2.urlopen(url).read()

        return response
