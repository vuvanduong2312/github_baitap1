#!/usr/bin/env python3
"""
Migration script - Add addresses table
"""
from app import create_app, db
from app.models import User, Address

def migrate_addresses():
    app = create_app()
    
    with app.app_context():
        print("="*60)
        print("DATABASE MIGRATION - Add Addresses")
        print("="*60)
        
        # Create addresses table
        db.create_all()
        print("\n✓ Created 'addresses' table")
        
        # Check if any users exist
        user_count = User.query.count()
        print(f"✓ Found {user_count} users in database")
        
        print("\n" + "="*60)
        print("Migration completed successfully!")
        print("="*60)
        
        print("\nNew features:")
        print("- Users can add multiple addresses")
        print("- Each address has label, recipient, phone, address")
        print("- One address can be set as default")
        print("- Admin can view customer addresses")
        print("- Admin can click customer name to view details")

if __name__ == '__main__':
    migrate_addresses()
