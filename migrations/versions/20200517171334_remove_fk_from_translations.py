"""remove fk from translations

Revision ID: b0e72eb8422c
Revises: 678202012ff2
Create Date: 2020-05-17 17:13:34.655053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0e72eb8422c'
down_revision = '678202012ff2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('translations_word_id_fkey', 'translations', type_='foreignkey')
    op.drop_constraint('translations_dictionary_id_fkey', 'translations', type_='foreignkey')
    op.drop_constraint('translations_user_id_fkey', 'translations', type_='foreignkey')
    op.drop_column('translations', 'user_id')
    op.drop_column('translations', 'dictionary_id')
    op.drop_column('translations', 'word_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('translations', sa.Column('word_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('translations', sa.Column('dictionary_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('translations', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('translations_user_id_fkey', 'translations', 'users', ['user_id'], ['id'])
    op.create_foreign_key('translations_dictionary_id_fkey', 'translations', 'dictionaries', ['dictionary_id'], ['id'])
    op.create_foreign_key('translations_word_id_fkey', 'translations', 'words', ['word_id'], ['id'])
    # ### end Alembic commands ###
