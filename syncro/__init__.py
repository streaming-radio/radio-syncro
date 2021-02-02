import datetime
import os
import time

from syncro.service.radio.RadioNRJ import RadioNRJ
from syncro.service.radio.RadioRTL2 import RadioRTL2
from syncro.service.radio.RadioVirgin import RadioVirgin

TOKEN = os.getenv("token")
CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")

print(" ==================== ")
print("Run with")
print("Token        = " + TOKEN)
print("ClientId     = " + CLIENT_ID)
print("ClientSecret = " + CLIENT_SECRET)
print(" ==================== ")

radios = [RadioRTL2(), RadioVirgin(), RadioNRJ()]


def run():
    print("Run at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for radio in radios:
        radio.execute(TOKEN, CLIENT_ID, CLIENT_SECRET)
    print(" ==================== ")
    time.sleep(600)
    run()


run()
