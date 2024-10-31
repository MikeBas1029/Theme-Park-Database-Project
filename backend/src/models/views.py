from sqlmodel import SQLModel, Field

class MonthlyWeeklyCustomerCounts(SQLModel, table=True):
    Month: int = Field(default=None, primary_key=True)
    Week: int = Field(default=None)
    Num_Customers: int = Field(default=None)


class FrequentRides(SQLModel, table=True):
    month: int = Field(primary_key=True, index=True)  # Assuming months are represented as integers (1-12)
    name: str  # Ride name
    num_rides: int  # Count of rides
