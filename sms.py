# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
from datetime import datetime
import socket
import errno 


##########################################################################
#                       Public Functions                                 #
##########################################################################
def send_receipt(phone_number, quantity, beer, total):
    """
    Sends a receipt SMS message to the user who just purchased beer

    Args:
        phone_number (string):
            The phone number that the SMS message is to be sent to.  Should be
            of format "+1XXXXXXXXX".  For example, if you want to text the
            number (412) 523-6164, the arg should be "+14125236164"

        quantity (int):
            The number of oz of beer the user bought

        beer (string):
            The kind of beer the user bought (i.e. "Blue Moon", "Bud Light",
            "Shock Top", etc...)

        total (float):
            The total amount that the user is to be charged

    Example:
    To send an SMS to (412) 523-6164 saying they just bought 12 oz of Blue Moon
    and are going to be charged $1.25, do the following:

        send_receipt("+14125236164", 12, "Blue Moon", 1.25)

    Return:
    True if message was sent succesfully.  False if otherwise

    """
    curr_time = str(datetime.now())
    msg_body = "Purchased {0} oz of {1} for a total of ${2} at {3}"\
        .format(quantity, beer, total, curr_time)
    __send(phone_number, msg_body)


def send_pin(phone_number, name, pin):
    """
    Sends an SMS message to the user with their PIN number

    Args:
        phone_number (string):
            The phone number that the SMS message is to be sent to.  Should be
            of format "+1XXXXXXXXX".  For example, if you want to text the
            number (412) 523-6164, the arg should be "+14125236164"

        name (string):
            The name of the person receiving the text message

        pin (int):
            The PIN number for the user

    Example:
    The following line of code:

        send_pin("+14125236164", "Nick", 1234)

    will send a text message to (412) 523-6164 with the contents:
    'Welcome Nick!  Your PIN # is 1234'

    Return:
    True if message was sent succesfully.  False if otherwise

    """
    msg_body = "Welcome {0}! Your PIN # is {1}".format(name, pin)
    __send(phone_number, msg_body)


###########################################################################
#                       Private Functions                                 #
###########################################################################
def __send(to_number, msg_body):
    # Find these values at https://twilio.com/user/account
    account_sid = "AC83492826650db9d730643243a37dc679"
    auth_token = "bb8fd116943adb81441763adf7be5bea"
    client = TwilioRestClient(account_sid, auth_token)

    from_number = "+14122468519"  # This is a valid Twilio number

    try:
        message = client.messages.create(to=to_number,
                                         from_=from_number,
                                         body=msg_body)

        # If there was an error sending the message, the errorcode
        #   attribute is set
        if hasattr(message, 'errorcode'):
            return False
        else:
            return True

    except socket.error, v:
        errorcode = v[0]
        if errorcode == errno.ECONNREFUSED:
            print "Sorry, Twilio couldn't connect to its servers. " \
                  "Please try again"
