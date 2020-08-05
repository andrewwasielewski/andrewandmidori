import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def next_available_row(sheet):
    str_list = list(filter(None, sheet.col_values(1)))
    return str(len(str_list)+1)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

def lambda_handler(event, context):

    # Find workbook by name and open the sheet
    spr = client.open("andrewandmidori_rsvp")
    sheet = spr.worksheet('RSVP')
    form_data = event['body']
    print(form_data)
    
    #Verify integrity of sheet with safety cell
    if sheet.acell('J2').value != 'SAFETY':
        print('safety check failed - cell is: ' +str(sheet.acell('J2')))
        return {
            'statusCode': 500,
            'body': json.dumps('Unable to save RSVP status.  Please contact the website admin')
        }

    #add the new guest form information
    new_record_row = next_available_row(sheet)
    print('inserting new record into row ' + str(new_record_row))
    sheet.update_acell("I{}".format(new_record_row), form_data)
    
    #add individual inputs
    fields = form_data.split('&')
    for i in range(0, len(fields)):
        if fields[i].startswith('name='):
            sheet.update_acell("A{}".format(new_record_row), fields[i][len('name='):])
        elif fields[i].startswith('guest='):
            #limit number of columns written to 
            if i <= 5:
                column = chr(ord('A') + i)
                sheet.update_acell("{}{}".format(column, new_record_row), fields[i][len('guest='):])
            else:
                print("form data overflow - field {}".format(i))
        elif fields[i].startswith('comments='):
            sheet.update_acell("G{}".format(new_record_row), fields[i][len('comments='):])
        elif i == len(fields) - 1:
            sheet.update_acell("H{}".format(new_record_row), fields[i][:-1])
    
    return {
        'statusCode': 302,
        'headers': {'location': 'http://andrewandmidori.com/#home'},
        'body': json.dumps('Updated RSVP status successfully')
    }
