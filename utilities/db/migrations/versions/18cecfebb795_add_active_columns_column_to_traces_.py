"""add active_columns column to traces table

Revision ID: 18cecfebb795
Revises: c00792d2243c
Create Date: 2023-01-02 11:00:34.110027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18cecfebb795'
down_revision = 'c00792d2243c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('traces', sa.Column('active_columns', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('traces', 'active_columns')
    # ### end Alembic commands ###
