
# Convery amount currency into Euro 
# TCS Jira Cloud GBSAR Dispute Management Project
'''
customfield_10740 = Dispute Amount
customfield_10741 = Dispute Currency
customfield_10745 = Dispute Amount Euro (€)
'''


import sys
import json
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth


def convert_currency(amount, currency):
    excel_file = 'euro_currency_exchange.xlsx'
    df = pd.read_excel(excel_file, sheet_name='euro_currency_exchange')
    curreny_rates = dict(zip(df.Currency,df.Rate))
    amount_euro = amount/curreny_rates[currency]
    return round(amount_euro,2)


issueKey=sys.argv[1]
jiraAPIToken=sys.argv[2]

# issueKey = 'GBSAR-3'
# jiraAPIToken = '9EE5fO46UZgHfEhmVytWFB0C'

email = 'jira.bot@technicolor.com'
auth = HTTPBasicAuth(email,jiraAPIToken)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

url='https://creative-studios.atlassian.net/rest/api/3/issue/'+issueKey
response = requests.request(
   "GET",
   url,
   headers=headers,
   auth=auth
)
#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

data = json.loads(response.text)
amount = data['fields']['customfield_10740']
currency = data['fields']['customfield_10741']['value']
amount_euro = convert_currency(amount, currency)

payload = json.dumps( {
    "fields": {
        "customfield_10745": amount_euro,       
        }
})

# Update Jira
response = requests.request(
    "PUT",
    url,
    data=payload,
    headers=headers,
    auth=auth
)
print(f'Response = {response.status_code, response.text}')
