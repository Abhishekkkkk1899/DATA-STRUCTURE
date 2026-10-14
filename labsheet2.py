
arr = list(map(int, input("Enter array elements: ").split()))

while True:
    print("\n1. Insert Element")
    print("2. Delete Element")
    print("3. Search Element")
    print("4. Display Array")
    print("5. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        index = int(input("Enter index: "))
        value = int(input("Enter value: "))

        if 0 <= index <= len(arr):
            arr.insert(index, value)
            print("Element inserted successfully.")
        else:
            print("Invalid index!")

    elif choice == 2:
        index = int(input("Enter index to delete: "))

        if 0 <= index < len(arr):
            arr.pop(index)
            print("Element deleted successfully.")
        else:
            print("Invalid index!")

    elif choice == 3:
        value = int(input("Enter value to search: "))
        found = False

        for i in range(len(arr)):
            if arr[i] == value:
                print("Element found at index:", i)
                found = True
                break

        if not found:
            print("Element not found.")

    elif choice == 4:
        print("Array:", arr)

    elif choice == 5:
        print("Program terminated.")
        break

    else:
        print("Invalid choice!")
