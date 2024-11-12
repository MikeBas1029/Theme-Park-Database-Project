"""Fix: removed check for current year in birthday trigger, should only check for month/day.

Revision ID: 5d671c537215
Revises: 6eade1e93696
Create Date: 2024-11-10 08:54:13.622188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d671c537215'
down_revision: Union[str, None] = '6eade1e93696'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the existing trigger if it exists (optional, based on your use case)
    op.execute("""
    DROP TRIGGER IF EXISTS birthday_discount_trigger;
    """)

    # Create or update the trigger
    op.execute(
    """
    CREATE TRIGGER IF NOT EXISTS birthday_discount_trigger
    AFTER UPDATE ON customers
    FOR EACH ROW
    BEGIN
        IF NEW.membership_type = 'Platinum' AND 
        MONTH(NEW.date_of_birth) = MONTH(CURDATE()) AND 
        DAY(NEW.date_of_birth) = DAY(CURDATE()) THEN
                                    
            -- Insert discounted ticket                         
            INSERT INTO tickets (customer_id, ticket_type, price, purchase_date, start_date, expiration_date, discount, status)
            VALUES (NEW.customer_id, 'WEEKEND', 75.00, CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 YEAR), 15.00, 'ACTIVE');
                                    
            -- Insert notification for new ticket
            INSERT INTO customer_notifications (customer_id, title, message, status, type, date_created)
            VALUES (
                NEW.customer_id,
                'Happy Birthday from ShastaLand!',
                'We wish you a happy birthday from us! Get 20% off a weekend pass.'
                'SENT',
                'PROMO',
                CURDATE()
            );                         
        END IF;
    END;
    """)

def downgrade():
    # Drop the trigger during downgrade to revert the changes
    op.execute("""
    DROP TRIGGER IF EXISTS update_total_price_trigger ON sales;
    """)

