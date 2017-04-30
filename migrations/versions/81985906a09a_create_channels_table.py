"""create channels table

Revision ID: 81985906a09a
Revises:
Create Date: 2017-04-28 17:52:24.314156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81985906a09a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'channels',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('slug', sa.Text, nullable=False),
        sa.Column('name', sa.Text),
        sa.Column('case', sa.Text),
        sa.Column('posted_at', sa.DateTime),
        sa.Column('imported_at', sa.DateTime),
        sa.Column('neighborhood', sa.Text),
        sa.Column('address', sa.Text),
        sa.Column('lat', sa.REAL),
        sa.Column('lon', sa.REAL),
        sa.Column('description', sa.Text),
        sa.Column('raw_text', sa.Text)
    )


def downgrade():
    op.drop_table('channels')
