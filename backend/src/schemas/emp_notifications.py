from enum import Enum 
from datetime import date
from pydantic import BaseModel 

class Status(str, Enum):
    SENT = "SENT"
    READ = "READ"
    DISMISSED = "DISMISSED"

class NotificationType(str, Enum):
    REMINDER = "REMINDER"
    PROMO = "PROMO"
    ALERT = "ALERT"

class EmployeeNotificationInputModel(BaseModel):
    employee_id: str
    title: str 
    message: str
    status: Status
    type: NotificationType

class EmployeeNotificationOutputModel(BaseModel):
    notification_id: str
    employee_id: str
    title: str 
    message: str
    status: Status
    type: NotificationType
    date_created: date 
