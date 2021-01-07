import json

def getresults_notebook(note):
    res=None
    with open(note, mode="r", encoding="utf-8") as f:
        myfile = json.load(f)
        # print(myfile["cells"][0]["outputs"])
        # print(myfile["cells"][1]["outputs"][0]["text"])
        for i in range(len(myfile["cells"])):
            if len(myfile["cells"][i]["outputs"]) != 0:
                #eval('res = np.array('+ myfile["cells"][i]["outputs"][0]["text"][0]+")")
                return res