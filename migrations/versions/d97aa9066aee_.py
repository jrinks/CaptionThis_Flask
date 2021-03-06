"""empty message

Revision ID: d97aa9066aee
Revises: d6bc5030da4e
Create Date: 2021-05-29 14:38:04.964459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd97aa9066aee'
down_revision = 'd6bc5030da4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_token', table_name='user')
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.create_index('ix_user_token', 'user', ['token'], unique=False)
    # ### end Alembic commands ###
