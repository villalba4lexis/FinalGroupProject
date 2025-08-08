# reset_db.py
from .models import model_loader

if __name__ == "__main__":
    print("Resetting database...")
    model_loader.reset_database()
    print("Database reset complete.")


#pytest tests/test_sandwiches.py
#python -m api.reset_db
