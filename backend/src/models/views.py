from sqlmodel import SQLModel, Field

class MonthlyWeeklyCustomerCounts(SQLModel, table=False):
    Month: int = Field(default=None, primary_key=True)
    Week: int = Field(default=None)
    Num_Customers: int = Field(default=None)


class FrequentRides(SQLModel, table=False):
    month: int = Field(primary_key=True, index=True)  # Assuming months are represented as integers (1-12)
    name: str  # Ride name
    num_rides: int  # Count of rides

class BrokenRides(SQLModel, table=False):
    Maintenance_Month: int = Field(primary_key=True, index=True)  # Assuming months are represented as integers (1-12)
    Num_Rides_Maintained: int  # Count of rides
    avg_rides_needing_maint: float 
