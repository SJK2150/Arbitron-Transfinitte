import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pdf_to_text import extract_text_from_pdf, save_text_to_file
from text_to_json import lines_to_list, write_list_to_files
from json_extraction import extract_entities_from_json
from myproject.myproject.spiders.first_spider import FirstSpider  # Import your web scraper spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Define the template for the LLM prompt
template = """
Answer below:
Here is the context: {context}
Question: {question}
Answer:
"""

# Initialize the LLM model
model = OllamaLLM(model="llama3.2:1b", streaming=True)
prompt = ChatPromptTemplate.from_template(template)

# Convert extracted text into chunks
def convert_text_to_chunks(input_text):
    lines = input_text.strip().splitlines()  # Split the input text into lines
    context_dict = {}  # Dictionary to store chunks by sections
    current_section = ""  # Track the current section

    # Process each line of text
    for line in lines:
        line = line.strip()

        # Check if the line indicates a new section (ends with a colon)
        if line.endswith(":"):
            current_section = line[:-1]  # Remove the colon
            if current_section not in context_dict:
                context_dict[current_section] = []  # Initialize a new section
        elif line.startswith("Entity"):
            # Add the line as a chunk to the current section
            chunk = f'"""\n  {line}\n"""'
            if current_section:
                # Ensure that no more than 20 chunks are added to the current section
                if len(context_dict[current_section]) < 20:
                    context_dict[current_section].append(chunk)

    # Generate the final output
    output = []
    for section, chunks in context_dict.items():
        # Convert the section's chunks into the desired format
        section_chunk = f"context_chunks_{section.lower()} = [\n  " + ",\n  ".join(chunks) + "\n]"
        output.append(section_chunk)

    # Return the formatted chunks
    return "\n\n".join(output)


# Parse contexts using Ollama LLM and a question
def parse_with_ollama(dom_chunks, question, max_chunks=3):
    # Slice to consider only the first max_chunks
    dom_chunks = dom_chunks[:max_chunks]
    chain = prompt | model
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"context": chunk, "question": question})
        print(f"Parsed chunk: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)



# Process all chunks with their associated questions
def process_all_chunks_with_questions(contexts_with_questions):
    results = []
    for entry in contexts_with_questions:
        result = parse_with_ollama(entry["context"], entry["question"])
        results.append(result)
    return results

# Convert JSON data from web scraping to text format
def json_to_txt(json_data):
    # Recursive function to process JSON data
    def process_json(data, indent=0):
        output = ""
        if isinstance(data, dict):
            for key, value in data.items():
                output += '  ' * indent + f"{key}:\n"
                output += process_json(value, indent + 1)
        elif isinstance(data, list):
            for item in data:
                output += process_json(item, indent)
        else:
            output += '  ' * indent + str(data) + '\n'
        return output

    return process_json(json_data)

# Function to run the Scrapy crawler programmatically
def run_web_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(FirstSpider)
    process.start()

    # Assuming your Scrapy spider saves output as a JSON file
    with open("output_scraped.json", 'r') as file:
        return json.load(file)

# Main function to handle the PDF and web scraping text extraction, chunking, and LLM processing
def main():
    # Step 1: Extract text from PDFs and save them to files
    pdf_paths = [
        r"C:\Users\Advaith\PycharmProjects\transfinitte(final)\Articles\adivis.pdf",
        r"C:\Users\Advaith\PycharmProjects\transfinitte(final)\Articles\vijaysales.pdf"
    ]

    output_files = []

    for i, pdf_path in enumerate(pdf_paths):
        extracted_text_path = f"extracted_text_{i + 1}.txt"
        pdf_text = extract_text_from_pdf(pdf_path)
        save_text_to_file(pdf_text, extracted_text_path)
        output_files.append(extracted_text_path)

    # Step 2: Convert text files to JSON and chunks
    contexts_with_questions = []

    for i, text_path in enumerate(output_files):
        line_list = lines_to_list(text_path)
        output_json_file = f'output_{i + 1}.json'
        write_list_to_files(line_list, text_path, output_json_file)

        # Step 3: Extract entities from the JSON file
        dynamic_keys = extract_entities_from_json(output_json_file)

        # Step 4: Convert text to chunks using the extracted entities
        chunked_contexts = convert_text_to_chunks(dynamic_keys)

        # Build contexts_with_questions for each context generated
        questions = [
            "What is the average rent of the store?",
            "What is the consumer electronics share?",
            "How does the warranty work?",
            "Tell me about loyalty programs and financing options?",
            "How is inventory management handled?"
        ]

        # Associate each chunked context with its respective question
        for question in questions:
            contexts_with_questions.append({"context": chunked_contexts, "question": question})

    # Step 5: Web scraping to get additional context
    scraped_data = run_web_scraper()
    scraped_text = json_to_txt(scraped_data)

    # Convert the scraped text to chunks
    scraped_chunks = convert_text_to_chunks(scraped_text)
    contexts_with_questions.append({"context": scraped_chunks, "question": "What are the main products on the website?"})

    # Step 6: Process all the contexts with questions through Ollama LLM
    final_results = process_all_chunks_with_questions(contexts_with_questions)

    # Print the results from all chunks with their respective questions
    for res in final_results:
        print(res)


if __name__ == "__main__":
    main()
