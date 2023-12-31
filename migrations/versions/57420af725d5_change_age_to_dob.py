"""change age to dob

Revision ID: 57420af725d5
Revises: 
Create Date: 2023-07-05 17:46:53.900561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57420af725d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dob', sa.Integer(), nullable=True))
        batch_op.drop_column('age')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.INTEGER(), nullable=True))
        batch_op.drop_column('dob')

    # ### end Alembic commands ###
