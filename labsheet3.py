
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data, position):
        new = Node(data)

        if position == 0:
            new.next = self.head
            self.head = new
            return

        temp = self.head
        for i in range(position - 1):
            if temp is None:
                print("Invalid position!")
                return
            temp = temp.next

        if temp is None:
            print("Invalid position!")
            return

        new.next = temp.next
        temp.next = new

    def delete(self, key):
        temp = self.head

        if temp and temp.data == key:
            self.head = temp.next
            print("Node deleted.")
            return

        while temp and temp.next:
            if temp.next.data == key:
                temp.next = temp.next.next
                print("Node deleted.")
                return
            temp = temp.next

        print("Value not found.")

    def display(self):
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")


sll = SinglyLinkedList()

while True:
    print("\n1.Insert  2.Delete  3.Display  4.Exit")
    ch = int(input("Enter choice: "))

    if ch == 1:
        data = int(input("Enter data: "))
        pos = int(input("Enter position (0 for head): "))
        sll.insert(data, pos)
    elif ch == 2:
        key = int(input("Enter value to delete: "))
        sll.delete(key)
    elif ch == 3:
        sll.display()
    elif ch == 4:
        break
    else:
        print("Invalid choice!")