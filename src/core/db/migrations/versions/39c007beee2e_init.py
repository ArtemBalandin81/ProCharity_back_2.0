"""Init

Revision ID: 39c007beee2e
Create Date: 2021-11-30 17:50:15.603734

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "39c007beee2e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "admin_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=48), nullable=False),
        sa.Column("first_name", sa.String(length=32), nullable=True),
        sa.Column("last_name", sa.String(length=32), nullable=True),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.Column("last_logon", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("archive", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("message", sa.String(length=4096), nullable=False),
        sa.Column("was_sent", sa.Boolean(), nullable=True),
        sa.Column("sent_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("sent_by", sa.String(length=48), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "admin_token_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=48), nullable=False),
        sa.Column("token", sa.String(length=128), nullable=False),
        sa.Column("token_expiration_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="registers_email_key"),
    )
    op.create_table(
        "statistics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=True),
        sa.Column("command", sa.String(length=100), nullable=True),
        sa.Column("added_date", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=True),
        sa.Column("email", sa.String(length=48), nullable=True),
        sa.Column("external_id", sa.Integer(), nullable=True),
        sa.Column("first_name", sa.String(length=32), nullable=True),
        sa.Column("last_name", sa.String(length=32), nullable=True),
        sa.Column("has_mailing", sa.Boolean(), nullable=True),
        sa.Column("date_registration", sa.TIMESTAMP(), nullable=True),
        sa.Column("banned", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("external_signup_date", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("telegram_id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("external_id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "users_categories",
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["telegram_id"],
            ["users.telegram_id"],
        ),
        sa.PrimaryKeyConstraint("telegram_id", "category_id"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("name_organization", sa.String(), nullable=True),
        sa.Column("deadline", sa.Date(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("bonus", sa.Integer(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("link", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("archive", sa.Boolean(), nullable=True),
        sa.Column("created_date", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_date", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "reasons_canceling",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=True),
        sa.Column("reason_canceling", sa.String(length=48), nullable=False),
        sa.Column("added_date", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_date", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("archive", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "external_site_users",
        sa.Column("external_id", sa.Integer(), nullable=False),
        sa.Column("external_id_hash", sa.String(length=256), nullable=False),
        sa.Column("email", sa.String(length=48), nullable=False),
        sa.Column("first_name", sa.String(length=32), nullable=True),
        sa.Column("last_name", sa.String(length=32), nullable=True),
        sa.Column("specializations", sa.String(), nullable=True),
        sa.Column("created_date", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_date", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("source", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("external_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("external_site_users")
    op.drop_table("reasons_canceling")
    op.drop_table("tasks")
    op.drop_table("users_categories")
    op.drop_table("users")
    op.drop_table("statistics")
    op.drop_table("admin_token_requests")
    op.drop_table("notifications")
    op.drop_table("categories")
    op.drop_table("admin_users")
    # ### end Alembic commands ###
