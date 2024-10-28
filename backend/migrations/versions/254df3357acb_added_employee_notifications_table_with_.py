"""added employee notifications table with relationship to employees table.

Revision ID: 254df3357acb
Revises: 937dc0e381ee
Create Date: 2024-10-26 18:46:32.630182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum as SAEnum
import sqlalchemy.dialects.mysql as mysql
from enum import Enum
from datetime import date

# revision identifiers, used by Alembic.
revision: str = '254df3357acb'
down_revision: Union[str, None] = '937dc0e381ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enum for notification status
class Status(str, Enum):
    SENT = "SENT"
    READ = "READ"
    DISMISSED = "DISMISSED"

# Enum for notification type
class NotificationType(str, Enum):
    REMINDER = "REMINDER"
    PROMO = "PROMO"
    ALERT = "ALERT"

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customer_notifications', 'date_created',
               existing_type=sa.DATE(),
               comment="Customer's registration date",
               existing_comment='Date the notification was created',
               existing_nullable=False)
    
    # Create the customer_notifications table
    op.create_table(
        'employee_notifications',
        sa.Column('notification_id', mysql.VARCHAR(length=12), nullable=False, primary_key=True, comment="Unique ID for each notification"),
        sa.Column('employee_id', mysql.VARCHAR(length=12), sa.ForeignKey('employees.employee_id'), nullable=False, comment="Foreign Key to employee_id in employee table."),
        sa.Column('title', mysql.VARCHAR(length=50), nullable=False, comment="Title of the notification"),
        sa.Column('message', mysql.VARCHAR(length=150), nullable=False, comment="Notification message to the employee"),
        sa.Column('status', SAEnum(Status, values_callable=lambda x: [e.value for e in x]), nullable=False, default=Status.SENT, comment="Status of the notification."),
        sa.Column('type', SAEnum(NotificationType, values_callable=lambda x: [e.value for e in x]), nullable=False, default=NotificationType.ALERT, comment="Type of notification."),
        sa.Column('date_created', sa.Date, default=date.today, nullable=False, comment="Date the notification was created"),
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customer_notifications', 'date_created',
               existing_type=sa.DATE(),
               comment='Date the notification was created',
               existing_comment="Customer's registration date",
               existing_nullable=False)
    
    # Drop the customer_notifications table
    op.drop_table('customer_notifications')
    # ### end Alembic commands ###