from functions.get_files_info import get_files_info

def main():
    # Test 1: Current Directory
    print('get_files_info("calculator", "."):')
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print()

    # Test 2: Sub-directory
    print('get_files_info("calculator", "pkg"):')
    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print()

    # Test 3: Outside path (Absolute)
    print('get_files_info("calculator", "/bin"):')
    print("Result for '/bin' directory:")
    print(f"    {get_files_info('calculator', '/bin')}")
    print()

    # Test 4: Outside path (Relative)
    print('get_files_info("calculator", "../"):')
    print("Result for '../' directory:")
    print(f"    {get_files_info('calculator', '../')}")

if __name__ == "__main__":
    main()