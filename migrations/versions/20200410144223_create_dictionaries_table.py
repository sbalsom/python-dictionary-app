"""create dictionaries table

Revision ID: 28829b02f963
Revises: ecefebb0e35f
Create Date: 2020-04-10 14:42:23.816498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28829b02f963'
down_revision = 'ecefebb0e35f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dictionary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dictionary')
    # ### end Alembic commands ###