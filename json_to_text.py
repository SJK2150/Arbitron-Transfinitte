# json_to_text.py
import json


def json_to_txt(json_data, output_file):
    # Open the output text file
    with open(output_file, 'w') as file:
        # Recursive function to process JSON data and write to file
        def process_json(data, indent=0):
            # For dictionary type data
            if isinstance(data, dict):
                for key, value in data.items():
                    file.write('  ' * indent + f"{key}:\n")
                    process_json(value, indent + 1)
            # For list type data
            elif isinstance(data, list):
                for item in data:
                    process_json(item, indent)
            # For other data types (strings, numbers)
            else:
                file.write('  ' * indent + str(data) + '\n')

        process_json(json_data)


# Example usage
if __name__ == "__main__":
    with open('output.json', 'r') as f:
        json_data = json.load(f)
    json_to_txt(json_data, 'output.txt')
