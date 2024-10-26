"""removed dept roles table.

Revision ID: 3e630a568ad6
Revises: a04bd5f20de5
Create Date: 2024-10-26 13:43:45.689458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3e630a568ad6'
down_revision: Union[str, None] = 'a04bd5f20de5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_department_role_id', table_name='deparmentroles')
    op.drop_table('deparmentroles')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deparmentroles',
    sa.Column('department_role_id', mysql.INTEGER(), autoincrement=True, nullable=False, comment='Unique ID for each department role'),
    sa.Column('department_id', mysql.INTEGER(), autoincrement=False, nullable=False, comment='Department ID this role belongs to'),
    sa.Column('role_description', mysql.VARCHAR(length=200), nullable=False, comment='Description of the department role'),
    sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], name='deparmentroles_ibfk_1'),
    sa.PrimaryKeyConstraint('department_role_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('idx_department_role_id', 'deparmentroles', ['department_role_id'], unique=False)
    # ### end Alembic commands ###
