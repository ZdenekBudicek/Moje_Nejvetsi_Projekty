from typing import List, Tuple
import psycopg2
import time
import psycopg2.extras
from connection import get_connection


class Database:
    """
    Třída pro připojení k databázi a spouštění dotazů.
    """
    def __init__(self) -> None:
        self.conn = get_connection()
        self.db_cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.order_required = None
        self.column_names = []
        self.table_names = []
        self.storage_table_name = "Storage"
        self.customers_table_name = "Customers"
        self.orders_table_name = "Orders"
        self.employees_table_name = "Employees"

    def __del__(self) -> None:
        """
        Aktivuje se při ukončení programu, ukončuje připojení k databázi.
        """
        self.db_cursor.close()
        self.conn.close()

    def execute_query(self, query: str, parameters: Tuple = None) -> None:
        """
        Spustí zadaný dotaz na databázi a uloží změny.

        :param query: str, SQL dotaz
        :param parameters: tuple, volitelný argument s parametry dotazu
        """
        self.db_cursor.execute(query, parameters)
        self.conn.commit()

    def execute_query_select_one(self, query: str, parameters: Tuple = None) -> Tuple:
        """
        Spustí zadaný dotaz na databázi a vrátí první nalezený výsledek.

        :param query: str, SQL dotaz
        :param parameters: tuple, volitelný argument s parametry dotazu
        :return: tuple, první nalezený výsledek
        """
        self.db_cursor.execute(query, parameters)
        return self.db_cursor.fetchone()

    def delete_row(self, table_name: str, pk_value: int) -> None:
        """
        Maže jeden řádek v databázi

        :param table_name: Název tabulky zadaný uživatelem
        :param pk_value: Číslo privátního klíče zadaný uživatelem
        """
        pk_column_string = self.get_pk_column(table_name)
        success = False
        try:
            self.db_cursor.execute(f"DELETE FROM \"{table_name}\" WHERE \"{pk_column_string}\" = %s;", (pk_value,))
            self.conn.commit()
            success = True
        except psycopg2.errors.ForeignKeyViolation:
            self.conn.rollback()
            print("Tento záznam nelze smazat, jelikož je stále evidovaný v jiné tabulce.")
        if success:
            print("Záznam byl úspěšně odstraněn.")

    def check_column_password(self, max_length_of_columns: List[int]):
        """
        Kontroluje zda se v tabulce nachází sloupec password, pokud ano, smaže ho

        :param max_length_of_columns: Počet znaků v každěm sloupci na daném řádku
        :return None nebo index hesla
        """
        password_index = None
        try:
            password_index = self.column_names.index("password")
            self.column_names.pop(password_index)
            max_length_of_columns.pop(password_index)
        except ValueError:
            pass
        return password_index

    def print_table(self, table_data: List[List]) -> None:
        """
        Zobrazí tabulku, vypíše názvy sloupců a podtrhne je a zarovná sloupce podle počtu znaků.

        :param table_data: List s listy a každý list je jeden řádek v tabulce
        """
        max_length_of_columns = [len(column_name) for column_name in self.column_names]
        if self.order_required:
            self.column_names.append("Doplnit zboží")
            max_length_of_columns.append(len("Doplnit zboží"))
        password_index = self.check_column_password(max_length_of_columns)
        for row in table_data:
            if password_index is not None:
                row.pop(password_index)
            for i, item in enumerate(row):
                max_length_of_columns[i] = max(max_length_of_columns[i], len(str(item)))
        format_string = " | ".join(["{{:^{}}}".format(max_length) for max_length in max_length_of_columns])
        print(format_string.format(*self.column_names))
        print("-" * sum(max_length_of_columns) + "---" * (len(max_length_of_columns) - 1))
        for row in table_data:
            if self.order_required:
                row = list(row)
                row.append("")
                row[-1] = 'Doplň zboží' if int(row[3]) <= 10 else '✔' if row[3] else "Záznam nenalezen"
            print(format_string.format(*[str(item).center(max_length_of_columns[i]) for i, item in enumerate(row)]))

    def get_pk_column(self, table_name: str) -> str:
        """
        Získá název privátního klíče z dané tabulky

        :param table_name: Název tabulky
        :return: Název sloupce který je PK
        """
        self.db_cursor.execute(f'SELECT column_name '
                               f'FROM information_schema.key_column_usage '
                               f'WHERE constraint_name = \'{table_name}_pkey\' AND table_name = \'{table_name}\';')
        pk_column = self.db_cursor.fetchall()
        return pk_column[0][0]

    def display_money_to_pay(self, table_name: str) -> List:
        """
        Zobrazí tabulku s Customer_id, Cutomer_name, Date_of_order, Pay - je celkévá částka k zaplacení

        :param table_name: Název tabulky
        :return: Data z tabulky, list a v něm listy a datum je v tuple
        """
        self.order_required = True if table_name == self.storage_table_name else False
        self.column_names = []
        self.db_cursor.execute(
            f'SELECT subquery."Customer_id", subquery."Customer_name", subquery."Date_of_order", SUM(subquery."Final_price") AS "Pay" '
            f'FROM ('
            f'  SELECT "{self.orders_table_name}"."Order_id", "{self.orders_table_name}"."Date_of_order", '
            f'    "{self.customers_table_name}"."Customer_id", "{self.customers_table_name}"."Customer_name", '
            f'    "{self.storage_table_name}"."Price (Kč)" * "{self.orders_table_name}"."Quantity" AS "Final_price" '
            f'  FROM "{self.orders_table_name}" '
            f'  JOIN "{self.customers_table_name}" ON "{self.orders_table_name}"."Customer_id" = "{self.customers_table_name}"."Customer_id" '
            f'  JOIN "{self.storage_table_name}" ON "{self.orders_table_name}"."Item_id" = "{self.storage_table_name}"."Item_id" '
            f') AS subquery '
            f'GROUP BY subquery."Customer_id", subquery."Date_of_order", subquery."Customer_name" '
            f'ORDER BY subquery."Date_of_order";'
        )
        table_data = self.db_cursor.fetchall()
        if not table_data:
            print("Žádná data nebyla nalezena.\n")
        self.column_names = [desc[0] for desc in self.db_cursor.description]
        return table_data

    def display_orders(self, table_name: str) -> List:
        """
        Získá data pro zobrazení tabulky Orders a napojí se i do ostatních tabulek a vypíše data z nich místo čísel

        :param table_name: Název tabulky
        :return: Data z tabulky, list a v něm listy a datum je v tuple
        """
        pk_column_string = self.get_pk_column(table_name)
        self.column_names = []
        self.order_required = True if table_name == self.storage_table_name else False
        self.db_cursor.execute(
            f'SELECT "{self.orders_table_name}"."Order_id", "{self.orders_table_name}"."Date_of_order", '
            f'"{self.customers_table_name}"."Customer_name", "{self.storage_table_name}"."Item", '
            f'"{self.orders_table_name}"."Quantity"'
            f'FROM "{self.orders_table_name}" '
            f'JOIN "{self.customers_table_name}" ON "{self.orders_table_name}"."Customer_id" = "{self.customers_table_name}"."Customer_id" '
            f'JOIN "{self.storage_table_name}" ON "{self.orders_table_name}"."Item_id" = "{self.storage_table_name}"."Item_id" '
            f'ORDER BY "{pk_column_string}" ASC;'
        )
        table_data = self.db_cursor.fetchall()
        if not table_data:
            print("Žádná data nebyla nalezena.\n")
        self.column_names = [desc[0] for desc in self.db_cursor.description]
        return table_data

    def display_table(self, table_name: str) -> List:
        """
        Získá data pro zobrazení tabulky

        :param table_name: Název tabulky
        :return: Data z tabulky, list a v něm listy a datum je v tuple
        """
        self.order_required = True if table_name == self.storage_table_name else False
        pk_column_string = self.get_pk_column(table_name)
        self.column_names = []
        self.db_cursor.execute(f'SELECT * FROM "{table_name}" ORDER BY "{pk_column_string}" ASC;')
        table_data = self.db_cursor.fetchall()
        if not table_data:
            print("Žádná data nebyla nalezena.\n")
        self.column_names = [desc[0] for desc in self.db_cursor.description]
        return table_data

    def show_table_names(self) -> List[str]:
        """
        Získá názvy tabulek v databázi

        :return: Názvy tabulek v databázi
        """
        self.table_names = []
        self.db_cursor.execute(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE';
            """
        )
        table_data = self.db_cursor.fetchall()
        for table in table_data:
            self.table_names.append(table[0])
        return self.table_names

    def add_order(self) -> None:
        """
        Přidá objednávku do databáze a ptá se jestli má zákazník více zboží,
        pokud ano, vloží se stejné customer_id a ptá se už jen na zboží a jeho množství
        """
        input_text = "Zadejte ID zákazníka: "
        error = "Špatný vstup, zadal si číslo mimo rozsah tabulky."
        print("Přidání objednávky")
        order_date = time.strftime('%Y-%m-%d')
        customer_id = self.valid_input_in_database(self.customers_table_name, input_text, error)
        while True:
            input_text = "Zadejte ID produktu: "
            product_id = self.valid_input_in_database(self.storage_table_name, input_text, error)
            quantity = self.valid_quantity(product_id)
            self.execute_query(
                f"""INSERT INTO "{self.orders_table_name}" ("Date_of_order", "Customer_id", "Item_id", "Quantity")
                VALUES (%s, %s, %s, %s);""",
                (order_date, customer_id, product_id, quantity)
            )
            self.execute_query(
                f'UPDATE "{self.storage_table_name}" SET "Quantity" = "Quantity" - {quantity} WHERE "Item_id"={product_id}')
            print("Objednávka byla úspěšně přidána.")
            if not self.cli.continue_in_order_loop():
                return None

    def table_name(self) -> str:
        """
        Uživatel zadá název tabulky, následně se zkontroluje zda je v databázi

        :return: Název tabulky zadaný uživatelem
        """
        while True:
            table_names = self.show_table_names()
            self.db_cursor.execute(
                'SELECT can_add_employees FROM "Employees" WHERE id = %s',
                (self.cli.user_id,))
            permission = self.db_cursor.fetchone()
            if not permission[0]:
                table_names.remove("Employees")
            print(" | ".join(table_names))
            input_table = input("Zadejte název tabulky kterou chcete upravit: ").capitalize()
            for one_table in table_names:
                if one_table == input_table:
                    break
            else:
                print("Špatně zadaný název tabulky, zkus to znovu.")
                continue
            break
        return input_table

    def add_employee(self) -> None:
        """
        Přidá zaměstnance do tabulky Employees
        """
        name = input("Zadejte jméno zaměstnance: ")
        role = input("Zadejte roli zaměstnance: ")
        username = input("Zadejte přihlašovací jméno zaměstnance: ")
        permissions = {}
        for permission in ["přidávat_záznamy", "mazat_záznamy", "upravovat_záznamy", "přidávat_zaměstnance"]:
            while True:
                value = input(f"Může zaměstnanec {permission.replace('_', ' ')}? (True/False): ").capitalize()
                if value == "True":
                    permissions[permission] = value
                    break
                elif value == "False":
                    permissions[permission] = value
                    break
                else:
                    print("Zadejte platnou hodnotu (True/False).")
        query = f'INSERT INTO "{self.employees_table_name}" (name, role, username, can_add, can_delete, can_edit, can_add_employees) ' \
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        parameters = (name, role, username, permissions['přidávat_záznamy'], permissions['mazat_záznamy'],
                      permissions['upravovat_záznamy'], permissions['přidávat_zaměstnance'])
        self.execute_query(query, parameters)

        print(f"Zaměstnanec byl úspěšně přidán do tabulky {self.employees_table_name}.")

    def change_text_or_stay_default(self, column_pk: str, row: List, input_table: str, row_id_input: int) -> None:
        """
        Mění postupně jeden řádek v tabulce, pokud uživatel nechá prázdný vstup, napíše se hodnota z databáze

        :param column_pk: Název sloupce který je PK
        :param row: List ve kterém je řádek z tabulky
        :param input_table: Název tabulky zadaný uživatelem
        :param row_id_input: Číslo řádku který chce uživatel upravit
        """
        column_names = [desc[0] for desc in self.db_cursor.description]
        column_names.remove(column_pk)
        try:
            column_names.remove("password")
        except ValueError:
            pass
        row = row[:0] + row[1:]
        row_dict = dict(zip(column_names, row))
        for column_name in column_names:
            new_value = input(
                f"Vložte text do sloupce {column_name} (Pokud hodnotu ve sloupci chcete zachovat, stisknete ENTER):\n")
            if not new_value:
                new_value = (row_dict[column_name])
            try:
                query = f"""UPDATE "{input_table}"
                                    SET "{column_name}" = %s
                                    WHERE "{column_pk}" = %s;"""
                parameters = (new_value, row_id_input)
                self.execute_query(query, parameters)
            except psycopg2.errors.InvalidTextRepresentation:
                print("Chyba: Neplatná hodnota!")
                self.conn.rollback()
                break

            print(f"Hodnota ve sloupci: {column_name} byla úspěšně změněna na: {new_value}.")

    def valid_quantity(self, product_id: int) -> int:
        """
        Kontroluje zda je na skladě dostatek kusů pro objednávku

        :param product_id: Číslo produktu v databázi PK
        :return: Počet kusů zadaný uživatelem
        """
        while True:
            while True:
                quantity = self.cli.get_valid_input_int("Zadejte množství: ")
                if quantity > 0:
                    break
            storage_quantity = \
                self.execute_query_select_one(
                    f'SELECT "Quantity" FROM "{self.storage_table_name}" WHERE "Item_id"={product_id};')[0]
            if quantity <= storage_quantity:
                break
            else:
                self.conn.rollback()
                print("Nedostatečný počet kusů na skladě.")
                continue
        return quantity

    def returns_items_to_storage(self, input_table: str, row_id_input: int) -> None:
        """
        Pokud uživatel smaže objednávku, tak se zboží doplní zpět na sklad

        :param input_table: Název tabulky
        :param row_id_input: Číslo řádku
        """
        orders_row = self.execute_query_select_one(
            f'SELECT * FROM "{input_table}" WHERE "Order_id"={row_id_input};')
        orders_quantity = orders_row[4]
        orders_item_id = orders_row[3]
        storage_quantity = self.execute_query_select_one(
            f'SELECT * FROM "{self.storage_table_name}" WHERE "Item_id"={orders_item_id};')[3]
        self.execute_query(
            f'UPDATE "{self.storage_table_name}" SET "Quantity" = {storage_quantity} + {orders_quantity} WHERE "Item_id"={orders_item_id}'
        )

    def valid_input_in_database(self, table, input_text, error) -> int:
        """
        Kontroluje zda se vstup od uživatele nachází v databázi

        :param table: Název tabulky
        :param input_text: Text pro dotaz na uživatele
        :param error: Chybová hláška
        :return: Číslo řádku které se nachází v databázi PK
        """
        self.db_cursor.execute(f'SELECT * FROM "{table}"')
        table_data = self.db_cursor.fetchall()
        while True:
            valid_input = self.cli.get_valid_input_int(input_text)
            for one_row in table_data:
                if valid_input == one_row[0]:
                    break
            else:
                print(error)
                continue
            break
        return valid_input

    def add_item_to_storage(self) -> None:
        """
        Přidá zboží do databáze
        """
        item_name = input("Zadejte název zboží: ")
        item_price = self.cli.get_valid_input_int("Zadejte cenu zboží: ")
        item_quantity = self.cli.get_valid_input_int("Zadejte množství zboží: ")
        self.execute_query(
            f"""INSERT INTO "{self.storage_table_name}" ("Item", "Price (Kč)", "Quantity") VALUES (%s, %s, %s);""",
            (item_name, item_price, item_quantity),
        )
        print(f"Zboží {item_name} bylo úspěšně přidáno.")

    def add_customer(self) -> None:
        """
        Přidá zákazníka do databáze
        """
        customer_name = input("Zadejte jméno zákazníka: ")
        customer_addres = input("Zadejte adresu zákazníka: ")
        customer_phone = self.cli.get_valid_input_int("Zadejte telefonní číslo zákazníka: ")
        self.execute_query(
            f"""INSERT INTO "{self.customers_table_name}" ("Customer_name", "Customer_address", "Customer_phone_number") VALUES (%s, %s, %s);""",
            (customer_name, customer_addres, customer_phone),
        )
        print(f"Zákazník {customer_name} byl úspěšně přidán.")

    def update_table_row(self) -> None:
        """
        Upraví řáděk v databázi, pokud uživatel nechá prázdný vstup zapíše se hodnota z databáze
        """
        input_text = "Vložte číslo řádku, který chcete upravit: "
        error = "Špatný vstup, zadal si číslo mimo rozsah tabulky."
        input_table = self.table_name()
        column_pk = self.get_pk_column(input_table)
        table_data = self.display_table(input_table)
        self.order_required = False
        self.cli.show_table(table_data)
        row_id_input = self.valid_input_in_database(input_table, input_text, error)
        row = self.execute_query_select_one(
            f'SELECT * FROM "{input_table}" WHERE "{column_pk}" = {row_id_input};')
        if row:
            if input_table == "Employees":
                row = row[:4] + row[5:]
            self.print_table([row])
        self.change_text_or_stay_default(column_pk, row, input_table, row_id_input)

    def delete_from_table(self) -> None:
        """
        Ptá se uživatele s jakou tabulkou chce pracovat a ověřuje vstupy, pokud je vybrána tabulka Orders vrátí kusy na sklad
        """
        input_text = "Zadejte číslo řádku, který chcete smazat: "
        error = "Špatný vstup, zadal si číslo mimo rozsah tabulky."
        input_table = self.table_name()
        table_data = self.display_table(input_table)
        self.order_required = False
        self.cli.show_table(table_data)
        row_id_input = self.valid_input_in_database(input_table, input_text, error)
        if input_table == self.orders_table_name:
            self.returns_items_to_storage(input_table, row_id_input)
        self.delete_row(input_table, row_id_input)
