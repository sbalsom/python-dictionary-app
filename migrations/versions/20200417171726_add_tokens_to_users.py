"""add tokens to users

Revision ID: 04acbaad1af2
Revises: 07c6ba86b4ed
Create Date: 2020-04-17 17:17:26.610217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04acbaad1af2'
down_revision = '07c6ba86b4ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_users_token'), 'users', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_token'), table_name='users')
    op.drop_column('users', 'token_expiration')
    op.drop_column('users', 'token')
    # ### end Alembic commands ###