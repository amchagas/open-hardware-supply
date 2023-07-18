import os
import requests
import csv
from scholarly import scholarly

# Output directory for all downloaded pdfs
output_directory = r"Downloaded_pdfs"

# Function to download a PDF file. Takes the url of a PDF file and fetches a get request,
# then writes the response to the file that uses Zotero ID as its name
def download_pdf(pdf_url, publication_key):
    response = requests.get(pdf_url)
    pdf_path = os.path.join(output_directory, f"{publication_key}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded PDF for publication: {publication_key}")

# Opens a CSV file that contains information about all PDFs that need to be downloaded
# and appends their Zotero ID "row[0]" and title of the publication "row[4]" to a list
# called "article_keys_and_titles"
article_keys_and_titles = []
with open('open_hardware_database.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        article_keys_and_titles.append([row[0], row[4]])

# Checks if a PDF file is already downloaded.
# If it is - does nothing, if not - sends a get request to Unpaywall API,
# querying for the publication with the specified title name.
# It then attempts to download the PDF file using the "url_for_pdf" provided by the response 
downloaded_articles = [os.path.splitext(filename)[0] for filename in os.listdir(output_directory)]
for article_key_and_title in article_keys_and_titles:
    key = article_key_and_title[0]
    title = article_key_and_title[1]
    if key not in downloaded_articles: 
        url = f"https://api.unpaywall.org/v2/search?query={title}&email=av337@sussex.ac.uk"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            try:
                pdf_url = result["results"][0]["response"]["best_oa_location"]["url_for_pdf"]
                download_pdf(pdf_url, key)
            except:
                print(f"Couldn't download from Unpaywall. Using scholarly: {key}")
        else:
            print(f"No data found for publication: {key}")