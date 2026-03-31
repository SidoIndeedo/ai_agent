from functions.write_file import write_file

def main():
    # Test 1: Overwrite existing file
    print("Test 1: Overwrite lorem.txt")
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result1)
    print()

    # Test 2: Create new file in a subdirectory
    print("Test 2: Create pkg/morelorem.txt")
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result2)
    print()

    # Test 3: Security check (attempt to write to /tmp)
    print("Test 3: Security breach attempt")
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result3)

if __name__ == "__main__":
    main()