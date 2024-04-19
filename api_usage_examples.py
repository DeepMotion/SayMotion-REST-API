import argparse
import os
import json
import requests
import time

_apiServerUrl = ''

def check_json(fpath):
    if not os.path.exists(fpath):
        raise argparse.ArgumentTypeError('Filename %r doesn\'t exist.' % fpath)
    
    if fpath[-5:] != '.json':
        raise argparse.ArgumentTypeError('%r is not a JSON file.' % fpath)

    return fpath

def parse_user_credentials():
    parser = argparse.ArgumentParser(prog='SayMotion REST API CLI Demo', 
            description='Specify JSON file with user credentials')
    parser.add_argument('credentials', 
        nargs='?', type=check_json, 
        help='A JSON file must be specified')
    args = parser.parse_args()
    return args.credentials

def read_user_credentials(fpath):
    with open(fpath) as f:
        jsonData = json.load(f)
        global _sessionCredentials
        _sessionCredentials = jsonData['clientId'], jsonData['clientSecret']
        global session
        session = get_session()
        print('Credentials successfully read. \n')

def get_session():
    authUrl = _apiServerUrl + '/account/v1/auth'
    session = requests.Session()
    session.auth = _sessionCredentials
    request = session.get(authUrl)
    if request.status_code == 200:
        return session
    else:
        print('Failed to authenticate ' + str(request.status_code) + '\n')
        main_options()

def get_response(urlPath):
    respUrl = _apiServerUrl + urlPath
    resp = session.get(respUrl)
    if resp.status_code == 200:
        return resp
    else:
        print('Failed to contact server ' + resp.status_code + '\n')
        main_options()

def print_list_portion(inputList, nameDelim, idDelim, timeDelim, currPos):
    endOfPortion = currPos + 25
    if endOfPortion > len(inputList):
        endOfPortion = len(inputList)
    while currPos < endOfPortion:
        cPosStr = str(currPos + 1) + ')'
        while len(cPosStr) < 6:
            cPosStr += ' '
        print(cPosStr, end='')
        if nameDelim != '':
            print(inputList[currPos][nameDelim], end='')
        if idDelim != '':
            print('\t\t' + inputList[currPos][idDelim], end='')
        if timeDelim != '':
            print('\t\t' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inputList[currPos][timeDelim]/1000.0)), end='')
        currPos += 1
        print('')

    listFinished = False
    if endOfPortion >= len(inputList):
        listFinished = True
    listStatus = (currPos, listFinished)
    return listStatus

def call_print_list_portion(inputList, nameDelim, idDelim = '', timeDelim = ''):
    currPos = 0
    listComplete = False
    selection = 'Y'
    while not listComplete:
        print('')
        if currPos != 0:
            selection = input('Press Y to show more inputs, N to exit: ')

        selection = selection.lower()
        if selection == 'n':
            break
        if selection != 'y':
            print('Please use "y", "Y", "n", or "N"')
            continue
        print('')
        listStatus = print_list_portion(inputList, nameDelim, idDelim, timeDelim, currPos)
        listComplete = listStatus[1]
        currPos = listStatus[0]

def list_models():
    print('')
    respText = get_response('/character/v1/listModels?stockModel=deepmotion').text
    jsonResp = json.loads(respText)
    call_print_list_portion(jsonResp['list'], 'name', 'id')
    print('')
    main_options()
    
def get_job_list(listPath):
    respText = get_response(listPath).text
    jsonResp = json.loads(respText)
    return jsonResp

def get_job_status(listPath):
    respText = get_response(listPath).text
    jsonResp = json.loads(respText)
    return jsonResp

def list_jobs():
    print("""\n=== Job Status List Filter ===
    1) IN PROGRESS
    2) SUCCEEDED
    3) FAILED
    4) ALL\n""")
    selection = int(input('Select option number from the list: '))
    print('')
    jobList = []

    if selection == 1 or selection == 4:
        jsonResp = get_job_list('/job/v1/list/PROGRESS/text2motion')
        print('Jobs in progress: ' + str(jsonResp['count']))
        jobList += jsonResp['list']

    if selection == 2 or selection == 4:
        jsonResp = get_job_list('/job/v1/list/SUCCESS/text2motion')
        print('Jobs succeeded: ' + str(jsonResp['count']))
        jobList += jsonResp['list']

    if selection == 3 or selection == 4:
        jsonResp = get_job_list('/job/v1/list/FAILURE/text2motion')
        print('Jobs failed: ' + str(jsonResp['count']))
        jobList += jsonResp['list']

    call_print_list_portion(sorted(jobList, key=lambda x : x['ctime'], reverse=True), '', 'rid', 'ctime')
    
    print('')
    main_options()

def download_job():
    print('download job started\n')
    print("""A list of jobs will appear. Once you find the job you
        want to download, exit the listing and input the number of the
        job you want to download.\n""")
    input('Press Enter to continue...\n')
    jobListJson = get_job_list('/job/v1/list/SUCCESS/text2motion')
    numJobs = jobListJson['count']
    jobListJson['list'] = sorted(jobListJson['list'], key=lambda x : x['ctime'], reverse=True)
    print('Jobs available for download: ' + str(numJobs))
    call_print_list_portion(jobListJson['list'], '', 'rid', 'ctime', )
    jobSelection = int(input('Input job number to download: '))
    if jobSelection > numJobs:
        print('Selection is out of range.\n')
        main_options()
    rid = jobListJson['list'][jobSelection - 1]['rid']

    dPath = os.getcwd() + os.path.sep + rid + '-'
    downloadResp = get_response('/job/v1/download/' + rid)
    downloadRespTxt = downloadResp.text
    downloadRespJson = json.loads(downloadRespTxt)
    print(downloadRespJson)
    if downloadRespJson['count'] > 0:
        urls = downloadRespJson['links'][0]['urls']
        for fileUrl in urls:
            files = fileUrl['files']
            for file in files:
                if 'bvh' in file:
                    uri = file['bvh']
                    dowloadResp = session.get(uri)
                    with open(dPath + fileUrl['name'] +'.bvh', 'wb') as f:
                        f.write(dowloadResp.content)
                        print('\nFile saved to ' + dPath + fileUrl['name'] + '.bvh')
                if 'fbx' in file:
                    uri = file['fbx']
                    dowloadResp = session.get(uri)
                    with open(dPath + fileUrl['name'] + '.zip', 'wb') as f:
                        f.write(dowloadResp.content)
                        print('\nFile saved to ' + dPath + fileUrl['name'] + '.zip')
                if 'mp4' in file:
                    uri = file['mp4']
                    dowloadResp = session.get(uri)
                    with open(dPath + fileUrl['name'] + '.mp4', 'wb') as f:
                        f.write(dowloadResp.content)
                        print('\nFile saved to ' + dPath + fileUrl['name'] + '.mp4')

    print('')
    main_options()

def printProgress(percent):
    prefix = 'Progress:'
    suffix = 'Complete'
    printEnd = "\r"
    print(f'{prefix} {percent}% {suffix}', end = printEnd)


def showProgress(rid, prefix):
    jobDone = False
    while jobDone == False:
        pStatusRespJson = get_job_status ('/job/v1/status/' + rid)
        if int(pStatusRespJson["count"]) > 0:
            statusData = pStatusRespJson["status"][0]; #We have one status for a single rid
            if statusData["status"] == "PROGRESS":
                total = float(statusData["details"]["total"])
                current = float(statusData["details"]["step"])
                if current > total:
                    current = total
                percentage = round((current * 100.0) / total, 2)
                printProgress(str(percentage))
                
            elif statusData["status"] == "FAILURE":
                print(prefix + ' is completed with Failure.')
                jobDone = True

            elif statusData["status"] == "SUCCESS":
                print(prefix + ' is completed successfully.')
                jobDone = True
            else:
                print(prefix + ' is in unknown status.')
                jobDone = True

        else:
            jobDone = True
    
        time.sleep(10)

        
def new_text2motion_job():
    charResp = get_response('/character/v1/listModels?stockModel=deepmotion').text
    charRespJson = json.loads(charResp)
    charList = charRespJson['list']
    call_print_list_portion(charList, 'name', 'id')
    charSel = int(input("""\nInput the index of the character you want to use: """))
    modelStr = 'model=' + charList[charSel - 1]['id']

    prompt = input("Please enter text prompt: ")
    number = float(input("Please enter the expected animation durantion between 1 and 10 seconds: "))
    number = max(1, min(number, 10))
    
    processUrl = _apiServerUrl + '/job/v1/process/text2motion'
    processCfgJson = None
    
    processCfgJson = {
        "params": [
            "prompt=\"" + prompt + "\"",
            "requestedAnimationDuration=" + str(number),
            modelStr
        ]
    }
    
    print(processUrl)
    print(processCfgJson)
    
    processResp = session.post(processUrl, json=processCfgJson)
    if processResp.status_code == 200:
        pRespJson = json.loads(processResp.text)
        print('Job is processing: ' + pRespJson['rid'])
        showProgress(pRespJson['rid'], "Job")
        
    else:
        print(processResp.status_code)
        print('failed to process')
    
    print('')
    main_options()

def upload_character():
    currPath = os.path.abspath(os.path.dirname(__file__))
    cInputPath = input('Input relative path of character model to upload: ')
    cFullPath = os.path.normpath(os.path.join(currPath, cInputPath))
    cFile = None
    if not os.path.exists(cFullPath):
        raise argparse.ArgumentTypeError('Filename %r doesn\'t exist.' % cFullPath)
    with open(cFullPath, 'rb') as f:
        cFile = f.read()
        f.close()
    if cFile == None:
        raise argparse.ArgumentTypeError('Could not read %r.' % cFullPath)
    cHeader = {'Content-Length': str(len(cFile)), 'Content-Type': 'application/octet-stream'}

    cFName, cExt = os.path.splitext(os.path.basename(cFullPath))
    uploadingUrl = _apiServerUrl + '/character/v1/getModelUploadUrl?name=' + cFName + '&modelExt=' + cExt[1:] + '&resumable=0'
    resp = session.get(uploadingUrl)
    if resp.status_code == 200:
        jsonResp = json.loads(resp.text)
        gcsModelUrl = jsonResp['modelUrl']
        cUploadResp = session.put(gcsModelUrl, headers=cHeader, data=cFile)
        if cUploadResp.status_code == 200:
            print('Uploaded model ' + cFName)
        else:
            print('Failed to upload model')
            main_options()
        storeUrl = _apiServerUrl + '/character/v1/storeModel'
        storeCfg = {
            "modelId": None,
            "modelUrl": gcsModelUrl,
            "thumbUrl": None,
            "modelName": cFName
        }
        storeResp = session.post(storeUrl, json=storeCfg)
        if storeResp.status_code == 200:
            print('Successfully stored model ' + json.loads(storeResp.text)['modelId'])
        else:
            print('Failed to store model')
    else:
        print('Failed to contact API server for upload.')

    print('')
    main_options()

def check_minutes_balance():
    respText = get_response('/account/v1/creditBalance').text
    jsonResp = json.loads(respText)
    print(jsonResp['credits'])
    
    print('')
    main_options()

mainOptions = {
    1: list_models,
    2: list_jobs,
    3: download_job,
    4: new_text2motion_job,
    5: upload_character,
    6: check_minutes_balance,
    7: exit
}

def main_options():
    print("""=== OPTIONS ===
    1) List Models
    2) List Jobs
    3) Download Completed Job
    4) Start Text-to-Motion Job
    5) Upload Custom Character
    6) Check Minutes Balance
    7) Exit\n""")
    selection = int(input('Select option number from the list: '))
    mainOptions[selection]()

def main():
    read_user_credentials(args)
    main_options()

if __name__ == '__main__':
    args = parse_user_credentials()
    main()