"""adds user words table

Revision ID: d1dc0b75eec4
Revises: 1dcce64c7d32
Create Date: 2020-04-16 23:24:27.809609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1dc0b75eec4'
down_revision = '1dcce64c7d32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_words',
    sa.Column('word_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('dictionary_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['dictionary_id'], ['dictionaries.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], )
    )

    op.create_index(op.f('ix_user_words_date_created'), 'user_words', ['date_created'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_words_date_created'), table_name='user_words')
    op.drop_table('user_words')
    # ### end Alembic commands ###
