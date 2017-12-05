#!/usr/bin/env python

import requests
import bs4
import sys
import argparse

###
# Facebook endpoints and configuration
##
fb_access_tokens_url = "https://developers.facebook.com/tools/accesstoken/"
fb_graph_url = "https://graph.facebook.com/"
fb_graph_url_version = "v2.11"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def getHtmlOfFbAccessTokensPage(fb_admin_id, cookie_xs):
    cookies = {
        'c_user': str(fb_admin_id),
        'xs': str(cookie_xs)
    }

    response = requests.get(fb_access_tokens_url, allow_redirects=False, cookies=cookies)

    if response.status_code != requests.codes.ok:
        print bcolors.FAIL + 'HTML Response is not correct' + bcolors.ENDC
        sys.exit(1)

    html = response.text

    return html

def getAppsConfigsFromHtml(html):
    """Parses the HTML getting the APPs configuration"""
    soup = bs4.BeautifulSoup(html, "html.parser")

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

def manageRole(app_config, action, role, fb_user_id):
    print bcolors.OKBLUE + '{} {}'.format(app_config['app_id'], app_config['app_name']) + bcolors.ENDC

    if app_config['user_token'] == None:
        print bcolors.WARNING + "\tAdmin user hasn't admin permissions on this application" + bcolors.ENDC
        return

    url = fb_graph_url + "/" + fb_graph_url_version + "/" + app_config['app_id'] + "/roles?access_token=" + app_config['user_token']
    data = {
        "user": fb_user_id,
        "role": role
    }

    if action == "add":
        response = requests.post(url, data=data)
    elif action == "remove":
        response = requests.delete(url, data=data)
    else:
        print "\tUnknown operation"
        system.exit(1)

    if response.status_code != requests.codes.ok:
        print "\tError while doing requested operation"
        print "\tMessage: " + response.text
        sys.exit(1)

    print bcolors.OKGREEN + "\t" + action.title() + " user to/from role " + role+ " was completed successfully" + bcolors.ENDC

def prepareArgs():
    parser = argparse.ArgumentParser(description="Allows you to manage Facebook user roles for a given administrator's applications in bulk")
    parser.add_argument('fb_admin_id', type=int, help="The Facebook app administrator ID (c_user cookie)")
    parser.add_argument('fb_admin_xs_cookie', help="The Facebook app administrator (xs cookie)")
    parser.add_argument('action', choices=['add', 'remove'], help="The operation you'd like to perform")
    parser.add_argument('fb_user_id', type=int, help="The user to give/remove role")
    parser.add_argument('role', choices=['administrators', 'developers', 'testers', 'insights users'], help="The role you want to add/remove to/from the user")
    return parser.parse_args()

if __name__ == "__main__":
    args = prepareArgs()

    fb_admin_id = args.fb_admin_id
    fb_user_id = args.fb_user_id
    cookie_xs = args.fb_admin_xs_cookie
    action = args.action
    role = args.role

    html = getHtmlOfFbAccessTokensPage(fb_admin_id, cookie_xs)

    apps_configs = getAppsConfigsFromHtml(html)

    for app_id in apps_configs:
        manageRole(apps_configs[app_id], action, role, fb_user_id)