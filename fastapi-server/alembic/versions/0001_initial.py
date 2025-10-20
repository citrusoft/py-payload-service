"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2025-10-20 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'payloads',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('origin', sa.String(length=3), nullable=True),
        sa.Column('destination', sa.String(length=3), nullable=True),
        sa.Column('julian_do_y', sa.Integer(), nullable=True),
        sa.Column('passengers', sa.Integer(), nullable=True),
        sa.Column('baggage', sa.Float(), nullable=True),
        sa.Column('cargo', sa.Float(), nullable=True),
    )


def downgrade():
    op.drop_table('payloads')
