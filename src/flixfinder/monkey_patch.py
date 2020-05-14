"""

Django 2.2 Monkey Patch.

This is necessary because of Django uses an undocumented API from MySQL.
Google App Engine does allow us to use the official MySQL client. So we're using an unofficial MySQL client,
Our client only gives compatibility for documented features.
Django has refused to fix this within the 2.2 branch.

This monkey patch removes the broken code.
Thankfully it isn't necessary functionality anyway.

@author Brian Wojtczak

"""

import django.db.backends.mysql.operations


def last_executed_query(self, cursor, sql, params):
    return None


django.db.backends.mysql.operations.DatabaseOperations.last_executed_query = last_executed_query
