from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from config import settings
from .prompt import prompt
from schemas import ExpenseSchema

def gemini(model_name: str = "gemini-3.1-flash-lite-preview"):
    return ChatGoogleGenerativeAI(
        model=model_name,
        api_key=settings.GEMINI_API_KEY
    )

llm = gemini()


async def call_llm(user_query: str, output_schema: BaseModel = ExpenseSchema):
    messages = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", user_query)
    ])

    chain = messages | llm.with_structured_output(output_schema)
    response = await chain.ainvoke({})
    print(response)
    return response
