"""initial_production_schema

Revision ID: 87dcf646c5e0
Revises: 
Create Date: 2026-09-21 09:44:18.389827

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87dcf646c5e0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. Workspaces table
    op.create_table(
        'workspaces',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('owner_id', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('is_synthetic', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workspaces_owner_id'), 'workspaces', ['owner_id'], unique=False)

    # 3. Workspace members table
    op.create_table(
        'workspace_members',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('joined_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workspace_members_user_id'), 'workspace_members', ['user_id'], unique=False)
    op.create_index(op.f('ix_workspace_members_workspace_id'), 'workspace_members', ['workspace_id'], unique=False)

    # 4. Orders table (Composite PK: workspace_id, id)
    op.create_table(
        'orders',
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('store_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('total_amount_minor', sa.Integer(), nullable=True),
        sa.Column('payment_method', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('customer_id', sa.String(), nullable=True),
        sa.Column('is_synthetic', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('workspace_id', 'id')
    )

    # 5. Payments table (Composite PK: workspace_id, id)
    op.create_table(
        'payments',
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=True),
        sa.Column('captured_at', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('amount_minor', sa.Integer(), nullable=True),
        sa.Column('method', sa.String(), nullable=True),
        sa.Column('gateway', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('workspace_id', 'id')
    )
    op.create_index(op.f('ix_payments_order_id'), 'payments', ['order_id'], unique=False)

    # 6. Courier settlements table (Composite PK: workspace_id, id)
    op.create_table(
        'courier_settlements',
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=True),
        sa.Column('courier_name', sa.String(), nullable=True),
        sa.Column('delivered_at', sa.String(), nullable=True),
        sa.Column('collected_amount_minor', sa.Integer(), nullable=True),
        sa.Column('settled_amount_minor', sa.Integer(), nullable=True),
        sa.Column('collection_currency', sa.String(), nullable=True),
        sa.Column('settlement_status', sa.String(), nullable=True),
        sa.Column('grace_days', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('workspace_id', 'id')
    )
    op.create_index(op.f('ix_courier_settlements_order_id'), 'courier_settlements', ['order_id'], unique=False)

    # 7. Refunds table (Composite PK: workspace_id, id)
    op.create_table(
        'refunds',
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=True),
        sa.Column('refunded_at', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('amount_minor', sa.Integer(), nullable=True),
        sa.Column('reason', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('workspace_id', 'id')
    )
    op.create_index(op.f('ix_refunds_order_id'), 'refunds', ['order_id'], unique=False)

    # 8. Purchase signals table (Composite PK: workspace_id, id)
    op.create_table(
        'purchase_signals',
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=True),
        sa.Column('signal_type', sa.String(), nullable=True),
        sa.Column('platform', sa.String(), nullable=True),
        sa.Column('event_name', sa.String(), nullable=True),
        sa.Column('event_id', sa.String(), nullable=True),
        sa.Column('reported_at', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('value_minor', sa.Integer(), nullable=True),
        sa.Column('consent_granted', sa.Boolean(), nullable=True),
        sa.Column('pixel_id', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('workspace_id', 'id')
    )
    op.create_index(op.f('ix_purchase_signals_order_id'), 'purchase_signals', ['order_id'], unique=False)

    # 9. Data sources table (Composite PK: workspace_id, id)
    op.create_table(
        'data_sources',
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('source_type', sa.String(), nullable=True),
        sa.Column('date_range_start', sa.String(), nullable=True),
        sa.Column('date_range_end', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('coverage_status', sa.String(), nullable=True),
        sa.Column('completeness_status', sa.String(), nullable=True),
        sa.Column('last_processed', sa.String(), nullable=True),
        sa.Column('record_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('workspace_id', 'id')
    )

    # 10. Findings table
    op.create_table(
        'findings',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workspace_id', sa.String(), nullable=True),
        sa.Column('rule_id', sa.String(), nullable=True),
        sa.Column('rule_name', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('order_id', sa.String(), nullable=True),
        sa.Column('observed', sa.String(), nullable=True),
        sa.Column('source_records', sa.JSON(), nullable=True),
        sa.Column('assumptions', sa.JSON(), nullable=True),
        sa.Column('not_proven', sa.JSON(), nullable=True),
        sa.Column('next_step', sa.String(), nullable=True),
        sa.Column('owner', sa.String(), nullable=True),
        sa.Column('amount_minor', sa.Integer(), nullable=True),
        sa.Column('amount_currency', sa.String(), nullable=True),
        sa.Column('confidence', sa.String(), nullable=True),
        sa.Column('explanation', sa.String(), nullable=True),
        sa.Column('recommended_action', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('is_healthy_control', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_findings_workspace_id'), 'findings', ['workspace_id'], unique=False)

    # 11. Upload metadata table
    op.create_table(
        'upload_metadata',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('source_type', sa.String(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=True),
        sa.Column('row_count', sa.Integer(), nullable=True),
        sa.Column('mapped_columns', sa.JSON(), nullable=True),
        sa.Column('warnings', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_upload_metadata_workspace_id'), 'upload_metadata', ['workspace_id'], unique=False)

    # 12. Audit runs table
    op.create_table(
        'audit_runs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('evaluated_orders', sa.Integer(), nullable=True),
        sa.Column('total_findings', sa.Integer(), nullable=True),
        sa.Column('healthy_controls_count', sa.Integer(), nullable=True),
        sa.Column('summary', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('completed_at', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_runs_workspace_id'), 'audit_runs', ['workspace_id'], unique=False)

    # 13. Audit logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workspace_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('timestamp', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_workspace_id'), 'audit_logs', ['workspace_id'], unique=False)


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('audit_runs')
    op.drop_table('upload_metadata')
    op.drop_table('findings')
    op.drop_table('data_sources')
    op.drop_table('purchase_signals')
    op.drop_table('refunds')
    op.drop_table('courier_settlements')
    op.drop_table('payments')
    op.drop_table('orders')
    op.drop_table('workspace_members')
    op.drop_table('workspaces')
    op.drop_table('users')
