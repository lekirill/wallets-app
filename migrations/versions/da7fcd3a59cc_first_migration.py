"""first migration

Revision ID: da7fcd3a59cc
Revises: 
Create Date: 2023-09-12 22:23:14.824811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da7fcd3a59cc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wallet',
    sa.Column('label', sa.String(length=255), nullable=False),
    sa.Column('balance', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wallet_id'), 'wallet', ['id'], unique=False)
    op.create_table('transaction',
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.Column('txid', sa.String(length=36), nullable=True),
    sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_id'), 'transaction', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_id'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_index(op.f('ix_wallet_id'), table_name='wallet')
    op.drop_table('wallet')
    # ### end Alembic commands ###
