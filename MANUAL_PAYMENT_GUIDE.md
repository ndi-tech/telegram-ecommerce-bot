# 🚀 1010boys Manual Bitcoin Payment Bot - Complete Guide

## ✅ What You Have Now

**ZERO setup required!** Your bot is ready to accept Bitcoin payments RIGHT NOW using your wallet address:
```
bc1qmx2ut0mjflv2qxhfv9nqk8rwf7wyg0x2f760ym
```

### Features Included:
- ✅ Manual Bitcoin payment system
- ✅ Your static Bitcoin address (all payments go directly to you!)
- ✅ Automatic BTC/GBP price conversion
- ✅ QR code generation for easy payments
- ✅ Customer payment proof submission
- ✅ Admin confirmation system
- ✅ Order tracking database
- ✅ Full shopping cart
- ✅ No third-party services needed!

---

## 📋 Quick Start (2 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Your Telegram User ID (For Admin Features)
1. Open Telegram
2. Message this bot: `@userinfobot`
3. It will reply with your user ID (example: `123456789`)
4. Open `bot.py` in a text editor
5. Find this line: `ADMIN_USER_ID = None`
6. Change it to: `ADMIN_USER_ID = 123456789` (use your actual ID)

### Step 3: Run the Bot
```bash
python bot.py
```

You should see:
```
🤖 1010boys Telegram Bot - MANUAL BITCOIN PAYMENTS
✅ Your Bitcoin Address: bc1qmx2ut0mjflv2qxhfv9nqk8rwf7wyg0x2f760ym
✅ Manual payment confirmation system
✅ QR code generation
✅ Order tracking
🚀 Bot is running. Press Ctrl+C to stop.
```

**That's it! You're accepting Bitcoin payments!** 🎉

---

## 🔄 How It Works

### Customer Flow:

1. **Browse & Shop**
   - Customer browses products
   - Adds items to cart
   - Clicks "Checkout"

2. **Payment Invoice**
   - Bot shows YOUR Bitcoin address
   - Displays exact BTC amount needed
   - Shows QR code for easy scanning
   - Displays current BTC price

3. **Customer Pays**
   - Customer sends Bitcoin from their wallet
   - Scans QR code or copies address
   - Sends exact amount shown

4. **Submit Proof**
   - Customer clicks "✅ I've Paid"
   - Bot asks for proof:
     - Transaction ID (txid), OR
     - Screenshot of payment, OR
     - Description (e.g., "Sent 0.0012 BTC at 14:30")

5. **You Confirm**
   - You receive notification
   - Check your wallet for payment
   - Type `/admin` to see pending orders
   - Click "✅ Confirm Payment"
   - Customer gets notification! ✅

### Your Flow (Admin):

```
Customer submits proof
        ↓
You receive notification (if ADMIN_USER_ID is set)
        ↓
Type: /admin
        ↓
See all pending orders with proof
        ↓
Check your Bitcoin wallet
        ↓
Click "✅ Confirm Payment" for verified orders
        ↓
Customer receives confirmation! 🎉
```

---

## 💻 Admin Commands

### `/admin` - View Pending Orders

Shows all orders waiting for confirmation:

```
📦 Admin Panel

3 pending orders:

🆔 Order: ORD-1707234567-123456
👤 User: @johndoe (ID: 123456)
💰 £80.00 = 0.00123456 BTC
📅 2025-02-04 12:30:45
📝 Proof: txid: a1b2c3d4e5f6...

[✅ Confirm Payment] [❌ Reject]
```

Click "✅ Confirm Payment" to approve orders!

---

## 🧪 Testing Your Bot

### Test the Complete Flow:

1. **Start bot**: `python bot.py`

2. **In Telegram**:
   - Message your bot: `/start`
   - Click "🇬🇧 English"
   - Click "🎁 Products"
   - Select a product
   - Click "➕ Add to Cart"
   - Click "🛒 View Cart"
   - Click "💳 Checkout"

3. **You'll see**:
   ```
   🧾 Order: ORD-xxx
   
   💰 Total: £40.00
   ₿ Bitcoin Amount: 0.00061234 BTC
   
   📍 Send Bitcoin to this address:
   bc1qmx2ut0mjflv2qxhfv9nqk8rwf7wyg0x2f760ym
   
   [QR CODE IMAGE]
   
   [✅ I've Paid] [❌ Cancel Order]
   ```

4. **Test payment submission**:
   - Click "✅ I've Paid"
   - Send any text as "proof" (e.g., "test payment")
   - Bot confirms: "✅ Payment Proof Submitted!"

5. **Test admin confirmation**:
   - Type `/admin` in your bot
   - See the pending order
   - Click "✅ Confirm Payment"
   - Customer receives confirmation!

---

## 🎯 Real-World Usage

### When a REAL customer orders:

1. **They checkout** → Bot shows payment invoice
2. **They pay** → Send Bitcoin to your address
3. **They submit proof** → Upload txid or screenshot
4. **You receive notification** (if ADMIN_USER_ID is set)
5. **Check your wallet**:
   - Open your Bitcoin wallet app
   - Check if you received the payment
   - Verify the amount matches
6. **Confirm in bot**:
   - Type `/admin`
   - Click "✅ Confirm Payment"
7. **Customer gets notified** → Order confirmed! ✅

### Checking Your Wallet:

Your payments go to: `bc1qmx2ut0mjflv2qxhfv9nqk8rwf7wyg0x2f760ym`

Check this address in:
- Your Bitcoin wallet app
- Or blockchain explorer: https://blockchair.com/bitcoin/address/bc1qmx2ut0mjflv2qxhfv9nqk8rwf7wyg0x2f760ym

---

## 📊 Database & Orders

### Database Location:
`bot.db` (SQLite database in same folder as bot.py)

### Tables Created:
- `users` - User preferences
- `cart` - Shopping cart items
- `products` - Product catalog
- `orders` - All orders with status
- `payments` - Payment tracking

### Order Statuses:
- `pending` - Order created, awaiting payment
- `proof_submitted` - Customer submitted payment proof
- `paid` - You confirmed payment ✅
- `cancelled` - Order cancelled
- `rejected` - Payment rejected

---

## 🔧 Configuration Options

### In `bot.py`:

```python
# Your Telegram Bot Token
BOT_TOKEN = "your_bot_token_here"

# Your Telegram User ID (for admin notifications)
ADMIN_USER_ID = None  # Change to your user ID!
```

### In `payment.py`:

```python
# Your Bitcoin wallet address
BITCOIN_ADDRESS = "bc1qmx2ut0mjflv2qxhfv9nqk8rwf7wyg0x2f760ym"
```

**Already configured with your address!** ✅

---

## ⚙️ Customization

### Change Bitcoin Address:
1. Open `payment.py`
2. Find: `BITCOIN_ADDRESS = "bc1q..."`
3. Replace with your new address
4. Restart bot

### Add Admin User:
1. Message `@userinfobot` on Telegram
2. Get your user ID
3. Open `bot.py`
4. Set: `ADMIN_USER_ID = your_id_here`
5. Restart bot

### Adjust Price Buffer:
In `payment.py`, find:
```python
btc_amount = (total_gbp / btc_price) * 1.01  # 1% buffer
```
Change `1.01` to adjust buffer (e.g., `1.02` = 2% buffer)

---

## 🐛 Troubleshooting

### "Unable to get Bitcoin price"
**Solution**: Internet connection issue. Try again.

### Bot doesn't respond
**Solution**: 
```bash
# Check if running
ps aux | grep bot.py

# Restart
python bot.py
```

### Admin commands don't work
**Solution**: Set `ADMIN_USER_ID` in `bot.py`

### QR code not showing
**Solution**: Install Pillow:
```bash
pip install Pillow
```

---

## 🔒 Security Best Practices

### 1. Protect Your Bot Token
Never share your bot token publicly. For production:

```python
import os
BOT_TOKEN = os.getenv('BOT_TOKEN')
```

Then run:
```bash
export BOT_TOKEN="your_token_here"
python bot.py
```

### 2. Verify Payments
ALWAYS check your Bitcoin wallet before confirming orders!

### 3. Backup Database
Regularly backup `bot.db`:
```bash
cp bot.db bot_backup_$(date +%Y%m%d).db
```

### 4. Use HTTPS Webhooks (Production)
For production, use webhooks instead of polling.

---

## 📈 Production Deployment

### For Real Business Use:

1. **Get a VPS** (DigitalOcean, Linode, etc.)
2. **Upload your files**
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Set environment variables**:
   ```bash
   export BOT_TOKEN="your_token"
   export ADMIN_USER_ID="your_id"
   ```
5. **Run with systemd** (auto-restart):

Create `/etc/systemd/system/1010bot.service`:
```ini
[Unit]
Description=1010boys Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/bot
Environment="BOT_TOKEN=your_token"
Environment="ADMIN_USER_ID=your_id"
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable 1010bot
sudo systemctl start 1010bot
```

---

## 📞 What's Complete vs What's Optional

### ✅ COMPLETE & WORKING NOW:
- Shopping cart
- Product catalog (10 products)
- Bitcoin payment invoices
- QR code generation
- Payment proof submission
- Admin confirmation system
- Order tracking
- Customer notifications

### 🚧 OPTIONAL ENHANCEMENTS (Future):

1. **Automatic Payment Verification**
   - Bot checks blockchain automatically
   - No manual confirmation needed
   - Requires blockchain API integration

2. **Email Notifications**
   - Send order confirmations via email
   - Requires SMTP setup

3. **Shipping Integration**
   - Add shipping addresses
   - Tracking numbers
   - Delivery status

4. **More Products**
   - Add more items to catalog
   - Categories and filters
   - Product search

5. **Discount Codes**
   - Coupon system
   - Referral rewards
   - Bulk discounts

---

## 🎉 You're Ready!

Your bot is **100% functional** and ready to accept Bitcoin payments!

### Quick Checklist:

- ✅ Bot configured with your Bitcoin address
- ✅ Dependencies installed
- ✅ ADMIN_USER_ID set (optional but recommended)
- ✅ Bot running
- ✅ Tested checkout flow

### Start Selling:

1. Share your bot link: `https://t.me/YOUR_BOT_USERNAME`
2. Customers can order immediately!
3. You receive payments directly to your wallet
4. Confirm orders with `/admin` command

---

## 💡 Pro Tips

1. **Test First**: Make test orders with small amounts
2. **Check Wallet Often**: Monitor your Bitcoin address
3. **Respond Quickly**: Confirm payments within 30 minutes
4. **Keep Bot Running**: Use systemd or screen/tmux
5. **Backup Database**: Daily backups of bot.db

---

## 📱 Customer Instructions

Share these instructions with your customers:

**"How to Pay with Bitcoin:"**
1. Click "Checkout" in bot
2. Copy Bitcoin address or scan QR code
3. Send exact BTC amount from your wallet
4. Click "I've Paid" and submit transaction ID
5. Wait for confirmation (usually < 30 minutes)

---

## 🆘 Support

If you need help:
1. Check bot logs for errors
2. Verify Bitcoin address is correct
3. Ensure dependencies are installed
4. Test with `/start` command

---

## 🎯 Summary

**What you have:**
- Complete Bitcoin payment bot
- Manual confirmation system (simple & secure)
- Your own Bitcoin address (no middleman!)
- Full order tracking
- Admin panel

**What you need to do:**
1. Set ADMIN_USER_ID (2 minutes)
2. Run the bot
3. Start accepting payments!

**Total setup time: 2 minutes** ⚡

**You're ready to start selling with Bitcoin!** 🚀

---

## Example Order Flow

```
Customer:
"I want to buy Melonade Strain"
        ↓
Adds to cart → Checkout
        ↓
Bot: "Send 0.00061 BTC to bc1q..."
        ↓
Customer sends Bitcoin
        ↓
Customer: Clicks "I've Paid"
Bot: "Please send transaction ID"
Customer: "a1b2c3d4e5f6..."
        ↓
Bot: "✅ Proof submitted!"
        ↓
You receive notification
        ↓
You check wallet: ✅ Payment received!
        ↓
You: /admin → Click "Confirm Payment"
        ↓
Customer: "✅ Payment Confirmed! 🎉"
        ↓
Done! Ship the order! 📦
```

**Simple, secure, and works immediately!** 🔥
