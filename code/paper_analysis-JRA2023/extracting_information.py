import os
import PyPDF2
import pandas as pd
import csv
import re

df = pd.read_csv('open_hardware_database.csv')
directory = r"Downloaded_pdfs"

# While using on my own PC
# df = pd.read_csv(r"C:\Users\Anton\Desktop\JRA\open_hardware_database.csv")
# directory = r"C:\Users\Anton\Desktop\JRA\Downloaded_pdfs"

output_csv_path = r"output.csv"
section_keywords = {"abstract", "introduction", "reults",
                    "method", "methods", "conclusion", "discussion", "references"}
open_hardware_variation = {"open hardware", "open_hardware"}


def section_keywords_searching(text, line_id, sections):
    while line_id >= 0:
        line = text[line_id].strip()
        if any(element in line.lower() for element in section_keywords) and len(line) < 40 and re.match("([A-Z]|[0-9])", line):
            # print(line)
            sections.add(line)
            return True
        line_id -= 1
    return False


for filename in os.listdir(directory)[1:10]:
    entry = df.loc[df['Key'] == filename[:-4]]
    csv_entry = [entry['Key'].values[0],
                 entry['Title'].values[0], entry['DOI'].values[0]]
    links = set()
    sections = set()
    f = os.path.join(directory, filename)
    print(filename)
    with open(f, 'rb') as pdf_file:
        pdf = PyPDF2.PdfReader(pdf_file)
        for page_id, page in enumerate(pdf.pages):

            # Searching for keywords
            text = page.extract_text().splitlines()
            for line_id in range(len(text)):
                if any(element in text[line_id].lower() for element in open_hardware_variation):
                    # print(page_id)
                    current_page_id = page_id
                    current_line_id = line_id
                    current_text = text
                    while current_page_id >= 0 and not section_keywords_searching(current_text, current_line_id, sections):
                        current_page_id -= 1
                        current_text = pdf.pages[current_page_id].extract_text(
                        ).splitlines()
                        current_line_id = len(current_text) - 1

            # Searching for hyperlinks
            if '/Annots' in page:
                for a in page['/Annots']:
                    obj = a.get_object()
                    if '/A' in obj.keys() and '/URI' in obj['/A'].keys():
                        if "doi" not in obj['/A']['/URI']:
                            links.add(obj['/A']['/URI'])

    # Appending an entry to a CSV file named Output.csv
    csv_entry.append(sections) if sections != set() else csv_entry.append(None)
    csv_entry.append(links) if links != set() else csv_entry.append(None)
    print(csv_entry)
    # with open(output_csv_path, 'a', newline='') as output:
    #     csv.writer(output).writerow(csv_entry)
