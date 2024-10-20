# text_to_json.py
import sys
import json

# Ensure console output uses UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

def lines_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
        # Remove any empty strings
        lines = [line for line in lines if line]
    return lines

def write_list_to_files(line_list, output_txt_file, output_json_file):
    # Write the list to output.txt as a list
    with open(output_txt_file, 'w', encoding='utf-8') as f:
        f.write(repr(line_list))  # Using repr to write the list format

    # Write the list to a JSON file
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(line_list, f, ensure_ascii=False, indent=4)  # Writing as JSON
