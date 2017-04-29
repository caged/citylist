"""add name to channels

Revision ID: 3aa348d922c2
Revises: 81985906a09a
Create Date: 2017-04-28 18:01:28.340706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa348d922c2'
down_revision = '81985906a09a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('channels', sa.Column('name', sa.UnicodeText))


def downgrade():
    op.drop_column('channels', 'name')
