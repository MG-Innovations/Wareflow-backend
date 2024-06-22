"""Change id column to UUID in Tenant table

Revision ID: 685ee5b58e42
Revises: 
Create Date: 2024-06-18 20:58:09.184490

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '685ee5b58e42'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Enable the uuid-ossp extension
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    # Add a new UUID column to the Tenant table
    op.add_column('Tenant', sa.Column('new_id', postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()'), nullable=False))

    # Copy the data from old id column to new_id column
    op.execute('UPDATE "Tenant" SET new_id = uuid_generate_v4()')

    # Temporarily drop the foreign key constraint in User table
    op.drop_constraint('User_tenant_id_fkey', 'User', type_='foreignkey')

    # Drop the old primary key constraint
    op.drop_constraint('Tenant_pkey', 'Tenant', type_='primary')

    # Drop the old id column
    op.drop_column('Tenant', 'id')

    # Rename the new_id column to id
    op.alter_column('Tenant', 'new_id', new_column_name='id')

    # Add a new primary key constraint on the id column
    op.create_primary_key('Tenant_pkey', 'Tenant', ['id'])

    # Update related foreign key constraints in User table
    op.alter_column('User', 'tenant_id',
                    existing_type=sa.Integer,
                    type_=postgresql.UUID(as_uuid=True),
                    existing_nullable=False,
                    postgresql_using='tenant_id::uuid')

    # Recreate the foreign key constraint in User table
    op.create_foreign_key('User_tenant_id_fkey', 'User', 'Tenant', ['tenant_id'], ['id'])

    # Recreate indexes if necessary
    op.create_index('ix_Tenant_id', 'Tenant', ['id'], unique=False)

def downgrade() -> None:
    # Temporarily drop the foreign key constraint in User table
    op.drop_constraint('User_tenant_id_fkey', 'User', type_='foreignkey')

    # Add the old id column back as an Integer
    op.add_column('Tenant', sa.Column('old_id', sa.Integer, autoincrement=True, nullable=False))

    # Copy UUID values back to the old id column
    op.execute('UPDATE "Tenant" SET old_id = nextval(\'"Tenant_id_seq"\'::regclass)')

    # Drop the new primary key constraint
    op.drop_constraint('Tenant_pkey', 'Tenant', type_='primary')

    # Drop the new id column
    op.drop_column('Tenant', 'id')

    # Rename the old_id column back to id
    op.alter_column('Tenant', 'old_id', new_column_name='id')

    # Recreate the old primary key constraint on the id column
    op.create_primary_key('Tenant_pkey', 'Tenant', ['id'])

    # Update related foreign key constraints in User table
    op.alter_column('User', 'tenant_id',
                    existing_type=postgresql.UUID(as_uuid=True),
                    type_=sa.Integer,
                    existing_nullable=False,
                    postgresql_using='tenant_id::integer')

    # Recreate the foreign key constraint in User table
    op.create_foreign_key('User_tenant_id_fkey', 'User', 'Tenant', ['tenant_id'], ['id'])

    # Recreate indexes if necessary
    op.create_index('ix_Tenant_id', 'Tenant', ['id'], unique=False)
