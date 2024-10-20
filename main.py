from pdf_to_text import extract_text_from_pdf, save_text_to_file
from text_to_json import lines_to_list, write_list_to_files
from json_extraction import extract_entities_from_json
from llama import process_all_chunks_with_questions  # Import Llama functions
from myproject.myproject.spiders.first_spider import FirstSpider  # Import your web scraper spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def convert_text_to_chunks(input_text, max_chunk_size=3000):
    # Splitting the input text into lines
    lines = input_text.strip().splitlines()

    # Dictionary to hold the formatted chunks by sections
    context_dict = {}
    current_section = ""
    current_chunk = []

    # Process each line and group lines into larger chunks
    for line in lines:
        line = line.strip()

        # Check if the line is a section header
        if line.endswith(":"):
            current_section = line[:-1]
            if current_section not in context_dict:
                context_dict[current_section] = []  # Create a new section list

        # Append lines to the current chunk
        if current_section and len(current_chunk) < max_chunk_size:
            current_chunk.append(line)
        else:
            # If the current chunk exceeds max_chunk_size, finalize and create a new one
            context_dict[current_section].append("\n".join(current_chunk))
            current_chunk = [line]

    # Add any remaining lines in the current chunk
    if current_chunk:
        context_dict[current_section].append("\n".join(current_chunk))

    # Generate final output of chunks by section
    output = []
    for section, chunks in context_dict.items():
        section_chunk = f"context_chunks_{section.lower()} = [\n  " + ",\n  ".join(
            f'"""\n{chunk}\n"""' for chunk in chunks) + "\n]"
        output.append(section_chunk)

    return "\n\n".join(output)


def save_chunks_to_file(chunks, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(chunks)
    print(f"Chunks saved to {output_file}")

def process_pdf(pdf_path, extracted_text_filename, output_txt_file, output_json_file, chunks_file):
    # Step 1: Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    save_text_to_file(pdf_text, extracted_text_filename)

    print(f"Extracted text saved to {extracted_text_filename}")

    # Step 2: Convert text to JSON
    line_list = lines_to_list(extracted_text_filename)
    write_list_to_files(line_list, output_txt_file, output_json_file)

    print(f"Text converted to JSON and saved to {output_json_file}")

    # Step 3: Extract entities from the JSON file
    dynamic_keys = extract_entities_from_json(output_json_file)

    # Prepare the entity data for chunking
    formatted_entities = ""
    for key, values in dynamic_keys.items():
        formatted_entities += f"{key}:\n"
        for value in values:
            formatted_entities += f"  Entity: {value['entity']}, Context: {value['context']}\n"

    # Step 4: Convert to chunks and save
    chunks = convert_text_to_chunks(formatted_entities)
    save_chunks_to_file(chunks, chunks_file)

    # Step 5: Return chunks for further processing (for Llama model)
    return formatted_entities  # Returning the chunks in the required format

def run_llama_on_chunks(chunks, questions):
    # Generate context chunks and questions for the Llama model
    contexts_with_questions = []
    for question in questions:
        context_chunk = convert_text_to_chunks(chunks)  # Convert the text into the right format
        contexts_with_questions.append({"context": context_chunk, "question": question})

    # Process the chunks with questions using the Llama model
    final_results = process_all_chunks_with_questions(contexts_with_questions)

    # Print results
    for result in final_results:
        print(result)

# Function to run the Scrapy crawler programmatically


def main():
    # Process adivis.pdf
    adivis_chunks = process_pdf(
        pdf_path=r"C:\Users\Advaith\PycharmProjects\transfinitte(final)\Articles\adivis.pdf",
        extracted_text_filename="extracted_text_adivis.txt",
        output_txt_file="output_adivis.txt",
        output_json_file="output_adivis.json",
        chunks_file="chunks_adivis.txt"
    )

    # Process vijaysales.pdf
    vijaysales_chunks = process_pdf(
        pdf_path=r"C:\Users\Advaith\PycharmProjects\transfinitte(final)\Articles\vijaysales.pdf",
        extracted_text_filename="extracted_text_vijaysales.txt",
        output_txt_file="output_vijaysales.txt",
        output_json_file="output_vijaysales.json",
        chunks_file="chunks_vijaysales.txt"
    )



    # Define questions to ask the Llama model
    questions = [
        "What is the average rent of the store?",
        "What is the consumer electronics share?",
        "How does the warranty work?",
        "Tell me about loyalty programs and financing options?",
        "How is inventory management handled?",
        "What are the main products listed on the website?"
    ]

    # Run the Llama model on the chunks extracted from PDFs
    print("Running Llama on Adivis chunks...")
    run_llama_on_chunks(adivis_chunks, questions)

    # Run the Llama model on the chunks extracted from the web scraping


if __name__ == "__main__":
    main()
