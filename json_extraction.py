# json_extraction.py
import spacy
from collections import defaultdict
import json

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define your custom entity types and keywords
custom_labels = {
    "CHANNEL": ["store", "online", "B2B", "retail"],
    "PRODUCT": ["electronics", "appliances", "private labels", "category mix", "assortment size", "category"],
    "CUSTOMER_SEGMENT": ["clients", "customers", "target audience", "audience"],
    "MARKETING_STRATEGY": ["social media", "influencer partnerships", "advertising", "campaign"],
    "AFTER_SALES": ["customer service", "recycling programs", "warranty", "disposal"],
    "AFFORDABILITY": ["financing options", "exchange policies", "affordable", "budget-friendly", "discounts",
                      "promotions", "price match guarantee", "loyalty programs", "payment plans", "cost-effective",
                      "value for money", "economical", "price reductions", "special offers", "buy now, pay later",
                      "seasonal sales", "clearance sales", "student discounts", "bulk purchase discounts",
                      "free trials", "money-back guarantees", "affordability assessments", "installment payments",
                      "affordable luxury", "financial assistance"],
    "SUPPLY_CHAIN": ["logistics", "inventory management", "distribution", "sourcing", "procurement",
                     "supplier relationships", "demand forecasting", "order fulfillment", "supply chain visibility",
                     "warehouse management", "transportation", "supply chain optimization", "cost reduction",
                     "risk management", "supply chain integration", "sustainable sourcing", "production planning",
                     "supplier diversity", "material handling", "supply chain analytics", "cross-docking",
                     "just-in-time delivery", "lead time reduction", "channel management", "reverse logistics"],
    "USABILITY": ["user experience", "interface design", "accessibility", "user-friendly", "interaction design",
                  "usability testing", "navigation", "responsive design", "intuitiveness", "feedback mechanisms",
                  "error prevention", "learnability", "consistency", "cognitive load", "affordance", "user research",
                  "task efficiency", "satisfaction", "mobile usability", "visual hierarchy", "personas", "prototyping",
                  "heuristic evaluation", "user scenarios", "performance metrics"]
}


# Function to generate a dictionary with context-based dynamic keys
def generate_dynamic_keys(entities, text):
    dynamic_keys = defaultdict(list)

    for entity, label in entities:
        # Store the entity along with its context (full sentence)
        dynamic_keys[label].append({
            "entity": entity,
            "context": text
        })

    return dict(dynamic_keys)


# Custom NER function to identify entities in the text
def custom_ner(text):
    doc = nlp(text)
    entities = []

    for token in doc:
        # Check against lowercase keywords for better matching
        for label, keywords in custom_labels.items():
            # Check if the token matches any keyword
            if token.text.lower() in keywords:
                entities.append((token.text, label))
                break

            # Check for phrases (for example, if two consecutive tokens form a valid phrase)
            if token.i < len(doc) - 1:  # Check next token if it exists
                phrase = f"{token.text} {doc[token.i + 1].text}".lower()
                if phrase in keywords:
                    entities.append((phrase, label))
                    break

    return entities


# Function to extract entities from a JSON file
def extract_entities_from_json(input_json_file):
    with open(input_json_file, "r",encoding='utf-8') as file:
        texts = json.load(file)

    # Process each text and generate a single dictionary for dynamic keys
    all_dynamic_keys = defaultdict(list)

    for text in texts:
        entities = custom_ner(text)
        dynamic_keys = generate_dynamic_keys(entities, text)

        # Merge the current dynamic keys into the overall dictionary, while keeping the context
        for key, values in dynamic_keys.items():
            all_dynamic_keys[key].extend(values)

    # Convert defaultdict to a regular dictionary
    all_dynamic_keys = dict(all_dynamic_keys)

    return all_dynamic_keys
