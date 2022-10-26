import xml.etree.ElementTree as ET
import re
import os
import random
import time

class book:

    source_path = "/Users/benjaminmoran/eebo_tcp_data/data/eebo_raw/eebo_raw_combined"

    def __init__(self, tcp_no):

        self.tcp_no = tcp_no
        self.file = f'{tcp_no}.P4.xml'
        self.tree = ET.parse(f'{self.source_path}/{self.file}')
        self.root = self.tree.getroot()

        def __add_title__(self):

            for e in self.tree.findall('.//'):
                if e.tag == "TITLE":
                    title = e.text
                    break
            return title
    
        def __add_author__(self):

            author = "Author unknown"
            for e in self.tree.findall('.//'):
                if e.tag == "AUTHOR":
                    author = e.text
                    break
            return author
    
        def __add_publication_date__(self):

            publication_date = 9999
            for date in self.root.iter('DATE'):
                text = date.text
                str_date = str(text)
                text_no_letters_or_punc = re.sub("[^0-9]","", str_date)
                if text_no_letters_or_punc == "":
                    continue
                else:
                    four_digit_year = int(text_no_letters_or_punc[:4])
                    if four_digit_year > 1450 and four_digit_year < 1750 and four_digit_year != "":
                        publication_date = four_digit_year
                
            return publication_date

        def __get_lines__(self):

            lines_id = 1
            lines_dict = {}
            for e in self.tree.findall('.//'):
                if e.tag == "L":
                    line_text = e.text
                    if line_text is not None:
                        cleaned_line_text = re.sub('[^0-9a-zA-Z\&,;:?\-\'\.\s|\b]+','',line_text)
                        final_line_text = cleaned_line_text.replace("\n","")
                        id_str = str(lines_id)
                        lines_dict[f'{id_str}'] = final_line_text
                        lines_id += 1 
            return lines_dict
            
        def __get_paragraphs__(self):

            id = 1
            paragraphs = {}

            for child in self.root[1][1].iter():
                if child.tag == "P":
                    paragraph_text = ''.join(child.itertext())
                    cleaned_paragraph_text = re.sub('[^0-9a-zA-Z\&,;:?\-\'\.\s\|\b]+','',paragraph_text)
                    final_paragraph_text = cleaned_paragraph_text.replace("\n","")
                    id_str = str(id)
                    paragraphs[f'{id_str}'] = final_paragraph_text
                    id += 1 
            if len(paragraphs) == 1:
                return paragraphs['<built-in function id>']
            else:
            return paragraphs

        __get_paragraphs__(self)
        self.title = __add_title__(self)
        self.author = __add_author__(self)
        self.publication_date = __add_publication_date__(self)
        self.lines = __get_lines__(self)
        self.paragraphs = __get_paragraphs__(self)

    def summary(self):
        print(f"\nTCP number: {self.tcp_no}")
        print(f"\nTitle: {self.title}")
        print(f"\nAuthor: {self.author}")
        if self.publication_date == 9999:
            print("\nError determining publication date")
        else:
            print(f"\nPublication Year: {self.publication_date}") 
        if (self.lines is None) or (len(self.lines) == 0):
            print("\nLength of the lines dictionary: 0") 
            lines_collected = "NA"
            print(f"\nLines sample: {lines_collected}") 


        else:
            print("\nLength of the lines dictionary: ", len(self.lines))
            line_dict_length = len(self.lines)
            sample_line_number = 0
            if line_dict_length > 6:
                sample_line_number = random.randint(1, line_dict_length-5)
                print("\nSample lines: ")
                print("     ", self.lines[str(sample_line_number)])
                print("     ", self.lines[str(sample_line_number+1)])
                print("     ", self.lines[str(sample_line_number+2)])
                print("     ", self.lines[str(sample_line_number+3)])
                print("     ", self.lines[str(sample_line_number+4)])
            elif (line_dict_length <6) and (line_dict_length>1) :
                for i in range(1,len(line_dict_length)):
                    print("\nSample lines: ")
                    print("     ", self.lines[str(i)])
            elif line_dict_length == 1:
                print("\nSample line: ")
                print("     ", self.lines['<built-in function id>'])


        if (self.paragraphs is None) or (len(self.paragraphs) == 0):
            print("\nLength of the paragraphs dictionary: 0")  

        else:
            print("\nLength of the paragraphs dictionary: ", len(self.paragraphs))
        
        if len(self.paragraphs) > 1:
            sample_paragraph_number = random.randint(1, (len(self.paragraphs)))
            timeout = time.time() + .05
            while len(self.paragraphs[str(sample_paragraph_number)]) < 50:
                sample_paragraph_number = random.randint(1, (len(self.paragraphs)))
                if time.time() > timeout:
                    sample_paragraph = self.paragraphs[str(sample_paragraph_number)]
                    print("\nSample paragraph: ")
                    print(sample_paragraph)
                    print("")
                    break
            else:
                if len(self.paragraphs[str(sample_paragraph_number)]) > 1000:
                    sample_paragraph = self.paragraphs[str(sample_paragraph_number)][0:1000]
                    print("\nSample paragraph: ")
                    print(sample_paragraph)
                    print("")
                else:
                    sample_paragraph = self.paragraphs[str(sample_paragraph_number)]
                    print("\nSample paragraph:")
                    print(self.paragraphs[str(sample_paragraph_number)])
                    print("")
        else: 
            sample_paragraph = "\nNo paragraphs identified in file"            
         
    def json(self):

        return

def __assign_ids__(files):

    files = files

    id_dict = {}
    id = 1

    for file in files: 
        tcp_no = str(file).split(".")[0]
        id_dict[id] = tcp_no
        id += 1
    
    return id_dict

def __get_random_tcp_no__(id_dict):

    random_id = random.randint(1, len(id_dict))
    random_tcp_no = id_dict[random_id]

    return random_tcp_no

def get_random_book_summary():

    folder = '/Users/benjaminmoran/eebo_tcp_data/data/eebo_raw/eebo_raw_combined'

    files = os.listdir(folder)

    id_dict = __assign_ids__(files)
    random_tcp_no = __get_random_tcp_no__(id_dict)

    random_book = book(random_tcp_no)
    random_book.summary()

if __name__ == "__main__":
    get_random_book_summary()