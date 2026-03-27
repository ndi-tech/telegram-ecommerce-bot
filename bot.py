# bot.py - WITH MANUAL BITCOIN PAYMENT SYSTEM
import telebot
import sqlite3
import logging
import payment  # Manual Bitcoin payment module
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== CONFIGURATION ==========
# Load .env file for local testing (optional)
load_dotenv()

# Get token from environment variable (Railway/Koyeb provides this)
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    print("Please set BOT_TOKEN in Railway/Koyeb Variables tab")
    exit(1)

# Get admin ID from environment variable
ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')
if ADMIN_USER_ID:
    ADMIN_USER_ID = int(ADMIN_USER_ID)
    print(f"✅ ADMIN_USER_ID loaded: {ADMIN_USER_ID}")
else:
    print("⚠️  ADMIN_USER_ID not set - admin commands won't work")

# User states for handling text input
user_states = {}

# Create bot
bot = telebot.TeleBot(BOT_TOKEN)

# ========== REAL PRODUCT DATA ==========
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

# ========== DATABASE ==========
def init_db():
    """Initialize database"""
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, language TEXT DEFAULT 'en')''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cart
                 (user_id INTEGER, product_id INTEGER, quantity INTEGER DEFAULT 1,
                  PRIMARY KEY (user_id, product_id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, price TEXT, 
                  description TEXT, category TEXT, image_url TEXT)''')
    
    # Add products
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        for product in REAL_PRODUCTS:
            c.execute('''INSERT OR IGNORE INTO products 
                         (id, name, price, description, category, image_url) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                     (product['id'], product['name'], product['price'], 
                      product['desc'], product['category'], product['image']))
    
    conn.commit()
    conn.close()
    logger.info("Database initialized")

# ========== CART FUNCTIONS ==========
def get_cart_count(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] else 0

def add_to_cart(user_id, product_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?", 
              (user_id, product_id))
    existing = c.fetchone()
    
    if existing:
        c.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?",
                  (user_id, product_id))
    else:
        c.execute("INSERT INTO cart (user_id, product_id) VALUES (?, ?)",
                 (user_id, product_id))
    conn.commit()
    conn.close()

def get_cart_items(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''SELECT p.id, p.name, p.price, c.quantity 
                 FROM cart c 
                 JOIN products p ON c.product_id = p.id 
                 WHERE c.user_id = ?''', (user_id,))
    items = c.fetchall()
    conn.close()
    return items

def clear_cart(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def remove_from_cart(user_id, product_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    conn.commit()
    conn.close()

def get_cart_total(user_id):
    items = get_cart_items(user_id)
    total = 0
    for _, _, price, quantity in items:
        try:
            total += float(price) * quantity
        except:
            pass
    return total

# ========== PRODUCT FUNCTIONS ==========
def get_products():
    return REAL_PRODUCTS

def get_product(product_id):
    for product in REAL_PRODUCTS:
        if product['id'] == product_id:
            return product
    return None

def get_categories():
    categories = {}
    for product in REAL_PRODUCTS:
        cat = product['category']
        categories[cat] = categories.get(cat, 0) + 1
    return categories

def get_products_by_category(category):
    if category == 'all':
        return REAL_PRODUCTS
    return [p for p in REAL_PRODUCTS if p['category'] == category]

# ========== KEYBOARDS ==========
def get_language_keyboard():
    markup = telebot.types.InlineKeyboardMarkup()
    buttons = [
        ("🇬🇧 English", "lang_en"),
        ("🇫🇷 Français", "lang_fr"),
        ("🇪🇸 Español", "lang_es"),
        ("🇵🇹 Português", "lang_pt"),
        ("🇮🇹 Italiano", "lang_it"),
        ("🇵🇱 Polski", "lang_pl")
    ]
    
    for i in range(0, len(buttons), 2):
        row = []
        row.append(telebot.types.InlineKeyboardButton(buttons[i][0], callback_data=buttons[i][1]))
        if i + 1 < len(buttons):
            row.append(telebot.types.InlineKeyboardButton(buttons[i+1][0], callback_data=buttons[i+1][1]))
        markup.row(*row)
    
    return markup

def get_main_menu_keyboard(user_id=None):
    cart_count = get_cart_count(user_id) if user_id else 0
    markup = telebot.types.InlineKeyboardMarkup()
    
    rows = [
        [("🤔 How does it work?", "menu_how"), ("🆘 Support", "menu_support")],
        [("📘 User Guide", "menu_guide"), ("🎁 Products", "menu_products")],
        [("⭐ Reviews", "menu_reviews"), ("📣 Ref & Earn", "menu_ref")],
        [("🎟 Coupons", "menu_coupons"), ("❤️ Friendly Services", "menu_services")],
        [("🎁 Gift Cards", "menu_giftcards")],
        [(f"🛒 Cart ({cart_count})", "menu_cart"), ("📦 Orders", "menu_orders")],
        [("⚙️ Settings", "menu_settings")]
    ]
    
    for row in rows:
        if len(row) == 1:
            markup.row(telebot.types.InlineKeyboardButton(row[0][0], callback_data=row[0][1]))
        else:
            markup.row(
                telebot.types.InlineKeyboardButton(row[0][0], callback_data=row[0][1]),
                telebot.types.InlineKeyboardButton(row[1][0], callback_data=row[1][1])
            )
    
    return markup

def get_categories_keyboard():
    categories = get_categories()
    markup = telebot.types.InlineKeyboardMarkup()
    
    buttons = []
    for cat, count in categories.items():
        buttons.append((f"📁 {cat} ({count})", f"cat_{cat}"))
    
    buttons.append(("🌟 All Products", "cat_all"))
    buttons.append(("🔙 Back", "menu_back"))
    
    for i in range(0, len(buttons), 2):
        row = []
        row.append(telebot.types.InlineKeyboardButton(buttons[i][0], callback_data=buttons[i][1]))
        if i + 1 < len(buttons):
            row.append(telebot.types.InlineKeyboardButton(buttons[i+1][0], callback_data=buttons[i+1][1]))
        markup.row(*row)
    
    return markup

def get_product_keyboard(product_id, in_cart=False):
    markup = telebot.types.InlineKeyboardMarkup()
    
    if in_cart:
        markup.row(
            telebot.types.InlineKeyboardButton("➖ Remove", callback_data=f"remove_{product_id}"),
            telebot.types.InlineKeyboardButton("➕ Add More", callback_data=f"add_{product_id}")
        )
    else:
        markup.row(
            telebot.types.InlineKeyboardButton("➕ Add to Cart", callback_data=f"add_{product_id}"),
            telebot.types.InlineKeyboardButton("🛒 Buy Now", callback_data=f"buy_{product_id}")
        )
    
    markup.row(
        telebot.types.InlineKeyboardButton("🔙 Back to Products", callback_data="menu_products"),
        telebot.types.InlineKeyboardButton("🛒 View Cart", callback_data="menu_cart")
    )
    
    return markup

def get_cart_keyboard():
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.row(
        telebot.types.InlineKeyboardButton("🗑️ Clear Cart", callback_data="cart_clear"),
        telebot.types.InlineKeyboardButton("💳 Checkout", callback_data="cart_checkout")
    )
    
    markup.row(
        telebot.types.InlineKeyboardButton("🔄 Continue Shopping", callback_data="menu_products"),
        telebot.types.InlineKeyboardButton("🔙 Main Menu", callback_data="menu_back")
    )
    
    return markup

def get_payment_keyboard(order_id):
    """Keyboard for payment actions"""
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.row(
        telebot.types.InlineKeyboardButton("✅ I've Paid", callback_data=f"paid_{order_id}"),
        telebot.types.InlineKeyboardButton("❌ Cancel Order", callback_data=f"cancel_{order_id}")
    )
    
    markup.row(
        telebot.types.InlineKeyboardButton("🔙 Main Menu", callback_data="menu_back")
    )
    
    return markup

def get_admin_keyboard(order_id):
    """Keyboard for admin order confirmation"""
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.row(
        telebot.types.InlineKeyboardButton("✅ Confirm Payment", callback_data=f"admin_confirm_{order_id}"),
        telebot.types.InlineKeyboardButton("❌ Reject", callback_data=f"admin_reject_{order_id}")
    )
    
    return markup

# ========== MESSAGE FORMATTING ==========
def format_product_message(product):
    message = f"🎁 *{product['name']}*\n\n"
    message += f"💰 *Price:* £{product['price']}\n"
    message += f"📁 *Category:* {product['category']}\n\n"
    message += f"📝 {product['desc'][:150]}...\n\n"
    message += f"🆔 ID: `{product['id']}`"
    return message

def format_cart_message(user_id):
    items = get_cart_items(user_id)
    
    if not items:
        return "🛒 *Your cart is empty*\n\nAdd some products to get started!"
    
    message = "🛒 *Your Shopping Cart*\n\n"
    total = 0
    item_count = 0
    
    for idx, (product_id, name, price, quantity) in enumerate(items, 1):
        try:
            item_total = float(price) * quantity
        except:
            item_total = 0
        
        total += item_total
        item_count += quantity
        
        message += f"{idx}. *{name}*\n"
        message += f"   Price: £{price} × {quantity} = £{item_total:.2f}\n"
        message += f"   ID: `{product_id}`\n\n"
    
    message += f"📦 *Total Items:* {item_count}\n"
    message += f"💰 *Total Amount:* £{total:.2f}\n\n"
    message += "Use buttons below to manage your cart."
    
    return message

# ========== HANDLERS ==========
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    init_db()
    
    welcome_msg = (
        "🌍 *Welcome to 1010boys Store!*\n\n"
        "We offer premium quality products with fast delivery.\n"
        "💰 *Payment: Bitcoin only*\n"
        "⚡ *Quick & Easy checkout!*\n\n"
        "Choose your language to begin:"
    )
    
    bot.send_message(
        message.chat.id,
        welcome_msg,
        reply_markup=get_language_keyboard(),
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    """Admin command to view pending orders"""
    user_id = message.from_user.id
    
    # Check if user is admin (you can set ADMIN_USER_ID in config)
    if ADMIN_USER_ID and user_id != ADMIN_USER_ID:
        bot.send_message(message.chat.id, "⛔ Unauthorized")
        return
    
    # Get pending orders
    pending = payment.get_pending_orders()
    
    if not pending:
        bot.send_message(
            message.chat.id,
            "📦 *Admin Panel*\n\nNo pending orders!",
            parse_mode='Markdown'
        )
        return
    
    # Show each pending order
    bot.send_message(
        message.chat.id,
        f"📦 *Admin Panel*\n\n*{len(pending)} pending orders:*",
        parse_mode='Markdown'
    )
    
    for order in pending:
        order_msg = payment.format_admin_order(order)
        bot.send_message(
            message.chat.id,
            order_msg,
            reply_markup=get_admin_keyboard(order[0]),  # order[0] is order_id
            parse_mode='Markdown'
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    try:
        data = call.data
        
        # Language selection
        if data.startswith('lang_'):
            conn = sqlite3.connect('bot.db')
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", 
                     (user_id, 'en'))
            conn.commit()
            conn.close()
            
            bot.send_message(
                chat_id,
                "🏠 *Main Menu*\n\nChoose an option below:",
                reply_markup=get_main_menu_keyboard(user_id),
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id, "Language set to English!")
        
        # Main menu
        elif data == 'menu_products':
            bot.send_message(
                chat_id,
                "📁 *Browse Products*\n\nSelect a category:",
                reply_markup=get_categories_keyboard(),
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id)
        
        elif data == 'menu_cart':
            cart_msg = format_cart_message(user_id)
            bot.send_message(
                chat_id,
                cart_msg,
                reply_markup=get_cart_keyboard(),
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id)
        
        elif data == 'menu_orders':
            # Show user's orders
            orders = payment.get_user_orders(user_id)
            
            if not orders:
                bot.send_message(
                    chat_id,
                    "📦 *Your Orders*\n\nNo orders yet. Start shopping!",
                    parse_mode='Markdown'
                )
            else:
                message = "📦 *Your Recent Orders*\n\n"
                for order_id, total, btc_amount, status, created in orders:
                    message += f"🆔 `{order_id}`\n"
                    message += f"💰 £{total:.2f} ({payment.format_btc(btc_amount)})\n"
                    message += f"📊 Status: *{status.upper()}*\n"
                    message += f"📅 {created}\n\n"
                
                bot.send_message(chat_id, message, parse_mode='Markdown')
            
            bot.answer_callback_query(call.id)
        
        elif data == 'menu_settings':
            bot.send_message(
                chat_id,
                "⚙️ *Settings*\n\nChoose your language:",
                reply_markup=get_language_keyboard(),
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id)
        
        elif data == 'menu_back':
            bot.send_message(
                chat_id,
                "🏠 *Main Menu*\n\nChoose an option below:",
                reply_markup=get_main_menu_keyboard(user_id),
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id)
        
        # Categories
        elif data.startswith('cat_'):
            category = data[4:]
            
            if category == 'all':
                products = get_products()
            else:
                products = get_products_by_category(category)
            
            if not products:
                bot.answer_callback_query(call.id, "No products!", show_alert=True)
                return
            
            product = products[0]
            product_msg = format_product_message(product)
            
            cart_items = [item[0] for item in get_cart_items(user_id)]
            in_cart = product['id'] in cart_items
            
            try:
                bot.send_photo(
                    chat_id,
                    product['image'],
                    caption=product_msg,
                    reply_markup=get_product_keyboard(product['id'], in_cart),
                    parse_mode='Markdown'
                )
            except:
                bot.send_message(
                    chat_id,
                    product_msg,
                    reply_markup=get_product_keyboard(product['id'], in_cart),
                    parse_mode='Markdown'
                )
            
            bot.answer_callback_query(call.id)
        
        # Product actions
        elif data.startswith('add_'):
            product_id = int(data[4:])
            product = get_product(product_id)
            
            if product:
                add_to_cart(user_id, product_id)
                bot.answer_callback_query(call.id, f"✅ {product['name']} added!")
                
                # Show updated cart
                cart_msg = format_cart_message(user_id)
                bot.send_message(
                    chat_id,
                    cart_msg,
                    reply_markup=get_cart_keyboard(),
                    parse_mode='Markdown'
                )
        
        elif data.startswith('remove_'):
            product_id = int(data[7:])
            remove_from_cart(user_id, product_id)
            bot.answer_callback_query(call.id, "❌ Removed from cart!")
            
            # Show updated cart
            cart_msg = format_cart_message(user_id)
            bot.send_message(
                chat_id,
                cart_msg,
                reply_markup=get_cart_keyboard(),
                parse_mode='Markdown'
            )
        
        elif data.startswith('buy_'):
            product = get_product(int(data[4:]))
            if product:
                # Add to cart and go to checkout
                add_to_cart(user_id, int(data[4:]))
                # Trigger checkout
                handle_checkout(chat_id, user_id)
        
        # Cart actions
        elif data == 'cart_clear':
            clear_cart(user_id)
            bot.answer_callback_query(call.id, "🗑️ Cart cleared!")
            
            cart_msg = format_cart_message(user_id)
            bot.send_message(
                chat_id,
                cart_msg,
                reply_markup=get_cart_keyboard(),
                parse_mode='Markdown'
            )
        
        elif data == 'cart_checkout':
            handle_checkout(chat_id, user_id)
            bot.answer_callback_query(call.id)
        
        # Payment actions
        elif data.startswith('paid_'):
            # Customer clicked "I've Paid"
            order_id = data[5:]
            
            # Ask for payment proof
            user_states[user_id] = f"awaiting_proof_{order_id}"
            
            bot.send_message(
                chat_id,
                "📝 *Payment Proof Required*\n\n"
                "Please send ONE of the following:\n\n"
                "1️⃣ Transaction ID (txid)\n"
                "   Example: `a1b2c3d4e5f6...`\n\n"
                "2️⃣ Screenshot of payment\n\n"
                "3️⃣ Description of payment\n"
                "   Example: 'Sent 0.0012 BTC from Coinbase at 14:30'\n\n"
                "Send it as a message now:",
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id)
        
        elif data.startswith('cancel_'):
            order_id = data[7:]
            payment.update_order_status(order_id, 'cancelled')
            bot.answer_callback_query(call.id, "❌ Order cancelled")
            
            bot.send_message(
                chat_id,
                "❌ Order cancelled. Your cart is still saved.",
                reply_markup=get_main_menu_keyboard(user_id)
            )
        
        # Admin actions
        elif data.startswith('admin_confirm_'):
            order_id = data[14:]
            
            # Confirm payment
            payment.confirm_payment_admin(order_id)
            
            # Get order details
            order = payment.get_order(order_id)
            
            # Notify customer
            try:
                bot.send_message(
                    order['user_id'],
                    f"✅ *Payment Confirmed!*\n\n"
                    f"Your order {order_id} has been confirmed.\n"
                    f"We're processing it now!\n\n"
                    f"Thank you for your purchase! 🎉",
                    parse_mode='Markdown'
                )
            except:
                pass
            
            bot.answer_callback_query(call.id, "✅ Payment confirmed!")
            bot.send_message(chat_id, f"✅ Order {order_id} confirmed!")
        
        elif data.startswith('admin_reject_'):
            order_id = data[13:]
            payment.update_order_status(order_id, 'rejected')
            
            bot.answer_callback_query(call.id, "❌ Order rejected")
            bot.send_message(chat_id, f"❌ Order {order_id} rejected")
        
        # Other menu items
        else:
            responses = {
                'menu_how': "🤔 *How does it work?*\n\n1. Browse products\n2. Add to cart\n3. Checkout with Bitcoin\n4. Send payment\n5. Receive confirmation\n\nSimple and secure!",
                'menu_support': "🆘 *Support*\n\nNeed help?\n📧 support@1010boys.com\n💬 Live chat: 24/7",
                'menu_guide': "📘 *User Guide*\n\n• Browse our products by category\n• Add items to your cart\n• Checkout and pay with Bitcoin\n• Track your orders\n\nAll payments are processed securely via Blockonomics.",
                'menu_reviews': "⭐ *Reviews*\n\nSee what customers say! Coming soon.",
                'menu_ref': "📣 *Ref & Earn*\n\nRefer friends, earn Bitcoin! Coming soon.",
                'menu_coupons': "🎟 *Coupons*\n\nDiscount codes coming soon!",
                'menu_services': "❤️ *Friendly Services*\n\n• Fast delivery\n• 24/7 support\n• Secure Bitcoin payments\n• Quality products",
                'menu_giftcards': "🎁 *Gift Cards*\n\nComing soon!"
            }
            
            if data in responses:
                bot.send_message(chat_id, responses[data], parse_mode='Markdown')
                bot.answer_callback_query(call.id)
    
    except Exception as e:
        logger.error(f"Error handling callback: {e}")
        bot.answer_callback_query(call.id, "Error occurred. Try again.", show_alert=True)

def handle_checkout(chat_id, user_id):
    """Handle checkout process"""
    items = get_cart_items(user_id)
    
    if not items:
        bot.send_message(chat_id, "🛒 Your cart is empty!")
        return
    
    total = get_cart_total(user_id)
    
    # Get username
    try:
        user = bot.get_chat(user_id)
        username = user.username
    except:
        username = None
    
    # Create order
    bot.send_message(chat_id, "⏳ Creating your Bitcoin payment invoice...")
    
    order_info, error = payment.create_order(user_id, username, items, total)
    
    if error:
        bot.send_message(
            chat_id,
            f"❌ *Error:* {error}\n\nPlease try again.",
            parse_mode='Markdown'
        )
        return
    
    # Send payment instructions
    payment_msg = payment.format_payment_message(order_info)
    
    # Generate and send QR code
    qr_image = payment.generate_payment_qr(
        order_info['btc_address'], 
        order_info['btc_amount']
    )
    
    if qr_image:
        bot.send_photo(
            chat_id,
            qr_image,
            caption=payment_msg,
            reply_markup=get_payment_keyboard(order_info['order_id']),
            parse_mode='Markdown'
        )
    else:
        bot.send_message(
            chat_id,
            payment_msg,
            reply_markup=get_payment_keyboard(order_info['order_id']),
            parse_mode='Markdown'
        )
    
    logger.info(f"Order created: {order_info['order_id']} for user {user_id}")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """Handle all text messages and payment proof"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # Check if user is submitting payment proof
    if user_id in user_states and user_states[user_id].startswith('awaiting_proof_'):
        order_id = user_states[user_id].split('_')[2]
        
        # Get proof text (could be text, caption from photo, etc.)
        proof_text = message.text or message.caption or "Screenshot provided"
        
        # Submit proof
        payment.submit_payment_proof(order_id, proof_text)
        
        # Clear state
        del user_states[user_id]
        
        # Notify user
        bot.send_message(
            chat_id,
            "✅ *Payment Proof Submitted!*\n\n"
            "We've received your payment proof.\n"
            "We'll verify and confirm within 30 minutes.\n\n"
            "You'll receive a notification once confirmed! 🎉",
            reply_markup=get_main_menu_keyboard(user_id),
            parse_mode='Markdown'
        )
        
        # Notify admin if set
        if ADMIN_USER_ID:
            try:
                order = payment.get_order(order_id)
                admin_msg = f"🔔 *New Payment Proof*\n\n{payment.format_order_summary(order)}"
                bot.send_message(
                    ADMIN_USER_ID,
                    admin_msg,
                    reply_markup=get_admin_keyboard(order_id),
                    parse_mode='Markdown'
                )
            except:
                pass
        
        logger.info(f"Payment proof submitted for {order_id}")
        return
    
    # Regular message handling
    if message.text and not message.text.startswith('/'):
        bot.send_message(
            chat_id,
            "Please use the menu buttons or /start!",
            reply_markup=get_main_menu_keyboard(user_id)
        )

# ========== MAIN ==========
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 1010boys Telegram Bot - MANUAL BITCOIN PAYMENTS")
    print("=" * 60)
    print(f"✅ Your Bitcoin Address: {payment.BITCOIN_ADDRESS}")
    print("✅ Manual payment confirmation system")
    print("✅ QR code generation")
    print("✅ Order tracking")
    print("=" * 60)
    print("📋 Admin Commands:")
    print("   /admin - View pending orders")
    print("=" * 60)
    
    if not ADMIN_USER_ID:
        print("⚠️  WARNING: ADMIN_USER_ID not set!")
        print("   Set your Telegram user ID in bot.py to receive notifications")
        print("   Message @userinfobot to get your ID")
        print("=" * 60)
    
    init_db()
    
    print("🚀 Bot is running. Press Ctrl+C to stop.")
    print("=" * 60)
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Bot stopped: {e}")