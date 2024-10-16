from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Employees, PaymentMethods

class EmployeePayments(SQLModel, table=True):
    __tablename__ = "employeepayments"
    
    employee_payment_id: int = Field(
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="EmployeePaymentID"
    )
    employee_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="employees.SSN",
        alias="EmployeeID"
    )
    payment_date: date = Field(sa_column=Column(mysql.DATE), alias="PaymentDate")
    payment_method_id: int = Field(
        sa_column=Column(mysql.INTEGER),
        foreign_key="paymentmethods.PaymentMethodID",
        ondelete="RESTRICT",
        alias="PaymentMethodID"
    )

    # Relationships
    employee: "Employees" = Relationship(back_populates="employee_payments", cascade='all, delete-orphan')
    payment_method: "PaymentMethods" = Relationship(back_populates="employee_payments")

    @property
    def hours_worked(self) -> float:
        """
        Calculate total hours worked from timesheet records
        for this employee during the payment period.
        """
        total_hours = 0.0
        # Assuming a `Timesheet` model exists where the work hours are recorded
        for timesheet in self.employee.timesheets:
            total_hours += timesheet.regular_hours  # Assuming this is already calculated for each shift
            total_hours += timesheet.overtime_hours  # Include overtime hours if applicable
        return round(total_hours, 2)

    @property
    def calculated_payment_amount(self) -> float:
        """
        Calculate the payment amount based on the hours worked
        and the employee's pay rate.
        """
        if self.employee.employee_type == "Hourly" and self.employee.hourly_wage:
            return self.employee.hourly_wage * self.hours_worked
        elif self.employee.employee_type == "Salary" and self.employee.salary:
            # Assuming salary is monthly, so calculate a pro-rated amount for the payment period if needed
            return self.employee.salary / 26  # Monthly salary converted to weekly or bi-weekly if needed
        return 0.0