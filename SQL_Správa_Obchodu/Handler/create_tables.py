import psycopg2.extras
from connection import get_connection

conn = get_connection()
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def create_storage():
    """
    Tvoří tabulku Storage a plní jí hodnotami
    """
    cursor.execute(
        """
    DROP TABLE IF EXISTS "Storage" CASCADE;
    CREATE TABLE "Storage"(
        "Item_id" SERIAL PRIMARY KEY,
        "Item" VARCHAR(100),
        "Price (Kč)" INT,
        "Quantity" INT
    );
    INSERT INTO "Storage" ("Item", "Price (Kč)", "Quantity")
    VALUES 
    ('Notebook HP Pavilion', 23990, '10'),
    ('Tablet Samsung Galaxy Tab A7', 6290, '15'),
    ('Televize LG OLED55C15LB', 55990, '5'),
    ('Mobilní telefon Xiaomi Redmi Note 11 Pro', 9990, '20'),
    ('Sluchátka Sony WH-1000XM4', 9990, '10'),
    ('Herní konzole Xbox Series X', 21990, '5'),
    ('Digitální fotoaparát Canon EOS 90D', 42990, '5'),
    ('Voděodolný reproduktor JBL Flip 5', 2290, '25'),
    ('Routery TP-Link Archer AX6000', 7190, '10'),
    ('Herní myš Logitech G Pro', 2690, '20'),
    ('Grafická karta NVIDIA GeForce RTX 3080', 38990, '5'),
    ('Nabíječka Anker PowerCore+ 26800 mAh', 2690, '20'),
    ('Monitor Samsung Odyssey G9', 39990, '3'),
    ('Klávesnice Corsair K70 RGB MK.2', 2790, '15'),
    ('Mikrofon Blue Yeti', 3490, '10'),
    ('Ovladač Xbox Wireless Controller', 1790, '30'),
    ('Interní pevný disk Seagate Barracuda 3TB', 2990, '10'),
    ('Televize Samsung', 15999, '10'),
    ('Notebook Dell', 24999, '5'),
    ('Mobilní telefon iPhone', 29999, '15'),
    ('Sluchátka Bose', 5999, '20'),
    ('Konzole Playstation 5', 35999, '8'),
    ('Razer Blade 15 Advanced', 59990, '5'),
    ('Tablet Apple iPad Air', 14990, '12'),
    ('Televize Sony Bravia', 46990, '6'),
    ('Mobilní telefon Samsung Galaxy S22', 15990, '25'),
    ('Sluchátka Sennheiser Momentum 3 Wireless', 8990, '8'),
    ('Herní konzole Nintendo Switch OLED', 14990, '10'),
    ('Digitální fotoaparát Nikon Z6 II', 52990, '3'),
    ('Voděodolný reproduktor Ultimate Ears Megaboom 3', 3990, '20'),
    ('Routery Asus RT-AX86U', 5490, '8'),
    ('Herní myš Razer DeathAdder Elite', 1590, '15'),
    ('Grafická karta AMD Radeon RX 6800 XT', 31990, '5'),
    ('Nabíječka Belkin Boost Charge Pro 10W', 1490, '30'),
    ('Monitor LG UltraGear 27GN950-B', 20990, '5'),
    ('Klávesnice Logitech G915 TKL', 4990, '10'),
    ('Mikrofon Rode NT1-A', 3990, '8'),
    ('Ovladač Sony DualSense Wireless Controller', 2290, '25'),
    ('Interní pevný disk Western Digital Black SN850 1TB', 8490, '15'),
    ('Televize Philips', 10999, '10'),
    ('Notebook Lenovo ThinkPad X1 Carbon', 39990, '5'),
    ('Mobilní telefon Google Pixel 6 Pro', 25990, '12'),
    ('Sluchátka Beats Studio Buds', 4990, '15'),
    ('Konzole Xbox Series S', 12990, '8'),
    ('Notebook Asus ROG Strix G15', 32990, '5'),
    ('Tablet Huawei MatePad Pro', 9990, '10'),
    ('Televize TCL 6 Series', 15990, '8'),
    ('Mobilní telefon OnePlus 10 Pro', 25990, '15'),
    ('Sluchátka Jabra Elite 85t', 6990, '12'),
    ('Herní konzole Sony PlayStation 4 Pro', 8490, '10'),
    ('Digitální fotoaparát Sony Alpha 7 III', 77990, '3'),
    ('Voděodolný reproduktor Bose SoundLink Revolve', 4990, '18'),
    ('Routery D-Link DIR-X5460', 3290, '10'),
    ('Herní myš SteelSeries Rival 600', 1690, '20'),
    ('Grafická karta AMD Radeon RX 6900 XT', 48990, '5');
        """
    )

    conn.commit()


def create_customers():
    """
    Tvoří tabulku Customers a plní jí hodnotami
    """
    cursor.execute(
        """
        DROP TABLE IF EXISTS "Customers" CASCADE;
        CREATE TABLE "Customers"(
            "Customer_id" SERIAL PRIMARY KEY,
            "Customer_name" VARCHAR(30),
            "Customer_address" VARCHAR(50),
            "Customer_phone_number" BIGINT
        );
        INSERT INTO "Customers" ("Customer_name", "Customer_address", "Customer_phone_number")
        VALUES
        ('John Smith', '123 Main St, Anytown USA', 1234567890),
        ('Jane Doe', '456 Oak St, Anytown USA', 2345678901),
        ('Bob Johnson', '789 Pine St, Anytown USA', 3456789012),
        ('Alice Williams', '321 Maple St, Anytown USA', 4567890123),
        ('Tom Brown', '654 Elm St, Anytown USA', 5678901234),
        ('Sarah Davis', '987 Cedar St, Anytown USA', 6789012345),
        ('Mike Wilson', '753 Hill St, Anytown USA', 7890123456),
        ('Linda Lee', '951 Valley St, Anytown USA', 8901234567),
        ('Bill Jackson', '357 River St, Anytown USA', 9012345678),
        ('Emily Davis', '864 Ocean St, Anytown USA', 1234567890),
        ('David Johnson', '159 Forest St, Anytown USA', 2345678901),
        ('Karen Smith', '753 Mountain St, Anytown USA', 3456789012),
        ('Chris Wilson', '951 Skyline St, Anytown USA', 4567890123),
        ('Mary Brown', '357 Sunset St, Anytown USA', 5678901234),
        ('Mark Lee', '864 Sunrise St, Anytown USA', 6789012345),
        ('Julie Johnson', '159 Oceanview St, Anytown USA', 7890123456),
        ('Tim Davis', '753 Beach St, Anytown USA', 8901234567),
        ('Anna Williams', '951 Park St, Anytown USA', 9012345678),
        ('Sam Smith', '357 Willow St, Anytown USA', 1234567890),
        ('Olivia Brown', '864 Oakwood St, Anytown USA', 2345678901);
        """
    )

    conn.commit()


def create_orders():
    """
    Tvoří tabulku Orders a plní jí hodnotami
    """
    cursor.execute(
        """
        DROP TABLE IF EXISTS "Orders" CASCADE;
        CREATE TABLE "Orders"(
            "Order_id" SERIAL PRIMARY KEY,
            "Date_of_order" DATE,
            "Customer_id" SERIAL REFERENCES "Customers" ("Customer_id"),
            "Item_id" SERIAL REFERENCES "Storage" ("Item_id"),
            "Quantity" INT
        );

        INSERT INTO "Orders" ("Date_of_order", "Customer_id", "Item_id", "Quantity")
        VALUES 
        ('2022-01-02', 18, 23, 3),
        ('2022-01-04', 20, 10, 4),
        ('2022-01-05', 8, 38, 1),
        ('2022-01-06', 6, 46, 6),
        ('2022-01-08', 14, 13, 2),
        ('2022-01-09', 9, 42, 3),
        ('2022-01-12', 5, 8, 5),
        ('2022-01-13', 7, 29, 1),
        ('2022-01-16', 4, 51, 4),
        ('2022-01-17', 13, 44, 1),
        ('2022-01-19', 1, 17, 2),
        ('2022-01-20', 2, 32, 3),
        ('2022-01-24', 15, 27, 1),
        ('2022-01-25', 16, 2, 2),
        ('2022-01-26', 3, 14, 4),
        ('2022-01-28', 17, 37, 1),
        ('2022-01-29', 11, 49, 2),
        ('2022-01-30', 10, 19, 3);
        """
    )

    conn.commit()


def create_employees():
    """
    Tvoří tabulku Employees a plní jí hodnotami
    """
    cursor.execute("""
        DROP TABLE IF EXISTS "Employees" CASCADE;
        CREATE TABLE "Employees" (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        role VARCHAR(255),
        username VARCHAR(50),
        password VARCHAR(150),
        can_add BOOLEAN,
        can_delete BOOLEAN,
        can_edit BOOLEAN,
        can_add_employees BOOLEAN
    );
    INSERT INTO "Employees" (name, role, username, can_add, can_delete, can_edit, can_add_employees)
    VALUES
    ('John Doe', 'manager', 'vali', True, True, True, True),
    ('Jane Smith', 'employee', 'sali', False, False, True, False),
    ('Bob Johnson', 'employee', 'salami', True, False, False, False);
    """)

    conn.commit()
