#!/usr/bin/env python
#ENTER API CREDITIALS
credentials = dict(
    url = "",
    authkey = "",
    siteid = ""
)

headers = dict(
    Authorization = f"Bearer {credentials['authkey']}",
    SiteId = credentials["siteid"],
    Client = 'ApiClient'
)

ticket =  dict(
    id = '',
    username = '',
    location =  '',
    fullname = '',
    userid = '',
    ticket_id_url = '',
    pending_view = ''
)

#ADD IMAGE PATH
path = dict(
    image = '',
    csv = '',
    pdf = '',
)
