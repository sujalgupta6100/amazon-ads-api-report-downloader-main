
"""
Created on Sun Jan 23 12:07:36 2022

@author: jonasschroeder
GitHub: https://github.com/JonasSchroeder
LinkedIn: https://www.linkedin.com/in/jonas-schröder-914a338a/

Please refer to the amazon ads api doc for further campaign report types

Note: You need to have registered as a developer to get your access token and refresh token.
Furthermore you need to know the profile id of the ads account you want the reports to download for.

Please read my blog post for further guidance:

This script (Jan 2022) expects v2 of the amazon ads api and might be outdated at the time of your use.

"""


import requests
import pandas as pd
import json


REFRESH_TOKEN = "Atzr|IwEBINub8sh2v-5e4GGV5LYemFAJEPt1p0c85iBjvOZCD15EtZ4Jrf6iGNE7ZgsdBKa4e6kqnK1cigKtd58W4az0Ph5nRC6_F3idTVWMboIyl-TPT-pbe1zpjCTFKweq-BDC70uKvEDprExrEcXxLjH6dqLxeK32ETl0wZRBYQW8SNUp-QaLp1WP7i6_fUyT7dtHAiAStUxyaeWUtyiWDb5aYhyJpJcmu7QXV7ufeSToRJXSNGnQ_znvT0_2ih8bXbnfJLN18ncI3S3IqlH3tKSUGGvTffhH6egtU0rqQ8M-HGVOvIfkSdxHw7BNbiSAwGBijqyFyb4gXWm7h4NN0xi5Yr0XPTWpi4fdbpNHDdxo4Qt5NXJNXmpTXNrNuIYHpdxymhW9pwNiOzgoTaDkPA_ZYpUrWUeW-dIbkkeCOnScZ3SZqVDGjkFqsDVakTIVBKvuQFXomaM6kLDmeaWEbl-bCVL1vxYhnZ3iDQTMRfj-HuzsCA"
CLIENT_ID = "amzn1.application-oa2-client.145367dc68244acd90fb337e7a7b2be9"
CLIENT_SECRET = "4653efd08b9833e0842b8ce7e5fb62841afab22b0831869defe031c9f8685407"
API_SCOPE = '3221326986185735'
#----------------------------------------------------------------------------------------------------------------
# Step 1: Get a new access token
#----------------------------------------------------------------------------------------------------------------

def get_access_token(REFRESH_TOKEN):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    
    data = {
      'grant_type': 'refresh_token',
      'client_id': CLIENT_ID,
      'refresh_token': REFRESH_TOKEN,
      'client_secret': CLIENT_SECRET
    }
    
    response = requests.post('https://api.amazon.com/auth/o2/token', headers=headers, data=data)
    r_json = response.json()
    return r_json["access_token"]


#----------------------------------------------------------------------------------------------------------------
# Step 2: Get a list of profile ids associated with the developer account
#----------------------------------------------------------------------------------------------------------------

def get_profile_ids():
    ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Authorization': f"Bearer {ACCESS_TOKEN}"
    }


    response = requests.get("https://advertising-api-eu.amazon.com/v2/profiles", headers=headers)

    r_json = response.json()
    print(r_json)

    # dataframe from json
    profile_ids_df = pd.json_normalize(response.json())
    # print(profile_ids_df)

    # get profile ids
    profile_ids = profile_ids_df["profileId"].tolist()
    print(profile_ids)

    return profile_ids

# get_profile_ids()
# Function to get portfolio
def get_portfolio():
    ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Authorization': ACCESS_TOKEN,
        'Amazon-Advertising-API-Scope': API_SCOPE
    }

    response = requests.get("https://advertising-api-eu.amazon.com/v2/portfolios", headers=headers)

    r_json = response.json()
    print(r_json)

    # dataframe from json
    portfolio_df = pd.json_normalize(response.json())
    print(portfolio_df)

# get_portfolio()

# Function to get billing
def get_billing():
    ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Authorization': ACCESS_TOKEN,
        'Amazon-Advertising-API-Scope': API_SCOPE
    }

    response = requests.get("https://advertising-api-eu.amazon.com/invoices", headers=headers)

    r_json = response.json()
    print(r_json)

    # dataframe from json
    # billing_df = pd.json_normalize(response.json())
    # print(billing_df)

# get_billing()

# Function to get campaigns
def get_campaigns():
    ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Authorization': ACCESS_TOKEN,
        'Amazon-Advertising-API-Scope': API_SCOPE
    }

    response = requests.get("https://advertising-api-eu.amazon.com/v2/campaigns", headers=headers)

    r_json = response.json()
    print(r_json)

    # dataframe from json
    # billing_df = pd.json_normalize(response.json())
    # print(billing_df)

# get_campaigns()

# Function to get ad groups
def get_ad_groups():
    ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Authorization': ACCESS_TOKEN,
        'Amazon-Advertising-API-Scope': API_SCOPE
    }

    response = requests.get("https://advertising-api-eu.amazon.com/v2/adGroups", headers=headers)

    r_json = response.json()
    print(r_json)

    # dataframe from json
    # billing_df = pd.json_normalize(response.json())
    # print(billing_df)

# get_ad_groups()

# Function to get keywords
def get_keywords():
    ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Authorization': ACCESS_TOKEN,
        'Amazon-Advertising-API-Scope': API_SCOPE
    }

    response = requests.get("https://advertising-api-eu.amazon.com/v2/keywords", headers=headers)

    r_json = response.json()
    print(r_json)

    # dataframe from json
    # billing_df = pd.json_normalize(response.json())
    # print(billing_df)

# get_keywords()

# Function to get product ads
def get_product_ads():
    ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Authorization': ACCESS_TOKEN,
        'Amazon-Advertising-API-Scope': API_SCOPE
    }

    response = requests.get("https://advertising-api-eu.amazon.com/v2/productAds", headers=headers)

    r_json = response.json()
    print(r_json)

    # dataframe from json
    # billing_df = pd.json_normalize(response.json())
    # print(billing_df)

# get_product_ads()

# Function to get Reports
def get_reports():
    ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

    headers = {
        
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Authorization': ACCESS_TOKEN,
        'Amazon-Advertising-API-Scope': API_SCOPE,
        'Content-Type': 'application/vnd.createasyncreportrequest.v3+json'
    }
    # timeUnit = 'DAILY' or 'SUMMARY'
    data = {
    "name":"SP campaigns report 7/5-7/10",
    "startDate":"2022-10-05",
    "endDate":"2022-11-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["campaign"],
        "columns":["impressions","clicks","cost","campaignId","startDate","endDate"],
        "reportTypeId":"spCampaigns",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}

            
    

    response = requests.post("https://advertising-api-eu.amazon.com/reporting/reports", headers=headers, data = data)

    r_json = response.json()
    print(r_json)

    # dataframe from json
    # billing_df = pd.json_normalize(response.json())
    # print(billing_df)

get_reports()
