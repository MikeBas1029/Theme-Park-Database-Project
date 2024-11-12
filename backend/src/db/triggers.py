from sqlalchemy import text 

# Birthday Discount Trigger
birthday_discount_trigger_after_insert = text("""
    CREATE TRIGGER IF NOT EXISTS birthday_discount_trigger_after_insert
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
birthday_discount_trigger_after_update = text("""
    CREATE TRIGGER IF NOT EXISTS birthday_discount_trigger_after_update
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

"""
Birthday Discount Trigger Documentation:

Purpose:
This trigger automatically creates a discounted weekend pass for reward members on their birthday.

Functionality:
1. Activates AFTER UPDATE operations on the 'customers' table.
2. Checks if the updated customer is a rewards member (rewards_member = 1).
3. Verifies if today is the customer's birthday by comparing month and day of birth_date with current date.
4. If conditions are met, inserts a new record into the 'tickets' table with the following details:
   - CustomerID: The ID of the customer whose record was updated
   - TicketType: 'WEEKEND'
   - Price: 75.00 (base price for a weekend pass)
   - PurchaseDate: Current date
   - StartDate: Current date
   - ExpirationDate: One year from the current date
   - Discount: 15.00 (20% discount)
   - Status: 'ACTIVE'

Important Considerations:
- This trigger will create a new ticket every time a qualifying customer's record is updated on their birthday.
- There's no built-in limit to prevent multiple discounts for the same birthday.
- The trigger assumes a fixed base price (100.00) and discount (20%) for the weekend pass.
- This trigger uses MySQL-specific date functions and syntax.
"""

# Ride Maintenance Status Trigger
change_status_if_not_inspected = text("""
CREATE TRIGGER IF NOT EXISTS update_ride_status
BEFORE UPDATE ON rides
FOR EACH ROW
BEGIN
    IF DATEDIFF(UTC_TIMESTAMP(), NEW.last_inspected) > 7 AND NEW.status != 'CLOSED(M)' THEN
        SET NEW.Status = 'CLOSED(M)';
    END IF;
END;
""")

"""
Ride Maintenance Status Trigger Documentation:

Purpose:
This trigger automatically updates a ride's status to 'CLOSED(M)' if it hasn't been inspected in the last 7 days.

Functionality:
1. Activates BEFORE UPDATE operations on the 'rides' table.
2. Calculates the number of days since the last inspection using DATEDIFF().
3. If more than 7 days have passed since the last inspection and the current status is not already 'CLOSED(M)',
   it changes the Status to 'CLOSED(M)'.

Important Considerations:
- This trigger will prevent any manual status updates that might overlook the need for maintenance.
- It ensures that rides are not operated if they haven't been inspected recently, promoting safety.
- The trigger uses UTC timestamp for consistency, especially if the system operates across multiple time zones.
"""