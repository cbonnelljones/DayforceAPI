import requests

COMPANY_ID = ""
LOGIN = ""
PASSWORD = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_EXPIRES = 0
API_URLS = {
    "BASE": "https://www.dayforcehcm.com/api",
    "TOKEN": "https://dfid.dayforcehcm.com/connect/token", 
    "TAGET_REDIRECT": "/V1/ClientMetadata",
    "EMPLOYEES": "/v1/Employees"
}
API_QUERY = {
    "set_xrefcode_by_employee_name": "?displayName=",
    "set_employee_details_by_xrefcode": "/"
}
EMPLOYEE_DATA = {}

def set_access_token():
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'password',
        'companyId': ''+COMPANY_ID+'',
        'username': ''+LOGIN+'',
        'password': ''+PASSWORD+'',
        'client_id': 'Dayforce.HCMAnywhere.Client'
    }
    send_request(request_type="post", request_headers=headers, request_data=data, request_action="token")

def set_url_redirect():
    global ACCESS_TOKEN
    headers = {
        'Authorization': 'Bearer '+ACCESS_TOKEN+''
    }
    send_request(request_type="get", request_headers=headers, request_action="redirect")

def set_employee_details_by_xrefcode(xrefcode=""):
    headers = {
        'Authorization': 'Bearer '+ACCESS_TOKEN+''
    }
    send_request(request_type="get", request_headers=headers, request_action="set_employee_details_by_xrefcode", search_data=xrefcode)

def set_xrefcode_by_employee_name(employee_name=""):
    headers = {
        'Authorization': 'Bearer '+ACCESS_TOKEN+''
    }
    send_request(request_type="get", request_headers=headers, request_action="set_xrefcode_by_employee_name", search_data=employee_name)

def send_request(request_type="post", request_headers="", request_data="", request_action="", search_data=""):
    global API_URLS, API_QUERY, ACCESS_TOKEN, ACCESS_TOKEN_EXPIRES, EMPLOYEE_DATA
    response_json = ""
    URL_REQUEST = ""
    if request_action == "token":
        URL_REQUEST = API_URLS["TOKEN"]
    elif request_action == "redirect":
        URL_REQUEST = API_URLS["BASE"] + "/" + COMPANY_ID + API_URLS["TAGET_REDIRECT"]
    elif request_action == "set_xrefcode_by_employee_name":
        URL_REQUEST = API_URLS["BASE"] + "/" + COMPANY_ID + API_URLS["EMPLOYEES"] + API_QUERY["set_xrefcode_by_employee_name"] + search_data
    elif request_action == "set_employee_details_by_xrefcode":
        URL_REQUEST = API_URLS["BASE"] + "/" + COMPANY_ID + API_URLS["EMPLOYEES"] + API_QUERY["set_employee_details_by_xrefcode"] + search_data
    
    #print(API_URLS["BASE"])

    if request_type == "post" and request_action =="token":
        r = requests.post(URL_REQUEST, headers=request_headers, data=request_data)
        response_json = r.json()
        if r.ok:
            ACCESS_TOKEN = response_json["access_token"]
            ACCESS_TOKEN_EXPIRES = response_json["expires_in"]
        else:
            ACCESS_TOKEN = ""
            ACCESS_TOKEN_EXPIRES = 0
    elif request_type == "get" and request_action == "redirect":
        r = requests.get(URL_REQUEST, headers=request_headers, allow_redirects=False)
        if r.status_code ==200:
            response_json = r.json()
            API_URLS["BASE"] = response_json["ServiceUri"]
        elif r.status_code == 302:
            r_redir = requests.get(r.headers["location"], headers=request_headers, allow_redirects=False)
            if r_redir.status_code ==200:
                redir_response_json = r_redir.json()
                API_URLS["BASE"] = redir_response_json["ServiceUri"]
                #print(redir_response_json)
                #print(redir_response_json["ServiceUri"])
                #print(r_redir.status_code)
                #print(r_redir.text)
                #print(API_URLS["BASE"])
    elif request_type == "get" and request_action == "set_xrefcode_by_employee_name":
        #print(URL_REQUEST)
        #print(request_headers)
        r = requests.get(URL_REQUEST, headers=request_headers)
        #print(r.status_code)
        if r.status_code ==200:
            response_json = r.json()
            #print(response_json["Data"][0]["XRefCode"])
            EMPLOYEE_DATA["XRefCode"] = response_json["Data"][0]["XRefCode"]
        else:
            EMPLOYEE_DATA["XRefCode"] = ""
    elif request_type == "get" and request_action == "set_employee_details_by_xrefcode":
        #print(URL_REQUEST)
        #exit()
        #print(request_headers)
        r = requests.get(URL_REQUEST, headers=request_headers)
        if r.status_code ==200:
            response_json = r.json()
            respnse_data_object = response_json["Data"]
            #print(response_json)
            EMPLOYEE_DATA["FirstName"] = respnse_data_object["FirstName"]
            EMPLOYEE_DATA["LastName"] = respnse_data_object["LastName"]
            EMPLOYEE_DATA["EmployeeNumber"] = respnse_data_object["EmployeeNumber"]
            EMPLOYEE_DATA["HireDate"] = respnse_data_object["HireDate"]
            EMPLOYEE_DATA["Clinic"] = respnse_data_object["HomeOrganization"]["LongName"]
            #return response_json["XRefCode"]
        else:
            EMPLOYEE_DATA = {}

    return r.ok

set_access_token()
set_url_redirect()
set_xrefcode_by_employee_name("bonnell-jones")
set_employee_details_by_xrefcode(EMPLOYEE_DATA["XRefCode"])

print(f"Name: {EMPLOYEE_DATA["FirstName"]} {EMPLOYEE_DATA["LastName"]}")
print(f"Employee Number: {EMPLOYEE_DATA["EmployeeNumber"]}")
print(f"Hire Date: {EMPLOYEE_DATA["HireDate"]}")
print(f"Clinic: {EMPLOYEE_DATA["Clinic"]}")