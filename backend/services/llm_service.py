from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def forRag(question: str, db):
    # Use direct similarity search instead of retriever
    results = db.similarity_search(question, k=5)
    context = "\n".join([doc.page_content for doc in results])

    llm = ChatGroq(
        groq_api_key="",
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
You are the best teacher in the world, brilliant in Java.
Explain concepts clearly with simple real-world analogies.
Use only the retrieved context to answer.
If context is insufficient, say "I don't know".

Context:
{context}

Question: {question}

Answer:
""")

    chain = (
        {
            "context": lambda q: context,   # use already retrieved context
            "question": lambda q: q
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(question)


def ask_llm(c: str, userm: str):
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    groq_api_key = ""
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
Role: You are a chatbot who explains the core topics in the data you get.
Context: Use the provided text to find core topics and explain clearly 
with examples (max 8 lines).Explain the concept whoch is core from the data ypu get

Data: {c}
Query: {userm}

Answer:
""")

    formatted = prompt.format(c=c, userm=userm)
    response = llm.invoke(formatted)
    print(c)
    return response.content
