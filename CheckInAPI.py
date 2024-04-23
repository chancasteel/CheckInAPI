import config
import csv
import requests
import sys 
import time
import csv
import datetime
import itertools
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

#Pulled from HTTP Request
timestr = time.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'CheckInAPI_{timestr}.log', filemode='w', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class MCLine(Flowable):
    """Creates a flowabale for a line that spans across the page
    
    Requires an input of width of line
    """
    def __init__(self, width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def __repr__(self):
        return "Line(w=%s)" % self.width

    def draw(self):
        """
        draw the line
        """
        self.canv.line(0, self.height, self.width, self.height)

class TextField(Flowable):
    def __init__(self, **options):
        Flowable.__init__(self)
        self.options = options
        # Use Reportlab's default size if not user provided
        self.width = options.get('width', 120)
        self.height = options.get('height', 36)
        self.fontSize = options.get('fontSize', 12)

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        form.textfieldRelative(**self.options)
        self.canv.restoreState()

def make_pdf(filename, username, fullName, location):
    """
    Creates a pdf using csv made earlier with username and assets in the template style
    for DuncanvilleISD with fillables for the employee
    """
    with open(filename,'r',newline='') as file:
        data = list(csv.reader(file))
    elements = []

    logging.info(f"Creating PDF using the following data:\n{data}")

    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']

    elements.append(Image(config.path['image'], 2.2 * inch, 2.2*inch))

    elements.append(Spacer(1,20))
    elements.append(Paragraph("<b>EQUIPMENT CHECK-IN SHEET</b>", 
        ParagraphStyle(
            name='Title',
            fontFamily='Helvetica', 
            fontSize=36,
            alignment=TA_CENTER)))
    elements.append(Spacer(1,30))
    elements.append(MCLine(8 * inch))
    elements.append(Spacer(1,25))

    dateLine = f'<b>Date</b>: {datetime.datetime.now().strftime("%B %d, %Y")}'
    userFullNameline = f'<b>This equipment was configured for:</b> {fullName}'
    locationLine = f'<b>Campus:</b> <b>{location}</b>'
    usernameLine = f'<b>Username:</b> <b>{username}</b>'
    dateSignLine = f'<b>Date: </b>'
    staffSigLine = f'<b>Departing Staff Signature:</b> '
    techMemSigLine = f'<b>Technology Staff Signature:</b> '

    elements.append(Paragraph(dateLine, styleNormal))
    elements.append(Paragraph(userFullNameline, styleNormal))
    elements.append(Paragraph(locationLine, styleNormal))

    elements.append(Spacer(1,12))

    elements.append(Paragraph(usernameLine, styleNormal))
    elements.append(Spacer(1,12))
    elements.append(Paragraph("<b>According to district records, the items listed below are district equipment that has been checked out to you and must be returned or the replacement cost will be required. <u>This only concerns the return of district materials and is NOT a release from employment.</u></b>", styleNormal))
    elements.append(Spacer(1, 15))

    LIST_STYLE = TableStyle(
        [('LINEABOVE', (0,0), (-1,0), 2, colors.blue),
        ('LINEBELOW', (0,0), (-1,0), 2, colors.blue),
        ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 2, colors.red),
        ('ALIGN', (1,1), (-1,-1), 'LEFT'),
        ('ALIGN', (4,1), (4,-1), 'CENTER'),
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold')]
    )


    for index, row in enumerate(data):
        for col, val in enumerate(row):
            data[index][col] = val.strip("'[]()")
    for row in range(1,len(data)):
        data[row][3] = TextField(name=f'cb_{row}', height=15, width=15, fontSize=8)

        
    t = Table(data)
    t.setStyle(LIST_STYLE)
    elements.append(t)

    elements.append(Spacer(1, 30))
    elements.append(Paragraph("<b>PLEASE NOTE: It is the employee's responsibility to retrieve his/her electronic data from the district's system before leaving the district. This includes email, items in the Google Drive website content from the teacher's site, and any staff development information in Eduphoria. This data will be deleted after the employee's last day.</b>", styleNormal))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph(dateSignLine,styleNormal))
    elements.append(TextField(name='date',tooltip='Date',height = 18))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph(staffSigLine, styleNormal))
    elements.append(TextField(name='exit_signature', tooltip='Staff Signature',height = 18, width = 320))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph(techMemSigLine, styleNormal))
    elements.append(TextField(name='tech_signature', tooltip='Tech Signature',height = 18, width = 320))

    doc = SimpleDocTemplate(config.path['pdf'], 
        pagesize=LETTER,
        topMargin=12, 
        rightMargin=12, 
        leftMargin=12,
        bottomMargin=6)
    doc.build(elements)

    logging.info(f"PDF created at {config.path['pdf']}")

def get_ids_for_view(view_id):
    """Searches a View for Tickets Already Sent to Exit Employees
    
    Returns a set of Ids for all Tickets in View
    """
    response = requests.post(
        url = f"{config.credentials['url']}/services/tickets/view/{view_id}/All?$s=20&$o=TicketPriority&$d=Descending",
        headers = config.headers,
    )
    sentTicketIDs = set()
    currSentTickets = response.json()
    for currTicket in currSentTickets['Items']:
        userID = currTicket['ForId']
        sentTicketIDs.add(userID)
    return sentTicketIDs

def get_assets_for_user(user_id):
    logging.info('Retrieving assets for user...')
    response = requests.get(
        url = f"{config.credentials['url']}/api/v1.0/assets/for/{user_id}",
        headers=config.headers
    )
    resp_json = response.json()
    if response.status_code not in (200, 201):
        logging.info('Failed connection to get assets')
        return
    else:
        logging.info('Assets retrieved for user')
        return resp_json

def form_assets_csv(resp_json):
    logging.info('Creating csv file...')
    config.path['csv'] = 'Docs/' + config.ticket['username'] + '_assets.csv'
    with open(config.path['csv'],'w',newline='') as newFile:
        writer = csv.writer(newFile)
        writer.writerow(['Asset Tag', 'Device Type', 'Purchase Price', 'Returned'])
        for item in resp_json['Items']: 
            price = '$' + '{:.2f}'.format(item['PurchasePrice']) if 'PurchasePrice' in item.keys() else ""
            writer.writerow([item['AssetTag'], item['Name'], price, 'Yes ? No'])
    logging.info(f"Created csv file at path {config.path['csv']}")

def ready_payload(ticketid):
    logging.info(f"Retrieving data from ticket id {ticketid}...")
    response = requests.post(
        url=f"{config.credentials['url']}/services/search",
        headers = config.headers,
        json={
            "Query": ticketid
        }
    )
    logging.info(response)
    resp_json = response.json()
    if response.status_code != 200:
        logging.info('Could not find ticket')
        return
    config.ticket['username'] = resp_json['Item']['Tickets'][0]['For']['Username']
    config.ticket['fullname'] = resp_json['Item']['Tickets'][0]['For']['Name']
    config.ticket['userid'] = resp_json['Item']['Tickets'][0]['For']['UserId']
    config.ticket['ticket_id_url'] = resp_json['Item']['Tickets'][0]['TicketId']
    config.ticket['location'] = resp_json['Item']['Tickets'][0]['For']['LocationName']
    logging.info(f"Data retrieved from {ticketid}:\n{config.ticket}")

def main(ticket_id):
    ready_payload(ticket_id)
    # seen_ids = get_ids_for_view(config.ticket['pending_view'])
    filename = "No file"
    # if config.ticket['userid'] not in seen_ids:
    resp_json = get_assets_for_user(user_id=config.ticket['userid'])
    form_assets_csv(resp_json=resp_json)
    config.path['pdf'] = 'Docs/' + config.ticket['username'] + '_CheckIn_Doc.pdf'
    make_pdf(filename=config.path['csv'],username=config.ticket['username'],fullName=config.ticket['fullname'],location=config.ticket['location'])
    filename = config.path['pdf']
    try:
        f = open(f"Logs/{config.ticket['username']}_ticketid.txt", "w")
        f.write(config.ticket['ticket_id_url'])
        f.close()
    except OSinfo as info:
        logging.info(f"Could not write to ticketid file")
    return filename

if __name__ == "__main__":
    ticket_id = sys.argv[1]
    print(main(ticket_id))
    print("Done")

