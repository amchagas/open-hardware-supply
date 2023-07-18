import os
import PyPDF2
import pandas as pd
import csv

df = pd.read_csv('open_hardware_database.csv')
directory = r"Downloaded_pdfs"
output_csv_path = r"output.csv"
section_keywords = {"abstract", "introduction", "reults",
                    "method", "methods", "conclusion", "discussion", "references"}
open_hardware_variation = {"open hardware", "open_hardware"}

for filename in os.listdir(directory)[:1]:
    entry = df.loc[df['Key'] == filename[:-4]]
    csv_entry = [entry['Key'].values[0],
                 entry['Title'].values[0], entry['DOI'].values[0]]
    links = set()
    f = os.path.join(directory, filename)
    print(f)
    with open(f, 'rb') as pdf_file:
        pdf = PyPDF2.PdfReader(pdf_file)
        for page_id, page in enumerate(pdf.pages):

            # Searching for keywords
            text = page.extract_text().splitlines()
            for line_id in range(len(text)):
                if any(element in text[line_id] for element in open_hardware_variation):
                    i = page_id
                    j = line_id
                    while i >= 0:
                        current_text = pdf.pages[i]
                        while j >= 0:
                            if any(element in current_text[j] for element in section_keywords):
                                print(current_text[j])
                                break
                            j -= 1
                        i -= 1
                    # print(text.splitlines())

            # Searching for hyperlinks
            if '/Annots' in page:
                for a in page['/Annots']:
                    obj = a.get_object()
                    if '/A' in obj.keys() and '/URI' in obj['/A'].keys():
                        if "doi" not in obj['/A']['/URI']:
                            links.add(obj['/A']['/URI'])

    # Appending an entry to a CSV file named Output.csv
    csv_entry.append(links)
    with open(output_csv_path, 'a', newline='') as output:
        csv.writer(output).writerow(csv_entry)
