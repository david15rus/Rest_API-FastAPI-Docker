"""create tables

Revision ID: 521846c7818d
Revises: 
Create Date: 2023-07-29 17:41:34.083706

"""
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '521846c7818d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'menus',
        sa.Column('id', sa.UUID, primary_key=True, index=True,
                  default=uuid.uuid4),
        sa.Column('title', sa.String, nullable=False, unique=True),
        sa.Column('description', sa.String, nullable=True),
    )

    op.create_table(
        'submenus',
        sa.Column('id', sa.UUID, primary_key=True, index=True,
                  default=uuid.uuid4),
        sa.Column('title', sa.String, nullable=False, unique=True),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('menu_id', sa.UUID, sa.ForeignKey('menus.id'),
                  nullable=False),
    )

    op.create_table(
        'dishes',
        sa.Column('id', sa.UUID, primary_key=True, index=True,
                  default=uuid.uuid4),
        sa.Column('title', sa.String, nullable=False, unique=True),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('submenu_id', sa.UUID,
                  sa.ForeignKey('submenus.id'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('dishes')
    op.drop_table('submenus')
    op.drop_table('menus')
