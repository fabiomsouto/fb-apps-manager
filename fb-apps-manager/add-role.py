
import requests
import bs4
import sys

# TO EDIT
fb_admin_user_id = '12345678'
fb_user_id_to_add = '987654321'
cookie_xs = '6asdfgbvcbsfgdh3A2%3A1418745315%3A1711'
#  END TO EDIT

fb_access_tokens_url = "https://developers.facebook.com/tools/accesstoken/"
fb_graph_url = "https://graph.facebook.com/"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def getHtmlOfFbAccessTokensPage():
    cookies = {
        'c_user': fb_admin_user_id,
        'xs': cookie_xs,
    }

    response = requests.get(fb_access_tokens_url, allow_redirects=False, cookies=cookies)

    if response.status_code != requests.codes.ok:
        print bcolors.FAIL + 'HTML Response is not correct' + bcolors.ENDC
        sys.exit(1)

    html = response.text

    return html

def getAppsConfigsFromHtml(html):
    """Parses the HTML getting the APPs configuration"""
    soup = bs4.BeautifulSoup(html)

    apps = soup.select('div + table')

    access_tokens = {}

    for app in apps:
        app_name = app.parent.find('div').get_text()

        user_token_td = app.select('td:nth-of-type(2) code')
        if not len(user_token_td):
            user_token = None
        else:
            user_token_td = user_token_td[0]
            user_token = user_token_td.get_text()

        app_token_td = app.select('td:nth-of-type(4) code')[0]
        app_token = app_token_td.get_text()

        app_id = app_token.split('|')[0]

        access_tokens[app_id] = {
            'app_id': app_id,
            'app_name': app_name,
            'app_token': app_token,
            'user_token': user_token,
        }

    return access_tokens

def addRole(app_config):
    print bcolors.OKBLUE + '{} {}'.format(app_config['app_id'], app_config['app_name']) + bcolors.ENDC

    if app_config['user_token'] == None:
        print bcolors.WARNING + "\tAdmin user hasn't admin permissions on this application" + bcolors.ENDC
        return

    url = fb_graph_url + app_config['app_id'] + "/roles?access_token=" + app_config['user_token']
    data = {
        "user": fb_user_id_to_add,
        "role": "testers",
    }

    response = requests.post(url, data=data)

    if response.status_code != requests.codes.ok:
        print "\tError adding user to appHTML Response is not correct"
        print "\tMessage: " + response.text
        sys.exit(1)

    print bcolors.OKGREEN + "\tAdded user" + bcolors.ENDC

if __name__ == "__main__":
    html = getHtmlOfFbAccessTokensPage()

    apps_configs = getAppsConfigsFromHtml(html)

    for app_id in apps_configs:
        addRole(apps_configs[app_id])
