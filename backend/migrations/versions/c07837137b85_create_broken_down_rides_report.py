"""Create broken down rides report.

Revision ID: c07837137b85
Revises: 27583e444355
Create Date: 2024-10-30 19:46:07.540020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c07837137b85'
down_revision: Union[str, None] = '27583e444355'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE VIEW broken_rides AS
    SELECT 
        MONTH(wo.date_created) AS maintenance_month,
        COUNT(DISTINCT wo.ride_id) AS Num_Rides_Maintained,
        AVG(COUNT(DISTINCT wo.ride_id)) OVER() AS avg_rides_needing_maint
    FROM `theme-park-db`.workorder as wo
    WHERE 
        wo.maintenance_type = 'repair'
        AND wo.ride_id IS NOT NULL
        AND wo.status != 'canceled'
    GROUP BY 
        MONTH(wo.date_created);
    """)

def downgrade():
    op.execute("DROP VIEW IF EXISTS broken_rides;")