import os
import requests
import csv
import scholarly
import json
import saving_user_info

def main(output, database, email):

    pg = scholarly.ProxyGenerator()
    pg.FreeProxies()
    scholarly.scholarly.use_proxy(pg)

    # Function to download a PDF file. Takes the url of a PDF file and fetches a get request,
    # then writes the response to the file that uses Zotero ID as its name
    def download_pdf(pdf_url, publication_key):
        response = requests.get(pdf_url)
        pdf_path = os.path.join(output, f"{publication_key}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded PDF for publication: {publication_key}")

    # Opens a CSV file that contains information about all PDFs that need to be downloaded
    # and appends their Zotero ID "row[0]" and doi of the publication "row[8]" to a list
    # called "articles"
    articles = []
    with open(database, 'r', encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            articles.append([row[0], row[8]])

    # Checks if a PDF file is already downloaded.
    # If it is - does nothing, if not - sends a get request to Unpaywall API,
    # querying for the publication with the specified title name.
    # It then attempts to download the PDF file using the "url_for_pdf" provided by the response 
    downloaded_articles = [os.path.splitext(filename)[0] for filename in os.listdir(output)]
    for article in articles[1:15]:
        key = article[0]
        doi = article[1]
        if key not in downloaded_articles:
            if doi != "":
                url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                try:
                    if result["is_oa"] == False:
                        print("Closed")
                    elif result["best_oa_location"]["url_for_pdf"] != None:
                        download_pdf(result["best_oa_location"]["url_for_pdf"], key)
                    else:
                        print(result["best_oa_location"]["url_for_landing_page"])

                except:
                    print(f"Couldn't download from Unpaywall: {key}")
            else:
                print(f"No data found for publication: {key}")

# Getting user information from the user_information.json
if __name__ == "__main__":
    file_name = "user_information.json"
    with open(file_name, "r") as f:
        data = json.load(f)
        database = data["database"]
        downloaded = data["downloaded"]
        email = data["email"]
    main(downloaded, database, email)