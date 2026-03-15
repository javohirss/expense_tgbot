from typing import Literal
from pydantic import BaseModel, Field

CatsType = Literal['Транспорт', 'Спорт', 'Одежда', 'Товары', 'Продукты', 'Здоровье', 'Сервисы/Подписки', 'Рестораны (готовая еда)', 'Развлечения']


class Expense(BaseModel):
    title: str = Field(..., description="Название траты из сообщения")
    category: CatsType = Field(..., description="Категория траты")
    amount: float = Field(..., description="Сумма траты")


class ExpenseSchema(BaseModel):
    expenses: list[Expense] = Field(..., description="Список трат")