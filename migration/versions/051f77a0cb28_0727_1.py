"""0727_1

Revision ID: 051f77a0cb28
Revises: 
Create Date: 2020-07-27 15:53:15.066036

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '051f77a0cb28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('phone', mysql.CHAR(length=15), nullable=True),
    sa.Column('password', mysql.TEXT(), nullable=True),
    sa.Column('nick_name', mysql.CHAR(length=50), nullable=True),
    sa.Column('picture', mysql.TEXT(), nullable=True),
    sa.Column('registered_at', mysql.DATETIME(), nullable=True),
    sa.Column('religion', mysql.TEXT(), nullable=True),
    sa.Column('smoke', sa.BOOLEAN(), nullable=True),
    sa.Column('job', mysql.TEXT(), nullable=True),
    sa.Column('school', mysql.TEXT(), nullable=True),
    sa.Column('major', mysql.TEXT(), nullable=True),
    sa.Column('company', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nick_name'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('user_sessions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', mysql.TEXT(), nullable=True),
    sa.Column('third_party_token', mysql.TEXT(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('expiry', mysql.DATETIME(), nullable=False),
    sa.Column('activated', sa.Integer(), server_default='1', nullable=True),
    sa.Column('admin', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_sessions')
    op.drop_table('users')
    # ### end Alembic commands ###
