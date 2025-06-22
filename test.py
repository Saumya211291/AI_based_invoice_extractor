from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key="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",  # replace with your actual key
    model="gpt-3.5-turbo-1106",
    temperature=0.7
)

response = llm.invoke("Hello, what is today's date?")
print(response)
