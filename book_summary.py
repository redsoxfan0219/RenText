import xml.etree.ElementTree as ET
import re
import os
import random
import sqlite3
import time


def __get_data__(file, tcp_no,folder):

    '''
    Defines the local data paths and parses the XML files.
    '''
    xml_folder_path = folder

    file = file
    tcp_no = tcp_no
    xml_file = f'{tcp_no}.P4.xml'
    tree = ET.parse(f'{xml_folder_path}/{xml_file}')
    root = tree.getroot()

    return tree, root

def __output_text_file(file, tcp_no, xml, folder):
    '''
    Outputs a plain .txt file with the tagless file content.
    '''
    tree, root = xml
    file = file
    tcp_no = tcp_no
    xml_file = f'{tcp_no}.P4.xml'
    xml_folder_path = folder

    with open(f'{xml_folder_path}/{xml_file}', 'r') as r:
        contents = r.read()
        r.close()

    with open(f'/Users/benjaminmoran/Desktop/eebo_strings/{tcp_no}.txt', 'w') as f:
        stringified_contents = ET.fromstring(contents)
        text = ''.join(stringified_contents[1][1].itertext())
        cleaned_text = re.sub('[^0-9a-zA-Z\&,;:?\-\'\.\s\|\b]+','',text)
        f.write(cleaned_text)
        f.close()

def __get_publication_date__(xml) -> str:
    '''
    Accesses the publication date.

    It was necessary to use a slightly more complicated approach
    because the XML has multiple 'DATE' tags without IDs that
    distinguish the early modern publication date from the 
    date the EEBO TCP text was published.
    There is also regular additional punctuation in this field
    that I had to clean out.
    '''
    tree, root = xml
    publication_date = 9999
    for date in root.iter('DATE'):
        text = date.text
        str_date = str(text)
        text_no_letters_or_punc = re.sub("[^0-9]","", str_date)
        if text_no_letters_or_punc == "":
            continue
        else:
            four_digit_year = int(text_no_letters_or_punc[:4])
            if four_digit_year > 1450 and four_digit_year < 1750 and four_digit_year is not "":
                publication_date = four_digit_year

    return publication_date

def __get_author__(xml) -> str:
    '''
    Retrieves the text's author.
    '''
    tree, root = xml
    author = "Author unknown"
    for e in tree.findall('.//'):
        if e.tag == "AUTHOR":
            author = e.text
            break

    return author
    
def __get_title__(xml) -> str:
    '''
    Retrieve's the work's title.
    '''
    tree, root = xml
    for e in tree.findall('.//'):
        if e.tag == "TITLE":
            title = e.text
            break

    return title

def __get_lines__(xml):
    tree, root = xml
    lines_dict = {}
    lines_id = 1
    for e in tree.findall('.//'):
        if e.tag == "L":
            line_text = e.text
            if line_text is not None:
                cleaned_line_text = re.sub('[^0-9a-zA-Z\&,;:?\-\'\.\s\|\b]+','',line_text)
                final_line_text = cleaned_line_text.replace("\n","")
                id_str = str(id)
                lines_dict[f'{id_str}'] = final_line_text
                lines_id += 1 

    return lines_dict

def __get_paragraphs__(xml):

    '''
    Extracts pertinent paragraphs from XML and adds them to a dictionary. 
    Excludes EEBO TCP header paragraphs.
    '''

    tree, root = xml
    id = 1
    paragraphs_dict = {}

    for child in root[1][1].iter():
        if child.tag == "P":
            paragraph_text = ''.join(child.itertext())
            cleaned_paragraph_text = re.sub('[^0-9a-zA-Z\&,;:?\-\'\.\s\|\b]+','',paragraph_text)
            final_paragraph_text = cleaned_paragraph_text.replace("\n","")
            id_str = str(id)
            paragraphs_dict[f'{id_str}'] = final_paragraph_text
            id += 1 

    return paragraphs_dict

def get_EEBO():

    '''
    Returns title, author, publication date, 5 consecutive lines of poetry 
    (if applicable), and a paragraph between 50 and 1000 characters in length
    (if applicable).
    '''
    folder = '/Users/benjaminmoran/eebo_tcp_data/data/eebo_raw/eebo_raw_combined/'
    database = r"/Users/benjaminmoran/Desktop/books.db"
    id = 1
    files = os.listdir(folder)
    start_time = time.time()


    for file in files:

        record_start_time = time.time()
        tcp_no = str(file).split(".")[0]
        file = f'{tcp_no}.P4.xml'
        title = ""
        author = ""
        lines_collected = ""
        publication_date = ""
        xml = __get_data__(file, tcp_no, folder)
        author = __get_author__(xml)
        title = __get_title__(xml)
        publication_date = __get_publication_date__(xml)
        lines = __get_lines__(xml)
        paragraphs = __get_paragraphs__(xml)
        print(f"TCP number: {tcp_no}")
        print(f"Title: {title}")
        print(f"Author: {author}")
        if publication_date == 0000:
            print("Error determining publication date")
        else:
            print(f"Publication Year: {publication_date}") 
        if (lines is None) or (len(lines) == 0):
            print("Length of the lines dictionary: 0") 
            lines_collected = "NA"
            print(f'Lines sample: {lines_collected}')

        else:
            print("Length of the lines dictionary: ", len(lines))
            line_dict_length = len(lines)
            sample_line_number = 0
            if line_dict_length > 6:
                sample_line_number = random.randint(1, line_dict_length-5)
                print("Sample lines: ")
                print("     ", lines[str(sample_line_number)])
                print("     ", lines[str(sample_line_number+1)])
                print("     ", lines[str(sample_line_number+2)])
                print("     ", lines[str(sample_line_number+3)])
                print("     ", lines[str(sample_line_number+4)])

                lines_collected = lines[str(sample_line_number)] + " / " + lines[str(sample_line_number+1)] + " / " + lines[str(sample_line_number+2)] + " / " + lines[str(sample_line_number+3)] + " / " + lines[str(sample_line_number+4)]
                print(lines_collected)

        if (paragraphs is None) or (len(paragraphs) == 0):
            print("Length of the paragraphs dictionary: 0")  

        else:
            print("Length of the paragraphs dictionary: ", len(paragraphs))
        
        if len(paragraphs) > 1:
            sample_paragraph_number = random.randint(1, (len(paragraphs)))
            timeout = time.time() + .05
            while len(paragraphs[str(sample_paragraph_number)]) < 50:
                sample_paragraph_number = random.randint(1, (len(paragraphs)))
                if time.time() > timeout:
                    sample_paragraph = paragraphs[str(sample_paragraph_number)]
                    print("Sample paragraph: ", sample_paragraph)
                    break
            else:
                if len(paragraphs[str(sample_paragraph_number)]) > 1000:
                    sample_paragraph = paragraphs[str(sample_paragraph_number)][0:1000]
                    print("Sample paragraph: ", sample_paragraph)
                else:
                    sample_paragraph = paragraphs[str(sample_paragraph_number)]
                    print("Sample paragraph: ", paragraphs[str(sample_paragraph_number)])
        else: 
            sample_paragraph = "No paragraphs identified in file"

        print("--- %s seconds for record to complete---" % (time.time() - record_start_time))

    print("--- %s seconds for batch job to complete---" % (time.time() - start_time))

    # conn = sqlite3.connect(database, timeout=60)
    # cur = conn.cursor()
    # cur.execute("INSERT INTO books VALUES(?,?,?,?,?,?,?)", (id, eebo_tcp_number, title, author, publication_date, lines_collected, sample_paragraph))   
    # conn.commit()
    # conn.close()
    # id += 1
if __name__ == "__main__":
    get_EEBO()