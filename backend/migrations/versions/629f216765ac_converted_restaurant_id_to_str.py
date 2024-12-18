"""converted restaurant id to str.

Revision ID: 629f216765ac
Revises: 0ab59e18949a
Create Date: 2024-10-24 20:09:05.002802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '629f216765ac'
down_revision: Union[str, None] = '0ab59e18949a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('guestservices_ibfk_2', 'guestservices', type_='foreignkey')
    op.drop_constraint('restaurants_ibfk_1', 'restaurants', type_='foreignkey')
    op.create_foreign_key('guestservices_ibfk_2', 'guestservices', 'employees', ['employee_id'], ['employee_id'])
    op.alter_column('restaurants', 'restaurant_id',
               existing_type=mysql.INTEGER(),
               type_=mysql.VARCHAR(length=12),
               existing_comment='Unique restaurant ID',
               existing_nullable=False)
    op.create_foreign_key('restaurants_ibfk_1', 'restaurants', 'sections', ['park_section_id'], ['section_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('restaurants', 'restaurant_id',
               existing_type=mysql.VARCHAR(length=12),
               type_=mysql.INTEGER(),
               existing_comment='Unique restaurant ID',
               existing_nullable=False)
    op.drop_constraint(None, 'guestservices', type_='foreignkey')
    op.create_foreign_key('guestservices_ibfk_2', 'guestservices', 'employees', ['employee_id'], ['employee_id'], ondelete='SET NULL')
    # ### end Alembic commands ###
