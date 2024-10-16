from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional
import sqlalchemy.dialects.mysql as mysql
from datetime import date, time, timedelta
from enum import Enum
from src.models import Employees, Section

# Enum for Timesheet Status
class TimesheetStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"

class Timesheet(SQLModel, table=True):
    __tablename__ = "timesheet"
    
    # Primary Key for the Assignment
    shift_id: int = Field(
        primary_key=True,
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="ShiftID"
    )

    # Foreign Keys for Employee and Section
    employee_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="employees.SSN",
        index=True,
        alias="EmployeeID"
    )
    
    section_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="sections.SectionID",
        index=True,
        alias="SectionID"
    )

    shift_date: date = Field(
        sa_column=Column(mysql.DATE, nullable=False),
        alias="ShiftDate"
    )
    
    # Punch In and Punch Out Times
    punch_in_time: time = Field(sa_column=Column(mysql.TIME, nullable=False), alias="PunchInTime")
    punch_out_time: time = Field(sa_column=Column(mysql.TIME, nullable=False), alias="PunchOutTime")
    
    # Meal Break (nullable, employee might not take one)
    meal_break_start: Optional[time] = Field(sa_column=Column(mysql.TIME), alias="MealBreakStart")
    meal_break_end: Optional[time] = Field(sa_column=Column(mysql.TIME), alias="MealBreakEnd")
    
    # Timesheet status (Pending, Approved, etc.)
    status: TimesheetStatus = Field(sa_column=Column(mysql.ENUM(TimesheetStatus), nullable=False), alias="Status")
    
    # Relationships with cascade options
    employee: "Employees" = Relationship(
        back_populates="timesheets",
        cascade_delete=True  # Cascade delete if employee is deleted
    )
    
    section: "Section" = Relationship(
        back_populates="timesheets",
        cascade_delete=True  # Cascade delete if section is deleted
    )
    
    # Derived Property to calculate total shift duration
    @property
    def shift_duration_calculated(self) -> Optional[float]:
        """Calculate the total shift duration, excluding meal breaks."""
        if self.punch_in_time and self.punch_out_time:
            # Calculate time difference between punch in and punch out
            punch_in = timedelta(hours=self.punch_in_time.hour, minutes=self.punch_in_time.minute)
            punch_out = timedelta(hours=self.punch_out_time.hour, minutes=self.punch_out_time.minute)
            shift_time = punch_out - punch_in
            
            # Subtract meal break if provided
            if self.meal_break_start and self.meal_break_end:
                meal_start = timedelta(hours=self.meal_break_start.hour, minutes=self.meal_break_start.minute)
                meal_end = timedelta(hours=self.meal_break_end.hour, minutes=self.meal_break_end.minute)
                meal_break_time = meal_end - meal_start
                shift_time -= meal_break_time
            
            # Convert shift time from seconds to hours
            total_hours = shift_time.total_seconds() / 3600.0
            return round(total_hours, 2)
        return None
    
    # Derived Property to calculate regular hours
    @property
    def regular_hours(self) -> Optional[float]:
        """Calculate the regular hours based on shift duration."""
        shift_duration = self.shift_duration_calculated
        if shift_duration:
            regular_limit = 8.0  # Regular hours limit (e.g., 8 hours)
            return min(shift_duration, regular_limit)
        return None
    
    # Derived Property to calculate overtime hours
    @property
    def overtime_hours(self) -> Optional[float]:
        """Calculate the overtime hours based on shift duration."""
        shift_duration = self.shift_duration_calculated
        if shift_duration:
            regular_limit = 8.0  # Regular hours limit (e.g., 8 hours)
            if shift_duration > regular_limit:
                return round(shift_duration - regular_limit, 2)
        return 0.0
    
    # Method to set shift based on punch in and punch out times
    def set_shift_times(self, punch_in: time, punch_out: time, meal_start: Optional[time] = None, meal_end: Optional[time] = None):
        """Set punch in, punch out, and meal break times."""
        self.punch_in_time = punch_in
        self.punch_out_time = punch_out
        self.meal_break_start = meal_start
        self.meal_break_end = meal_end

