"""create_plans_table

Revision ID: 7aa9ef86959c
Revises: 473cd5268579
Create Date: 2024-11-20 20:45:52.666705

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7aa9ef86959c'
down_revision: Union[str, None] = '473cd5268579'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('plans',
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('plan_name', sa.Text()),
        sa.Column('plan_code', sa.Text()),
        sa.Column('plan_type', sa.Text()),
        sa.Column('sub_type', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('network_name', sa.Text()),
        sa.Column('network_region', sa.Text()),
        sa.Column('network_type', sa.Text()),
        sa.Column('deductible_individual', sa.Numeric(10, 2)),
        sa.Column('deductible_family', sa.Numeric(10, 2)),
        sa.Column('oop_max_individual', sa.Numeric(10, 2)),
        sa.Column('oop_max_family', sa.Numeric(10, 2)),
        sa.Column('premium_base_rate', sa.Numeric(10, 2)),
        sa.Column('prior_auth_requirements', sa.Text()),
        sa.Column('copay_structure', sa.Text()),
        sa.Column('covered_services_summary', sa.Text()),
        sa.Column('exclusions', sa.Text()),
        sa.Column('dental_coverage', sa.Text()),
        sa.Column('vision_coverage', sa.Text()),
        sa.Column('hearing_coverage', sa.Text()),
        sa.Column('fitness_benefits', sa.Text()),
        sa.Column('telehealth_coverage', sa.Text()),
        sa.Column('dental_vendor', sa.Text()),
        sa.Column('vision_vendor', sa.Text()),
        sa.Column('hearing_vendor', sa.Text()),
        sa.Column('fitness_vendor', sa.Text()),
        sa.Column('effective_date', sa.Date(), nullable=False),
        sa.Column('termination_date', sa.Date()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.Column('created_by', sa.Text(), nullable=False),
        sa.Column('last_modified_by', sa.Text()),
        sa.Column('external_network_vendors', sa.Text()),
        sa.PrimaryKeyConstraint('plan_id')
    )

def downgrade() -> None:
    op.drop_table('plans')