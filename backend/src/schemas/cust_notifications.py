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

class CustomerNotificationInputModel(BaseModel):
    customer_id: str
    title: str 
    message: str
    status: Status
    type: NotificationType
    # date_created: date 

class CustomerNotificationOutputModel(BaseModel):
    notification_id: str
    customer_id: str
    title: str 
    message: str
    status: Status
    type: NotificationType
    date_created: date 
