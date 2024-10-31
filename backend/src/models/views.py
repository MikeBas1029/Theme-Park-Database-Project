from sqlmodel import SQLModel, Field

class MonthlyWeeklyCustomerCounts(SQLModel, table=True):
    Month: int = Field(default=None, primary_key=True)
    Week: int = Field(default=None)
    Num_Customers: int = Field(default=None)