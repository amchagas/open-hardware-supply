import os
import pandas as pd
import re
import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine, LTComponent

section_keywords = {"abstract", "introduction", "reults", "method", "conclusion", "discussion", "references"}
open_hardware_variation = {"open hardware", "open_hardware", "open-hardware"}

# Searching for sections
def section_keywords_searching(pages: list[LTComponent], page_id : int, element_id : int, found_font_name : str):
    if page_id >= 0:
        page = list(pages[page_id])
        while element_id >= 0:
            if isinstance(page[element_id], LTTextContainer):
                score = 0
                line = page[element_id]._objs[0]
                text = line.get_text()
                first_char_font_name = [char.fontname for char in line if isinstance(char, LTChar)][0]
                if first_char_font_name != found_font_name:
                    score += 1
                if re.match("[A-Z]", text):
                    score += 1
                if any(element in text.lower() for element in section_keywords):
                    score += 2
                if re.match("([0-9]\.)", text):
                    score += 3
                if "," in text:
                    score -= 2
                if len(text) > 40:
                    score -= 1
                if re.search('[a-zA-Z]', text) == None:
                    score -= 5
                if score > 2:
                    return text[:-1]
            element_id -= 1
        return section_keywords_searching(pages, page_id - 1, len(pages[page_id - 1]) - 1, found_font_name)
    return "Error: No sections found"

# Searching for hyperlinks
def hyperlinks_searching(page, include : set, exclude : set):
    if '/Annots' in page:
        for a in page['/Annots']:
            obj = a.get_object()
            if '/A' in obj.keys() and '/URI' in obj['/A'].keys():
                uri = obj['/A']['/URI']
                if any(element in uri for element in include) and not any(element in uri for element in exclude):
                    return obj['/A']['/URI']
    else:
        return None

def main(output_csv, database, downloaded):

    df = pd.read_csv(database)

    for filename in os.listdir(downloaded)[4:10]:
        entry = df.loc[df['Key'] == filename[:-4]]
        csv_entry = [entry['Key'].values[0], entry['Title'].values[0], entry['DOI'].values[0]]
        links = set()
        sections = set()
        f = os.path.join(downloaded, filename)
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

            # Adding links
            reader = PyPDF2.PdfReader(f)
            page_pdf2 = reader.pages[page_id]
            uri = hyperlinks_searching(page_pdf2, {"mendeley", "osf", "github", "gitlab", ".zip"}, {"orchid", "nih", "doi"})
            if uri != None: links.add(uri)

        # Appending an entry to a CSV file named Output.csv
        csv_entry.append(sections) if sections != set() else csv_entry.append(None)
        csv_entry.append(links) if links != set() else csv_entry.append(None)
        print(csv_entry)
        # with open(output_csv, 'a', newline='') as output:
        #     csv.writer(output).writerow(csv_entry)


if __name__ == "__main__":
    output = input("Path to the output csv file: ")
    database = input("Path to the downloaded database: ")
    downloaded = input("Path to the downloaded pdf files: ")
    main(output, database, downloaded)