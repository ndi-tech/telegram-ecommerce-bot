#!/usr/bin/env python3
"""
Database Fix Script
This script fixes the bot.db database by:
1. Clearing the old products table
2. Inserting products with the correct IDs (478, 496, etc.)
3. Clearing the corrupted cart table
"""

import sqlite3
import sys

# The correct product data with proper IDs
REAL_PRODUCTS = [
    {
        'id': 496, 'name': '🍈 Melonade Strain', 'price': '400',
        'desc': 'The "Melonade" strain is a cannabis hybrid known for its distinctive flavor profile.',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg33.jpg'
    },
    {
        'id': 494, 'name': '🍩 Donut Shop - Hybrid', 'price': '40',
        'desc': 'Hybrid disposable made with THCA diamond infused distillate live resin.',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg32.jpg'
    },
    {
        'id': 492, 'name': '🧙‍♂️ Wizard trees - Sativa', 'price': '40',
        'desc': 'Rechargeable disposable vape with 1000mg. Wizard trees Flavor',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg31.jpg'
    },
    {
        'id': 490, 'name': '🍯 Biskante - Hybrid', 'price': '40',
        'desc': 'Rechargeable disposable vape with 1000mg. Biskante Flavor',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg30.jpg'
    },
    {
        'id': 488, 'name': '🌺 Hawaiian Znowcone - Hybrid', 'price': '40',
        'desc': 'Rechargeable disposable vape with 1000mg. Hawaiian Znowcone Flavor',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg29.jpg'
    },
    {
        'id': 486, 'name': '🎤 Snoop Dogg OG - Indica', 'price': '40',
        'desc': 'Rechargeable disposable vape with 1000mg. Snoop Dogg OG Flavor',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg28.jpg'
    },
    {
        'id': 484, 'name': '🍉 Watermelon Gelato - Indica', 'price': '40',
        'desc': 'Rechargeable disposable vape with 1000mg. Watermelon Gelato Flavor',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg27.jpg'
    },
    {
        'id': 482, 'name': '🎂 Wedding Cheesecake - Indica', 'price': '40',
        'desc': 'Rechargeable disposable vape with 1000mg. Wedding Cheesecake Flavor',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg26.jpg'
    },
    {
        'id': 480, 'name': '🍫 Mint Chocolate Chip - Sativa', 'price': '40',
        'desc': 'Rechargeable disposable vape with 1000mg. Mint Chocolate Chip Flavor',
        'category': '1G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg25.jpg'
    },
    {
        'id': 478, 'name': '🍏 Glazed Apple Sour - Sativa', 'price': '45',
        'desc': 'Rechargeable disposable vape with 2000mg. Glazed Apple Sour Flavor',
        'category': '2G 1010boys', 'image': 'https://official1010boys.com/wp-content/uploads/2025/07/mg24.jpg'
    }
]

def fix_database(db_path):
    """Fix the database by resetting products and cart"""
    
    print("=" * 70)
    print("DATABASE FIX SCRIPT")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Show current state
        print("\n📊 CURRENT STATE:")
        c.execute("SELECT COUNT(*) FROM products")
        prod_count = c.fetchone()[0]
        print(f"  Products: {prod_count}")
        
        c.execute("SELECT COUNT(*) FROM cart")
        cart_count = c.fetchone()[0]
        print(f"  Cart items: {cart_count}")
        
        # Step 1: Clear products table
        print("\n🗑️  Step 1: Clearing old products...")
        c.execute("DELETE FROM products")
        print("  ✅ Products cleared")
        
        # Step 2: Insert correct products
        print("\n📦 Step 2: Inserting correct products...")
        for product in REAL_PRODUCTS:
            c.execute('''INSERT INTO products 
                         (id, name, price, description, category, image_url) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                     (product['id'], product['name'], product['price'], 
                      product['desc'], product['category'], product['image']))
            print(f"  ✅ Added: {product['name']} (ID: {product['id']})")
        
        # Step 3: Clear cart (it has wrong data anyway)
        print("\n🛒 Step 3: Clearing corrupted cart...")
        c.execute("DELETE FROM cart")
        print("  ✅ Cart cleared")
        
        # Commit changes
        conn.commit()
        
        # Verify
        print("\n✅ VERIFICATION:")
        c.execute("SELECT COUNT(*) FROM products")
        prod_count = c.fetchone()[0]
        print(f"  Products: {prod_count}")
        
        c.execute("SELECT id, name FROM products ORDER BY id DESC LIMIT 3")
        products = c.fetchall()
        print("\n  Sample products:")
        for prod in products:
            print(f"    ID: {prod[0]}, Name: {prod[1]}")
        
        c.execute("SELECT COUNT(*) FROM cart")
        cart_count = c.fetchone()[0]
        print(f"\n  Cart items: {cart_count}")
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ DATABASE FIXED SUCCESSFULLY!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Replace your bot.db with this fixed version")
        print("2. Restart your bot")
        print("3. Try adding products to cart")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = "bot.db"
    
    print(f"\nFixing database: {db_path}\n")
    fix_database(db_path)
