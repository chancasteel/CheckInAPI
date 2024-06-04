import config
import requests
import sys 
import time
import logging
from reportlab.lib import colors
from reportlab.lib.enums import *
from  reportlab.graphics.shapes import *
from reportlab.lib.pagesizes import *
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import *
import time

timestr = time.strftime("%m-%d-%Y-%H:%M:%S")
logging.basicConfig(filename=f'comment_post_{timestr}.log', filemode='w', level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


def main(file_url, ticket_url):
    logging.debug(f"Attempting to post comment on ticket url({ticket_url})")
    response = requests.post(
        url=f"{config.credentials['url']}/api/v1.0/tickets/{ticket_url}/activities/new",
        headers = config.headers,
        json={
            "TicketId" : ticket_url,
            "ActivityItems": [
                {
                    "$type": "Spark.Shared.Models.TicketActivityComment, Spark.Shared",
                    "TicketActivityTypeId": 6,
                    "Comments": f"Please fill out the Equipment Check-In Sheet linked here: {file_url}"
                }
            ],
            "IsPublic": True,
            "WaitForResponse" : True,
            "TicketWasUpdated": True
        }
    )
    if response.status_code != 201:
        logging.debug(f"Failed to post {file_url} comment on ticket")
        return
    logging.debug(f"{file_url} Comment successfully posted on ticket")
    return file_url

if __name__ == "__main__":
    sharepoint_url = sys.argv[1]
    file_path = "" + sys.argv[2] + "_ticketid.txt"
    try:
        f = open(file_path, "r")
        ticket_url = f.read()
        f.close()
        print(main(sharepoint_url, ticket_url))
    except:
        logging.debug(f'Could not read ticket_url file at path {file_path}')
    print("Done")

