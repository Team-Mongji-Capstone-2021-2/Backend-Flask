"""empty message

Revision ID: 05efe27db97b
Revises: 
Create Date: 2021-10-22 18:25:38.848151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05efe27db97b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_tests',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=32), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=8), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('tests',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=32), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=8), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('datas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('local', sa.String(length=32), nullable=False),
    sa.Column('DataTime', sa.String(length=32), nullable=False),
    sa.Column('stressData', sa.Boolean(), nullable=True),
    sa.Column('arrhythmia', sa.Boolean(), nullable=True),
    sa.Column('image', sa.String(length=32), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_datas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('local', sa.String(length=32), nullable=False),
    sa.Column('DataTime', sa.String(length=32), nullable=False),
    sa.Column('stressData', sa.Boolean(), nullable=True),
    sa.Column('arrhythmia', sa.Boolean(), nullable=True),
    sa.Column('image', sa.String(length=32), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['test_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_datas')
    op.drop_table('datas')
    op.drop_table('users')
    op.drop_table('tests')
    op.drop_table('test_users')
    op.drop_table('test_tests')
    # ### end Alembic commands ###
