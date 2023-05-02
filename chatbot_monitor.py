"""schedule the mail and removing the token at specified time"""
import pytz
import schedule
import time
from utils import mail, remove_token
from load_config import load_config
config_dict = load_config('config.yml')
TZ_IST = pytz.timezone(config_dict["timezone"])
# creya chatbot
schedule.every().day.at(config_dict["creya_chatbot"]["time"],
                        tz=TZ_IST).do(mail,
                                      config_dict["creya_chatbot"]["endpoint"],
                                      config_dict["creya_chatbot"]["bot_name"],
                                      config_dict["send_mail_details"][
                                          "sender"]["email"],
                                      config_dict["send_mail_details"][
                                          "sender"]["password"],
                                      config_dict["send_mail_details"][
                                          "receiver"])
# Xmplar website chatbot
schedule.every().day.at(config_dict["xmplar_chatbot"]["time"],
                        tz=TZ_IST).do(mail,
                                      config_dict["xmplar_chatbot"]["endpoint"],
                                      config_dict["xmplar_chatbot"]["bot_name"],
                                      config_dict["send_mail_details"]["sender"]
                                      ["email"],
                                      config_dict["send_mail_details"]["sender"]
                                      ["password"],
                                      config_dict["send_mail_details"][
                                          "receiver"])

# Crest whatsapp chatbot
schedule.every().day.at(config_dict["whatsapp_chatbot"]["time"],
                        tz=TZ_IST).do(mail, config_dict["whatsapp_chatbot"]
                    ["endpoint"], config_dict["whatsapp_chatbot"]["bot_name"],
                    config_dict["send_mail_details"]["sender"]["email"],
                    config_dict["send_mail_details"]["sender"]["password"],
                    config_dict["send_mail_details"]["receiver"])
while True:
    schedule.run_pending()
    time.sleep(1)
