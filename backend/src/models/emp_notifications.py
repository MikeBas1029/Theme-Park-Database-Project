'''
you could add a FK to userID, add a user type(employee, customer, admin), 
title, message,  created_at date, status (sent, read dismissed) ,
 notification type (reminder, promotion, alert) and i think its it for now maybe a 

'''

import string
import secrets
from enum import Enum 
from datetime import date
from sqlalchemy import Enum as SAEnum
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey, func

if TYPE_CHECKING:
    from src.models.employees import Employees

class Status(str, Enum):
    SENT = "SENT"
    READ = "READ"
    DISMISSED = "DISMISSED"

class NotificationType(str, Enum):
    REMINDER = "REMINDER"
    PROMO = "PROMO"
    ALERT = "ALERT"

class EmployeeNotifications(SQLModel, table=True):
    __tablename__ = "employee_notifications"

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    

    notification_id: str = Field(
        default_factory=lambda: EmployeeNotifications.generate_random_id(),
        sa_column=Column(mysql.VARCHAR(12), nullable=False, primary_key=True, comment="Unique ID for each notification"),
        alias="Notification ID"
    )

    employee_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("employees.employee_id"),
            nullable=False,
            comment="Foreign Key to employee_id in employees table."
        )
    )
    
    title: str = Field(
        sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="Title of the notification"), 
        alias="Title"
    )

    message: str = Field(
        sa_column=Column(
            mysql.VARCHAR(150), 
            nullable=False, 
            comment="Notification message to the employee"
        )
    )

    status: Status = Field(
        sa_column=Column(
            SAEnum(Status, values_callable=lambda x: [e.value for e in x]), 
            nullable=False, default=Status.SENT, 
            comment="Status of the notification."
        ), 
    )

    type: NotificationType = Field(
        sa_column=Column(
            SAEnum(NotificationType, values_callable=lambda x: [e.value for e in x]), 
            nullable=False, default=NotificationType.ALERT, 
            comment="Type of notification."
        ), 
    )
    
    # registration_date is the date when the customer registered for the service.
    date_created: date = Field(
        default_factory=date.today, 
        sa_column=Column(
            mysql.DATE, 
            nullable=False, 
            comment="Date the notification was created"
            ), 
        )


    # Relationships
    employee: "Employees" = Relationship(back_populates="emp_notification")
