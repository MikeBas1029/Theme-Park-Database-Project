"""added customer notification table and relationship with customers table.

Revision ID: 937dc0e381ee
Revises: 959d713bd309
Create Date: 2024-10-26 18:16:15.293989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum as SAEnum
import sqlalchemy.dialects.mysql as mysql
from enum import Enum
from datetime import date


# revision identifiers, used by Alembic.
revision: str = '937dc0e381ee'
down_revision: Union[str, None] = '959d713bd309'
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
    # Create the customer_notifications table
    op.create_table(
        'customer_notifications',
        sa.Column('notification_id', mysql.VARCHAR(length=12), nullable=False, primary_key=True, comment="Unique ID for each notification"),
        sa.Column('customer_id', mysql.VARCHAR(length=12), sa.ForeignKey('customers.customer_id'), nullable=False, comment="Foreign Key to customer_id in customers table."),
        sa.Column('title', mysql.VARCHAR(length=50), nullable=False, comment="Title of the notification"),
        sa.Column('message', mysql.VARCHAR(length=150), nullable=False, comment="Notification message to the customer"),
        sa.Column('status', SAEnum(Status, values_callable=lambda x: [e.value for e in x]), nullable=False, default=Status.SENT, comment="Status of the notification."),
        sa.Column('type', SAEnum(NotificationType, values_callable=lambda x: [e.value for e in x]), nullable=False, default=NotificationType.ALERT, comment="Type of notification."),
        sa.Column('date_created', sa.Date, default=date.today, nullable=False, comment="Date the notification was created"),
    )


def downgrade() -> None:
    # Drop the customer_notifications table
    op.drop_table('customer_notifications')