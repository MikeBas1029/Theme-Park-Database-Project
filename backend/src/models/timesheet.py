from enum import Enum
from datetime import timezone, datetime
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, TYPE_CHECKING
from datetime import date, time, timedelta
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

if TYPE_CHECKING:
    from src.models.employees import Employees
    from src.models.sections import Section

# Enum for Timesheet Status
class TimesheetStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"

class Timesheet(SQLModel, table=True):
    """
    Represents an employee's timesheet for a specific shift, including shift times,
    meal breaks, and timesheet status.

    Attributes:
        shift_id (int): Unique identifier for the shift.
        employee_id (int): Foreign key reference to the employee (SSN).
        section_id (int): Foreign key reference to the section where the employee worked.
        shift_date (date): The date of the shift.
        punch_in_time (time): The time the employee punched in.
        punch_out_time (time): The time the employee punched out.
        meal_break_start (Optional[time]): The start time of the employee's meal break.
        meal_break_end (Optional[time]): The end time of the employee's meal break.
        status (TimesheetStatus): The current status of the timesheet (Pending, Approved, etc.).

    Relationships:
        employee (Employees): The employee associated with the timesheet.
        section (Section): The section associated with the timesheet.

    Methods:
        shift_duration_calculated: Calculates the total shift duration, excluding meal breaks.
        regular_hours: Calculates the regular hours of the shift (up to 8 hours).
        overtime_hours: Calculates the overtime hours (if shift exceeds 8 hours).
        set_shift_times: Sets the punch-in, punch-out, and meal break times for the shift.
    """

    __tablename__ = "timesheet"
    
    shift_id: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            primary_key=True, 
            nullable=False,
            comment="Unique identifier for the shift."
        ),
        alias="ShiftID"
    )

    employee_id: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("employees.ssn"),
            nullable=False,
            comment="Foreign key reference to the employee (SSN)."
        ),
        alias="EmployeeID"
    )
    
    section_id: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("sections.section_id"),
            nullable=False,
            comment="Foreign key reference to the section where the employee worked."
        ),
        alias="SectionID"
    )

    shift_date: date = Field(
        sa_column=Column(
            mysql.DATE, 
            nullable=False,
            comment="The date of the shift."
        ),
        alias="ShiftDate"
    )
    
    punch_in_time: time = Field(
        sa_column=Column(
            mysql.TIME, 
            nullable=False,
            comment="The time the employee punched in."
        ), 
        alias="PunchInTime"
    )
    
    punch_out_time: time = Field(
        sa_column=Column(
            mysql.TIME, 
            nullable=False,
            comment="The time the employee punched out."
        ), 
        alias="PunchOutTime"
    )
    
    meal_break_start: Optional[time] = Field(
        sa_column=Column(
            mysql.TIME,
            comment="The start time of the employee's meal break."
        ),
        alias="MealBreakStart"
    )
    
    meal_break_end: Optional[time] = Field(
        sa_column=Column(
            mysql.TIME, 
            comment="The end time of the employee's meal break."
        ),
        alias="MealBreakEnd"
    )
    
    status: TimesheetStatus = Field(
        sa_column=Column(
            mysql.ENUM(TimesheetStatus), 
            nullable=False,
            comment="The current status of the timesheet (Pending, Approved, etc.)."
        ), 
        alias="Status"
    )

    created_on: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            mysql.DATETIME, 
            nullable=False,
            comment="The timestamp when the timesheet was created."
        ),
        alias="CreatedOn"
    )
    
    updated_on: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            mysql.DATETIME, 
            nullable=True,
            sa_column_kwargs={"onupdate": "CURRENT_TIMESTAMP"}, 
            comment="The timestamp when the timesheet was last updated."
        ),
        alias="UpdatedOn"
    )
    
    created_by: str = Field(
        default=None, 
        sa_column=Column(
            mysql.VARCHAR(9),
            ForeignKey("employees.ssn"), 
            nullable=False,
            comment="Foreign key to the employee who created the timesheet."
        ),
        alias="CreatedBy"
    )
    
    updated_by: Optional[str] = Field(
        default=None, 
        sa_column=Column(
            mysql.VARCHAR(9),
            ForeignKey("employees.ssn"), 
            nullable=True,
            comment="Foreign key to the employee who last updated the timesheet."
        ),
        alias="UpdatedBy"
    )
    
    # Relationships
    employee: "Employees" = Relationship(
        back_populates="timesheets"
    )
    creator: "Employees" = Relationship(
        back_populates="timesheets"
    )
    updater: "Employees" = Relationship(
        back_populates="timesheets"
    )
    
    section: "Section" = Relationship(
        back_populates="timesheets"
    )

    
    @property
    def shift_duration_calculated(self) -> Optional[float]:
        """
        Calculates the total shift duration, excluding meal breaks. 
        The shift duration is computed by subtracting the punch-in time 
        from the punch-out time, and subtracting meal break time if applicable.
        
        Returns:
            Optional[float]: The total shift duration in hours, or None if 
            punch-in or punch-out times are not set.
        """
        if self.punch_in_time and self.punch_out_time:
            punch_in = timedelta(hours=self.punch_in_time.hour, minutes=self.punch_in_time.minute)
            punch_out = timedelta(hours=self.punch_out_time.hour, minutes=self.punch_out_time.minute)
            shift_time = punch_out - punch_in
            
            if self.meal_break_start and self.meal_break_end:
                meal_start = timedelta(hours=self.meal_break_start.hour, minutes=self.meal_break_start.minute)
                meal_end = timedelta(hours=self.meal_break_end.hour, minutes=self.meal_break_end.minute)
                meal_break_time = meal_end - meal_start
                shift_time -= meal_break_time
            
            total_hours = shift_time.total_seconds() / 3600.0
            return round(total_hours, 2)
        return None
    
    @property
    def regular_hours(self) -> Optional[float]:
        """
        Calculates the regular hours worked during the shift (up to 8 hours).
        
        If the shift duration exceeds 8 hours, only the first 8 hours are counted 
        as regular hours.

        Returns:
            Optional[float]: The regular hours worked during the shift, or None if 
            shift duration cannot be calculated.
        """
        shift_duration = self.shift_duration_calculated
        if shift_duration:
            regular_limit = 8.0
            return min(shift_duration, regular_limit)
        return None
    
    @property
    def overtime_hours(self) -> Optional[float]:
        """
        Calculates the overtime hours worked during the shift, if the shift duration 
        exceeds 8 hours.

        Overtime is calculated as any time worked beyond 8 hours in a shift.

        Returns:
            Optional[float]: The overtime hours worked during the shift, or 0.0 if 
            there is no overtime.
        """
        shift_duration = self.shift_duration_calculated
        if shift_duration:
            regular_limit = 8.0
            if shift_duration > regular_limit:
                return round(shift_duration - regular_limit, 2)
        return 0.0
    
    def set_shift_times(self, punch_in: time, punch_out: time, meal_start: Optional[time] = None, meal_end: Optional[time] = None):
        """
        Sets the punch-in, punch-out, and meal break times for the shift.
        
        This method allows you to define the times for the shift and meal breaks,
        which are then used in the calculation of shift duration and hours worked.

        Args:
            punch_in (time): The time the employee punched in for the shift.
            punch_out (time): The time the employee punched out from the shift.
            meal_start (Optional[time]): The start time of the meal break, if applicable.
            meal_end (Optional[time]): The end time of the meal break, if applicable.
        """
        self.punch_in_time = punch_in
        self.punch_out_time = punch_out
        self.meal_break_start = meal_start
        self.meal_break_end = meal_end

    __table_args__ = (
        Index("idx_shift_id", "shift_id"),
        Index("idx_employee_id", "employee_id"),
        Index("idx_section_id", "section_id")
    )