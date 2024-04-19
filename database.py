import sqlite3

import debug
import config as cfg

class DatabaseConnection:
    def __init__(self):
        self.conn = sqlite3.connect(cfg.dbname)
        self.db = self.conn.cursor()
        debug.msg("Connected to the database successfully.")

    def __enter__(self):
        try:
            if not self.db_check():
                debug.error("Database table does not exist. Creating...")
                self.db.execute(f"CREATE TABLE {cfg.table_name} ({cfg.fields})")
                self.conn.commit()
                debug.msg("Database table created successfully.")
        except sqlite3.Error as e:
            debug.error(f"Error connecting to database: {e}")
        return self

    def db_check(self):
        try:
            self.db.execute(f"SELECT * FROM {cfg.table_name}")
            debug.msg("Database table exists.")
            return True
        except sqlite3.Error as e:
            debug.error(f"Error checking database table: {e}")
            return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            debug.msg("Closed the database connection successfully.")
        
    def get_posts(self, query=None):
        base_query = f"SELECT * FROM {cfg.table_name}"
        order_by = "ORDER BY created_at"
        search_condition = f"WHERE full_text LIKE '%{query}%'" if query else ""
        archive_condition = "WHERE is_archived = 0" if not cfg.show_archived else ""
    
        if search_condition and archive_condition:
            # Both conditions are present
            conditions = f"{search_condition} AND is_archived = 0"
        elif search_condition or archive_condition:
            # Only one condition is present
            conditions = search_condition or archive_condition
        else:
            # No conditions are present
            conditions = ""
    
        final_query = f"{base_query} {conditions} {order_by}"
    
        try:
            debug.msg(f"Fetching posts via query: {final_query}")
            self.db.execute(final_query)
            return self.db.fetchall()
        except sqlite3.Error as e:
            debug.error(f"Error executing SQL query: {e}")
            return []