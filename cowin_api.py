import logging
import requests
import datetime
import json
import re

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode ='a', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

API_URLS ={
    0: 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode',
    1: 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id'
}

class Getvaccine(object):

    def __init__(self, option_code, url_option):
        
        self.option_code = option_code
        self.current_date = datetime.datetime.today().strftime("%d-%m-%Y")
        self.url = API_URLS[url_option]+"={}&date={}".format(option_code, self.current_date)

    @staticmethod
    def prepare_center_name(center_idx, center):

        #prepare center banner
        center_name = '''\
===============================
{count}) {center_name}
{block_name}
{district_name}
{state_name}
{pincode}
Timing :{time_from} - {to}
Fee : {fee_type}
--------------------------------
\
'''.format(count=center_idx,center_name=center["name"], block_name=center["block_name"],district_name=center["district_name"], state_name=center["state_name"], pincode=center["pincode"],time_from=center['from'], to=center['to'], fee_type=center["fee_type"])

        return center_name


    @staticmethod
    def prepare_center_sessions(session):

        #prepare session data
        session_name ='''\
Date: {date}
Capacity Avail.: {available_capacity}
Vaccine: {vaccine}
Min. Age: {min_age}
\n\
'''.format(date=session["date"], available_capacity=session["available_capacity"], vaccine=session["vaccine"], min_age=session["min_age_limit"])

        return session_name


    @staticmethod
    def prepare_center_price(vaccine, fee):

        #prepare vaccination  price
        text_body = '''\
Vaccines Avail:
{vaccine} : ₹{price}
\
'''.format(vaccine=vaccine, price=fee)

        return text_body

    def get_centers(self):

        #prepare the request
        response = requests.get(self.url,  headers={"accept": "application/json", "Accept-Language": "en_US"})

        print(response)
        print(response.request.url)

        if response.ok:

            logging.info('{} : {}'.format(response.status_code, response.request.url))

            resp_json = response.json()
            #print(json.dumps(resp_json, indent = 1))

            message_body = ""
            center_count = 0
            if resp_json["centers"]:

                if len(resp_json["centers"]) == 0:
                    print("No centers Availble !")
                else:

                    for center in resp_json["centers"]:
                        
                        center_flag = False

                        #loop through all the sessions of a center
                        for session in center["sessions"]:

                            if session["available_capacity"] >0 and session["min_age_limit"] ==18:
                                
                                if center_flag is False:
                                    message_body += self.prepare_center_name(center_count, center)
                                    #print(message_body)
                                    center_flag = True
                                    center_count+=1
                                    
                                    #print("center Flag ", center_flag)
                                    #print("center count ={}".format(center_count))
                                    #print(message_body)
                                    #print(self.prepare_center_sessions(session))
                                
                                #prepare sessions from the center
                                message_body += self.prepare_center_sessions(session)
                                #print(message_body)
                                #pdb.set_trace()

                        #check the vaccine price if fee_type is Paid
                        if center_flag is True and center["fee_type"]=="Paid" and "vaccine_fees" in center:
                            
                            for vac in center["vaccine_fees"]:
                                
                                message_body += self.prepare_center_price(vac["vaccine"], vac["fee"])
                                #print(message_body)

            else:
                print("No Vaccination Centers available from {} to next 7 days".format(self.current_date))
                logging.info("No Vaccination Centers available from {} to next 7 days".format(self.current_date))

            if message_body !="":
                print(message_body)
            else:
                print("Blank message !")

        else:
            logging.warning('ERROR : {} : {}'.format(response.status_code, response.request_url))




if __name__ == "__main__":

    #api_ob = Getvaccine(382424, 0)
    #api_ob = Getvaccine(110001, 0)
    #api_ob = Getvaccine(382041, 0)
    #api_ob = Getvaccine(833201, 0)
    api_ob = Getvaccine(412215, 0)

    api_ob.get_centers()
