"""Feat: add event to check daily for birthdays and updated trigger.

Revision ID: 9759d001386a
Revises: 5d671c537215
Create Date: 2024-11-10 09:10:35.728413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9759d001386a'
down_revision: Union[str, None] = '5d671c537215'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Drop the existing triggers if they exist
    op.execute("""
    DROP TRIGGER IF EXISTS birthday_discount_trigger_after_insert;
    DROP TRIGGER IF EXISTS birthday_discount_trigger_after_update;
    """)

    # Create the AFTER INSERT trigger with random ticket_id generation
    op.execute("""
    CREATE TRIGGER birthday_discount_trigger_after_insert
    AFTER INSERT ON customers
    FOR EACH ROW
    BEGIN
        DECLARE ticket_id CHAR(12);
        DECLARE notification_id CHAR(12);
        SET ticket_id = CONCAT(
            SUBSTRING(MD5(RAND()), 1, 6),
            SUBSTRING(MD5(RAND()), 7, 6)
        );
        SET notification_id = CONCAT(
            SUBSTRING(MD5(RAND()), 1, 6),
            SUBSTRING(MD5(RAND()), 7, 6)
        );

        IF NEW.membership_type = 'Platinum' AND 
           MONTH(NEW.date_of_birth) = MONTH(CURDATE()) AND 
           DAY(NEW.date_of_birth) = DAY(CURDATE()) THEN
           
            -- Insert discounted ticket with random ticket_id, only if not already given today
            IF NOT EXISTS (SELECT 1 FROM tickets WHERE customer_id = NEW.customer_id AND purchase_date = CURDATE()) THEN
                INSERT INTO tickets (ticket_id, customer_id, ticket_type, price, purchase_date, start_date, expiration_date, discount, status)
                VALUES (ticket_id, NEW.customer_id, 'WEEKEND', 75.00, CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 YEAR), 15.00, 'ACTIVE');
            END IF;

            -- Insert notification, only if not already sent today
            IF NOT EXISTS (SELECT 1 FROM customer_notifications WHERE customer_id = NEW.customer_id AND date_created = CURDATE()) THEN
                INSERT INTO customer_notifications (notification_id, customer_id, title, message, status, type, date_created)
                VALUES (
                    notification_id,
                    NEW.customer_id,
                    'Happy Birthday from ShastaLand!',
                    'We wish you a happy birthday from us! Get 20% off a weekend pass.',
                    'SENT',
                    'PROMO',
                    CURDATE()
                );
            END IF;
        END IF;
    END;
    """)

    # Create the AFTER UPDATE trigger with random ticket_id generation
    op.execute("""
    CREATE TRIGGER birthday_discount_trigger_after_update
    AFTER UPDATE ON customers
    FOR EACH ROW
    BEGIN
        DECLARE ticket_id CHAR(12);
        DECLARE notification_id CHAR(12);
        SET ticket_id = CONCAT(
            SUBSTRING(MD5(RAND()), 1, 6),
            SUBSTRING(MD5(RAND()), 7, 6)
        );
        SET notification_id = CONCAT(
            SUBSTRING(MD5(RAND()), 1, 6),
            SUBSTRING(MD5(RAND()), 7, 6)
        );

        IF NEW.membership_type = 'Platinum' AND 
           MONTH(NEW.date_of_birth) = MONTH(CURDATE()) AND 
           DAY(NEW.date_of_birth) = DAY(CURDATE()) THEN
           
            -- Insert discounted ticket with random ticket_id, only if not already given today
            IF NOT EXISTS (SELECT 1 FROM tickets WHERE customer_id = NEW.customer_id AND purchase_date = CURDATE()) THEN
                INSERT INTO tickets (ticket_id, customer_id, ticket_type, price, purchase_date, start_date, expiration_date, discount, status)
                VALUES (ticket_id, NEW.customer_id, 'WEEKEND', 75.00, CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 YEAR), 15.00, 'ACTIVE');
            END IF;

            -- Insert notification, only if not already sent today
            IF NOT EXISTS (SELECT 1 FROM customer_notifications WHERE customer_id = NEW.customer_id AND date_created = CURDATE()) THEN
                INSERT INTO customer_notifications (notification_id, customer_id, title, message, status, type, date_created)
                VALUES (
                    notification_id,
                    NEW.customer_id,
                    'Happy Birthday from ShastaLand!',
                    'We wish you a happy birthday from us! Get 20% off a weekend pass.',
                    'SENT',
                    'PROMO',
                    CURDATE()
                );
            END IF;
        END IF;
    END;
    """)

    # Create the scheduled event with random ticket_id generation
    op.execute(
    """
    CREATE EVENT IF NOT EXISTS birthday_discount_event
    ON SCHEDULE EVERY 1 DAY
    DO
    BEGIN
        DECLARE ticket_id CHAR(12);
        DECLARE notification_id CHAR(12);

        -- Insert discounted ticket for each eligible customer whose birthday is today
        INSERT INTO tickets (ticket_id, customer_id, ticket_type, price, purchase_date, start_date, expiration_date, discount, status)
        SELECT 
            CONCAT(SUBSTRING(MD5(RAND()), 1, 6), SUBSTRING(MD5(RAND()), 7, 6)) AS ticket_id, 
            customer_id, 
            'WEEKEND', 
            75.00, 
            CURDATE(), 
            CURDATE(), 
            DATE_ADD(CURDATE(), INTERVAL 1 YEAR), 
            15.00, 
            'ACTIVE'
        FROM customers
        WHERE membership_type = 'Platinum' AND 
              MONTH(date_of_birth) = MONTH(CURDATE()) AND 
              DAY(date_of_birth) = DAY(CURDATE())
              AND customer_id NOT IN (SELECT customer_id FROM tickets WHERE purchase_date = CURDATE());

        -- Insert notification for eligible customers whose birthday is today
        INSERT INTO customer_notifications (customer_id, title, message, status, type, date_created)
        SELECT 
                CONCAT(SUBSTRING(MD5(RAND()), 1, 6), SUBSTRING(MD5(RAND()), 7, 6)) AS notification_id,
                customer_id, 
               'Happy Birthday from ShastaLand!', 
               'We wish you a happy birthday from us! Get 20% off a weekend pass.', 
               'SENT', 
               'PROMO', 
               CURDATE()
        FROM customers
        WHERE membership_type = 'Platinum' AND 
              MONTH(date_of_birth) = MONTH(CURDATE()) AND 
              DAY(date_of_birth) = DAY(CURDATE())
              AND customer_id NOT IN (SELECT customer_id FROM customer_notifications WHERE date_created = CURDATE());
    END;
    """
    )

def downgrade():
    # Drop the trigger and event during downgrade
    op.execute("""
    DROP TRIGGER IF EXISTS birthday_discount_trigger_after_insert;
    DROP TRIGGER IF EXISTS birthday_discount_trigger_after_update;
    """)
    
    op.execute("""
    DROP EVENT IF EXISTS birthday_discount_event;
    """)