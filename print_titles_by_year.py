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

    return tree, root


def __check_for_date_match__(entered_year, xml):

    tree, root = xml
    entered_year = entered_year
    for year in root.iter('DATE'):
        text = year.text
        str_date = str(text)
        text_no_letters_or_punc = re.sub("[^0-9]","", str_date)

    if text_no_letters_or_punc == entered_year:
        year_check = True

    else:
        year_check = False

    return year_check

def __get_title_for_book__(year_check, xml):

    year_check = year_check
    tree, root = xml

    if year_check == False:
        return
    else:
        for e in root.iter('DATE'):
            title = e.text
    return title

def __get_author_for_book__(year_check, xml):

    year_check = year_check
    tree, root = xml

    if year_check == False:
        return
    else:
        for e in root.iter('AUTHOR'):
            author = e.text
    return author

def __create_new_row__(tcp_no, title, author, year_check):

    if year_check == True:

        tcp_no = tcp_no
        title = title
        author = author

        new_row = {'EEBO_TCP_Number': tcp_no, 'Title': title, 'Author': author}
        print(new_row)
        return new_row
    

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

def print_output_to_csv(decision, dataframe, entered_year):

    if decision == True:

        file = f'titles_for{entered_year}.csv'
        output_df.to_csv()
        print("Your book history is available at: ", str(os.getcwd() + "/" + file))


def print_titles_by_year():

    entered_year = input("Enter the year for which you'd like to print titles: ")

    # Need to do some validation here to ensure format of year is correct.
    # Need to also ensure that the date is within the permissible range.

    title_dataframe = pd.DataFrame(columns=['EEBO_TCP_Number', 'Title', 'Author'])
    print("This is going to take a few minutes. Sit tight.")
    
    for file in os.listdir(xml_path):

        tcp_no = str(file).split(".")[0]
        loaded_xml = __load_xml__(tcp_no, file)
        year_check = __check_for_date_match__(entered_year, loaded_xml)
        author = __get_author_for_book__(year_check, loaded_xml)
        title = __get_title_for_book__(year_check, loaded_xml)
        new_row = __create_new_row__(tcp_no, title, author, year_check)
        title_dataframe.append(new_row, ignore_index=True)

    print("")
    print(f"Titles for {entered_year}")
    print("")
    print("")

    print(title_dataframe)

    decision = query_yes_no("Do you want to save your word history as a csv?")
    print_output_to_csv(decision, title_dataframe, entered_year)


if __name__ == "__main__":
    print_titles_by_year()