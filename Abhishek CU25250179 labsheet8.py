"""
LAB SHEET 8: Self-Balancing & Multi-way Search Trees
Tasks: 1) BST  2) AVL (LL, RR, LR, RL)  3) B-Tree (order 3)  4) Insertion & Bucket sort
"""



# TASK 1: Binary Search Tree (insertion + deletion)
class BSTNode:
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node  # duplicates ignored

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:          # 0 or 1 child (right)
                return node.right
            if node.right is None:         # 1 child (left)
                return node.left
            succ = node.right              # 2 children: inorder successor
            while succ.left:
                succ = succ.left
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)
        return node

    def inorder(self):
        out = []
        def go(n):
            if n:
                go(n.left); out.append(n.key); go(n.right)
        go(self.root)
        return out

    def height(self):
        def h(n):
            return 0 if n is None else 1 + max(h(n.left), h(n.right))
        return h(self.root)


# TASK 2: AVL Tree with balance-factor tracking
class AVLNode:
    def __init__(self, key):
        self.key, self.left, self.right, self.height = key, None, None, 1


class AVLTree:
    def __init__(self, verbose=True):
        self.root = None
        self.verbose = verbose
        self.rotation_log = []

    @staticmethod
    def _h(n):
        return n.height if n else 0

    def balance_factor(self, n):
        return self._h(n.left) - self._h(n.right) if n else 0

    def _update(self, n):
        n.height = 1 + max(self._h(n.left), self._h(n.right))

    def _rotate_right(self, y):
        x = y.left
        y.left, x.right = x.right, y
        self._update(y); self._update(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        x.right, y.left = y.left, x
        self._update(x); self._update(y)
        return y

    def _log(self, kind, node_key):
        msg = f"  Node {node_key} unbalanced -> {kind} rotation"
        self.rotation_log.append(msg)
        if self.verbose:
            print(msg)

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node

        self._update(node)
        bf = self.balance_factor(node)

        if bf > 1 and key < node.left.key:        # LL
            self._log("LL (single right)", node.key)
            return self._rotate_right(node)
        if bf < -1 and key > node.right.key:      # RR
            self._log("RR (single left)", node.key)
            return self._rotate_left(node)
        if bf > 1 and key > node.left.key:        # LR
            self._log("LR (left-right double)", node.key)
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if bf < -1 and key < node.right.key:      # RL
            self._log("RL (right-left double)", node.key)
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def inorder(self):
        out = []
        def go(n):
            if n:
                go(n.left); out.append(n.key); go(n.right)
        go(self.root)
        return out

    def preorder(self):
        out = []
        def go(n):
            if n:
                out.append(n.key); go(n.left); go(n.right)
        go(self.root)
        return out

    def balance_table(self):
        rows = []
        def go(n):
            if n:
                go(n.left)
                rows.append((n.key, n.height, self.balance_factor(n)))
                go(n.right)
        go(self.root)
        return rows

    def print_tree(self, node=None, prefix="", is_left=True, first=True):
        if first:
            node = self.root
        if node is None:
            return
        if node.right:
            self.print_tree(node.right, prefix + ("│   " if is_left else "    "), False, False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.key))
        if node.left:
            self.print_tree(node.left, prefix + ("    " if is_left else "│   "), True, False)


# ============================================================
# TASK 3: B-Tree simulator, order M = 3 (max 2 keys, max 3 children)
# ============================================================
class BTreeNode:
    def __init__(self, leaf=True):
        self.keys, self.children, self.leaf = [], [], leaf


class BTree:
    def __init__(self, order=3, verbose=True):
        self.M = order
        self.max_keys = order - 1
        self.root = BTreeNode()
        self.verbose = verbose

    def insert(self, key):
        result = self._insert(self.root, key)
        if result:                              # root split -> new root
            mid, right = result
            new_root = BTreeNode(leaf=False)
            new_root.keys = [mid]
            new_root.children = [self.root, right]
            self.root = new_root
            if self.verbose:
                print(f"  Root split, new root = [{mid}]")

    def _insert(self, node, key):
        """Returns (median, new_right_node) if node split, else None."""
        if key in node.keys:
            return None
        if node.leaf:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            result = self._insert(node.children[i], key)
            if result:
                mid, right = result
                node.keys.insert(i, mid)
                node.children.insert(i + 1, right)

        if len(node.keys) > self.max_keys:      # overflow -> split
            return self._split(node)
        return None

    def _split(self, node):
        mid_idx = len(node.keys) // 2
        mid = node.keys[mid_idx]
        right = BTreeNode(leaf=node.leaf)
        right.keys = node.keys[mid_idx + 1:]
        left_keys = node.keys[:mid_idx]
        if not node.leaf:
            right.children = node.children[mid_idx + 1:]
            node.children = node.children[:mid_idx + 1]
        if self.verbose:
            print(f"  Split {node.keys} -> {left_keys} | {mid} (promoted) | {right.keys}")
        node.keys = left_keys
        return mid, right

    def search(self, key, node=None):
        node = node or self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == key:
            return True
        return False if node.leaf else self.search(key, node.children[i])

    def print_tree(self):
        level = [self.root]
        depth = 0
        while level:
            print(f"  Level {depth}: " + "  ".join(str(n.keys) for n in level))
            level = [c for n in level for c in n.children]
            depth += 1


# ============================================================
# TASK 4: Insertion sort and Bucket sort
# ============================================================
def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def bucket_sort(arr, num_buckets=None):
    if not arr:
        return []
    n = num_buckets or len(arr)
    lo, hi = min(arr), max(arr)
    if lo == hi:
        return arr[:]
    size = (hi - lo) / n
    buckets = [[] for _ in range(n)]
    for x in arr:
        idx = min(int((x - lo) / size), n - 1)
        buckets[idx].append(x)
    result = []
    for b in buckets:
        result.extend(insertion_sort(b))        # sort each bucket
    return result

if __name__ == "__main__":
    print("=" * 60)
    print("TASK 1: BINARY SEARCH TREE")
    print("=" * 60)
    bst = BST()
    for k in [50, 30, 70, 20, 40, 60, 80, 35, 45]:
        bst.insert(k)
    print("Inorder after inserts :", bst.inorder())
    bst.delete(20)   # leaf
    print("Delete 20 (leaf)      :", bst.inorder())
    bst.delete(30)   # two children
    print("Delete 30 (2 children):", bst.inorder())
    bst.delete(70)   # two children
    print("Delete 70 (2 children):", bst.inorder())
    print("Height:", bst.height())

    print("\n" + "=" * 60)
    print("TASK 2: AVL TREE")
    print("=" * 60)
    tests = {
        "LL case": [30, 20, 10],
        "RR case": [10, 20, 30],
        "LR case": [30, 10, 20],
        "RL case": [10, 30, 20],
    }
    for name, seq in tests.items():
        print(f"\n{name}: insert {seq}")
        t = AVLTree()
        for k in seq:
            t.insert(k)
        print("  Preorder:", t.preorder())

    print("\nMixed sequence: 10, 20, 30, 40, 50, 25")
    avl = AVLTree()
    for k in [10, 20, 30, 40, 50, 25]:
        print(f"Insert {k}")
        avl.insert(k)
    print("\nFinal tree (right at top):")
    avl.print_tree()
    print("\nKey | Height | Balance Factor")
    for key, h, bf in avl.balance_table():
        print(f"{key:>3} | {h:>6} | {bf:>+d}")

    print("\n" + "=" * 60)
    print("TASK 3: B-TREE (M = 3)")
    print("=" * 60)
    bt = BTree(order=3)
    for k in [10, 20, 5, 6, 12, 30, 7, 17]:
        print(f"Insert {k}")
        bt.insert(k)
        bt.print_tree()
    print("Search 12:", bt.search(12), "| Search 99:", bt.search(99))

    print("\n" + "=" * 60)
    print("TASK 4: INSERTION SORT & BUCKET SORT")
    print("=" * 60)
    data = [29, 25, 3, 49, 9, 37, 21, 43]
    print("Input         :", data)
    print("Insertion sort:", insertion_sort(data))
    print("Bucket sort   :", bucket_sort(data))
    fdata = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    print("Float input   :", fdata)
    print("Bucket sort   :", bucket_sort(fdata))
