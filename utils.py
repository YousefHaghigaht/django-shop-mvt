from django.contrib.auth.mixins import UserPassesTestMixin

from kavenegar import *

def send_otp_code(phone_number,code):
    try:
        api = KavenegarAPI('Your APIKey')
        params = {
            'sender': '',  # optional
            'receptor': {phone_number},  # multiple mobile number, split by comma
            'message': f'Your code: {code}',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


class IsAdminMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

