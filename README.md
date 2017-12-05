Facebook Apps Manager
===============

Introduction
------------

The script [fb-apps-manager/manage-role.py](https://github.com/fabiomsouto/fb-apps-manager/blob/master/fb-apps-manager/manage-role.py) manages a user's role in all Facebook Apps.

First, the script makes a request with the provided cookie to the page [https://developers.facebook.com/tools/accesstoken/](https://developers.facebook.com/tools/accesstoken/) and gets the configuration of the applications. For each application, it allows you to add or remove a user to the applications roles.

Usage
-----

Invoke the script providing the requested parameters. As an example, imagining you want to add Mark Zuckerberg as a tester to all the apps of an administrator:

	$ ./manage-role.py 12345 'thisisacookie' add 4 'testers'

Calling the script with `-h` will provide you all the possible parameters.