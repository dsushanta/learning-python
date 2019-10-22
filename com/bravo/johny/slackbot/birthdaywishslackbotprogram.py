import random
from slack import WebClient
from datetime import date, datetime


def getTodaysDay():
    today = date.today()
    return today.day


def getTodaysMonth():
    today = date.today()
    return today.month


def getDisplayNamesOfBirthdayPersons():
    slack_client = WebClient(BOT_TOKEN)
    slack_client_without_bot_token = WebClient(AUTH_TOKEN)
    slack_client.rtm_connect()
    user_list_str = slack_client.users_list()
    users = user_list_str.get('members')
    for user in users:
        try:
            user_id = user.get('id')
            name = user.get('name')
            user_info = slack_client_without_bot_token.users_profile_get(user=user_id)
            bday_string = user_info.get('profile').get('fields').get('XfNVGXDAS1').get('value')
            date_object = datetime.strptime(bday_string, BIRTHDAY_FORMAT).date()
            day = date_object.day
            month = date_object.month
            if month == getTodaysMonth() and day == getTodaysDay():
                birthday_persons.append('<@'+user_id+'>')
        except AttributeError:
            print('User %s has not set birth date' % name)
            continue
        except ValueError:
            print('Invalid date format : %s , moving on ' % bday_string)
            continue


def postBirthdayWishes():
    slack_client = WebClient(BOT_TOKEN)
    slack_client.rtm_connect()
    for birthday_person in birthday_persons:
        random_number = random.randint(0, len(BIRTHDAY_WISHES)-1)
        birthday_wish = BIRTHDAY_WISHES[random_number]
        message = birthday_wish % birthday_person
        slack_client.chat_postMessage(channel=CHANNEL_NAME, text=message)


AUTH_TOKEN = 'xoxp-10189127591-646277697476-801784336784-8bc2c7ea006c6ac38a1239c67e2c3d30'
BOT_TOKEN = 'xoxb-10189127591-790313797619-lnFEWMw8bQuTw812dHM0NIGm'
BIRTHDAY_FORMAT = '%Y-%m-%d'
CHANNEL_NAME = 'birthdaywishingslackbot'
BIRTHDAY_WISHES = [
    'I hope your special day will bring you lots of happiness, love, and fun. You deserve them a lot. Enjoy! :birthday: - %s ',
    'May this special day bring you endless joy and tons of precious memories! :birthday: - %s ',
    'Happy birthday! Here’s to a bright, healthy and exciting future! :birthday: - %s ',
    'May your birthday be full of happy hours and special moments to remember for a long long time! :birthday: - %s ',
    'I wish you to enjoy your special day, relax and let yourself be spoiled, you deserve it! :birthday: - %s '
]
birthday_persons = []

getDisplayNamesOfBirthdayPersons()
postBirthdayWishes()
