# Information about the usage of the scripts

The scripts provided in this folder are used for extracting information from the articles stored in the Zotero database.

## 1. Extracting Zotero database

In order to start working with the information about PDF files, we need to extract it first. This can be done by running the Zotero app and navigating to __Files>Export Library...__ and then choosing CSV as the export format.

## 2. Downloading the PDF files

The scripts use a number of Python libraries that first need to be installed. Their names are stored in the requirements.txt file and they can be installed using `pip install -r requirements.txt` command. After that, you need to run the *downloading_pdfs.py* script. It will prompt you to type in the information required for the scripts to work, such as paths where you retrieve from and store newly acquired information and email used to send requests to Unpaywall API. It is stored in `user_information.json` which you can later edit if you need to.

## 3. Extracting useful information

You can then use *extracting_information.py* to output some insights, in a form of a CSV file, found from analysing the downloaded papers. Currently, that includes under which section in the paper was the term "open hardware" found and useful links that have been provided by the author (github repositories, documentation, etc.).