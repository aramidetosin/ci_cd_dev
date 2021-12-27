#!/usr/bin/env python

"""
Messing around with Nornir and FastAPI
"""

from fastapi import FastAPI
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from yaml import safe_load
import urllib3
from tools import nornir_set_creds
# Disable warnings
# If running into ArubaCX sessions full error or blank info
# run the following at the console "https-server session close all"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
norn = InitNornir(config_file="configs/config.yaml", core={"raise_on_error": True})
nornir_set_creds(norn)
app = FastAPI()



@app.get("/")
async def root():
    """Says hi!"""
    return {"message": "Hello JulioPDX"}



@app.get("/devices")
async def get_devices():
    """Returns a list of devices loaded from our hosts file"""
    with open("./configs/hosts.yaml", encoding="utf-8") as file:
        devices = safe_load(file)
    return {"devices": devices}



@app.get("/devices/{hostname}/napalm_get/{getter}")
async def get_config(hostname: str, getter: str):
    """Function used to interact with NAPALM and devices"""
    rtr = norn.filter(name=f"{hostname}")
    return rtr.run(name=f"Get {hostname} {getter}", task=napalm_get, getters=[f"{getter}"])
