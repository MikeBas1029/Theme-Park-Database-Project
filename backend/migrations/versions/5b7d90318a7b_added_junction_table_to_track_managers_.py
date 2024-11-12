"""added junction table to track managers of departments

Revision ID: 5b7d90318a7b
Revises: 963e9c267805
Create Date: 2024-11-10 10:43:12.223490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5b7d90318a7b'
down_revision: Union[str, None] = '963e9c267805'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department_managers',
    sa.Column('department_id', mysql.INTEGER(), nullable=False, comment='ID of the department'),
    sa.Column('employee_id', mysql.VARCHAR(length=8), nullable=False, comment='ID of the employee managing the department'),
    sa.Column('manager_start_date', sa.DATE(), nullable=False, comment='Start date of the department manager'),
    sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('department_id', 'employee_id')
    )
    op.drop_constraint('departments_ibfk_1', 'departments', type_='foreignkey')
    op.drop_column('departments', 'manager_id')
    op.drop_column('departments', 'manager_start_date')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('departments', sa.Column('manager_start_date', sa.DATE(), nullable=False, comment='Start date of the department manager'))
    op.add_column('departments', sa.Column('manager_id', mysql.VARCHAR(length=9), nullable=False, comment='ID of the manager for this department'))
    op.create_foreign_key('departments_ibfk_1', 'departments', 'employees', ['manager_id'], ['employee_id'])
    op.drop_table('department_managers')
    # ### end Alembic commands ###
