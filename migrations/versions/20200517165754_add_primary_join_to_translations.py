"""add primary join to translations

Revision ID: 678202012ff2
Revises: eee8dd22498b
Create Date: 2020-05-17 16:57:54.607091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '678202012ff2'
down_revision = 'eee8dd22498b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('translations', sa.Column('dictionary_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'translations', 'dictionaries', ['dictionary_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'translations', type_='foreignkey')
    op.drop_column('translations', 'dictionary_id')
    # ### end Alembic commands ###
