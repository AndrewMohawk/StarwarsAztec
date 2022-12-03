import os
import sys
import json 
from aztec_code_generator import AztecCode

apk_decompile_path = "/Users/andrewmohawk/Private/disney/apk/disney_latest/com.disney.playdisneyparks.goo_2.24.0-30091_minAPI26(arm64-v8a,armeabi-v7a,x86,x86_64)(nodpi)_apkmirror.com"
version = "93"
apk_file = f"{apk_decompile_path}/assets/firestore-db/starWarsGalaxysEdgeGame_{version}_installation-data.json"

description_file = f"{apk_decompile_path}/assets/firestore-db/starWarsGalaxysEdgeGame_{version}_item-data.json"

desc_file = open(description_file, "r")
desc_data = json.load(desc_file)

def fetchItemInfo(itemId):
    for item in desc_data:
        
        if desc_data[item]['id']  == itemId:
            thisItem = desc_data[item]
            subtype = thisItem['subtype']
            name = thisItem['name']
            return f"{name} [{subtype}]"



if len(sys.argv) > 1:
    apk_file = sys.argv[1]

# Open the JSON File
codes_file = open(apk_file)
data = json.load(codes_file)
entryid = 0
for entry in data:
    if 'barcodeData' in data[entry]:
        barcode = data[entry]['barcodeData']
        itemname = "unknown" 
        if 'firstTimeRewards' in data[entry]:
            rewards = data[entry]['firstTimeRewards']
            if(len(rewards) == 0):
                itemname = "No immediate reward. -- likely part of challenge"
            for reward in rewards:
                thisItemId = reward['itemId']
                itemname = fetchItemInfo(thisItemId)
            
            
        
        print(f"{entryid}: {barcode} - {itemname}")
        aztec_code = AztecCode(barcode)
        
        #save it to the barcodes folder
        tmp_description = f"{itemname}"
        tmp_description = tmp_description.replace(" ", "_")
        filename = f"barcodes/{entryid}_{barcode}-{tmp_description}.png"
        aztec_code.save(filename)
        entryid += 1
    
    
codes_file.close()
desc_file.close()
