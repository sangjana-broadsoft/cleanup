import urllib3 
import requests

def getAllServiceItems(server, ip, headers) :
    filename = "./output/ActiveServiceItems_" + server + ".csv"
    file1 = open(filename,"w") 
    file2 = open("./output/InactiveServices_" + server + ".txt", "w");
    count = 0
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);
    try:
        url = "https://{}/api/v1.0/service-catalog/service-items".format(ip);
        response = requests.get(url, headers=headers, verify=False) 
        #  response = requests.get(defaultWFUrl, headers=headers, verify=False) 
        resp = response.json();
        file1.write ("Service Item Name, WorkflowKey, Version,  WorkflowId, WorkflowName, Resource \n");
        wfFileList = [];
        for item in resp["data"]:
            id =  item["categoryIds"];
            #print(item["status"]) ;
            if item["status"] == "Active":
                workflowId = item["workflow"][0]["id"];
                workflowKey = item["workflow"][0]["key"];
                workflowName = item["workflow"][0]["name"];
              #  workflowResource = item["workflow"][0]["resource"];
                version =str(item["workflow"][0]["version"]);
               # if workflowResource not in wfFileList:
                  #  wfFileList.append(workflowResource)
                count +=  1;
                msg = item["name"]  + "," + workflowKey +  "," + version +","  + workflowId + "," + workflowName + "," +   "\n";
                file1.write (msg);
            else:
                file2.write(item["name"] + "\n")
    except Exception as e:
        print("Oops Error!", e.__class__, "occurred.")
        
    print("There are " + str(count) + " active service items");
    
    file1.close()
    file2.close();
 #   return wfFileList;
    