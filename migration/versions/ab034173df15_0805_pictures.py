"""0805_pictures

Revision ID: ab034173df15
Revises: 69ac4343dd8f
Create Date: 2020-08-05 12:28:14.187779

"""
from alembic import op
import sqlalchemy as sa
from libs.database.types import TwolipTypes
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ab034173df15'
down_revision = '69ac4343dd8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pictures', TwolipTypes.TextTuple(), nullable=True))
    op.drop_column('users', 'picture')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('picture', mysql.TEXT(), nullable=True))
    op.drop_column('users', 'pictures')
    # ### end Alembic commands ###