import xml.etree.ElementTree as ET
import re
import os
import random
import time

def __output_text_file(file, tcp_no, folder):
    '''
    Outputs a plain .txt file with the tagless file content.
    '''

    file = file
    tcp_no = tcp_no
    xml_file = f'{tcp_no}.P4.xml'
    xml_folder_path = folder
    destination = '/Users/benjaminmoran/Desktop/eebo_strings'

    with open(f'{xml_folder_path}/{xml_file}', 'r') as r:
        contents = r.read()
        r.close()

    with open(f'{destination}/{tcp_no}.txt', 'w') as f:
        stringified_contents = ET.fromstring(contents)
        text = ''.join(stringified_contents[1][1].itertext())
        cleaned_text = re.sub('[^0-9a-zA-Z\&,;:?\-\'\.\s\|\b]+','',text)
        f.write(cleaned_text)
        f.close()

def convert_xml_to_txt():

    '''
    Converts input .XML files to cleaned .txt files.
    '''
    folder = '/Users/benjaminmoran/eebo_tcp_data/data/eebo_raw/eebo_raw_combined/'
    files = os.listdir(folder)
    start_time = time.time()

    for file in files:

        record_start_time = time.time()
        tcp_no = str(file).split(".")[0]
        file = f'{tcp_no}.P4.xml'
        __output_text_file(file, tcp_no, folder)
        print("--- %s seconds for record to complete---" % (time.time() - record_start_time))

    print("--- %s seconds for batch job to complete---" % (time.time() - start_time))

if __name__ == "__main__":
    convert_xml_to_txt()