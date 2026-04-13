from datetime import datetime, timezone
from decimal import Decimal
from google.genai.errors import ServerError

from sqlalchemy import func, insert, select

from database.models import Expense, User
from database.session import MyAsyncSession
from llm.llm import call_llm
from .user import UserService


class ExpenseService:
    @classmethod
    async def get_expense_by_id(cls, eid):
        async with MyAsyncSession() as session:
            query = select(Expense).where(Expense.id == eid)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    
    @classmethod
    async def insert_expenses(cls, telegram_user_id: int, raw_text: str):
        async with MyAsyncSession() as session:
            user = await UserService.get_or_create_user(telegram_user_id)
            primary_model = "gemini-3.1-flash-lite-preview"
            fallback_model = "gemini-3-flash-preview"

            try:
                llm_result = await call_llm(raw_text, primary_model)
            except ServerError as e:
                is_503_unavailable = e.code == 503 and e.status == "UNAVAILABLE"
                if not is_503_unavailable:
                    raise

                llm_result = await call_llm(raw_text, fallback_model)

            parsed_expenses = llm_result.expenses if llm_result else []
            if not parsed_expenses:
                return []

            query = insert(Expense).returning(Expense)
            values = [
                {
                    "user_id": user.id,
                    "title": expense.title,
                    "category": expense.category,
                    "amount": expense.amount,
                    "raw_text": raw_text
                }
                for expense in parsed_expenses
            ]
            result = await session.execute(query, values)
            await session.commit()
            return result.scalars().all()
        
        
    @classmethod
    async def get_today_totals(cls, telegram_user_id: int):
        now = datetime.now(timezone.utc)
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        async with MyAsyncSession() as session:
            query = (
                select(
                    Expense.category,
                    func.sum(Expense.amount).label("total_amount"),
                )
                .join(User, User.id == Expense.user_id)
                .where(User.telegram_user_id == telegram_user_id)
                .where(Expense.created_at >= day_start)
                .where(Expense.created_at <= now)
                .group_by(Expense.category)
                .order_by(Expense.category)
            )
            result = await session.execute(query)

            return [
                {
                    "category": category,
                    "total_amount": float(total_amount or Decimal("0")),
                }
                for category, total_amount in result.all()
            ]


    @classmethod
    async def get_current_month_totals_by_category(cls, telegram_user_id: int):
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        async with MyAsyncSession() as session:
            query = (
                select(
                    Expense.category,
                    func.sum(Expense.amount).label("total_amount"),
                )
                .join(User, User.id == Expense.user_id)
                .where(User.telegram_user_id == telegram_user_id)
                .where(Expense.created_at >= month_start)
                .where(Expense.created_at <= now)
                .group_by(Expense.category)
                .order_by(Expense.category)
            )
            result = await session.execute(query)

            return [
                {
                    "category": category,
                    "total_amount": float(total_amount or Decimal("0")),
                }
                for category, total_amount in result.all()
            ]


