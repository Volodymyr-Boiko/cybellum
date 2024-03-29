"""empty message

Revision ID: 8a15a2940459
Revises: 
Create Date: 2023-10-05 14:18:21.965951

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8a15a2940459"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "post",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "comment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["post.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("comment")
    op.drop_table("post")
    op.drop_table("user")
    # ### end Alembic commands ###
