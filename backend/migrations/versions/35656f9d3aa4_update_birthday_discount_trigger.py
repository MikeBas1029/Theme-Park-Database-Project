"""Update birthday discount trigger.

Revision ID: 35656f9d3aa4
Revises: 5796fe19b0a5
Create Date: 2024-10-24 06:34:02.639834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35656f9d3aa4'
down_revision: Union[str, None] = '5796fe19b0a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the existing trigger if it exists (optional, based on your use case)
    op.execute("""
    DROP TRIGGER IF EXISTS birthday_discount_trigger;
    """)

    # Create or update the trigger
    op.execute("""
    CREATE TRIGGER IF NOT EXISTS birthday_discount_trigger
    AFTER UPDATE ON customers
    FOR EACH ROW
    BEGIN
        IF NEW.membership_type = 'Platinum' AND 
        YEAR(NEW.date_of_birth) = YEAR(CURDATE()) AND
        MONTH(NEW.date_of_birth) = MONTH(CURDATE()) AND 
        DAY(NEW.date_of_birth) = DAY(CURDATE()) THEN
            INSERT INTO tickets (customer_id, ticket_type, price, purchase_date, start_date, expiration_date, discount, status)
            VALUES (NEW.customer_id, 'WEEKEND', 75.00, CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 YEAR), 15.00, 'ACTIVE');
        END IF;
    END;
""")

def downgrade():
    # Drop the trigger during downgrade to revert the changes
    op.execute("""
    DROP TRIGGER IF EXISTS update_total_price_trigger ON sales;
    """)
