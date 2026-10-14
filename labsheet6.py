
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def inorder(root):
    if root:
        inorder(root.left)
        print(root.data, end=" ")
        inorder(root.right)


def preorder(root):
    if root:
        print(root.data, end=" ")
        preorder(root.left)
        preorder(root.right)


def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.data, end=" ")


def iterative_inorder(root):
    stack = []
    curr = root

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        print(curr.data, end=" ")
        curr = curr.right


def iterative_preorder(root):
    if not root:
        return

    stack = [root]

    while stack:
        curr = stack.pop()
        print(curr.data, end=" ")

        if curr.right:
            stack.append(curr.right)
        if curr.left:
            stack.append(curr.left)


def iterative_postorder(root):
    if not root:
        return

    stack1 = [root]
    stack2 = []

    while stack1:
        curr = stack1.pop()
        stack2.append(curr)

        if curr.left:
            stack1.append(curr.left)
        if curr.right:
            stack1.append(curr.right)

    while stack2:
        print(stack2.pop().data, end=" ")


# Construct the binary tree
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

print("Recursive Inorder:")
inorder(root)

print("\nRecursive Preorder:")
preorder(root)

print("\nRecursive Postorder:")
postorder(root)

print("\n\nIterative Inorder:")
iterative_inorder(root)

print("\nIterative Preorder:")
iterative_preorder(root)

print("\nIterative Postorder:")
iterative_postorder(root)
print()