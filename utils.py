from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

def create_docs(user_pdf_list):
    import pandas as pd
    import re

    df = pd.DataFrame(columns=[
        'Invoice no.', 'Description', 'Quantity', 'Date', 'Unit price',
        'Amount', 'Total', 'Email', 'Phone number', 'Address'
    ])

    for filename in user_pdf_list:
        raw_data = get_pdf_text(filename)
        print("extracted raw data")

        llm_extracted_data = extracted_data(raw_data)

        # Extract dictionary from LLM response
        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)
        if match:
            extracted_text = match.group(1)
            data_dict = eval('{' + extracted_text + '}')
        else:
            print("No match found.")
            data_dict = {}

        df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)

    return df

def get_pdf_text(pdf_doc):
    from pypdf import PdfReader
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
def extracted_data(pages_data):
    template = """
    Extract the following from the text:
    - Invoice no.
    - Description
    - Quantity
    - Date
    - Unit price
    - Amount
    - Total
    - Email
    - Phone number
    - Address

    Text:
    {pages}

    Expected Output:
    {{'Invoice no.': '...', 'Description': '...', 'Quantity': '...', 'Date': '...', 'Unit price': '...', 'Amount': '...', 'Total': '...', 'Email': '...', 'Phone number': '...', 'Address': '...'}}
    """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7,
        model="gpt-3.5-turbo-1106"
    )

    return llm.invoke(prompt_template.format(pages=pages_data))

