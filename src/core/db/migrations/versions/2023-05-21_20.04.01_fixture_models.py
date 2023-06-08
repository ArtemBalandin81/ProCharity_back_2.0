"""fixture models

Revision ID: edf9d4b6cdea
Revises: bb02384217e4
Create Date: 2023-05-21 20:04:01.734393

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "edf9d4b6cdea"
down_revision = "bb02384217e4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("categories", "archive", nullable=False, new_column_name="is_archived")
    op.add_column("tasks", sa.Column("title", sa.String(), nullable=False))
    op.add_column("tasks", sa.Column("name_organization", sa.String(), nullable=True))
    op.add_column("tasks", sa.Column("deadline", sa.Date(), nullable=True))
    op.add_column("tasks", sa.Column("description", sa.String(), nullable=False))
    op.alter_column("tasks", "archive", nullable=False, new_column_name="is_archived")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("tasks", "is_archived", nullable=False, new_column_name="archive")
    op.drop_column("tasks", "description")
    op.drop_column("tasks", "deadline")
    op.drop_column("tasks", "name_organization")
    op.drop_column("tasks", "title")
    op.alter_column("categories", "is_archived", nullable=False, new_column_name="archive")
    # ### end Alembic commands ###
