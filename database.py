import sqlite3
from time import sleep
from config import DATABASE_PATH, MAX_BALANCE, MAX_TRANSACTION, USERNAME_MAX_LENGTH, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH

def delete_table():
    print("⚠WARNING⚠")
    print("IF YOU DID THIS ACTION, YOU WILL DELETE THE TABLE COMPLETELY WITHOUT ANY TRACE")
    print("THIS ACTION CANNOT BE UNDONE!")
    status = input("IF YOU UNDERSTAND, FACE YOUR OWN RISK! (yes/no): ")
    if status.lower() == "yes":
        print("⚠WARNING⚠")
        sleep(0.5)
        print("THE TABLE WILL BE DELETED SOON!")
        sleep(0.5)
        print("===CONNECTING TO SQLITE===")
        sleep(0.5)
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        print("===DELETING THE TABLE RIGHT NOW!===")
        sleep(0.5)
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'users'")
        print("===CHANGES SAVED===")
        connection.commit()
        cursor.close()
        connection.close()

def create_table():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance INTEGER NOT NULL DEFAULT 0
    );
    """)
    connection.commit()
    cursor.close()
    connection.close()

def verification(username):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0]
    else:
        return None

def search_username(username):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is not None:
        result = result[0]
    cursor.close()
    connection.close()
    return result

def add_user(username, password):
    if not isinstance(username, str):
        return "ENTER CHARACTERS ONLY!"
    if not isinstance(password, str):
        return "ENTER CHARACTERS ONLY!"
    length_new_user = len(username)
    length_new_pass = len(password)
    if length_new_user == 0:
        return "DO NOT LEAVE USERNAME OR NEW USERNAME BLANK!"
    if length_new_user > USERNAME_MAX_LENGTH:
        return f"YOUR USERNAME IS TOO LONG (Maximum {USERNAME_MAX_LENGTH} Characters)!"
    if username.isalnum() == False:
        return "SYMBOLS ARE NOT ALLOWED!"
    if length_new_pass == 0:
        return "DO NOT LEAVE THE PASSWORD BLANK!"
    if length_new_pass < PASSWORD_MIN_LENGTH:
        return f"YOUR PASSWORD IS TOO SHORT (Minimum {PASSWORD_MIN_LENGTH} Characters)!"
    if length_new_pass > PASSWORD_MAX_LENGTH:
        return f"YOUR PASSWORD IS TOO LONG (Maximum {PASSWORD_MAX_LENGTH} Characters)!"
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return "USERNAME IS ALREADY TAKEN! PLEASE CHOOSE THE OTHER ONE!"
    finally:
        cursor.close()
        connection.close()

def update_username_password(status, username, new_username="", new_password=""):
    if not isinstance(status, bool):
        return "UNKNOWN CONDITION!"
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        check = cursor.fetchone()
        if check is None:
            return "UNKNOWN USERNAME!"
        else:
            # When the status value is "True", the changes lead to "Username".
            if status is True:
                if not isinstance(new_username, str):
                    return "ENTER CHARACTERS ONLY!"
                length_new_user = len(new_username)
                if length_new_user == 0:
                    return "DO NOT LEAVE USERNAME OR NEW USERNAME BLANK!"
                cursor.execute("SELECT username FROM users WHERE username = ?", (new_username,))
                validation = cursor.fetchone()
                if validation is not None:
                    validation = validation[0]
                if username == new_username:
                    return "DO NOT ENTER THE SAME USERNAME AS THE NEW USERNAME!"
                if length_new_user > USERNAME_MAX_LENGTH:
                    return f"YOUR USERNAME IS TOO LONG (Maximum {USERNAME_MAX_LENGTH} Characters)!"
                if new_username.isalnum() == False:
                    return "SYMBOLS ARE NOT ALLOWED!"
                if validation == new_username:
                    return "USERNAME IS ALREADY TAKEN! PLEASE CHOOSE THE OTHER ONE!"
                else:
                    try:
                        cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, username))
                        connection.commit()
                        return True
                    except sqlite3.IntegrityError:
                        return "USERNAME IS ALREADY TAKEN! PLEASE CHOOSE THE OTHER ONE!"
            # When the status value is "False", the changes lead to "Password".
            elif status is False:
                if not isinstance(new_password, str):
                    return "ENTER CHARACTERS ONLY!"
                length_new_pass = len(new_password)
                cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
                validation = cursor.fetchone()
                if validation is not None:
                    validation = validation[0]
                if validation == new_password:
                    return "DO NOT ENTER THE SAME PASSWORD AS THE NEW PASSWORD!"
                if length_new_pass == 0:
                    return "DO NOT LEAVE THE PASSWORD BLANK!"
                if length_new_pass < PASSWORD_MIN_LENGTH:
                    return f"YOUR PASSWORD IS TOO SHORT (Minimum {PASSWORD_MIN_LENGTH} Characters)!"
                if length_new_pass > PASSWORD_MAX_LENGTH:
                    return f"YOUR PASSWORD IS TOO LONG (Maximum {PASSWORD_MAX_LENGTH} Characters)!"
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
                connection.commit()
                return True
    finally:
        cursor.close()
        connection.close()

def delete_user(username):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE username  = ?", (username,))
    connection.commit()
    success = cursor.rowcount > 0
    cursor.close()
    connection.close()
    return success

def view_balance(username):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
    balance = cursor.fetchone()
    if balance is not None:
        balance = balance[0]
    cursor.close()
    connection.close()
    return balance

def add_balance(username, amount):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        amount = int(amount)
        if amount > 0:
            if amount > MAX_TRANSACTION:
                return f"EXCEEDED MAXIMUM MONEY TRANSACTION (MAX {MAX_TRANSACTION:,})!"
            else:
                cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
                balance = cursor.fetchone()
                if balance is None:
                    return "UNKNOWN USERNAME!"
                balance = balance[0]
                if (balance + amount) > MAX_BALANCE:
                    return f"EXCEEDED MAXIMUM BALANCE (MAX {MAX_BALANCE:,})!"
                else:
                    cursor.execute("UPDATE users SET balance = (balance + ?) WHERE username = ?", (amount, username))
                    result = cursor.rowcount
                    if result != 0:
                        connection.commit()
                        return True
                    else:
                        connection.rollback()
                        return "UNKNOWN USERNAME!"
        else:
            return "DO NOT ENTER ZERO OR MINUS NUMBERS!"
    except ValueError:
        return "NUMBER ONLY!"
    except TypeError:
        return "NUMBER ONLY!"
    except OverflowError:
        return "DO NOT ENTER A HUGE NUMBER!"
    finally:
        cursor.close()
        connection.close()

def decrease_balance(username, amount):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        amount = int(amount)
        if amount > 0:
            if amount > MAX_TRANSACTION:
                return f"EXCEEDED MAXIMUM MONEY TRANSACTION (MAX {MAX_TRANSACTION:,})!"
            else:
                cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
                balance = cursor.fetchone()
                if balance is None:
                    return "UNKNOWN USERNAME!"
                balance = balance[0]
                if amount <= balance:
                    cursor.execute("UPDATE users SET balance = (balance - ?) WHERE username = ?", (amount, username))
                    result = cursor.rowcount
                    if result != 0:
                        connection.commit()
                        return True
                    else:
                        connection.rollback()
                        return "UNKNOWN USERNAME!"
                else:
                    return "DO NOT WITHDRAW MORE THAN YOUR BALANCE!"
        else:
            return "DO NOT ENTER ZERO OR MINUS NUMBERS!"
    except ValueError:
            return "NUMBER ONLY!"
    except TypeError:
        return "NUMBER ONLY!"
    except OverflowError:
        return "DO NOT ENTER A HUGE NUMBER!"
    finally:
        cursor.close()
        connection.close()

def transfer_balance(username, amount, receiver):
    if username == receiver:
        return "DO NOT TRY TO TRANSFER TO YOURSELF!"
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        amount = int(amount)
        if amount > 0:
            if amount > MAX_TRANSACTION:
                return f"EXCEEDED MAXIMUM MONEY TRANSACTION (MAX {MAX_TRANSACTION:,})!"
            else:
                cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
                balance = cursor.fetchone()
                if balance is None:
                    return "UNKNOWN USERNAME!"
                balance = balance[0]
                cursor.execute("SELECT balance FROM users WHERE username = ?", (receiver,))
                balance_receiver = cursor.fetchone()
                if balance_receiver is None:
                    return "UNKNOWN RECEIVER USERNAME!"
                balance_receiver = balance_receiver[0]
                if (balance_receiver + amount) > MAX_BALANCE:
                    return f"EXCEEDED MAXIMUM RECEIVER BALANCE (MAX {MAX_BALANCE:,})!"
                else:
                    if balance < amount:
                        return "DO NOT TRY TO TRANSFER MORE THAN YOUR BALANCE!"
                    cursor.execute("UPDATE users SET balance = (balance + ?) WHERE username = ?", (amount, receiver))
                    success = cursor.rowcount
                    cursor.execute("UPDATE users SET balance = (balance - ?) WHERE username = ?", (amount, username))
                    success += cursor.rowcount
                    if success != 2:
                        connection.rollback()
                        return "TRANSACTION FAILED!"
                    else:
                        connection.commit()
                        return True
        else:
            return "DO NOT ENTER NEGATIVE NUMBER, OR ZERO!"
    except TypeError:
        return "DO ENTER NUMBER ONLY"
    except ValueError:
        return "ENTER APPROPRIATE USERNAME OR MONEY!"
    except OverflowError:
        return "DO NOT ENTER A HUGE NUMBER!"
    except sqlite3.Error:
        connection.rollback()
        return "UNKNOWN ERROR!"
    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    """=== MAINTENANCE MODE ==="""

    # MENAMBAH dan MENGHAPUS akun NASABAH:
    # print(f"Status: {add_user("admin", "admin1234")}")
    # print(f"Status: {delete_user("admin")}")
    
    # MENGGANTI USERNAME dan PASSWORD NASABAH:
    # print(f"Status: {update_username_password(True, "admin", "admin2")}")

    # VERIFIKASI apakah USERNAME dan PASSWORD ADA atau TIDAK:
    # print(f"Status: {verification("admin")}")
    
    # MENCARI USERNAME ADA atau TIDAK:
    # print(f"Username has been found: {search_username("admin")}")

    # MELIHAT SALDO milik NASABAH:
    # print(f"Balance: {view_balance("admin")}")

    # MENAMBAH dan MENGURANGI SALDO milik NASABAH:
    # print(f"Status: {add_balance("admin", 1000)}")
    # print(f"Status: {decrease_balance("admin", 1000)}")

    # TRANSFER UANG NASABAH:
    # print(f"Status: {transfer_balance("admin", 1000, "admin")}")

    """
    ===== ⚠BERBAHAYA⚠ =====
    Jangan pernah jalankan perintah ini kecuali keadaan darurat, seperti:
    - Isi database rusak
    - Database tak bisa diakses
    Gunakan ini sebijak mungkin
    """
    # delete_table()
    # create_table()