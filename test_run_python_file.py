from functions.run_python_file import run_python_file

def main():
    # Test 1: Run main.py (No args)
    print("--- Test 1: main.py (Usage) ---")
    print(run_python_file("calculator", "main.py"))
    print()

    # Test 2: Run main.py (With calculation)
    print("--- Test 2: main.py (3 + 5) ---")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    # Test 3: Run tests.py
    print("--- Test 3: tests.py ---")
    print(run_python_file("calculator", "tests.py"))
    print()

    # Test 4: Security Breach
    print("--- Test 4: Security Breach ---")
    print(run_python_file("calculator", "../main.py"))
    print()

    # Test 5: Non-existent file
    print("--- Test 5: Non-existent ---")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    # Test 6: Not a python file
    print("--- Test 6: Wrong Extension ---")
    print(run_python_file("calculator", "lorem.txt"))

if __name__ == "__main__":
    main()