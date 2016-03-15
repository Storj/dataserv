"""empty message

Revision ID: d1cb862c6066
Revises: 5fee40ea374b
Create Date: 2016-03-09 20:05:27.931038

"""

# revision identifiers, used by Alembic.
revision = 'd1cb862c6066'
down_revision = '5fee40ea374b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('farmer', sa.Column('ip', sa.String(length=40), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('farmer', 'ip')
    ### end Alembic commands ###