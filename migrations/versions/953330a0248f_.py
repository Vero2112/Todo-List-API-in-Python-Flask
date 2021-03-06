"""empty message

Revision ID: 953330a0248f
Revises: 06ae3912609c
Create Date: 2022-06-24 09:51:53.440101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '953330a0248f'
down_revision = '06ae3912609c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('text', table_name='task')
    op.drop_index('text_2', table_name='task')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('text_2', 'task', ['text'], unique=False)
    op.create_index('text', 'task', ['text'], unique=False)
    # ### end Alembic commands ###
