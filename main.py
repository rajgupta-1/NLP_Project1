import os

def main():
    print("Welcome to the Speech Program")
    print("1. Text to Speech (OP1)")
    print("2. Speech to Text + Speech (OP2)")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        os.system("python OP1.py")
    elif choice == '2':
        os.system("python OP2.py")
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
