"""add case to channel

Revision ID: 47fd38ab7a01
Revises: 3aa348d922c2
Create Date: 2017-04-28 20:52:50.634846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47fd38ab7a01'
down_revision = '3aa348d922c2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('channels', sa.Column('case', sa.UnicodeText))


def downgrade():
    op.drop_column('channels', 'case')
