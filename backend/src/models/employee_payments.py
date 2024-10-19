from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey, Index
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.employees import Employees
    from src.models.payment_methods import PaymentMethods

class EmployeePayments(SQLModel, table=True):
    __tablename__ = "employeepayments"
    
    # EmployeePaymentID is the primary key that uniquely identifies each payment record.
    employee_payment_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique ID for each payment record"),
        alias="EmployeePaymentID"
    )
    
    # EmployeeID is the foreign key that links to the employee who received the payment.
    # It refers to the SSN of the employee in the employees table.
    employee_id: str = Field(
        sa_column=Column(mysql.VARCHAR(9), ForeignKey("employees.ssn"), nullable=False, comment="ID of the employee receiving the payment"),
        alias="EmployeeID"
    )
    
    # PaymentDate represents the date when the payment was made to the employee.
    # This is a required field, stored as a date value.
    payment_date: date = Field(sa_column=Column(mysql.DATE, nullable=False, comment="Date the payment was made"), alias="PaymentDate")
    
    # PaymentMethodID is the foreign key that links to the method used for the payment (e.g., direct deposit, check).
    # It refers to the PaymentMethodID in the paymentmethods table.
    payment_method_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("paymentmethods.payment_method_id", ondelete="RESTRICT"), nullable=False, comment="Payment method used for the payment"),
        alias="PaymentMethodID"
    )

    # Relationships
    # An employee can have multiple payments, linked through the employee_payment relationship.
    employee: "Employees" = Relationship(back_populates="employee_payments", cascade_delete=True)
    
    # Each payment record is associated with a payment method (e.g., direct deposit, check).
    payment_method: "PaymentMethods" = Relationship(
        back_populates="employee_payments",
        sa_relationship_kwargs={"lazy": "joined"}  # Eager load PaymentMethods with a JOIN
        )

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
        # For hourly employees, payment is based on hourly wage and hours worked
        if self.employee.employee_type == "Hourly" and self.employee.hourly_wage:
            return self.employee.hourly_wage * self.hours_worked
        
        # For salaried employees, payment is calculated as a pro-rated salary (e.g., bi-weekly)
        elif self.employee.employee_type == "Salary" and hasattr(self.employee, 'salary'):
            return self.employee.salary / 26  # Assuming salary is monthly, converted to bi-weekly pay

        # If no valid wage/salary is provided, return 0.0
        return 0.0
    
    # Table index: Adds an index on the employee_payment_id field.
    # This index improves performance for queries filtering by the employee_payment_id.
    __table_args__ = (
        Index("idx_employee_payment_id", "employee_payment_id"),
    )