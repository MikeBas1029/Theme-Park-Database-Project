from sqlalchemy import text 

# Birthday Discount Trigger
birthday_discount_trigger_after_insert = text("""
    CREATE IF NOT EXISTS TRIGGER birthday_discount_trigger_after_insert
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
birthday_discount_trigger_after_update = text("""
    CREATE TRIGGER IF NOT EXISTS birthday_discount_trigger_after_update
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

"""
Birthday Discount Trigger Documentation:

Purpose:
These triggers automatically create a birthday promotion notification for customers with a Platinum membership when it is their birthday. The triggers work for both newly inserted customers and existing customers whose information is updated.

Trigger Details:
1. **Triggers**:
   - `birthday_discount_trigger_after_insert`: Activated after a new customer record is inserted.
   - `birthday_discount_trigger_after_update`: Activated after an existing customer record is updated.
   
2. **Conditions**:
   - The customer must have a Platinum membership.
   - The customer's birthday must match the current date (both month and day).

3. **Functionality**:
   - When conditions are met, a new `notification_id` is generated for the birthday message.
   - A check is performed to ensure that a notification has not already been sent on the customer’s birthday for the current date.
   - If no notification has been sent today, an entry is added to the `customer_notifications` table with the following details:
     - `notification_id`: A randomly generated ID for the notification.
     - `customer_id`: The ID of the birthday customer.
     - `title`: A birthday greeting, e.g., "Happy Birthday from ShastaLand!"
     - `message`: Promotion message, e.g., "We wish you a happy birthday from us! Get 20% off a weekend pass."
     - `status`: Set to 'SENT' to mark it as sent.
     - `type`: Set to 'PROMO' indicating a promotional message.
     - `date_created`: Set to the current date.

Important Considerations:
- This trigger prevents multiple notifications from being sent on the same day by checking for existing notifications created today.
- The birthday promotion is only available to Platinum members.
- The `notification_id` is generated using a random hash to create a unique 12-character identifier.
- This trigger uses MySQL-specific functions and syntax, including date functions to determine the birthday match.

Usage:
- Insert this trigger in the database to automatically send a birthday notification and discount promotion to qualifying customers on their birthday.
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