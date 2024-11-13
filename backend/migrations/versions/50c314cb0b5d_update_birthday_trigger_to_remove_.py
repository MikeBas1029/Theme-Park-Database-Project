"""Update birthday trigger to remove ticket insert.

Revision ID: 50c314cb0b5d
Revises: 642c2f001d74
Create Date: 2024-11-13 10:30:29.881337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50c314cb0b5d'
down_revision: Union[str, None] = '642c2f001d74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the existing triggers if they exist
    op.execute("""
    DROP TRIGGER IF EXISTS birthday_discount_trigger_after_insert;
    DROP TRIGGER IF EXISTS birthday_discount_trigger_after_update;
    """)

    # Create the AFTER INSERT trigger
    op.execute("""
    CREATE TRIGGER birthday_discount_trigger_after_insert
    AFTER INSERT ON customers
    FOR EACH ROW
    BEGIN
        DECLARE notification_id CHAR(12);
        SET notification_id = CONCAT(
            SUBSTRING(MD5(RAND()), 1, 6),
            SUBSTRING(MD5(RAND()), 7, 6)
        );

        IF NEW.membership_type = 'Platinum' AND 
           MONTH(NEW.date_of_birth) = MONTH(CURDATE()) AND 
           DAY(NEW.date_of_birth) = DAY(CURDATE()) THEN

            -- Insert notification, only if not already sent today
            IF NOT EXISTS (SELECT 1 FROM customer_notifications WHERE customer_id = NEW.customer_id AND date_created = CURDATE()) THEN
                INSERT INTO customer_notifications (notification_id, customer_id, title, message, status, type, date_created)
                VALUES (
                    notification_id,
                    NEW.customer_id,
                    'Happy Birthday from ShastaLand!',
                    'Use promo code BIRTHDAY to get 20% off a Weekend pass.',
                    'SENT',
                    'PROMO',
                    CURDATE()
                );
            END IF;
        END IF;
    END;
    """)

    # Create the AFTER UPDATE trigger
    op.execute("""
    CREATE TRIGGER birthday_discount_trigger_after_update
    AFTER UPDATE ON customers
    FOR EACH ROW
    BEGIN
        DECLARE notification_id CHAR(12);
        SET notification_id = CONCAT(
            SUBSTRING(MD5(RAND()), 1, 6),
            SUBSTRING(MD5(RAND()), 7, 6)
        );

        IF NEW.membership_type = 'Platinum' AND 
           MONTH(NEW.date_of_birth) = MONTH(CURDATE()) AND 
           DAY(NEW.date_of_birth) = DAY(CURDATE()) THEN

            -- Insert notification, only if not already sent today
            IF NOT EXISTS (SELECT 1 FROM customer_notifications WHERE customer_id = NEW.customer_id AND date_created = CURDATE()) THEN
                INSERT INTO customer_notifications (notification_id, customer_id, title, message, status, type, date_created)
                VALUES (
                    notification_id,
                    NEW.customer_id,
                    'Happy Birthday from ShastaLand!',
                    'Use promo code BIRTHDAY to get 20% off a Weekend pass.',
                    'SENT',
                    'PROMO',
                    CURDATE()
                );
            END IF;
        END IF;
    END;
    """)

    # Create the scheduled event
    op.execute("""
    CREATE EVENT IF NOT EXISTS birthday_discount_event
    ON SCHEDULE EVERY 1 DAY
    DO
    INSERT INTO customer_notifications (notification_id, customer_id, title, message, status, type, date_created)
    SELECT 
        CONCAT(SUBSTRING(MD5(RAND()), 1, 6), SUBSTRING(MD5(RAND()), 7, 6)) AS notification_id,
        customer_id, 
        'Happy Birthday from ShastaLand!', 
        'Use promo code BIRTHDAY to get 20% off a Weekend pass.',
        'SENT', 
        'PROMO', 
        CURDATE()
    FROM customers
    WHERE membership_type = 'Platinum' AND 
          MONTH(date_of_birth) = MONTH(CURDATE()) AND 
          DAY(date_of_birth) = DAY(CURDATE())
          AND customer_id NOT IN (SELECT customer_id FROM customer_notifications WHERE date_created = CURDATE());
    """)


def downgrade():
    # Drop the trigger and event during downgrade
    op.execute("""
    DROP TRIGGER IF EXISTS birthday_discount_trigger_after_insert;
    DROP TRIGGER IF EXISTS birthday_discount_trigger_after_update;
    """)

    op.execute("""
    DROP EVENT IF EXISTS birthday_discount_event;
    """)