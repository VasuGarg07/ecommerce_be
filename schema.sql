CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'CUSTOMER',
    CONSTRAINT chk_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_phone CHECK (phone ~ '^\+?[0-9\s\-\(\)]{7,20}$'),
    CONSTRAINT chk_role CHECK (role IN ('CUSTOMER', 'STORE'))
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    image_url TEXT,
    description TEXT,
    price NUMERIC(12, 2) NOT NULL DEFAULT 0,
    quantity_available INTEGER NOT NULL DEFAULT 0,
    quantity_reserved INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    store_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    order_status VARCHAR(20) DEFAULT 'PLACED',
    order_value NUMERIC(16, 2) NOT NULL DEFAULT 0,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deliver_date TIMESTAMP DEFAULT NULL,
    return_date TIMESTAMP DEFAULT NULL,
    CONSTRAINT chk_order_status CHECK (order_status IN ('PLACED', 'DELIVERED', 'CANCELLED', 'RETURNED'))
);

CREATE TABLE IF NOT EXISTS orders_products (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 0,
    unit_value NUMERIC(12, 2) NOT NULL DEFAULT 0
);