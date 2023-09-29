import json
from datetime import datetime
import requests


client_id = "client_id"
client_secret = "client_secret"
username = "username"
password = "password"
api_version = "v58.0"
security_token = "security_token"
domain = "domain"
instance_url = f'instance_url'
query_endpoint = f'{instance_url}/services/data/v58.0/query/'
token_url = f'token_url'


# Request access token
data = {
    'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password + security_token
}
r  = requests.post(token_url, data=data)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")


#QUERY AREA
AccountQuery="SELECT Name FROM Account "


def sf_api_call(action, parameters = {}, method = 'get', data = {}):
    """
    Helper function to make calls to Salesforce REST API.
    Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
    """
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }

    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
    elif method in ['delete']:
        r = requests.request(method, instance_url + action, headers=headers,json=data, timeout=10)
    else:
        # other methods not implemented in this example
        raise ValueError('Method should be get or post or patch.')
    print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        elif method =='delete':

            return print('successfully deleted')

        else:
            return r.json()
    else:
        raise Exception('API error when calling %s : %s' % (r.url, r.content))


def postAccoutn ( Name,Phone,NumberOfEmployees,Type):
    Actions='/services/data/v58.0/sobjects/Account/'
    method='post'
    values={
        'Name': Name,
        'Phone': Phone,
        'NumberOfEmployees':NumberOfEmployees,
        'Type':Type
    }
    sf_api_call(f'{Actions}',method=method,data=values)


#postAccoutn(Name="Dert Denem2e",Phone='05309522322',NumberOfEmployees=43000,Type='other')


def postOpp(Name,AccountId,Amount,CloseDate,StageName,ForecastCategoryName):
    Actions = '/services/data/v58.0/sobjects/Opportunity/'
    method='patch'

    date_object = datetime.strptime(CloseDate, '%m-%d-%Y').date()
    values={
        'Name': Name,
        'AccountId':AccountId,
        'Amount':Amount,
        'CloseDate' :f'{date_object}',
        'StageName':StageName,
        'ForecastCategoryName':ForecastCategoryName
    }
    sf_api_call(f'{Actions}', method=method, data=values)


#postOpp(Name='Süper Python Yazarı',AccountId='0018d00000nPgghAAC',Amount=5000,CloseDate= '09-19-2022',StageName='Closed Won',ForecastCategoryName='commit')


def updateAccount(Id,Name):
    Actions=f'/services/data/v58.0/sobjects/Account/{Id}'
    method='patch'
    values={
        'Name':Name
    }
    sf_api_call(f'{Actions}',method=method,data=values)


#updateAccount(Id='0018d00000nPgghAAC',Name='Update Deneme Python')


def deleteAccount(Id):
    Actions=f'/services/data/v58.0/sobjects/Account/{Id}/'
    method='delete'
    values = {
        'result':"succesfully deleted"
    }
    sf_api_call(f'{Actions}',method=method)


#deleteAccount(Id='0018d00000nSM9WAAW')


def getAccount():
    query=f"{AccountQuery}"
    actions='/services/data/v58.0/query/'
    results=sf_api_call(actions,{'q':query})
    return print(json.dumps(results,indent=2))


#getAccount()


def getAccountByName(Name):
    query=f"{AccountQuery} WHERE Name ='{Name}'"
    actions='/services/data/v58.0/query/'
    results=sf_api_call(actions,{'q':query})
    return print(json.dumps(results,indent=2))


#getAccountByName("UOS")















