import psycopg2.extras
import Handler.create_tables
from connection import get_connection
from client import CLI
from control_database import Database

db = Database()
cli = CLI(db)

# vložení instance třídy CLI do instance třídy Database
db.cli = cli

conn = get_connection()
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

table_names = [db.storage_table_name, db.customers_table_name, db.orders_table_name, db.employees_table_name]
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [table[0] for table in cursor.fetchall()]

for table_name in table_names:
    if table_name not in tables:
        if table_name == db.storage_table_name:
            Handler.create_tables.create_storage()

        elif table_name == db.customers_table_name:
            Handler.create_tables.create_customers()

        elif table_name == db.orders_table_name:
            Handler.create_tables.create_orders()

        elif table_name == db.employees_table_name:
            Handler.create_tables.create_employees()

if __name__ == "__main__":
    try:
        cli.login()
        cli.display_menu()
    except IndexError:
        print("Nastala neočekávaná chyba, pravděpodobně se tabulka nenachází v databázi.")
