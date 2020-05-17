"""adds translations to words

Revision ID: 35ae5ae49c42
Revises: 1f90679c932d
Create Date: 2020-05-17 16:39:47.216140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35ae5ae49c42'
down_revision = '1f90679c932d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('translations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sentences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('translation_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['translation_id'], ['translations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user_words', sa.Column('description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_words', 'description')
    op.drop_table('sentences')
    op.drop_table('translations')
    # ### end Alembic commands ###