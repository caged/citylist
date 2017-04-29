"""add raw text to channels

Revision ID: d8db28da1daf
Revises: 47fd38ab7a01
Create Date: 2017-04-29 14:19:12.421609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8db28da1daf'
down_revision = '47fd38ab7a01'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('channels', sa.Column('raw_text', sa.UnicodeText))


def downgrade():
    op.drop_column('channels', 'raw_text')
