from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

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

