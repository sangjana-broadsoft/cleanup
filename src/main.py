#!/usr/bin/env python
import sys
import os
import urllib3 
import requests
import configparser
import re
from datetime import datetime
from getDefinedWorkflows import getDefinedWorkflows
from getDefinedWorkflows import getValidUnusedWorkflows
from getAllServiceItems import getAllServiceItems
from os import listdir
from os.path import isfile, join
# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

ip = "10.122.126.194/bpa"
server = "";
headers = {
  #VM121  'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZTk3NDE3MC00NjEwLTExZWQtODBmOS02NTQxYWUwMmE4ZWIiLCJuYW0iOiJhZG1pbiIsImlzcyI6IkJQQS1hZG1pbihicGFhZG1pbkBjaXNjby5jb20pIGNpc2Nvc3lzdGVtcyIsInJvbCI6IiIsInJybCI6IkJQQSBTdXBlciBBZG1pbiIsImV4cCI6MTY5NzA0NTI1NTAwMCwiZm5tIjoiYWRtaW4iLCJsbm0iOiJhZG1pbiIsImVtbCI6InNhbmdqYW5hQGNpc2NvLmNvbSIsInNpZCI6IjQ3MGEzOWMwLTY4NTctMTFlZS1iYjVhLWQxNjQyYTk0OGY5NyIsImFkbSI6dHJ1ZSwicmRtIjp0cnVlLCJhZWkiOjMwLCJ0bnQiOiIwZDZhNDY5MC02M2U2LTExZWQtOWE3Zi00OTlmMjkzZjM0NmQiLCJ0eXBlIjoiYWNjZXNzIiwiYXV0aC1tb2RlIjoibG9jYWwiLCJncm91cC1hdXRoIjpmYWxzZSwiaWF0IjoxNjk3MDQzNDU1fQ.2PM39BpRKzWM8z63j44btTHLpOPZ9cf2Q4OQTq-KSS8"
   # 'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMjVlZGYyMC1hZDgyLTExZWQtOGM2MS0zZDVlNTFmZDMyZGYiLCJuYW0iOiJhZG1pbiIsImlzcyI6IkJQQS1hZG1pbihicGFhZG1pbkBjaXNjby5jb20pIGNpc2Nvc3lzdGVtcyIsInJvbCI6IiIsInJybCI6IkJQQSBTdXBlciBBZG1pbiIsImV4cCI6MTY5NzEzMTY4NTAwMCwiZm5tIjoiYWRtaW4iLCJsbm0iOiJhZG1pbiIsImVtbCI6InJhamFra2hhQGNpc2NvLmNvbSIsInNpZCI6IjgzNDZhOGEwLTY5MjAtMTFlZS1hN2MwLWEzMTFjNTY4MjYyZCIsImFkbSI6dHJ1ZSwicmRtIjp0cnVlLCJhZWkiOjMwLCJ0bnQiOiIwZDZhNDY5MC02M2U2LTExZWQtOWE3Zi00OTlmMjkzZjM0NmQiLCJ0eXBlIjoiYWNjZXNzIiwiYXV0aC1tb2RlIjoibG9jYWwiLCJncm91cC1hdXRoIjpmYWxzZSwiaWF0IjoxNjk3MTI5ODg1fQ.umjfbAaTHG3p37zDZbnYjzbApDs0EZ2Sn6-ey1D6Bfg"
    }  
def deleteWorkflows(userFile) :
    filename = "deletedworkflows_" + server + ".txt"
    file1 = open(filename,"w") 
    count = 0
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);
    with open(os.path.join(here, userFile)) as file:
        count = 0
        start = datetime.now()
        for line in file:
            print ("Line: " + line);
            values = line.strip().split(",")
            
            try:
                id = values[2];
                print("Deleting workflow: " + values[0] + ":" + values[1]) #key:version
                    #/api/v1.0/workflow/process-definition/{id}    
                deleteUrl = "https://"+ip+"/api/v1.0/workflow/process-definition/" +id;
                print(deleteUrl);
                response = requests.delete(deleteUrl, headers=headers, verify=False);
               
                if response.status_code != 200:
                    print("unable to delete the workflow "+ values[0] + ":" + values[1]) #key:version
                    print(response.status_code);
                    print(response._content)
                else:
                    count +=  1;
                    msg = line;
                    file1.write (msg);
            except Exception as e:
                print("Oops Error!", e.__class__, "occurred.")
               
            
    file.close()
    msg = "Deleted Workflows Count = " + str(count)
    
    file1.close()
    

    print (msg)

  
location = os.path.abspath(__file__)
def getSubWorkflowFiles():
    search = "calledElement="
    #wfPath = "C:\\Cisco\\Project\\ATT-Conexus\\Conexus-BPA-Development\\Workflows"
 #   wfPath = "C:/Cisco/Project/ATT-Conexus/Conexus-BPA-Development/Workflows"
#    onlyfiles = [f for f in listdir(wfPath) if isfile(join(wfPath, f))]

 #   print (onlyfiles)
    wfPath = os.path.join("C:", os.sep, "Cisco", "Project", "ATT-Conexus", "Conexus-BPA-Development", "Workflows");
    files =listdir(wfPath);
 #   print("Files " + files)
  #  files = os.listdir(r"C:/Cisco/Project/ATT-Conexus/Conexus-BPA-Development/Workflows")
  #  files = os.listdir(r"C:\Cisco\Project\ATT-Conexus\Conexus-BPA-Development\Workflows")
    file1 = open("subworkflows.txt" ,"w") 
    subwfList =[];
 
    for f in files:
        print("File: " , f);
        try:
            with open(os.path.join(wfPath, f), "r") as fp:
                for line in fp:
                    if search in line:
                        index = line.find(search);
                        substr = line[index:]
                        val = re.findall('"([^"]*)"', substr);
                        subwfName = val[0];
                        
                        if subwfName not in subwfList and subwfName != "${calledElement}": 
                            subwfList.append(subwfName);
                            file1.write(subwfName + "," + f + "\n")
        
        except FileNotFoundError:
            print("File not found: " + f)
    with open("systemDefinedWorkflows.txt") as fp:
        for line in fp:
            file1.write(line)
    file1.close();


def deleteWorkflowsUsingId() :
    filename = "deletedworkflows_" + server + ".txt"
    file1 = open(filename,"w") 
    count = 0
    invalidWorkflowsFile = "invalidWorkflows_" + server + ".csv";
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);
    
    with open(os.path.join(here, invalidWorkflowsFile)) as file:
        count = 0
        start = datetime.now()
        for line in file:
            try:
                    id = line[2];
                    print("Deleting workflow: " + line[0] + ":" + line[1]) #key:version
                        #/api/v1.0/workflow/process-definition/{id}    
                    deleteUrl = "https://"+ip+"/api/v1.0/workflow/process-definition/" +id;
                    print(deleteUrl);
                    response = requests.delete(deleteUrl, headers=headers, verify=False);
                    print(response.status_code);
                    if response.status_code != 200:
                            print("unable to delete the workflow "+ line[0] + ":" + line[1]) #key:version
                    else:
                        count +=  1;
                        msg = line;
                        file1.write (msg);
            except Exception as e:
                print("Oops Error!", e.__class__, "occurred.")
               
            
    
    msg = "Deleted Workflows Count = " + str(count)
    file1.close()
    print (msg)

def main(*args):
    """My main script function.
    
    Displays the full patch to this script, and a list of the arguments passed
    to the script.
    """
    config = configparser.ConfigParser()
    config.read('input.config')
    config.sections()
    portal = config['DEFAULT']['portal'];
    server = config['DEFAULT']['name'];
    print("Script Location:", location)
    print("VM used:", portal)
    ip = portal + "/bpa";
   # workflowPath = config['DEFAULT']['resources'];
    token = config['DEFAULT']['token'].strip();
    
    if token == "" or portal.strip() == "":
        print ("Server Token is missing");
        exit();
    token = "Bearer " + token;
    headers = {
    'Authorization': token
    }  
#   
#  print("Verify the default workflows are copied from systemDefinedWorkflows.txt file to subworkflows file")
#  input("Press Enter to continue...")
    if args[0] == 'DEL':
        deleteWorkflows(args[1]);
        
    elif args[0] == 'SUB':
        print("get Sub Workflows used in the system")
        getSubWorkflowFiles();

    else:
        getAllServiceItems(server, ip, headers);
        print("Create the Invalid file list")
        getDefinedWorkflows(server, ip, headers);
        getValidUnusedWorkflows(server);
        print ("Completed.")
   
# Check to see if this file is the "__main__" script being executed
if __name__ == '__main__':
    _, *script_args = sys.argv
    main(*script_args)
    