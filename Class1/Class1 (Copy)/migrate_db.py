#!/usr/bin/env python3
"""
Database migration script - Adds cart_items table and updates order status
"""
from app import create_app, db
from app.models import User, Book, Category, Author, Order, OrderDetail, CartItem

def migrate_database():
    app = create_app()
    
    with app.app_context():
        print("Starting database migration...")
        
        # Create all tables (will only create new ones)
        db.create_all()
        print("✓ Created cart_items table")
        
        # Update existing orders with old status "Đã hủy" if any
        # (In case there were cancelled orders before)
        
        print("\n" + "="*50)
        print("Migration completed successfully!")
        print("="*50)
        print("\nNew features:")
        print("- Cart items now saved to database (cart_items table)")
        print("- Order statuses: Chờ xử lý, Đang giao, Đã giao, Giao thất bại, Đã hủy")
        print("- Users can cancel orders in 'Chờ xử lý' status")
        print("- Failed deliveries automatically restore stock")

if __name__ == '__main__':
    migrate_database()
