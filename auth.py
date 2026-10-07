from database import add_user, verification
from config import USERNAME_MAX_LENGTH, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH

def validation_format(name, password):
    if not isinstance(name, str):
        return "ENTER CHARACTERS ONLY!"
    if not isinstance(password, str):
        return "ENTER CHARACTERS ONLY!"
    name_length = len(name)
    password_length = len(password)
    if name_length == 0 or password_length == 0:
        return "Do not leave PASSWORD or USERNAME BLANK!"
    elif name_length > USERNAME_MAX_LENGTH:
        return f"Your USERNAME is too LONG (Maximum {USERNAME_MAX_LENGTH} Characters)!"
    elif password_length < PASSWORD_MIN_LENGTH:
        return f"Your PASSWORD is too SHORT (Minimum {PASSWORD_MIN_LENGTH} Characters)!"
    elif password_length > PASSWORD_MAX_LENGTH:
        return f"Your PASSWORD is too LONG (Maximum {PASSWORD_MAX_LENGTH} Characters)!"
    elif not name.isalnum():
        return "SYMBOLS are not ALLOWED!"
    return True

def validation(name, password):
    return password == verification(name)

def haveAccount():
    while True:
        x = input("\nDo you have account or not (yes/no): ")
        if x.lower() == "yes":
            return True
        elif x.lower() == "no":
            return False
        print("\nPlease enter APPROPRIATE ANSWER!")

def login():
    name = input("\nYour username: ")
    password = input("Password: ")
    valid = validation_format(name, password)
    if valid is not True:
        return f"\nLOGIN FAILED {valid}"
    elif validation(name, password):
        return name
    else:
        return False

def register():
    name = input("\nYour username: ")
    password = input("Password: ")
    valid = validation_format(name, password)
    if valid is not True:
        return f"\nREGISTRATION FAILED: {valid}"
    else:
        result = add_user(name, password)
        if result is True:
            return f"\nREGISTRATION SUCCESSFUL: Account {name} has been SUCCESSFULLY REGISTERED!"
        else:
            return f"\nREGISTRATION FAILED: {result}"


if __name__ == "__main__":
    """=== MAINTENANCE MODE ==="""
    
    # Menguji auth.py dari NOL!
    # haveAccount()

    # MENAMBAHKAN akun BARU secara MANUAL:
    # print(f"Status: {register()}")

    # Menguji apakah AKUN bisa LOGIN atau TIDAK:
    # print(f"Status: {login()}")

    # Menguji apakah sistem VALIDASI FORMAT BEKERJA atau TIDAK:
    # print(f"Status: {validation_format("admin", "admin1234")}")

    # Menguji apakah USERNAME dan PASSWORD BENAR, SALAH, atau TIDAK ADA:
    # print(f"Status: {validation("admin", "admin1234")}")