"""Fix id field

Revision ID: 6edde13ef857
Revises: f4fa92f587b5
Create Date: 2022-09-18 22:09:27.189142

"""
from alembic import op
import sqlalchemy as sa
from fastapi_authz import boot  # noqa



# revision identifiers, used by Alembic.
revision = '6edde13ef857'
down_revision = 'f4fa92f587b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
