import asyncio

from services.user import UserService
from services.expense import ExpenseService
from llm.llm import call_llm
from schemas import ExpenseSchema

async def main():
    # users = await UserService.get_all_users()
    # print(users)
    raw_text = "Здарова че как"
    # await call_llm(raw_text, output_schema=ExpenseSchema)
    expenses = await ExpenseService.insert_expenses(1, raw_text)
    print(expenses)

if __name__=="__main__":
    asyncio.run(main())