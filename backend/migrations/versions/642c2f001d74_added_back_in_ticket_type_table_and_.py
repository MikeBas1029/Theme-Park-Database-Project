"""added back in ticket type table and relationship.

Revision ID: 642c2f001d74
Revises: 9670082e60e3
Create Date: 2024-11-12 07:11:48.194384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '642c2f001d74'
down_revision: Union[str, None] = '9670082e60e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('ticket_type')

    # Create the new ticket_type table with auto-incrementing primary key
    op.create_table(
        'ticket_type',
        sa.Column('ticket_type_id', sa.Integer, primary_key=True, autoincrement=True, nullable=False, comment="Auto-incrementing ID for ticket types"),
        sa.Column('ticket_type', mysql.VARCHAR(20), unique=True, nullable=False, comment="Type of the ticket (e.g., 'SEASONAL', 'VIP')"),
        sa.Column('description', mysql.VARCHAR(255), nullable=True, comment='Description of the ticket type with details of its features'),
        sa.Column('base_price', mysql.DECIMAL(precision=10, scale=2), nullable=False, comment='The base price of this ticket type')
    )

    # Insert initial data into the ticket_type table
    op.execute("""
        INSERT INTO ticket_type (ticket_type_id, ticket_type, description, base_price)
        VALUES
            (1, 'SEASONAL', 'Seasonal pass with extended validity', 50.00),
            (2, 'WEEKEND', 'Weekend pass valid for Saturdays and Sundays', 35.00),
            (3, 'DAY_PASS', 'Single day pass for unlimited rides', 20.00),
            (4, 'VIP', 'VIP pass with priority access and additional perks', 100.00),
            (5, 'GROUP', 'Group pass with discounts for groups of 4 or more', 70.00),
            (6, 'STUDENT', 'Discounted day pass for students', 15.00);
    """)

    # Remove old ticket_type column from tickets
    # op.drop_column('tickets', 'ticket_type')

    # Add ticket_type_id column to tickets table with foreign key to ticket_type.ticket_type_id
    # op.add_column(
    #     'tickets',
    #     sa.Column('ticket_type_id', sa.Integer, sa.ForeignKey('ticket_type.ticket_type_id'), nullable=False, comment="Foreign key linking to ticket_type table")
    # )

    # Create foreign key constraint
    op.create_foreign_key(
        'fk_tickets_2',
        'tickets', 'ticket_type',
        ['ticket_type_id'], ['ticket_type_id']
    )


def downgrade() -> None:
    # Drop the foreign key constraint between tickets and ticket_type
    op.drop_constraint('fk_tickets_2', 'tickets', type_='foreignkey')

    # Remove the ticket_type_id column from tickets
    op.drop_column('tickets', 'ticket_type_id')

    # Add back the old ticket_type column as an ENUM
    op.add_column(
        'tickets',
        sa.Column('ticket_type', sa.Enum('SEASONAL', 'WEEKEND', 'DAY_PASS', 'VIP', 'GROUP', 'STUDENT', name='tickettype'), nullable=False, comment="The type of the ticket (e.g., 'VIP', 'DAY_PASS')")
    )

    # Drop the ticket_type table
    op.drop_table('ticket_type')