import os
import sys
import hashlib
import time
from typing import List, Dict


class CLI:
    """
    Třída pro interakci s uživatelem a zobrazování dat.
    """
    def __init__(self, database) -> None:
        self.order_required = False
        self.database = database
        self.db_cursor = self.database.db_cursor
        self.storage_table_name = self.database.storage_table_name
        self.customers_table_name = self.database.customers_table_name
        self.orders_table_name = self.database.orders_table_name
        self.employees_table_name = self.database.employees_table_name
        self.password = None
        self.user_id = None

    def login(self) -> None:
        """
        Přihlášení do aplikace, řeší přihlašovací jméno.
        """
        pk_column_string = self.database.get_pk_column(self.employees_table_name)
        self.db_cursor.execute(f'SELECT * FROM "{self.employees_table_name}" ORDER BY "{pk_column_string}" ASC;')
        table_data = self.db_cursor.fetchall()
        while True:
            input_username = input("Zadejte své uživatelské jméno: ")
            for one_row in table_data:
                if input_username == one_row[3]:
                    self.user_id = one_row[0]
                    break
            else:
                print("Zadal jsi špatné uživatelské jméno, zkus to znovu.")
                time.sleep(2)
                os.system('cls')
                continue
            break
        self.password_checker(table_data, input_username)

    def choose_password(self, more_save: bytes, input_username: str) -> None:
        """
        Uživatel si volí heslo

        :param more_save: Slouží k většímu zabezpečení šifrování
        :param input_username: Uživatelské jméno
        :return:
        """
        while True:
            input_new_password = str(input("Zvolte si své heslo: "))
            if len(input_new_password) >= 5:
                hashed_input_password = hashlib.pbkdf2_hmac('sha256', input_new_password.encode('utf-8'),
                                                            more_save, 100000)
                self.database.execute_query(
                    f'UPDATE "{self.employees_table_name}" SET password = %s WHERE username = %s',
                    (hashed_input_password.hex(), input_username)
                )
                break
            else:
                print("Zvolil sis příliš krátké heslo.")

    def input_password(self, more_save: bytes):
        """
        Uživatel zadá heslo které se následně porovnáva s heslem v databázi

        :param more_save: Slouží k většímu zabezpečení šifrování
        """
        while True:
            input_password = input("Zadejte heslo: ")
            hashed_input_password_hex = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), more_save,
                                                            100000).hex()
            if hashed_input_password_hex == self.password.hex():
                print("\nProbíhá přihlášení!")
                time.sleep(2)
                os.system('cls')
                break
            else:
                print("Heslo je špatně, zkuste to znovu!")

    def password_checker(self, table_data: List, input_username: str) -> None:
        """
        Přihlášení do aplikace, řeší přihlašovací heslo. Pokud uživatel žádné heslo nemá, nechá si ho zvolit.
        Heslo šifruje a porovnává zašifrované heslo v databázi s přihlašovacím heslem.

        :param table_data: Data z tabulky
        :param input_username: Uživatelské jméno
        """
        more_save = b'random_string'
        for one_row in table_data:
            if input_username == one_row[3]:
                if one_row[4] is not None:
                    self.password = bytes.fromhex(one_row[4])
                else:
                    self.password = one_row[4]
                break
        if self.password is None:
            self.choose_password(more_save, input_username)
        else:
            self.input_password(more_save)

    def default_menu_option(self) -> Dict:
        """Dictionary možností s hlavním menu a podmenu a k ním přiřazené funkce a pravomoce

        :return: Dictionary možností menu
        """
        menu_options = {
            1: {
                "title": "Sklad",
                "submenu": {
                    1: {
                        "title": "Zobrazit seznam zboží",
                        "function": self.database.display_table,
                        "table": self.storage_table_name
                    },
                    2: {
                        "title": "Přidat zboží na sklad",
                        "function": self.database.add_item_to_storage,
                        "permission": "add"
                    },
                    3: {
                        "title": "Zpět",
                        "function": self.return_to_main_menu
                    }
                }
            },
            2: {
                "title": "Zákazníci",
                "submenu": {
                    1: {
                        "title": "Zobrazit seznam zákazníků",
                        "function": self.database.display_table,
                        "table": self.customers_table_name
                    },
                    2: {
                        "title": "Přidat nového zákazníka",
                        "function": self.database.add_customer,
                        "permission": "add"
                    },
                    3: {
                        "title": "Zpět",
                        "function": self.return_to_main_menu
                    }
                }
            },
            3: {
                "title": "Objednávky",
                "submenu": {
                    1: {
                        "title": "Zobrazit seznam objednávek",
                        "function": self.database.display_orders,
                        "table": self.orders_table_name
                    },
                    2: {
                        "title": "Zobrazit sumy k zaplacení",
                        "function": self.database.display_money_to_pay,
                        "table": self.orders_table_name
                    },
                    3: {
                        "title": "Přidat objednávku",
                        "function": self.database.add_order,
                        "permission": "add"
                    },
                    4: {
                        "title": "Zpět",
                        "function": self.return_to_main_menu
                    }
                }
            },
            4: {
                "title": "Zaměstnanci",
                "submenu": {
                    1: {
                        "title": "Zobrazit seznam zaměstnanců",
                        "function": self.database.display_table,
                        "table": self.employees_table_name
                    },
                    2: {
                        "title": "Přidat nového zaměstnance",
                        "function": self.database.add_employee,
                        "permission": "add_employees"
                    },
                    3: {
                        "title": "Zpět",
                        "function": self.return_to_main_menu
                    }
                }
            },
            5: {
                "title": "Upravit/Smazat",
                "submenu": {
                    1: {
                        "title": "Upravit pole v tabulce",
                        "function": self.database.update_table_row,
                        "permission": "edit"
                    },
                    2: {
                        "title": "Smazat záznam z tabulky",
                        "function": self.database.delete_from_table,
                        "permission": "delete"
                    },
                    3: {
                        "title": "Zpět",
                        "function": self.return_to_main_menu
                    }
                }
            },
            6: {
                "title": "Konec",
                "function": self.exit_application
            }
        }

        return menu_options

    def return_to_main_menu(self) -> None:
        """
        Vyčistí obrazovku a zavolá znova hlavní menu
        """
        os.system('cls')
        self.display_menu()

    @staticmethod
    def get_valid_input_int(prompt: str) -> int:
        """
        Zajistí aby uživatel zadal správný číselný input.

        :return: validní input od uživatele
        """
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Neplatný vstup, zkuste to znovu.")

    def end_or_repeat(self) -> bool:
        """
        Ptá se uživatele jestli se chce vrátit do hlavní nabídky po nějaké akci.

        :return: boolean vrátí do menu nebo ukončí program
        """
        while True:
            end_or_again = input("Chcete zpět do menu? Ano/Ne\n").lower()
            if end_or_again in ["ano", "a", "yes", "y"]:
                os.system('cls')
                return True
            elif end_or_again in ["ne", "n", "no"]:
                del self.database
                return False
            else:
                print("Špatný vstup, zkus to znovu.")

    def show_table(self, table_data: List) -> None:
        """
        Ptá se uživatele zda chce zobrazit tabulku
        """
        show_table = input("Chcete zobrazit tabulku? Ano/Ne\n").lower()
        if show_table in ["ano", "a", "yes", "y"]:
            self.database.print_table(table_data)
        elif show_table in ["ne", "n", "no"]:
            pass
        else:
            print("Špatně zadaný vstup")

    @staticmethod
    def continue_in_order_loop() -> bool:
        """
        Ptá se zda chce uživatel vložit další zboží na stejného zákazníka

        :return: boolean
        """
        while True:
            add_another_order = input("Chcete vložit další objednávku pro stejného zákazníka? (ano/ne): ")
            if add_another_order.lower() == "ano":
                return True
            elif add_another_order.lower() == "ne":
                return False
            print("Neplatná odpověď, zadejte prosím 'ano' nebo 'ne'")

    @staticmethod
    def exit_application():
        """
        Ukončí aplikaci při odchodu z hlavní nabídky
        """
        print("Děkujeme za použití aplikace!")
        time.sleep(2)
        os.system('cls')
        sys.exit(0)

    def has_permission(self, action: str) -> bool:
        """
        Kontroluje, zda má zaměstnanec s daným ID oprávnění k provedení dané akce

        :param action: Pravomoc potřebná k vykonání dané operace
        :return: Vrací boolean z databáze který zjišťuje zda zaměstnanec tuto pravomoc má
        """
        self.db_cursor.execute(
            'SELECT can_add, can_delete, can_edit, can_add_employees FROM "Employees" WHERE id = %s',
            (self.user_id,))
        permissions = self.db_cursor.fetchone()
        if action == "add":
            return permissions[0]
        elif action == "delete":
            return permissions[1]
        elif action == "edit":
            return permissions[2]
        elif action == "add_employees":
            return permissions[3]
        else:
            return False

    def print_main_menu(self) -> None:
        """
        Vypisuje hlavní menu
        """
        print("Hlavní menu:\n")
        for key, option in self.default_menu_option().items():
            if option['title'] == "Konec":
                print()
            print(f"{key}: {option['title']}")
        print()

    @staticmethod
    def print_submenu(submenu_options) -> None:
        """
        Vypisuje podmenu
        :param submenu_options: Podmožnosti z hlavní nabídky, vybrané uživatelem
        """
        print("Vedlejší menu:\n")
        for key, option in submenu_options.items():
            if option['title'] == "Zpět":
                print()
            print(f"{key}: {option['title']}")
        print()

    def submenu_options(self, option: Dict) -> None:
        """
        Možnosti podmenu
        :param option: Dictionary s výběrem z hlavního menu a obsahuje další Dictionary s podmožnostmi
        """
        while True:
            self.print_submenu(option["submenu"])
            submenu_choice = self.get_valid_input_int("Vyberte volbu z podmenu: ")
            if submenu_choice in option["submenu"]:
                if "permission" in option["submenu"][submenu_choice]:
                    if not self.has_permission(option["submenu"][submenu_choice]["permission"]):
                        print("\nNemáte oprávnění pro tuto akci.")
                        time.sleep(2)
                        os.system('cls')
                        continue
                if "table" in option["submenu"][submenu_choice]:
                    table_data = option["submenu"][submenu_choice]["function"](
                        option["submenu"][submenu_choice]["table"])
                    self.database.print_table(table_data)
                else:
                    option["submenu"][submenu_choice]["function"]()
                break
            else:
                print("Neplatná volba. Zkuste to prosím znovu.")
                time.sleep(2)
                os.system('cls')
                continue

    def display_menu(self) -> None:
        """
        Základní komponent aplikace, řídí hlavní menu
        """
        while True:
            print("Vítejte v aplikaci pro správu obchodu.\n")
            self.print_main_menu()
            choice = self.get_valid_input_int("\nJaké kroky chcete provést? (Vyberte číslem)\n")
            menu_options = self.default_menu_option()
            if choice in menu_options:
                option = menu_options[choice]
                if "submenu" in option:
                    self.submenu_options(option)
                else:
                    option["function"]()

                if not self.end_or_repeat():
                    break
            else:
                print("Neplatná volba. Zkuste to prosím znovu.")
                time.sleep(2)
                os.system('cls')
                continue
