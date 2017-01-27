from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Dawn of Civilization'

iWorldX = 124
iWorldY = 68

iNumLanguages = 41
(iLangEgyptian, iLangEgyptianArabic, iLangIndian, iLangChinese, iLangTibetan,
 iLangBabylonian, iLangPersian, iLangGreek, iLangPhoenician, iLangLatin,
 iLangJapanese, iLangEthiopian, iLangKorean, iLangMayan, iLangByzantine,
 iLangViking, iLangArabian, iLangKhmer, iLangIndonesian, iLangSpanish,
 iLangFrench, iLangEnglish, iLangGerman, iLangRussian, iLangDutch,
 iLangMalian, iLangPolish, iLangPortuguese, iLangQuechua, iLangItalian,
 iLangMongolian, iLangAztec, iLangTurkish, iLangThai, iLangCongolese,
 iLangPrussian, iLangAmerican, iLangCeltic, iLangMexican, iLangPolynesian,
 iLangHarappan) = range(iNumLanguages)

FIRST_SHEET = [iLangEgyptian, iLangChinese, iLangBabylonian, iLangGreek, iLangIndian, iLangPhoenician, iLangPersian, iLangLatin, iLangEthiopian, iLangKorean, iLangMayan, iLangByzantine, iLangJapanese]
SECOND_SHEET = [iLangViking, iLangArabian, iLangTibetan, iLangKhmer, iLangIndonesian, iLangSpanish, iLangFrench, iLangEnglish, iLangGerman, iLangRussian, iLangMalian, iLangPolish, iLangPortuguese, iLangQuechua]
THIRD_SHEET = [iLangItalian, iLangMongolian, iLangAztec, iLangTurkish, iLangThai, iLangCongolese, iLangDutch, iLangPrussian, iLangAmerican, iLangMexican, iLangPolynesian, iLangHarappan]

RANGE = 'A1:DS68'

LANGUAGE_NAMES = {
    iLangEgyptian : "Egyptian",
    iLangChinese : "Chinese",
    iLangBabylonian : "Babylonian",
    iLangGreek : "Greek",
    iLangIndian : "Indian",
    iLangPhoenician : "Phoenician",
    iLangPersian : "Persian",
    iLangLatin : "Latin",
    iLangEthiopian : "Ethiopian",
    iLangKorean : "Korean",
    iLangMayan : "Mayan",
    iLangByzantine : "Byzantine",
    iLangJapanese : "Japanese",
    iLangViking : "Viking",
    iLangArabian : "Arabian",
    iLangTibetan : "Tibetan",
    iLangKhmer : "Khmer",
    iLangIndonesian : "Indonesian",
    iLangSpanish : "Spanish",
    iLangFrench : "French",
    iLangEnglish : "English",
    iLangGerman : "German",
    iLangRussian : "Russian",
    iLangMalian : "Malian",
    iLangPolish : "Polish",
    iLangPortuguese : "Portuguese",
    iLangQuechua : "Quechua",
    iLangItalian : "Italian",
    iLangMongolian : "Mongolian",
    iLangAztec : "Aztec",
    iLangTurkish : "Turkish",
    iLangThai : "Thai",
    iLangCongolese : "Congolese",
    iLangDutch : "Dutch",
    iLangPrussian : "Prussian",
    iLangAmerican : "American",
    iLangMexican : "Mexican",
    iLangPolynesian : "Polynesian",
    iLangHarappan : "Harappan"
}

def getLanguageSheet(iLang):
    if iLang in FIRST_SHEET:
        return '1q1zn8jyTW6QU0rsz7CgH5a2ORWAS5T4z1zh9pWItUM4'
    elif iLang in SECOND_SHEET:
        return '1yHjhq_aM3Zrf12A-M3AFelXz1F0-v1iBDHsBnSQQMu8'
    elif iLang in THIRD_SHEET:
        return '1vUNB2RnAwvFYYFR-A6UAMwwuFlm0z6gLcgoh_raJLto'

    return ''

def getLanguageName(iLang):
    return LANGUAGE_NAMES[iLang]

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def printLanguageMap(service, iLang):
    spreadsheet_id = getLanguageSheet(iLang)
    language_name = getLanguageName(iLang)

    range_name = language_name + '!' + RANGE

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    values = result.get('values', [])

    print(language_name + ' : ')
    print('(', end="")

    for i, row in enumerate(values):
        if i > 0: print("")
        print('(', end="")
        if not row:
            for j in range(iWorldX):
                print('"",', end="")
        for name in row:
            print(name, end="")
        print(')', end="")
    print(')')



def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    for iLang in LANGUAGE_NAMES.keys():
        printLanguageMap(service, iLang)


if __name__ == '__main__':
    main()
