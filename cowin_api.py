from messages import messages
from dotenv import load_dotenv
from os.path import join, dirname
import telegram
import logging
import requests
import datetime
import time
import json
import re
import os


logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode ='a', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

API_URLS ={
    0: 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode',
    1: 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id'
}

#previous session IDs
previous_session = {}

class Getvaccine(object):

    def __init__(self, option_code, url_option):
        
        self.option_code = option_code
        self.current_date = datetime.datetime.today().strftime("%d-%m-%Y")
        self.url = API_URLS[url_option]+"={}&date={}".format(option_code, self.current_date)
        self.previous_session ={}


    def process_previous_sessions(self):


        try:

            #loads previous session ids from disk
            with open('previous_session.json','r') as f:
                self.previous_session = json.loads(f.read())

            #loop through each session ids, remove the ones which are older than 24 hrs
            for key in list(self.previous_session):
                
                diff = time.time() - self.previous_session[key]

                if int(diff/86400) >= 12:
                    del self.previous_session[key]

            #print(self.previous_session)
        
        except OSError as e:
            print("Previous session file not found ! ",e)


    def get_centers(self):

        #prepare the request
        response = requests.get(self.url,  headers={"accept": "application/json", "Accept-Language": "en_US", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"})

        print(response)
        print(response.request.url)

        if response.ok:

            logging.info('{} : {}'.format(response.status_code, response.request.url))

            resp_json = response.json()
            #print(json.dumps(resp_json, indent = 1))

            #logging.info(json.dumps(resp_json, indent = 1))

            message_body = ""
            center_count = 0
            if resp_json["centers"]:

                if len(resp_json["centers"]) == 0:
                    print("No centers Availble !")
                else:

                    for center in resp_json["centers"]:
                        
                        center_flag = False
                        cowin_link =""

                        #loop through all the sessions of a center
                        for session in center["sessions"]:

                            if session['session_id'] not in self.previous_session and session["available_capacity"] >0 and session["min_age_limit"] ==18:
                                
                                if center_flag is False:
                                    message_body = messages.prepare_center_name(center_count, center)
                                    #print(message_body)
                                    center_flag = True
                                    center_count+=1
                                    cowin_link =""

                                #prepare sessions from the center
                                message_body += messages.prepare_center_sessions(session)
                                #pdb.set_trace()

                                self.previous_session[session["session_id"]] = time.time()

                        #check the vaccine price if fee_type is Paid
                        if center_flag is True and center["fee_type"]=="Paid" and "vaccine_fees" in center:
                            
                            for vac in center["vaccine_fees"]:
                                message_body += messages.prepare_center_price(vac["vaccine"], vac["fee"])

                        
                        if cowin_link =="":
                            cowin_link = messages.add_cowin_link()
                            
                            if message_body !="":
                                message_body +=cowin_link
                        

                        if message_body !="":
                            #print('+_+_+_+_')
                            #message_body +=messages.add_cowin_link()
                            print(message_body)
                            bot.send_message(chat_id="@%s" % os.environ.get("CHAT_ID"), text=message_body, parse_mode=telegram.ParseMode.HTML)
                            message_body = ""

            else:
                print("No Vaccination Centers available from {} to next 7 days".format(self.current_date))
                logging.info("No Vaccination Centers available from {} to next 7 days".format(self.current_date))

            '''
            if message_body !="":
                print(message_body)
                bot.send_message(chat_id="@%s" % os.environ.get("CHAT_ID"), text=message_body, parse_mode=telegram.ParseMode.HTML)
            else:
                print("No Slots for 18-44 !")
            '''

        else:
            logging.warning('ERROR : {} : {}'.format(response.status_code, response.request.url))


    def save_previous_sessions(self):
        
        with open("previous_session.json", "w") as file:
            file.write(json.dumps(self.previous_session))


if __name__ == "__main__":

    #load env variables
    load_dotenv()

    #Initialize BOT
    #bot = telegram.Bot(token="@%s"%os.environ.get("BOT_TOKEN"))
    bot = telegram.Bot(token="{}".format(os.environ.get("BOT_TOKEN")))

    #Initialize api objects
    api_ob = Getvaccine(263, 1)

    #get and process previous sessions
    api_ob.process_previous_sessions()

    #fetch contents
    api_ob.get_centers()

    #save sessions
    api_ob.save_previous_sessions()


