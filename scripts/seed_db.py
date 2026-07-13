"""Initialise la base et crée les tables."""
from app.db.session import init_db

if __name__ == "__main__":
    init_db()
    print("Base de données initialisée.")