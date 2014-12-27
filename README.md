Facebook Apps Manager
===============

Introduction
------------

The script [fb-apps-manager/add-role.py](https://github.com/ianmonge/fb-apps-manager/blob/master/fb-apps-manager/add-role.py) adds a user in all Facebook Apps as a new role.

First, the script makes a request with the provided cookie to the page [https://developers.facebook.com/tools/accesstoken/](https://developers.facebook.com/tools/accesstoken/) and gets the configuration of the applications. For each application, it adds the new user as a new role in each application.

Usage
-----

Edit file [fb-apps-manager/add-role.py](https://github.com/ianmonge/fb-apps-manager/blob/master/fb-apps-manager/add-role.py) and update the variables:
* **fb_admin_user_id**: Facebook user id of the administrator that has privileges to add a new role.
* **fb_user_id_to_add**: Facebook user id of the user that is going to be added to the apps.
* **cookie_xs**: Cookie "xs" of the administrator when access to the page of Access Tokens.
