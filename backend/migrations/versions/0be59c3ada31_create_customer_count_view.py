"""Create customer count view.

Revision ID: 0be59c3ada31
Revises: 742fb06d7738
Create Date: 2024-10-30 18:57:17.160274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0be59c3ada31'
down_revision: Union[str, None] = '742fb06d7738'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE VIEW monthly_weekly_customer_counts AS
    SELECT 
        MONTH(visit_date) AS Month,
        WEEK(visit_date) AS Week,
        COUNT(DISTINCT(customer_id)) AS Num_Customers
    FROM 
        `theme-park-db`.visits
    GROUP BY 
        MONTH(visit_date), 
        WEEK(visit_date)
    ORDER BY 
        Month ASC;
    """)

def downgrade():
    op.execute("DROP VIEW IF EXISTS monthly_weekly_customer_counts;")