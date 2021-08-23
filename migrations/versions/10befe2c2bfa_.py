"""empty message

Revision ID: 10befe2c2bfa
Revises: a436e4cc1ace
Create Date: 2021-08-21 00:58:29.634647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10befe2c2bfa'
down_revision = 'a436e4cc1ace'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'state')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('state', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
