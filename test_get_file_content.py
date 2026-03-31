from functions.get_file_content import get_file_content

def main():
    # 1. Test Truncation (Keep this truncated in console if you want, but check length)
    print("--- Testing Lorem (Truncation) ---")
    print(get_file_content("calculator", "lorem.txt"))
    print()

    # 2. Test Main.py - PRINT THE WHOLE THING
    print("--- Testing main.py ---")
    print(get_file_content("calculator", "main.py"))
    print()

    # 3. Test Sub-directory File - PRINT THE WHOLE THING
    print("--- Testing calculator.py ---")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    # 4. Test Security Breach
    print("--- Testing /bin/cat (Should Error) ---")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    # 5. Test Missing File
    print("--- Testing Non-existent File ---")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()