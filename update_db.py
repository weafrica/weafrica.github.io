import sqlite3

DATABASE = 'final_project.db'

def add_image_url_column():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE products ADD COLUMN image_url TEXT")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_image_url_column()
    print("Added image_url column to products table.")
