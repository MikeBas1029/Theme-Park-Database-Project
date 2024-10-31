"""Create most frequent rides view.

Revision ID: 27583e444355
Revises: 0be59c3ada31
Create Date: 2024-10-30 19:21:50.235492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27583e444355'
down_revision: Union[str, None] = '0be59c3ada31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE VIEW frequent_rides AS
    SELECT 
        MONTH(ru.usage_date) AS Month,
        ride.name,
        COUNT(ru.customer_id) AS num_rides
    FROM `theme-park-db`.`ride_usage` AS ru
    LEFT JOIN `theme-park-db`.rides AS ride
    ON ru.ride_id = ride.ride_id
    GROUP BY 
        ru.ride_id, 
        ride.name, 
        MONTH(usage_date)
    ORDER BY month, num_rides DESC;
    """)

def downgrade():
    op.execute("DROP VIEW IF EXISTS frequent_rides;")