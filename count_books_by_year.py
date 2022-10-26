import xml.etree.ElementTree as ET
import re
import os
import random
import time
from collections import OrderedDict
import pandas as pd
from datetime import datetime
import sys

import xml.etree.ElementTree as ET
import re
import os
import random
import time
from collections import OrderedDict
import pandas as pd
from datetime import datetime
import sys

text_path = '/Users/benjaminmoran/Desktop/eebo_strings'
xml_path = '/Users/benjaminmoran/eebo_tcp_data/data/eebo_raw/eebo_raw_combined'

def __load_xml__(tcp_no, file):

    tree = ET.parse(f'{xml_path}/{tcp_no}.P4.xml')
    root = tree.getroot()

    return tree, root, tcp_no


def __get_publication_date__(xml):

    tree, root, tcp_no = xml
    publication_date = 9999
    for date in root.iter('DATE'):
        text = date.text
        str_date = str(text)
        text_no_letters_or_punc = re.sub("[^0-9]","", str_date)
        if text_no_letters_or_punc == "":
            continue
        four_digit_year = int(text_no_letters_or_punc[:4])
        if (four_digit_year > 1450) and (four_digit_year < 1750) and (four_digit_year != ""):
            publication_date = four_digit_year

    return publication_date


def __count_books_by_year(publication_date, year_dict, year_dict_id):

    if publication_date not in year_dict:
        year_dict[publication_date] = 1
    else:
        year_dict[publication_date] += 1
    

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "

    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            decision = valid[default]
            return decision
        elif choice in valid:
            decision = valid[choice]
            return decision
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def print_output_to_csv(decision, year_dict, date):

    if decision == True:
        output_df = pd.DataFrame(data=(sorted(year_dict.items())))
        file = f'books_by_year_outputrecord.csv'
        output_df.to_csv()
        print("Your book history is available at: ", str(os.getcwd() + "/" + file))


def print_number_of_books_by_year():

    year_dict = {}
    date = str(datetime.now())
    year_dict_id = 1
    print("This is going to take a few minutes. Sit tight.")
    
    for file in os.listdir(xml_path):

        tcp_no = str(file).split(".")[0]
        loaded_xml = __load_xml__(tcp_no, file)
        publication_date = __get_publication_date__(loaded_xml)
        __count_books_by_year(publication_date, year_dict, year_dict_id)   

    print("")
    print("Year : Number of Books Printed In Year ")
    for key, value in sorted(year_dict.items()):
        
        print(f'{key}, : {value}')

    decision = query_yes_no("Do you want to save your word history as a csv?")
    print_output_to_csv(decision, year_dict, date)


if __name__ == "__main__":
    print_number_of_books_by_year()