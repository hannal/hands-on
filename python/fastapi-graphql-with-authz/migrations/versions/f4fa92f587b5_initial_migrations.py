"""Initial migrations

Revision ID: f4fa92f587b5
Revises: 
Create Date: 2022-09-18 20:23:29.222674

"""
from alembic import op
import sqlalchemy as sa
from fastapi_authz import boot  # noqa



# revision identifiers, used by Alembic.
revision = 'f4fa92f587b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userroles',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Unicode(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name', name='uq_user_roles_name')
    )
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.Unicode(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username', name='uq_user_username')
    )
    op.create_table('user_userrole_association',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('userrole_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['userrole_id'], ['userroles.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_userrole_association')
    op.drop_table('users')
    op.drop_table('userroles')
    # ### end Alembic commands ###