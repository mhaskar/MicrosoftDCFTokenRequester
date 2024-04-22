#!/usr/bin/python3

import json
import signal
import requests
from termcolor import cprint

def ctrlc(sig, frame):
    pass

signal.signal(signal.SIGINT, ctrlc)

def print_success(text) -> str:
    message = "[+] %s" % text
    cprint(message, "green")

def print_error(text) -> str:
    message = "[-] %s" % text
    cprint(message, "red")

def print_progress(text) -> str:
    message = "[!] %s" % text
    cprint(message, "yellow")


def request_code_and_device_code() -> str:
    auth_url =  "https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0"
    data = {
    "client_id": "1950a258-227b-4e31-a9cf-717495945fc2",
    "resource": "https://graph.microsoft.com"
    }
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    headers = {"User-Agent": user_agent}
    print_progress("Requesting Device Code ..")
    try:
        req = requests.post(auth_url, data=data, headers=headers)
        results = json.loads(req.text)
        user_code = results["user_code"]
        device_code = results["device_code"]
        print_success("User Code: %s" % user_code)
        print_success("Device Code: %s" % device_code)
        return device_code
    except:
        print_error("Can't request Device Code!")



def get_azure_tokens(code) -> dict:
    auth_url =  "https://login.microsoftonline.com/Common/oauth2/token?api-version=1.0"
    data = {
    "client_id": "1950a258-227b-4e31-a9cf-717495945fc2",
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    "code": code
    }
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    headers = {"User-Agent": user_agent}
    print_progress("Retrieving Tokens ..")
    try:
        req = requests.post(auth_url, data=data, headers=headers)
        results = json.loads(req.text)
        if "error" in results.keys():
            if results["error"] == "authorization_pending":
                print_error("Authorization pending")
                print_error("Make sure to submit the code")
            else:
                print_error(results["error"])
        
        if "token_type" in results.keys():
            print_success("Tokens Retrieved successfully")
            print_success(results)
            exit()
    except Exception as e:
        print_error("Error while retrieving tokens")
        print_error(e)
        exit()



device_code = request_code_and_device_code()

while True:
    request_token = input("Request Token? (Y/N) >> ").lower()

    if request_token != "y" and request_token != "n":
        print_error("Please answer Y or N")
        pass
    if request_token == "y":
        get_azure_tokens(device_code)

    if request_token == "exit":
        exit()


