import spacy
from spacy.matcher import Matcher
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        num_pages = pdf_reader.getNumPages()
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text

def check_for_relevant_info(text):
    # Keywords and synonyms for relevant entities
    keywords = {
        "settlement_date": ["settlement date", "settle date", "settleday"],
        "trade_date": ["trade date", "tradeday"],
        "price": ["price", "cost", "value"],
        "amount": ["amount", "total"],
        "quantity": ["quantity", "qty"],
    }

    # Keywords for symbol, ticker, and description
    symbols = ["AAPL", "GOOGL", "AMZN", "MSFT"]
    tickers = ["AAPL", "GOOG", "AMZN", "MSFT"]
    descriptions = ["Apple Inc.", "Alphabet Inc.", "Amazon.com Inc.", "Microsoft Corporation"]

    # Step 2: Initialize NLP model (spaCy)
    nlp = spacy.load("en_core_web_sm", disable=["ner"])

    # Step 3: Tokenize the text
    doc = nlp(text)

    # Step 4: Search for Keywords and Synonyms
    matcher = Matcher(nlp.vocab)
    for key, syns in keywords.items():
        patterns = [[{"LOWER": syn.lower()}] for syn in syns]
        matcher.add(key, None, *patterns)

    matches = matcher(doc)

    # Step 5: Search for Symbol, Ticker, and Description
    matches["symbol"] = [entity.text for entity in doc if entity.text in symbols]
    matches["ticker"] = [entity.text for entity in doc if entity.text in tickers]
    matches["description"] = [entity.text for entity in doc if entity.text in descriptions]

    # Step 6: Extract Relevant Information
    relevant_info = {}
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        value = doc[start:end].text
        if label not in relevant_info:
            relevant_info[label] = value

    return relevant_info

if __name__ == "__main__":
    # Replace 'your_pdf_file.pdf' with the path to your PDF
    pdf_file_path = 'your_pdf_file.pdf'

    # Step 1: Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # Step 2-6: Check for relevant information for each page separately
    relevant_info_per_page = []
    pages = pdf_text.split('\x0c')  # Split the text by page separators
    for page_text in pages:
        relevant_info = check_for_relevant_info(page_text)
        relevant_info_per_page.append(relevant_info)

    # Step 7: Display the extracted relevant information for each page
    for page_num, info in enumerate(relevant_info_per_page, 1):
        print(f"Page {page_num}:")
        for key, value in info.items():
            print(f"{key}: {value}")
        print("\n")
