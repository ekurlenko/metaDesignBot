class BaseRepository():
    def __init__(self):
        from dataBase.config import db as default_db
        self.db = default_db

    def __enter__(self):
        if self.db.is_closed():
            self.db.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.db.is_closed():
            self.db.close()
        return False
