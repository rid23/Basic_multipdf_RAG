"""this module is responsible for the LLM brain of the agent. It uses the Google Gemini 2.5 Flash model to generate responses based on the prompts provided by the agent.
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser




def the_brain(llm , context:str , query:str) -> str:

    template = """You are a helpful assistant that provides concise and accurate answers to user queries based on the provided context. Use the context to answer the question.

    Context: {context}
    Question: {question}
    Answer:"""
    
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    rag_chain = (
         prompt | llm | StrOutputParser()    )


    result = rag_chain.invoke({"context": context , "question": query})
    
    return result