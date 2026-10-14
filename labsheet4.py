
stack = []
MAX = 5

while True:
    print("\n1. Push  2. Pop  3. Display  4. Exit")
    ch = int(input("Enter choice: "))

    if ch == 1:
        if len(stack) == MAX:
            print("Stack Overflow!")
        else:
            x = int(input("Enter element: "))
            stack.append(x)
            print("Element pushed.")

    elif ch == 2:
        if not stack:
            print("Stack Underflow!")
        else:
            print("Popped element:", stack.pop())

    elif ch == 3:
        print("Stack:", stack[::-1])

    elif ch == 4:
        break

    else:
        print("Invalid choice!")

