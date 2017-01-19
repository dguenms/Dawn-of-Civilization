from apiclient import discovery
from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()

def main():
    print str(credentials)

    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', discoveryServiceUrl=discoveryUrl, credentials=credentials)

    spreadsheetId = '1q1zn8jyTW6QU0rsz7CgH5a2ORWAS5T4z1zh9pWItUM4'

    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId).execute()
    values = result.get('values', [])

    if not values:
        print('No data found')
    else:
        print('Name, Major:')
        for row in values:
            print str(row)

if __name__ == '__main__':
    main()
