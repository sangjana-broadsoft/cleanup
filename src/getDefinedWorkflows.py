import urllib3 
import requests
import sys

#For each item in AllWorkflows, if not found in subworkflows or ActiveServiceitem, then it is marked as invalid
def getDefinedWorkflows(server, ip, headers) :
    filename = "./output/AllWorkflows_" + server + ".csv"
    file1 = open(filename,"w") 
    validWorkflowFile = open("./output/ActiveServiceItems_" + server + ".csv", "a");
   
    invalidWorkflowsFile = open("./output/invalidWorkflows_" + server + ".csv", "w");
    invalidWorkflowsFile.write("Workflow Key, Version, WorkflowID, Workflow Name\n")
    count = 0
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);
    
    
    try:
        url = "https://{}/api/v1.0/workflow/process-definition/draft".format(ip);
        response = requests.get(url, headers=headers, verify=False) 
        resp = response.json();
        file1.write ("WorkflowKey, Version,  WorkflowId, WorkflowName,\n");
        with open("subworkflows.txt") as subworkflowFile:
            content = subworkflowFile.read();
        with open("./output/ActiveServiceItems_" + server + ".csv") as valid:
            validcontent = valid.read();
        
        for item in resp:
            #print(item["status"])
            if item["status"] == "Deployed":
                msg = item["key"]+ "," +  str(item["version"]) + "," + item["id"] ;
                if item["name"] :
                    msg += "," + item["name"] ;
                msg = msg.strip() + "\n";
                
               
                file1.write (msg);
              
                searchItem = item["key"];
                if searchItem in content:
                    validWorkflowFile.write("Sub/Default," + msg );
                elif searchItem not in validcontent:
                    invalidWorkflowsFile.write(msg)
                    count +=  1;
              
    except Exception as e:
        type, value, traceback = sys.exc_info()
        print('Error opening %s: %s' % (value.filename, value.strerror))
        print("Unable to continue: ",  type , " Error in getting Workflows!", value.strerror, " Check trace: ", traceback.print_exc)
        
    print("Invalid workflows Count = " + str(count));
    
    file1.close()
    validWorkflowFile.close();
    invalidWorkflowsFile.close()
   
def getValidUnusedWorkflows(server) :
    filename = "./output/ValidUnusedWorkflows_" + server + ".csv"
    file1 = open(filename,"w") 
    count = 0
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);
    
    workflowKey = 0;
    version = 1;
    workflowId = 2;
    workflowName = 3;
    resource  = 5;
    added = [];
    try:
       
        file1.write ("WorkflowKey, Version,  WorkflowId, WorkflowName,\n");
        #allFile = open("AllWorkflows_" + server + ".csv")
        with open("./output/ActiveServiceItems_" + server + ".csv") as validFile:
            for validline in validFile:
                if count == 0:
                    count += 1;
                    continue;
                line = validline.split(",");
                key = line[workflowKey+1]
                id = line[workflowId+1]
                
                
                
                with open("./output/AllWorkflows_" + server + ".csv") as allFile:
                    for allFileLine in allFile:
                        allFileLines = allFileLine.split(",")
                                    
                        if key.strip() == allFileLines[workflowKey].strip() and id != allFileLines[workflowId]:
                            if allFileLine in added:
                            #    print(allFileLine + " is skipped");
                                continue;
                
                            file1.write(allFileLine);
                            added.append(allFileLine);
                            
                            count += 1;
                    
    except Exception as e:
        print("Oops Error!", e.__class__, "occurred.")
        
    print("Valid Unused Workflow Count = " + str(count-1));
    
    file1.close()
    
    