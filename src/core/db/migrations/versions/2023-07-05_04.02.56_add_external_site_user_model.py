"""Add external site user model

Revision ID: 42469a350651
Revises: 84e25a1e5eee
Create Date: 2023-07-05 04:02:56.454988

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "42469a350651"
down_revision = "84e25a1e5eee"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "external_site_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_hash", sa.String(length=256), nullable=False),
        sa.Column("email", sa.String(length=48), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=True),
        sa.Column("specializations", sa.ARRAY(sa.Integer), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("created_at", sa.Date(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column(
            "updated_at",
            sa.Date(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("external_site_users")
    # ### end Alembic commands ###
