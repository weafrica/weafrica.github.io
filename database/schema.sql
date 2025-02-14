CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT,  -- Column to save the image filename
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
