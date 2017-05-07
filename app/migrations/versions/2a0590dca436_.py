"""add link column

Revision ID: 2a0590dca436
Revises: 81985906a09a
Create Date: 2017-05-07 15:24:29.747227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a0590dca436'
down_revision = '81985906a09a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('channels', sa.Column('link', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('channels', 'link')
