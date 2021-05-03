import requests
import datetime
import json
import re


if __name__ == "__main__":
    
    current_date = datetime.datetime.today().strftime("%d-%m-%Y")
    print(current_date)

    #postal_code = 382041
    #postal_code = 110001
    postal_code = 382424
    #curl "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=110001&date=31-03-2021" -H "accept: application/json" -H "Accept-Language: en_US"
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(postal_code, current_date)

    response = requests.get(URL,  headers={"accept": "application/json", "Accept-Language": "en_US"})
    print(response)
    print(response.request.url) 
    if response.ok:
        resp_json = response.json()
        #print(json.dumps(resp_json, indent = 1))
        center_count = 0
        if resp_json["centers"]:

            for center in resp_json["centers"]:
                center_flag = False

                center_body = '''\
===============================
{count}) {center_name} ({center_id})
{block_name}
{district_name}
{state_name}
{pincode}
Timing :{time_from} - {to}
Fee : {fee_type}
--------------------------------
\
'''.format(count=center_count,center_name=center["name"], center_id=center["center_id"], block_name=center["block_name"],district_name=center["district_name"], state_name=center["state_name"], pincode=center["pincode"],time_from=center['from'], to=center['to'], fee_type=center["fee_type"])

                #loop through all the session of the center
                for session in center["sessions"]:

                    if session["available_capacity"] >0 and session["min_age_limit"] >=18:

                        if center_flag is False:

                            print("center Flag ", center_flag)

                            #add vacc center name once
                            text_body = '''\
===============================
{count}) {center_name} ({center_id})
{block_name}
{district_name}
{state_name}
{pincode}
Timing :{time_from} - {to}
Fee : {fee_type}
--------------------------------
\
'''.format(count=center_count,center_name=center["name"], center_id=center["center_id"], block_name=center["block_name"],district_name=center["district_name"], state_name=center["state_name"], pincode=center["pincode"],time_from=center['from'], to=center['to'], fee_type=center["fee_type"])

                            center_flag = True
                            center_count+=1
                            print("center count ={}".format(center_count))

                        text_body +='''\
Date: {date}
Capacity Avail.: {available_capacity}
Vaccine: {vaccine}
\n\
'''.format(date=session["date"], available_capacity=session["available_capacity"], vaccine=session["vaccine"])
                if center_flag is True and center["vaccine_fees"]:
                    for vac in center["vaccine_fees"]:
                        text_body += '''\
Vaccines Avail:
{vaccine} : ₹{price}
\
'''.format(vaccine=vac["vaccine"], price=vac["fee"])
        else:
            text_body ="No Vaccination Centers available from {} to next 7 days".format(current_date)

        print(text_body)
        print(re.sub(r"[\t]*", "", text_body))


    else:
        print(response.status_code)