import json
import os

# Takes user information to be used in the other scripts and saves it in the user_information.json
email, database, downloaded, output = None, None, None, None
file_name = "user_information.json"
if not os.path.exists(file_name):
    database = input("Path to the Zotero database: ")
    downloaded = input("Path to the downloaded pdf files: ")
    email = input("Your email for Unpaywall API: ")
    output = input("Path to the output csv file: ")
    info_dict = {"database": database, "downloaded": downloaded, "email": email, "output": output}
    with open(file_name, "w") as f:
        json.dump(info_dict, f)
else:
    print("User info is already saved")