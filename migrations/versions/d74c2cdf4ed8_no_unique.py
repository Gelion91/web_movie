"""no unique

Revision ID: d74c2cdf4ed8
Revises: 45689cf7c965
Create Date: 2020-11-10 20:13:15.798373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd74c2cdf4ed8'
down_revision = '45689cf7c965'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('serials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('published', sa.DateTime(), nullable=True),
    sa.Column('year', sa.String(), nullable=True),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('name_lower', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('kino_id', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('producer', sa.String(), nullable=True),
    sa.Column('film_page', sa.String(), nullable=True),
    sa.Column('actors', sa.String(), nullable=True),
    sa.Column('writers', sa.String(), nullable=True),
    sa.Column('operator', sa.String(), nullable=True),
    sa.Column('music_author', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('rating', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_serials_actors'), 'serials', ['actors'], unique=False)
    op.create_index(op.f('ix_serials_category'), 'serials', ['category'], unique=False)
    op.create_index(op.f('ix_serials_country'), 'serials', ['country'], unique=False)
    op.create_index(op.f('ix_serials_img'), 'serials', ['img'], unique=False)
    op.create_index(op.f('ix_serials_kino_id'), 'serials', ['kino_id'], unique=True)
    op.create_index(op.f('ix_serials_music_author'), 'serials', ['music_author'], unique=False)
    op.create_index(op.f('ix_serials_name'), 'serials', ['name'], unique=False)
    op.create_index(op.f('ix_serials_name_lower'), 'serials', ['name_lower'], unique=False)
    op.create_index(op.f('ix_serials_operator'), 'serials', ['operator'], unique=False)
    op.create_index(op.f('ix_serials_producer'), 'serials', ['producer'], unique=False)
    op.create_index(op.f('ix_serials_rating'), 'serials', ['rating'], unique=False)
    op.create_index(op.f('ix_serials_tags'), 'serials', ['tags'], unique=False)
    op.create_index(op.f('ix_serials_writers'), 'serials', ['writers'], unique=False)
    op.create_index(op.f('ix_serials_year'), 'serials', ['year'], unique=False)
    op.drop_index('ix_film_img', table_name='film')
    op.create_index(op.f('ix_film_img'), 'film', ['img'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_film_img'), table_name='film')
    op.create_index('ix_film_img', 'film', ['img'], unique=1)
    op.drop_index(op.f('ix_serials_year'), table_name='serials')
    op.drop_index(op.f('ix_serials_writers'), table_name='serials')
    op.drop_index(op.f('ix_serials_tags'), table_name='serials')
    op.drop_index(op.f('ix_serials_rating'), table_name='serials')
    op.drop_index(op.f('ix_serials_producer'), table_name='serials')
    op.drop_index(op.f('ix_serials_operator'), table_name='serials')
    op.drop_index(op.f('ix_serials_name_lower'), table_name='serials')
    op.drop_index(op.f('ix_serials_name'), table_name='serials')
    op.drop_index(op.f('ix_serials_music_author'), table_name='serials')
    op.drop_index(op.f('ix_serials_kino_id'), table_name='serials')
    op.drop_index(op.f('ix_serials_img'), table_name='serials')
    op.drop_index(op.f('ix_serials_country'), table_name='serials')
    op.drop_index(op.f('ix_serials_category'), table_name='serials')
    op.drop_index(op.f('ix_serials_actors'), table_name='serials')
    op.drop_table('serials')
    # ### end Alembic commands ###
