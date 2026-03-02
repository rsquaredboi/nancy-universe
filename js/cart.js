// Nancy Universe — Cart System v2
// Branded, funky, scarcity-driven. Small batch = real positioning.
// localStorage-backed, self-contained (injects CSS + HTML)
(function() {
  'use strict';

  const STORAGE_KEY = 'nancy_cart';
  const FREE_SHIP_THRESHOLD = 89;
  const CART_ICON_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>';

  // Scarcity data — fake but believable stock per product slug
  // Seeded from slug hash so it's consistent per product
  function getStockLeft(slug) {
    let h = 0;
    for (let i = 0; i < slug.length; i++) h = ((h << 5) - h + slug.charCodeAt(i)) | 0;
    return 3 + Math.abs(h % 12); // 3-14 left
  }

  // Fun "people viewing" count
  function getViewers(slug) {
    let h = 0;
    for (let i = 0; i < slug.length; i++) h = ((h << 5) - h + slug.charCodeAt(i)) | 0;
    return 18 + Math.abs(h % 47); // 18-64 viewers
  }

  // Toast copy rotation
  const TOAST_LINES = [
    'Great taste. ',
    'Excellent choice. ',
    'You have good energy. ',
    'Smart move. ',
    'We love that for you. ',
  ];
  function randomToastLine() {
    return TOAST_LINES[Math.floor(Math.random() * TOAST_LINES.length)];
  }

  // ═══════════════════════════════════════════════
  // INJECT CSS
  // ═══════════════════════════════════════════════
  const style = document.createElement('style');
  style.textContent = `
    /* ═══ CART OVERLAY ═══ */
    .cart-overlay {
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.5);
      backdrop-filter: blur(6px);
      z-index: 9998;
      opacity: 0; pointer-events: none;
      transition: opacity 0.3s ease;
    }
    .cart-overlay.open { opacity: 1; pointer-events: auto; }

    /* ═══ CART DRAWER ═══ */
    .cart-drawer {
      position: fixed; top: 0; right: 0;
      width: min(440px, 94vw);
      height: 100dvh;
      background: #faf8f5;
      z-index: 9999;
      transform: translateX(100%);
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex; flex-direction: column;
      box-shadow: -8px 0 50px rgba(0,0,0,0.15);
    }
    .cart-drawer.open { transform: translateX(0); }

    /* Header */
    .cart-drawer-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 1.2rem 1.5rem 1rem;
      border-bottom: 1.5px solid #f0ece6;
    }
    .cart-drawer-title {
      font-family: 'PP Editorial New', Georgia, serif;
      font-weight: 400; font-size: 1.3rem;
      font-style: italic;
    }
    .cart-drawer-count {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 700; font-size: 0.7rem;
      background: #ff30cc; color: white;
      padding: 0.15rem 0.5rem; border-radius: 100px;
      margin-left: 0.5rem; vertical-align: middle;
      letter-spacing: 0.03em;
    }
    .cart-drawer-close {
      width: 36px; height: 36px; border-radius: 50%;
      border: none; background: #f0ece6; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.2rem; color: #555;
      transition: all 0.2s;
    }
    .cart-drawer-close:hover { background: #e5e0d8; transform: rotate(90deg) scale(1.1); }

    /* Shipping Progress Bar */
    .cart-shipping-bar {
      padding: 0.7rem 1.5rem;
      background: #fff0fa;
      border-bottom: 1px solid #f0ece6;
    }
    .cart-shipping-text {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.75rem; font-weight: 600;
      text-align: center; margin-bottom: 0.4rem;
      color: #333;
    }
    .cart-shipping-text span { color: #ff30cc; }
    .cart-shipping-track {
      height: 4px; background: #f0ece6; border-radius: 4px;
      overflow: hidden;
    }
    .cart-shipping-fill {
      height: 100%; background: linear-gradient(90deg, #ff30cc, #ccfd28);
      border-radius: 4px;
      transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Items area */
    .cart-drawer-items {
      flex: 1; overflow-y: auto;
      padding: 0.75rem 1.5rem;
      scrollbar-width: thin;
    }
    .cart-drawer-items::-webkit-scrollbar { width: 3px; }
    .cart-drawer-items::-webkit-scrollbar-thumb { background: #ddd; border-radius: 3px; }

    /* Cart item */
    .cart-item {
      display: grid;
      grid-template-columns: 76px 1fr 28px;
      gap: 0.85rem;
      padding: 0.85rem 0;
      border-bottom: 1px solid #f0ece6;
      align-items: start;
    }
    .cart-item:last-child { border-bottom: none; }
    .cart-item-img {
      width: 76px; height: 76px;
      border-radius: 14px; overflow: hidden;
      background: #f3efe9;
      position: relative;
    }
    .cart-item-img img { width: 100%; height: 100%; object-fit: cover; }
    .cart-item-details { min-width: 0; }
    .cart-item-name {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 700; font-size: 0.9rem;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .cart-item-variant {
      font-size: 0.72rem; color: #888; margin-top: 0.1rem;
    }
    .cart-item-scarcity {
      display: inline-flex; align-items: center; gap: 0.25rem;
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.65rem; font-weight: 600;
      color: #d9534f;
      margin-top: 0.25rem;
      letter-spacing: 0.02em;
    }
    .cart-item-scarcity::before {
      content: '';
      width: 5px; height: 5px; border-radius: 50%;
      background: #d9534f;
      animation: scarcity-pulse 1.5s ease-in-out infinite;
    }
    @keyframes scarcity-pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }
    .cart-item-price-row {
      display: flex; align-items: center; gap: 0.5rem;
      margin-top: 0.3rem;
    }
    .cart-item-price {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 700; font-size: 0.9rem;
    }
    .cart-item-qty {
      display: flex; align-items: center; gap: 0;
      margin-top: 0;
      border: 1.5px solid #e5e0d8; border-radius: 100px;
      overflow: hidden;
    }
    .cart-item-qty button {
      width: 28px; height: 28px;
      border: none; background: transparent; cursor: pointer;
      font-size: 0.85rem; font-weight: 600; color: #555;
      display: flex; align-items: center; justify-content: center;
      transition: all 0.15s;
    }
    .cart-item-qty button:hover { background: #f0ece6; color: #ff30cc; }
    .cart-item-qty span {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 700; font-size: 0.8rem;
      min-width: 1.6rem; text-align: center;
    }
    .cart-item-remove {
      align-self: center;
      background: none; border: none; cursor: pointer;
      color: #ccc; font-size: 1.1rem; padding: 0.2rem;
      transition: all 0.2s;
      line-height: 1;
    }
    .cart-item-remove:hover { color: #ff4b6e; transform: scale(1.2); }

    /* Empty state */
    .cart-empty {
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      height: 100%; text-align: center; padding: 2.5rem 1.5rem;
    }
    .cart-empty-icon { font-size: 3.5rem; margin-bottom: 0.6rem; }
    .cart-empty-title {
      font-family: 'PP Editorial New', Georgia, serif;
      font-size: 1.4rem; font-style: italic; font-weight: 400;
      margin-bottom: 0.3rem;
    }
    .cart-empty-sub {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.8rem; color: #999; line-height: 1.5;
      max-width: 260px; margin-bottom: 1.5rem;
    }
    .cart-empty-shop {
      padding: 0.8rem 2.2rem;
      background: #111; color: white;
      border: none; border-radius: 100px;
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 700; font-size: 0.8rem;
      text-transform: uppercase; letter-spacing: 0.06em;
      cursor: pointer; transition: all 0.3s;
    }
    .cart-empty-shop:hover { background: #ff30cc; transform: scale(1.04); box-shadow: 0 4px 20px rgba(255,48,204,0.25); }

    /* Footer */
    .cart-drawer-footer {
      padding: 1rem 1.5rem 1.25rem;
      border-top: 1.5px solid #f0ece6;
      background: white;
    }
    .cart-footer-note {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.7rem; color: #999;
      text-align: center; margin-bottom: 0.6rem;
      line-height: 1.4;
    }
    .cart-footer-note strong { color: #555; }
    .cart-subtotal {
      display: flex; justify-content: space-between; align-items: baseline;
      margin-bottom: 0.6rem;
    }
    .cart-subtotal-label {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 600; font-size: 0.85rem; color: #555;
      text-transform: uppercase; letter-spacing: 0.05em;
    }
    .cart-subtotal-value {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 800; font-size: 1.3rem;
    }
    .cart-saved-tag {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.7rem; font-weight: 700;
      color: #16a34a; text-align: right;
      margin-bottom: 0.8rem;
    }
    .cart-checkout-btn {
      display: flex; align-items: center; justify-content: center; gap: 0.5rem;
      width: 100%; padding: 1rem;
      background: #111; color: white;
      border: none; border-radius: 100px;
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 700; font-size: 0.95rem;
      cursor: pointer; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      text-transform: uppercase; letter-spacing: 0.06em;
      position: relative; overflow: hidden;
    }
    .cart-checkout-btn::before {
      content: ''; position: absolute; inset: 0;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
      transform: translateX(-100%);
      animation: checkout-shimmer 2s ease-in-out infinite;
    }
    @keyframes checkout-shimmer {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }
    .cart-checkout-btn:hover {
      background: #ff30cc;
      transform: scale(1.02);
      box-shadow: 0 6px 24px rgba(255,48,204,0.3);
    }
    .cart-trust-row {
      display: flex; justify-content: center; gap: 1rem;
      margin-top: 0.6rem;
    }
    .cart-trust-item {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.65rem; color: #aaa;
      display: flex; align-items: center; gap: 0.25rem;
    }

    /* ═══ QUICK ADD BUTTON (collection cards) ═══ */
    .product-card { position: relative; }
    .quick-add-btn {
      position: absolute;
      bottom: 0; left: 0; right: 0;
      padding: 0.75rem;
      background: rgba(17,17,17,0.92);
      backdrop-filter: blur(8px);
      color: white;
      border: none;
      font-family: 'ESRebondGrotesque', 'DM Sans', sans-serif;
      font-weight: 700; font-size: 0.75rem;
      text-transform: uppercase; letter-spacing: 0.08em;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 0.4rem;
      opacity: 0; transform: translateY(8px);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 5;
      border-radius: 0 0 var(--radius-sm, 12px) var(--radius-sm, 12px);
    }
    .quick-add-btn svg { width: 14px; height: 14px; }
    .product-card:hover .quick-add-btn,
    .product-card:focus-within .quick-add-btn {
      opacity: 1; transform: translateY(0);
    }
    .quick-add-btn:hover { background: #ff30cc; }
    .quick-add-btn.added {
      background: #ccfd28 !important; color: #111 !important;
    }

    /* ═══ SOLD OUT MODAL ═══ */
    .soldout-modal-overlay {
      position: fixed; inset: 0;
      background: rgba(0,0,0,0.6);
      backdrop-filter: blur(8px);
      z-index: 10001;
      display: flex; align-items: center; justify-content: center;
      opacity: 0; pointer-events: none;
      transition: opacity 0.3s ease;
    }
    .soldout-modal-overlay.open { opacity: 1; pointer-events: auto; }

    .soldout-modal {
      background: white;
      border-radius: 28px;
      padding: 2.5rem 2rem 2rem;
      max-width: 400px; width: 92%;
      text-align: center;
      transform: scale(0.9) translateY(20px);
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 24px 80px rgba(0,0,0,0.2);
      position: relative;
      overflow: hidden;
    }
    .soldout-modal::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0;
      height: 4px;
      background: linear-gradient(90deg, #ff30cc, #ccfd28, #ff30cc);
      background-size: 200% 100%;
      animation: gradient-slide 3s ease infinite;
    }
    @keyframes gradient-slide {
      0%, 100% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
    }
    .soldout-modal-overlay.open .soldout-modal {
      transform: scale(1) translateY(0);
    }
    .soldout-badge {
      display: inline-block;
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.65rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 0.1em;
      background: #fff0fa; color: #ff30cc;
      padding: 0.3rem 0.8rem; border-radius: 100px;
      margin-bottom: 0.8rem;
    }
    .soldout-title {
      font-family: 'PP Editorial New', Georgia, serif;
      font-size: 1.8rem; font-weight: 400;
      font-style: italic; margin-bottom: 0.2rem;
    }
    .soldout-sub-head {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.95rem; font-weight: 700;
      margin-bottom: 0.6rem;
    }
    .soldout-sub {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.82rem; color: #777;
      margin-bottom: 1.3rem; line-height: 1.6;
    }
    .soldout-sub strong { color: #ff30cc; font-weight: 600; }
    .soldout-stats {
      display: flex; justify-content: center; gap: 1.5rem;
      margin-bottom: 1.3rem;
    }
    .soldout-stat {
      text-align: center;
    }
    .soldout-stat-num {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 800; font-size: 1.3rem; color: #111;
    }
    .soldout-stat-label {
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.6rem; color: #999;
      text-transform: uppercase; letter-spacing: 0.06em;
    }
    .soldout-email-form {
      display: flex; gap: 0.5rem; margin-bottom: 0.8rem;
    }
    .soldout-email-input {
      flex: 1; padding: 0.8rem 1rem;
      border: 2px solid #f0ece6; border-radius: 100px;
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.85rem; outline: none;
      transition: border-color 0.2s;
      background: #faf8f5;
    }
    .soldout-email-input:focus { border-color: #ff30cc; background: white; }
    .soldout-email-input::placeholder { color: #bbb; }
    .soldout-notify-btn {
      padding: 0.8rem 1.5rem;
      background: #ff30cc; color: white;
      border: none; border-radius: 100px;
      font-family: 'ESRebondGrotesque', sans-serif;
      font-weight: 700; font-size: 0.8rem;
      text-transform: uppercase; letter-spacing: 0.04em;
      cursor: pointer; transition: all 0.2s;
      white-space: nowrap;
    }
    .soldout-notify-btn:hover { background: #e620b5; transform: scale(1.03); }
    .soldout-notify-btn.submitted {
      background: #ccfd28; color: #111; pointer-events: none;
    }
    .soldout-close-btn {
      background: none; border: none;
      color: #bbb; font-size: 0.8rem;
      cursor: pointer; padding: 0.5rem 1rem;
      font-family: 'ESRebondGrotesque', sans-serif;
      transition: color 0.2s;
    }
    .soldout-close-btn:hover { color: #555; }

    /* ═══ ADD TO CART TOAST ═══ */
    .cart-toast {
      position: fixed;
      top: 80px; right: 1.5rem;
      background: #111; color: white;
      padding: 0.9rem 1.3rem;
      border-radius: 16px;
      font-family: 'ESRebondGrotesque', sans-serif;
      font-size: 0.82rem;
      display: flex; align-items: center; gap: 0.6rem;
      z-index: 10000;
      opacity: 0; transform: translateX(20px) scale(0.95);
      transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
      box-shadow: 0 8px 30px rgba(0,0,0,0.25);
      max-width: 320px;
    }
    .cart-toast.show {
      opacity: 1; transform: translateX(0) scale(1);
      pointer-events: auto;
    }
    .cart-toast-check {
      width: 22px; height: 22px; min-width: 22px;
      background: #ccfd28; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      color: #111; font-size: 0.7rem; font-weight: 800;
    }
    .cart-toast-text { line-height: 1.3; }
    .cart-toast-text strong { font-weight: 700; }
    .cart-toast-text small { display: block; font-size: 0.7rem; color: #aaa; margin-top: 0.1rem; }

    /* ═══ NAV CART BADGE ═══ */
    .cart-count { display: none !important; }
    .cart-count.has-items { display: flex !important; }
    .nav-cart { cursor: pointer; }

    /* Mobile */
    @media (max-width: 768px) {
      .cart-drawer { width: 100vw; }
      .cart-toast { right: 0.75rem; left: 0.75rem; max-width: none; justify-content: center; }
      .soldout-email-form { flex-direction: column; }
      .soldout-stats { gap: 1rem; }
    }
  `;
  document.head.appendChild(style);

  // ═══════════════════════════════════════════════
  // INJECT DRAWER HTML
  // ═══════════════════════════════════════════════
  function injectDrawer() {
    if (document.getElementById('cart-drawer')) return;

    const overlay = document.createElement('div');
    overlay.className = 'cart-overlay';
    overlay.id = 'cart-overlay';

    const drawer = document.createElement('div');
    drawer.className = 'cart-drawer';
    drawer.id = 'cart-drawer';
    drawer.innerHTML = `
      <div class="cart-drawer-header">
        <div class="cart-drawer-title">Your Bag <span class="cart-drawer-count" id="cart-drawer-count" style="display:none"></span></div>
        <button class="cart-drawer-close" id="cart-drawer-close" aria-label="Close cart">&times;</button>
      </div>
      <div class="cart-shipping-bar" id="cart-shipping-bar" style="display:none;">
        <div class="cart-shipping-text" id="cart-shipping-text"></div>
        <div class="cart-shipping-track"><div class="cart-shipping-fill" id="cart-shipping-fill" style="width:0%"></div></div>
      </div>
      <div class="cart-drawer-items" id="cart-drawer-items"></div>
      <div class="cart-drawer-footer" id="cart-drawer-footer" style="display:none;">
        <div class="cart-footer-note" id="cart-footer-note"></div>
        <div class="cart-subtotal">
          <span class="cart-subtotal-label">Subtotal</span>
          <span class="cart-subtotal-value" id="cart-subtotal-value">$0</span>
        </div>
        <div class="cart-saved-tag" id="cart-saved-tag" style="display:none"></div>
        <button class="cart-checkout-btn" id="cart-checkout-btn">
          Secure Checkout
        </button>
        <div class="cart-trust-row">
          <span class="cart-trust-item">&#128274; Encrypted</span>
          <span class="cart-trust-item">&#128230; Discreet box</span>
          <span class="cart-trust-item">&#9889; Ships tomorrow</span>
        </div>
      </div>
    `;

    const toast = document.createElement('div');
    toast.className = 'cart-toast';
    toast.id = 'cart-toast';
    toast.innerHTML = '<span class="cart-toast-check">&#10003;</span><div class="cart-toast-text" id="cart-toast-text"></div>';

    // Sold out modal
    const soldoutOverlay = document.createElement('div');
    soldoutOverlay.className = 'soldout-modal-overlay';
    soldoutOverlay.id = 'soldout-overlay';
    soldoutOverlay.innerHTML = `
      <div class="soldout-modal">
        <div class="soldout-badge">Limited Production Run</div>
        <div class="soldout-title">Almost Here</div>
        <div class="soldout-sub-head">This drop hasn't launched yet.</div>
        <p class="soldout-sub">
          We make each product in <strong>small batches of 500</strong> to keep quality obsessive and waste minimal. Join the waitlist to get early access + a <strong>launch-day discount</strong>.
        </p>
        <div class="soldout-stats">
          <div class="soldout-stat">
            <div class="soldout-stat-num" id="soldout-waitlist-count">2,847</div>
            <div class="soldout-stat-label">On Waitlist</div>
          </div>
          <div class="soldout-stat">
            <div class="soldout-stat-num">500</div>
            <div class="soldout-stat-label">Per Batch</div>
          </div>
          <div class="soldout-stat">
            <div class="soldout-stat-num">50+</div>
            <div class="soldout-stat-label">Countries</div>
          </div>
        </div>
        <div class="soldout-email-form">
          <input type="email" class="soldout-email-input" id="soldout-email" placeholder="your@email.com" />
          <button class="soldout-notify-btn" id="soldout-notify-btn">Get Early Access</button>
        </div>
        <button class="soldout-close-btn" id="soldout-close">I'll check back later</button>
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(drawer);
    document.body.appendChild(toast);
    document.body.appendChild(soldoutOverlay);
  }

  // ═══════════════════════════════════════════════
  // CART STATE
  // ═══════════════════════════════════════════════
  function getCart() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
    catch { return []; }
  }

  function saveCart(cart) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    updateBadge(cart);
    renderDrawer(cart);
  }

  function addToCart(item) {
    const cart = getCart();
    const existing = cart.find(c => c.id === item.id && c.variant === item.variant);
    if (existing) {
      existing.qty += 1;
    } else {
      cart.push({ ...item, qty: 1 });
    }
    saveCart(cart);
    showToast(item);

    if (typeof fbq === 'function') {
      fbq('track', 'AddToCart', {
        content_name: item.name,
        content_type: 'product',
        value: item.price,
        currency: 'USD'
      });
    }
  }

  function removeFromCart(id, variant) {
    let cart = getCart();
    cart = cart.filter(c => !(c.id === id && c.variant === variant));
    saveCart(cart);
  }

  function updateQty(id, variant, delta) {
    const cart = getCart();
    const item = cart.find(c => c.id === id && c.variant === variant);
    if (!item) return;
    item.qty = Math.max(1, item.qty + delta);
    saveCart(cart);
  }

  function getSubtotal(cart) {
    return cart.reduce((sum, i) => sum + (i.price * i.qty), 0);
  }
  function getTotalItems(cart) {
    return cart.reduce((sum, i) => sum + i.qty, 0);
  }

  // ═══════════════════════════════════════════════
  // BADGE
  // ═══════════════════════════════════════════════
  function updateBadge(cart) {
    cart = cart || getCart();
    const total = getTotalItems(cart);
    document.querySelectorAll('.cart-count').forEach(el => {
      el.textContent = total;
      el.classList.toggle('has-items', total > 0);
    });
  }

  // ═══════════════════════════════════════════════
  // RENDER DRAWER
  // ═══════════════════════════════════════════════
  function renderDrawer(cart) {
    cart = cart || getCart();
    const itemsEl = document.getElementById('cart-drawer-items');
    const footerEl = document.getElementById('cart-drawer-footer');
    const countEl = document.getElementById('cart-drawer-count');
    const subtotalEl = document.getElementById('cart-subtotal-value');
    const shipBar = document.getElementById('cart-shipping-bar');
    const shipText = document.getElementById('cart-shipping-text');
    const shipFill = document.getElementById('cart-shipping-fill');
    const footerNote = document.getElementById('cart-footer-note');
    const savedTag = document.getElementById('cart-saved-tag');
    if (!itemsEl) return;

    const total = getTotalItems(cart);
    const subtotal = getSubtotal(cart);

    // Count badge in header
    if (total > 0) {
      countEl.style.display = 'inline';
      countEl.textContent = total;
    } else {
      countEl.style.display = 'none';
    }

    // Shipping progress bar
    if (total > 0) {
      shipBar.style.display = 'block';
      const pct = Math.min(100, (subtotal / FREE_SHIP_THRESHOLD) * 100);
      shipFill.style.width = pct + '%';
      if (subtotal >= FREE_SHIP_THRESHOLD) {
        shipText.innerHTML = '&#127881; <span>Free shipping unlocked!</span> Your order ships free.';
        shipFill.style.background = 'linear-gradient(90deg, #ccfd28, #16a34a)';
      } else {
        const remaining = FREE_SHIP_THRESHOLD - subtotal;
        shipText.innerHTML = 'Add <span>$' + remaining + ' more</span> for free shipping';
        shipFill.style.background = 'linear-gradient(90deg, #ff30cc, #ccfd28)';
      }
    } else {
      shipBar.style.display = 'none';
    }

    // Empty state
    if (cart.length === 0) {
      footerEl.style.display = 'none';
      itemsEl.innerHTML = `
        <div class="cart-empty">
          <div class="cart-empty-icon">&#127819;</div>
          <div class="cart-empty-title">Nothing here yet</div>
          <div class="cart-empty-sub">Each Nancy product is made in small batches of 500. When they're gone, they're gone until the next drop.</div>
          <button class="cart-empty-shop" onclick="document.getElementById('cart-overlay').click()">Start Exploring</button>
        </div>
      `;
      return;
    }

    footerEl.style.display = 'block';
    subtotalEl.textContent = '$' + subtotal;

    // Footer note — rotating scarcity + brand messages
    const notes = [
      '<strong>Small batch.</strong> We make 500 per run. When they sell out, the next batch takes 6-8 weeks.',
      '<strong>Designed in HK.</strong> Body-safe silicone. 1-year warranty. Discreet everything.',
      '<strong>500K+ happy customers</strong> across 50+ countries. Rated 4.8 stars.',
    ];
    footerNote.innerHTML = notes[Math.floor(Date.now() / 10000) % notes.length];

    // Saved amount
    savedTag.style.display = 'none'; // Savings displayed only if we track compareAt prices

    // Render items
    itemsEl.innerHTML = cart.map(item => {
      const stock = getStockLeft(item.id);
      const viewers = getViewers(item.id);
      return `
        <div class="cart-item" data-id="${item.id}" data-variant="${item.variant || ''}">
          <div class="cart-item-img">
            <img src="${item.image}" alt="${item.name}" onerror="this.parentElement.innerHTML='&#127819;'">
          </div>
          <div class="cart-item-details">
            <div class="cart-item-name">${item.name}</div>
            ${item.variant ? `<div class="cart-item-variant">${item.variant}</div>` : ''}
            <div class="cart-item-scarcity">Only ${stock} left &middot; ${viewers} people viewing</div>
            <div class="cart-item-price-row">
              <div class="cart-item-price">$${item.price}</div>
              <div class="cart-item-qty">
                <button class="cart-qty-minus" aria-label="Decrease">&minus;</button>
                <span>${item.qty}</span>
                <button class="cart-qty-plus" aria-label="Increase">+</button>
              </div>
            </div>
          </div>
          <button class="cart-item-remove" aria-label="Remove" title="Remove">&times;</button>
        </div>
      `;
    }).join('');

    // Bind qty / remove
    itemsEl.querySelectorAll('.cart-item').forEach(el => {
      const id = el.dataset.id;
      const variant = el.dataset.variant;
      el.querySelector('.cart-qty-minus').addEventListener('click', () => updateQty(id, variant, -1));
      el.querySelector('.cart-qty-plus').addEventListener('click', () => updateQty(id, variant, 1));
      el.querySelector('.cart-item-remove').addEventListener('click', () => removeFromCart(id, variant));
    });
  }

  // ═══════════════════════════════════════════════
  // OPEN / CLOSE DRAWER
  // ═══════════════════════════════════════════════
  function openDrawer() {
    renderDrawer();
    requestAnimationFrame(() => {
      document.getElementById('cart-overlay').classList.add('open');
      document.getElementById('cart-drawer').classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  }

  function closeDrawer() {
    document.getElementById('cart-overlay').classList.remove('open');
    document.getElementById('cart-drawer').classList.remove('open');
    document.body.style.overflow = '';
  }

  // ═══════════════════════════════════════════════
  // TOAST
  // ═══════════════════════════════════════════════
  let toastTimer;
  function showToast(item) {
    const toast = document.getElementById('cart-toast');
    const text = document.getElementById('cart-toast-text');
    if (!toast) return;
    const stock = getStockLeft(item.id);
    const line = randomToastLine();
    text.innerHTML = `<strong>${item.name}</strong> added<small>${line}Only ${stock} left in stock.</small>`;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
  }

  // ═══════════════════════════════════════════════
  // SOLD OUT MODAL
  // ═══════════════════════════════════════════════
  function showSoldOut() {
    const overlay = document.getElementById('soldout-overlay');
    if (!overlay) return;

    // Randomize waitlist count slightly
    const base = 2847;
    const jitter = Math.floor(Math.random() * 200);
    const countEl = document.getElementById('soldout-waitlist-count');
    if (countEl) countEl.textContent = (base + jitter).toLocaleString();

    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';

    if (typeof fbq === 'function') {
      fbq('track', 'InitiateCheckout', {
        content_type: 'product',
        value: getSubtotal(getCart()),
        currency: 'USD',
        num_items: getTotalItems(getCart())
      });
    }
  }

  function closeSoldOut() {
    const overlay = document.getElementById('soldout-overlay');
    if (!overlay) return;
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  // ═══════════════════════════════════════════════
  // EXTRACT PRODUCT DATA
  // ═══════════════════════════════════════════════
  function slugify(str) {
    return str.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  }

  function extractFromBsCard(card) {
    const name = card.querySelector('.bs-name')?.textContent?.trim() || 'Product';
    const priceStr = card.querySelector('.bs-current')?.textContent?.trim() || '$0';
    const price = parseInt(priceStr.replace(/[^0-9]/g, ''), 10) || 0;
    const img = card.querySelector('img')?.getAttribute('src') || '';
    return { id: slugify(name), name, price, image: img, variant: '' };
  }

  function extractFromCollectionCard(card) {
    const name = card.querySelector('h3')?.textContent?.trim() || 'Product';
    const priceStr = card.querySelector('.product-card-current')?.textContent?.trim() || '$0';
    const price = parseInt(priceStr.replace(/[^0-9]/g, ''), 10) || 0;
    const img = card.querySelector('img')?.getAttribute('src') || '';
    return { id: slugify(name), name, price, image: img, variant: '' };
  }

  function extractFromPDP() {
    const name = document.querySelector('.pdp-info h1')?.textContent?.trim() || 'Product';
    const priceStr = document.querySelector('.pdp-price-current')?.textContent?.trim() || '$0';
    const price = parseInt(priceStr.replace(/[^0-9]/g, ''), 10) || 0;
    const img = document.querySelector('#pdp-main-img')?.getAttribute('src') || '';
    const variant = document.getElementById('color-name')?.textContent?.trim() || '';
    return { id: slugify(name), name, price, image: img, variant };
  }

  // ═══════════════════════════════════════════════
  // INJECT QUICK-ADD BUTTONS
  // ═══════════════════════════════════════════════
  function injectQuickAddButtons() {
    document.querySelectorAll('.product-card').forEach(card => {
      if (card.querySelector('.quick-add-btn')) return;
      const imageWrap = card.querySelector('.product-card-image');
      if (!imageWrap) return;

      const btn = document.createElement('button');
      btn.className = 'quick-add-btn';
      btn.innerHTML = CART_ICON_SVG + ' Quick Add';
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const data = extractFromCollectionCard(card);
        addToCart(data);
        btn.classList.add('added');
        btn.innerHTML = '&#10003; Added!';
        setTimeout(() => {
          btn.classList.remove('added');
          btn.innerHTML = CART_ICON_SVG + ' Quick Add';
        }, 1500);
      });

      imageWrap.style.position = 'relative';
      imageWrap.style.overflow = 'hidden';
      imageWrap.appendChild(btn);
    });
  }

  // ═══════════════════════════════════════════════
  // BIND EXISTING BUTTONS
  // ═══════════════════════════════════════════════
  function bindExistingButtons() {
    // Homepage bestseller add-to-cart
    document.querySelectorAll('.bs-card .add-to-cart').forEach(btn => {
      if (btn.dataset.cartBound) return;
      btn.dataset.cartBound = 'true';
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const card = btn.closest('.bs-card');
        if (!card) return;
        const data = extractFromBsCard(card);
        addToCart(data);
        btn.classList.add('added');
        const orig = btn.innerHTML;
        btn.innerHTML = '&#10003; Added!';
        setTimeout(() => { btn.classList.remove('added'); btn.innerHTML = orig; }, 1500);
      });
    });

    // PDP add-to-cart
    document.querySelectorAll('.pdp-add-to-cart').forEach(btn => {
      if (btn.dataset.cartBound) return;
      btn.dataset.cartBound = 'true';
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const data = extractFromPDP();
        addToCart(data);
        btn.classList.add('added');
        const orig = btn.innerHTML;
        btn.innerHTML = '&#10003; Added to Cart!';
        setTimeout(() => { btn.classList.remove('added'); btn.innerHTML = orig; }, 2000);
      });
    });

    // Nav cart icon
    document.querySelectorAll('.nav-cart').forEach(el => {
      if (el.dataset.cartBound) return;
      el.dataset.cartBound = 'true';
      el.addEventListener('click', (e) => { e.preventDefault(); openDrawer(); });
    });
  }

  // ═══════════════════════════════════════════════
  // BIND DRAWER EVENTS
  // ═══════════════════════════════════════════════
  function bindDrawerEvents() {
    document.getElementById('cart-overlay')?.addEventListener('click', closeDrawer);
    document.getElementById('cart-drawer-close')?.addEventListener('click', closeDrawer);
    document.getElementById('cart-drawer')?.addEventListener('click', (e) => e.stopPropagation());

    // Checkout → sold out
    document.getElementById('cart-checkout-btn')?.addEventListener('click', function(e) {
      e.preventDefault();
      closeDrawer();
      setTimeout(showSoldOut, 350);
    });

    // Sold out modal
    document.getElementById('soldout-close')?.addEventListener('click', closeSoldOut);
    document.getElementById('soldout-overlay')?.addEventListener('click', function(e) {
      if (e.target === this) closeSoldOut();
    });

    // Notify email
    document.getElementById('soldout-notify-btn')?.addEventListener('click', function() {
      const email = document.getElementById('soldout-email')?.value?.trim();
      if (!email || !email.includes('@')) {
        const input = document.getElementById('soldout-email');
        input.style.borderColor = '#ff4b6e';
        input.setAttribute('placeholder', 'Enter a valid email');
        return;
      }

      if (typeof fbq === 'function') {
        fbq('track', 'Lead', { content_name: 'waitlist_signup' });
      }

      this.classList.add('submitted');
      this.textContent = "You're on the list!";
      setTimeout(closeSoldOut, 2200);
    });
  }

  // ═══════════════════════════════════════════════
  // INIT
  // ═══════════════════════════════════════════════
  function init() {
    injectDrawer();
    bindDrawerEvents();
    injectQuickAddButtons();
    bindExistingButtons();
    updateBadge();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(init, 300));
  } else {
    setTimeout(init, 300);
  }

  // Re-bind when includes.js loads nav
  const observer = new MutationObserver((mutations) => {
    for (const m of mutations) {
      for (const node of m.addedNodes) {
        if (node.nodeType === 1 && (node.tagName === 'NAV' || node.querySelector?.('nav'))) {
          bindExistingButtons();
          updateBadge();
        }
      }
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });

})();
