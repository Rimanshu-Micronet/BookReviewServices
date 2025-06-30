"""Initial migration - Create books and reviews tables

Revision ID: 001
Revises: 
Create Date: 2024-12-19 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create books table
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=False),
        sa.Column('published_date', sa.DateTime(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('isbn', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('isbn')
    )
    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=False)
    op.create_index(op.f('ix_books_title'), 'books', ['title'], unique=False)
    
    # Create reviews table
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('reviewer_name', sa.String(length=100), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reviews_book_id'), 'reviews', ['book_id'], unique=False)
    op.create_index(op.f('ix_reviews_id'), 'reviews', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_reviews_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_book_id'), table_name='reviews')
    op.drop_table('reviews')
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.drop_table('books')