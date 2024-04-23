#!/usr/bin/env python
credentials = dict(
    url = "https://duncanvilleisd.incidentiq.com",
    authkey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjNzdhNjg2My1jMTNkLTRmMzktYTk5NS01ZmUzN2FjM2Y5MTAiLCJzY29wZSI6Imh0dHBzOi8vZHVuY2FudmlsbGVpc2QuaW5jaWRlbnRpcS5jb20iLCJzdWIiOiJhYmUzMWQ3Ny1lMDVhLTQyYjctYmNlNC02NGUwY2M3ODAxOTMiLCJqdGkiOiIxNjQ3ZmE0NS1kZWQ2LWVjMTEtYjY1Ni0wMDE1NWQ5ODAzZjEiLCJpYXQiOjE2NTI5MDEwNzQuMjMzLCJleHAiOjE3NDc1OTU0NzQuMjR9.AUpuzI82trLWMDVUbg4PlGn3gyDwYNPevdzYSlh3iWE",
    siteid = "c77a6863-c13d-4f39-a995-5fe37ac3f910"
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
    pending_view = 'e47dbd75-49fb-ee11-aaf0-000d3a0e23bd'
)

path = dict(
    image = 'DvilleLogo.png',
    csv = '',
    pdf = '',
)

#Finish Config and Split Comment to seperate Python