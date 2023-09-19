import os
import pandas as pd
import re
import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine, LTComponent
import json
import saving_user_info

# Set of keywords used for determining if a line of text is a section or not
section_keywords = {"abstract", "introduction", "results", "method", "conclusion", "discussion", "references"}
# set of keywords used for finding "open hardware" term in a document
open_hardware_variation = {"open hardware", "open_hardware", "open-hardware", "open source hardware","open-source hardware"}

# Function that returns a section under which term "open hardware" was found.
# It takes in all the pages from the document, page id where the term was found,
# position on the page where the term was found, and the font used in that section of text.
def section_keywords_searching(pages: LTComponent, page_id : int, element_id : int, found_font_name : str):
    if page_id >= 0:
        page = list(pages[page_id])
        while element_id >= 0:
            # Check whether an element is a piece of text or not
            if isinstance(page[element_id], LTTextContainer):
                score = 0
                line = page[element_id]._objs[0]
                text = line.get_text()
                first_char_font_name = [char.fontname for char in line if isinstance(char, LTChar)][0]
                # Adds points if the fonts of the text line and the term are different
                if first_char_font_name != found_font_name:
                    score += 1
                # Adds a point if the text line starts with a capital letter
                if re.match("[A-Z]", text):
                    score += 1
                # Adds points if any of the section keywords are found in the text line
                if any(element in text.lower() for element in section_keywords):
                    score += 2
                # Adds points if the text line starts with a number followed by a dot
                if re.match("([0-9]\.)", text):
                    score += 3
                # Removes points if there is a comma present in the text line
                if "," in text:
                    score -= 2
                # Removes points if the length of the text line exceeds 40 characters
                if len(text) > 40:
                    score -= 1
                # Removes points if there are no letters found in the text line
                if re.search('[a-zA-Z]', text) == None:
                    score -= 5
                if score > 2:
                    return text[:-1]
            element_id -= 1
        # If no text line that could be considered a section was found on a page, call the function with the previous page's id
        return section_keywords_searching(pages, page_id - 1, len(pages[page_id - 1]) - 1, found_font_name)
    return "Error: No sections found"

# Function that returns hyperlinks found on a page.
# It takes in a page that needs to be searched for hyperlinks, set of keywords that need to be present in the link,
# set of keywords that need to be excluded
def hyperlinks_searching(page, include : set, exclude : set):
    if '/Annots' in page:
        for a in page['/Annots']:
            obj = a.get_object()
            if '/A' in obj.keys() and '/URI' in obj['/A'].keys():
                uri = obj['/A']['/URI']
                if any(element in uri for element in include) or not any(element in uri for element in exclude):
                    return obj['/A']['/URI']
    else:
        return None

# Main function that runs the whole script.
# It takes in the path to the output csv file, the path to the downloaded Zotero database, and the path to the downloaded PDF files.
def main(output_csv, database, downloaded):
    df = pd.read_csv(database)
    for filename in os.listdir(downloaded):
        # Getting a row in the database
        entry = df.loc[df['Key'] == filename[:-4]]
        csv_entry = [entry['Key'].values[0], entry['Title'].values[0], entry['DOI'].values[0]]
        links = set()
        sections = set()
        f = os.path.join(downloaded, filename)
        # Extracting pages from the file and starting to search for keywords and links
        try:
            pages = list(extract_pages(f))
            for page_id, page in enumerate(pages):
                page = list(page)

                # Searching for keywords
                for element_id, element in enumerate(page):
                    if isinstance(element, LTTextContainer):
                        text_objects = [object for object in element._objs if isinstance(object, LTTextLine)]
                        for line in text_objects:
                            if any(phrase in line.get_text().lower() for phrase in open_hardware_variation):
                                sections.add(section_keywords_searching(pages, page_id, element_id, [char.fontname for char in line if isinstance(char, LTChar)][0]))

                # Searching for links
                reader = PyPDF2.PdfReader(f)
                page_pdf2 = reader.pages[page_id]
                uri = hyperlinks_searching(page_pdf2, {"mendeley", "osf", "github", "gitlab", ".zip"}, {"orcid", "nih", "doi","mailto:","creativecommons.org"})
                if uri != None: links.add(uri)

            # Appending an entry to a CSV file named Output.csv
            csv_entry.append(sections) if sections != set() else csv_entry.append(None)
            csv_entry.append(links) if links != set() else csv_entry.append(None)
            print(csv_entry)
            # with open(output_csv, 'a', newline='') as output:
            #     csv.writer(output).writerow(csv_entry)
        except:
            print(f"Couldn't process {filename}. Check its contents at {f}.")

# Getting user information from the user_information.json
if __name__ == "__main__":
    file_name = "user_information.json"
    with open(file_name, "r+") as f:
        data = json.load(f)
        database = data["database"]
        downloaded = data["downloaded"]
        output = data["output"]
    main(output, database, downloaded)