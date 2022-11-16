
"""
Created on Sun Jan 23 12:07:36 2022

@author: jonasschroeder
GitHub: https://github.com/JonasSchroeder

Please refer to the amazon ads api doc for further campaign report types

Note: You need to have registered as a developer to get your access token and refresh token.
Furthermore you need to know the profile id of the ads account you want the reports to download for.

Please read my blog post for further guidance:

This script (Jan 2022) expects v2 of the amazon ads api and might be outdated at the time of your use.

"""

import time
import requests
import pandas as pd
import numpy as np
import gzip
import json
import io


REFRESH_TOKEN = "Atzr|IwEBINub8sh2v-5e4GGV5LYemFAJEPt1p0c85iBjvOZCD15EtZ4Jrf6iGNE7ZgsdBKa4e6kqnK1cigKtd58W4az0Ph5nRC6_F3idTVWMboIyl-TPT-pbe1zpjCTFKweq-BDC70uKvEDprExrEcXxLjH6dqLxeK32ETl0wZRBYQW8SNUp-QaLp1WP7i6_fUyT7dtHAiAStUxyaeWUtyiWDb5aYhyJpJcmu7QXV7ufeSToRJXSNGnQ_znvT0_2ih8bXbnfJLN18ncI3S3IqlH3tKSUGGvTffhH6egtU0rqQ8M-HGVOvIfkSdxHw7BNbiSAwGBijqyFyb4gXWm7h4NN0xi5Yr0XPTWpi4fdbpNHDdxo4Qt5NXJNXmpTXNrNuIYHpdxymhW9pwNiOzgoTaDkPA_ZYpUrWUeW-dIbkkeCOnScZ3SZqVDGjkFqsDVakTIVBKvuQFXomaM6kLDmeaWEbl-bCVL1vxYhnZ3iDQTMRfj-HuzsCA"
CLIENT_ID = "amzn1.application-oa2-client.145367dc68244acd90fb337e7a7b2be9"
CLIENT_SECRET = "4653efd08b9833e0842b8ce7e5fb62841afab22b0831869defe031c9f8685407"
PROFILE_ID = "3221326986185735"

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
    print("Getting access token...")
    return r_json["access_token"]



#----------------------------------------------------------------------------------------------------------------
# Step 2: Create Report of date and defined metrics
#----------------------------------------------------------------------------------------------------------------

def create_report_and_get_reportid(metrics, report_date):
    
    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Amazon-Advertising-API-Scope': PROFILE_ID,
        'Authorization': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    data = {
            "stateFilter": "enabled",
            "metrics": metrics,
            "reportDate": report_date
    }
    
    response = requests.post("https://advertising-api-eu.amazon.com/v2/sp/productAds/report", headers=headers, json=data)
    r_json = response.json()
    return r_json["reportId"]


#----------------------------------------------------------------------------------------------------------------
# Step 3: Download report, convert to dataframe
#----------------------------------------------------------------------------------------------------------------

def download_and_convert_report(date_temp):
    
    headers = {
        'Amazon-Advertising-API-ClientId':CLIENT_ID,
        'Amazon-Advertising-API-Scope': PROFILE_ID,
        'Authorization': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"https://advertising-api-eu.amazon.com/v2/reports/{report_id}/download", headers=headers)
    
    response = response.content
    zip_file = io.BytesIO(response)
    with gzip.open(zip_file, 'rb') as f: 
        file_content = f.read() 
    
    json_data = json.loads(file_content)
    with open("filename.json", "w") as outfile: 
        json.dump(json_data, outfile)
    
    # dataframe from json
    report_df = pd.json_normalize(json_data)
    report_df["date"] = date_temp
    
    return report_df
        

#----------------------------------------------------------------------------------------------------------------
# Loop through list of dates and repeat steps 2 and 3, append returned dfs to create an overall report dataframe
#----------------------------------------------------------------------------------------------------------------

ACCESS_TOKEN = get_access_token(REFRESH_TOKEN)

# define metrics here as comma separated values
metrics = "campaignName,adGroupName,impressions,clicks,cost,asin,sku"

# define dates here
report_start_date = 20221001 # start date
date_range_days = 3 # range of days
dates_list = np.arange(report_start_date, report_start_date+date_range_days, 1)

final_df = pd.DataFrame()

# loop through dates
for date_temp in dates_list:
    
    # convert date to str
    date_temp = date_temp.astype(str)
    
    print(f"Requesting Amazon to create report for date {date_temp}")
    
    # request amazon to create day report
    report_id = create_report_and_get_reportid(metrics, date_temp)
    
    # wait for amazon to create report
    print(f"Waiting for amazon to create report.")
    time.sleep(10)
    
    # download report from amazon
    print(f"Downloading report.")
    report_df_temp = download_and_convert_report(date_temp)
    
    # append to final_df
    final_df = final_df.append(report_df_temp)
    print(final_df)


#----------------------------------------------------------------------------------------------------------------
# Save dataframe to storages as csv for PowerBI, Tableau, or Excel
#----------------------------------------------------------------------------------------------------------------

export_path = "C:/Users/sujal/Desktop"
final_df.to_csv(f"{export_path}/final_amazon_report.csv", index=False)


Print 