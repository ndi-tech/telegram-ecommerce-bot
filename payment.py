# payment.py - Manual Bitcoin Payment System
import requests
import sqlite3
import time
import qrcode
import io
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ========== CONFIGURATION ==========
# Your Bitcoin wallet address - all payments go here
BITCOIN_ADDRESS = "bc1qmx2ut0mjflv2qxhfv9nqk8rwf7wyg0x2f760ym"

# Blockchain API for price checking (free, no account needed)
BLOCKCHAIN_API_URL = "https://blockchain.info"

# ========== DATABASE FUNCTIONS ==========
def init_payment_db():
    """Initialize payment and orders tables"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        user_id INTEGER,
        username TEXT,
        total_amount REAL,
        btc_amount REAL,
        btc_address TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        paid_at TIMESTAMP,
        items TEXT,
        payment_proof TEXT
    )''')
    
    # Payment tracking
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        btc_address TEXT,
        expected_amount REAL,
        status TEXT DEFAULT 'pending',
        payment_proof TEXT,
        last_checked TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )''')
    
    conn.commit()
    conn.close()
    logger.info("Payment database initialized")

# ========== BITCOIN PRICE FUNCTIONS ==========
def get_btc_price():
    """Get current BTC price in GBP using free API"""
    try:
        # Try blockchain.info first
        response = requests.get(
            "https://blockchain.info/ticker",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return float(data['GBP']['last'])
        
        # Fallback to CoinGecko (also free)
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=gbp",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return float(data['bitcoin']['gbp'])
        
        logger.error(f"Failed to get BTC price")
        return None
    except Exception as e:
        logger.error(f"Error getting BTC price: {e}")
        return None

def check_blockchain_payment(address, expected_amount_btc):
    """Check if payment received on blockchain (optional feature)"""
    try:
        # This is a basic check using blockchain.info API
        response = requests.get(
            f"https://blockchain.info/q/addressbalance/{address}",
            timeout=10
        )
        if response.status_code == 200:
            satoshis = int(response.text)
            btc_received = satoshis / 100000000
            return btc_received >= expected_amount_btc * 0.995  # 0.5% tolerance
        return False
    except Exception as e:
        logger.error(f"Error checking blockchain: {e}")
        return False

# ========== ORDER FUNCTIONS ==========
def create_order(user_id, username, cart_items, total_gbp):
    """Create new order with manual Bitcoin payment"""
    # Generate unique order ID
    order_id = f"ORD-{int(time.time())}-{user_id}"
    
    # Get BTC price
    btc_price = get_btc_price()
    if not btc_price:
        return None, "Unable to get Bitcoin price. Please try again."
    
    # Calculate BTC amount (with small buffer for price fluctuation)
    btc_amount = (total_gbp / btc_price) * 1.01  # 1% buffer
    btc_amount = round(btc_amount, 8)  # Bitcoin has 8 decimal places
    
    # Use your static Bitcoin address
    btc_address = BITCOIN_ADDRESS
    
    # Save order to database
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Convert cart items to string
    items_json = json.dumps(cart_items)
    
    c.execute('''INSERT INTO orders 
                 (order_id, user_id, username, total_amount, btc_amount, btc_address, status, items)
                 VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)''',
              (order_id, user_id, username, total_gbp, btc_amount, btc_address, items_json))
    
    # Create payment tracking entry
    c.execute('''INSERT INTO payments 
                 (order_id, btc_address, expected_amount, status)
                 VALUES (?, ?, ?, 'pending')''',
              (order_id, btc_address, btc_amount))
    
    conn.commit()
    conn.close()
    
    logger.info(f"Order created: {order_id} - £{total_gbp} = {btc_amount} BTC")
    
    return {
        'order_id': order_id,
        'btc_address': btc_address,
        'btc_amount': btc_amount,
        'gbp_amount': total_gbp,
        'btc_price': btc_price
    }, None

def get_order(order_id):
    """Get order details"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute('''SELECT order_id, user_id, total_amount, btc_amount, 
                        btc_address, status, created_at, paid_at, items
                 FROM orders WHERE order_id = ?''', (order_id,))
    
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'order_id': row[0],
            'user_id': row[1],
            'total_amount': row[2],
            'btc_amount': row[3],
            'btc_address': row[4],
            'status': row[5],
            'created_at': row[6],
            'paid_at': row[7],
            'items': row[8]
        }
    return None

def update_order_status(order_id, status, paid_at=None):
    """Update order status"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    if paid_at:
        c.execute('''UPDATE orders 
                     SET status = ?, paid_at = ?
                     WHERE order_id = ?''',
                  (status, paid_at, order_id))
    else:
        c.execute('''UPDATE orders 
                     SET status = ?
                     WHERE order_id = ?''',
                  (status, order_id))
    
    conn.commit()
    conn.close()
    logger.info(f"Order {order_id} status updated to: {status}")

def get_user_orders(user_id, limit=10):
    """Get user's orders"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute('''SELECT order_id, total_amount, btc_amount, status, created_at
                 FROM orders 
                 WHERE user_id = ?
                 ORDER BY created_at DESC
                 LIMIT ?''', (user_id, limit))
    
    orders = c.fetchall()
    conn.close()
    
    return orders

# ========== PAYMENT VERIFICATION ==========
def submit_payment_proof(order_id, proof_text):
    """Customer submits payment proof (txid or description)"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Update order with payment proof
    c.execute('''UPDATE orders 
                 SET payment_proof = ?, status = 'proof_submitted'
                 WHERE order_id = ?''',
              (proof_text, order_id))
    
    # Update payment tracking
    c.execute('''UPDATE payments 
                 SET payment_proof = ?, status = 'proof_submitted'
                 WHERE order_id = ?''',
              (proof_text, order_id))
    
    conn.commit()
    conn.close()
    
    logger.info(f"Payment proof submitted for order {order_id}")
    return True

def confirm_payment_admin(order_id):
    """Admin manually confirms payment"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Update order status
    c.execute('''UPDATE orders 
                 SET status = 'paid', paid_at = ?
                 WHERE order_id = ?''',
              (datetime.now().isoformat(), order_id))
    
    # Update payment tracking
    c.execute('''UPDATE payments 
                 SET status = 'confirmed'
                 WHERE order_id = ?''',
              (order_id,))
    
    conn.commit()
    conn.close()
    
    logger.info(f"Payment confirmed for order {order_id}")
    return True

def get_pending_orders():
    """Get all orders pending confirmation"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute('''SELECT order_id, user_id, username, total_amount, btc_amount, 
                        payment_proof, created_at
                 FROM orders 
                 WHERE status IN ('pending', 'proof_submitted')
                 ORDER BY created_at DESC''')
    
    orders = c.fetchall()
    conn.close()
    
    return orders

# ========== QR CODE GENERATION ==========
def generate_payment_qr(btc_address, amount):
    """Generate QR code for Bitcoin payment"""
    try:
        # Bitcoin URI format
        bitcoin_uri = f"bitcoin:{btc_address}?amount={amount}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(bitcoin_uri)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return buf
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        return None

# ========== HELPER FUNCTIONS ==========
def format_btc(amount):
    """Format BTC amount"""
    return f"{amount:.8f} BTC"

def format_payment_message(order_info):
    """Format payment instruction message"""
    message = f"🧾 *Order: {order_info['order_id']}*\n\n"
    message += f"💰 *Total: £{order_info['gbp_amount']:.2f}*\n"
    message += f"₿ *Bitcoin Amount: {format_btc(order_info['btc_amount'])}*\n\n"
    message += f"📍 *Send Bitcoin to this address:*\n"
    message += f"`{order_info['btc_address']}`\n\n"
    message += f"⚡ *Current BTC Price: £{order_info['btc_price']:,.2f}*\n\n"
    message += "⏰ *Payment Instructions:*\n"
    message += "1. Send EXACTLY the BTC amount shown above\n"
    message += "2. Scan the QR code below (easiest way)\n"
    message += "3. After sending, click '✅ I've Paid'\n"
    message += "4. Submit your transaction ID or screenshot\n"
    message += "5. We'll confirm within 30 minutes\n\n"
    message += "⚠️ *Important:* Send only Bitcoin (BTC) to this address!\n"
    message += "💡 *Tip:* Copy transaction ID from your wallet after sending"
    
    return message

def format_order_summary(order):
    """Format order summary"""
    
    message = f"📦 *Order #{order['order_id']}*\n\n"
    
    # Parse items
    try:
        items = json.loads(order['items'])
        message += "🛍️ *Items:*\n"
        for item in items:
            message += f"• {item[1]} x{item[3]} - £{float(item[2]) * item[3]:.2f}\n"
    except:
        pass
    
    message += f"\n💰 *Total: £{order['total_amount']:.2f}*\n"
    message += f"₿ *BTC: {format_btc(order['btc_amount'])}*\n"
    message += f"📅 *Date: {order['created_at']}*\n"
    message += f"📊 *Status: {order['status'].upper()}*\n"
    
    if order.get('payment_proof'):
        message += f"📝 *Proof: {order['payment_proof'][:50]}...*\n"
    
    if order.get('paid_at'):
        message += f"✅ *Paid: {order['paid_at']}*"
    
    return message

def format_admin_order(order):
    """Format order for admin review"""
    order_id, user_id, username, total, btc_amount, proof, created = order
    
    message = f"🆔 *Order: {order_id}*\n"
    message += f"👤 User: @{username or 'N/A'} (ID: {user_id})\n"
    message += f"💰 £{total:.2f} = {format_btc(btc_amount)}\n"
    message += f"📅 {created}\n"
    
    if proof:
        message += f"📝 *Proof:* {proof[:100]}\n"
    else:
        message += f"⚠️ *No proof submitted yet*\n"
    
    return message

# Initialize database on import
init_payment_db()
