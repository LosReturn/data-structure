import random


class Stack:
    """
    Class implementing STACK ADT.
    Supported methods are: push, pop, top, is_empty

    """
    def __init__(self):
        """ Initialize empty stack based on Python list """
        self._data = []

    def push(self, value: object) -> None:
        """ Add new element on top of the stack """
        self._data.append(value)

    def pop(self):
        """ Remove element from top of the stack and return its value """
        return self._data.pop()

    def top(self):
        """ Return value of top element without removing from stack """
        return self._data[-1]

    def is_empty(self):
        """ Return True if the stack is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "STACK: { " + ", ".join(data_str) + " }"


class Queue:
    """
    Class implementing QUEUE ADT.
    Supported methods are: enqueue, dequeue, is_empty

    """
    def __init__(self):
        """ Initialize empty queue based on Python list """
        self._data = []

    def enqueue(self, value: object) -> None:
        """ Add new element to the end of the queue """
        self._data.append(value)

    def dequeue(self):
        """ Remove element from the beginning of the queue and return its value """
        return self._data.pop(0)

    def is_empty(self):
        """ Return True if the queue is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "QUEUE { " + ", ".join(data_str) + " }"


class TreeNode:
    """
    AVL Tree Node class
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        """
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    def __str__(self):
        return 'AVL Node: {}'.format(self.value)


class AVL:
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL tree
        """
        self.root = None

        # populate AVL with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form using pre-order traversal
        """
        values = []
        self._str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, cur, values):
        """
        Helper method for __str__. Does pre-order traversal
        """
        if cur:
            values.append(str(cur.value))
            self._str_helper(cur.left, values)
            self._str_helper(cur.right, values)

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        """
        s = Stack()
        s.push(self.root)
        while not s.is_empty():
            node = s.pop()
            if node:
                # check for correct height (relative to children)
                l = node.left.height if node.left else -1
                r = node.right.height if node.right else -1
                if node.height != 1 + max(l, r):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                s.push(node.right)
                s.push(node.left)
        return True



    def update_node_height(self, node: TreeNode):
        active = True
        while node and active:
            prev = node.height
            l = node.left.height if node.left else -1
            r = node.right.height if node.right else -1
            node.height = max(l,r) + 1
            active = node.height != prev
            node = node.parent

    def rotate_left(self, p, c):
        f = p.parent
        s2 = c.left
        p.right = s2
        if s2:
            s2.parent = p
        c.left = p
        p.parent = c

        if f is None:
            self.root = c
            self.root.parent = None
        else:
            if f.right == p:
                f.right = c
            else:
                f.left = c
            c.parent = f

        self.update_node_height(p)
        self.update_node_height(c.parent)

        return c

    def rotate_right(self, p, c):
        f = p.parent
        s2 = c.right
        p.left = s2
        if s2:
            s2.parent = p
        c.right = p
        p.parent = c

        if f is None:
            self.root = c
            self.root.parent = None
        else:
            if f.right == p:
                f.right = c
            else:
                f.left = c
            c.parent = f

        self.update_node_height( p )
        self.update_node_height( c.parent )

        return c

    def rotate_right_left(self, p, c):
        f = p.parent
        g = c.left

        # right_rotate
        s3 = g.right
        c.left = s3
        if s3:
            s3.parent = c
        g.right = c
        c.parent = g

        # left_rotate
        s2 = g.left
        p.right = s2
        if s2:
            s2.parent = p
        g.left = p
        p.parent = g

        if f is None:
            self.root = g
            self.root.parent = None
        else:
            if f.right == p:
                f.right = g
            else:
                f.left = g
            g.parent = f
        self.update_node_height(p)
        self.update_node_height(c)

        return g

    def rotate_left_right(self, p, c):
        f = p.parent
        g = c.right

        # left_rotate
        s2 = g.left
        c.right = s2
        if s2:
            s2.parent = c
        g.left = c
        c.parent = g

        # right_rotate
        s3 = g.right
        p.left = s3
        if s3:
            s3.parent = p
        g.right = p
        p.parent = g

        if f is None:
            self.root = g
            self.root.parent = None
        else:
            if (f.right == p):
                f.right = g
            else:
                f.left = g
            g.parent = f
        #
        self.update_node_height(p)
        self.update_node_height(c)


        return g

    def calculate_bf(self, node: TreeNode):

        l = node.left.height if node.left else -1
        r = node.right.height if node.right else -1
        return r-l

    def add(self, value: object) -> None:
        """
        [rr]:
                        F
                      /  \
                 SubTree  A
                           \
                            B
                             \
                              C
        [rotate]:
                        F
                      /  \
                 SubTree  B
                         / \
                        A   C
        ---
        [LL]:
                        F
                      /  \
                     A   SubTree
                    /
                   B
                  /
                 C
        [rotate]:
                        F
                       / \
                      B  SubTree
                     / \
                    C   A
        """

        root: TreeNode = self.root
        if not root:
            self.root = TreeNode( value )
            return

        while True:
            if value == root.value:
                return
            elif value < root.value:
                if root.left:
                    root = root.left
                else:
                    root.left = TreeNode( value )
                    root.left.parent = root
                    node = root.left
                    self.update_node_height( root )
                    break
            else:
                if root.right:
                    root = root.right
                else:
                    root.right = TreeNode( value )
                    root.right.parent = root
                    node = root.right
                    self.update_node_height(root)
                    break
        #rebalance
        while node.parent:
            if node.parent.left == node:
                if self.calculate_bf( node.parent ) == -2:

                    if self.calculate_bf(node) > 0:
                        self.rotate_left_right( node.parent, node )
                    else:
                        self.rotate_right( node.parent, node )
                elif self.calculate_bf(node.parent) > 0:
                    break
                else:
                    node = node.parent
                    continue
            else:
                if self.calculate_bf(node.parent) == 2:

                    if self.calculate_bf(node) <0:
                        self.rotate_right_left( node.parent, node )
                    else:
                        self.rotate_left( node.parent, node )
                elif self.calculate_bf(node.parent) < 0:

                    break
                else:
                    node = node.parent
                    continue

    def search(self, value: object):
        node = self.root
        while node:
            if value == node.value:
                return node
            elif value > node.value:
                node = node.right
            else:
                node = node.left
        return None

    def  _rebalance(self, node:TreeNode):
        if self.calculate_bf(node) == 2:
            if self.calculate_bf(node.right) < 0:
                self.rotate_right_left( node, node.right )
            else:
                self.rotate_left(node,node.right)
        elif self.calculate_bf(node) == -2:
            if self.calculate_bf(node.left) > 0:
                self.rotate_left_right(node,node.left)
            else:
                self.rotate_right( node, node.left )

    def _removeLeaf(self, c: TreeNode):
        p = c.parent
        if p:
            if p.left == c:
                p.left = None
            else:
                p.right = None
            self.update_node_height( p )
        else:
            self.root = None
        del c

        node = p
        while (node):
            if not self.calculate_bf(node) in [ -1, 0, 1 ]:
                self._rebalance( node )
            node = node.parent

    def _removeBranch(self, c: TreeNode):
        p = c.parent
        if (p):
            if p.left == c:
                p.left = c.right if c.right else c.left
            else:
                p.right = c.right if c.right else c.left
            if c.left:
                c.left.parent = p
            else:
                c.right.parent = p
            self.update_node_height( p )
        else:
            self.root = c.left if c.left else c.right
            self.root.parent = None
        del c

        node = p
        while (node):
            if not self.calculate_bf(node) in [ -1, 0, 1 ]:
                self._rebalance( node )
            node = node.parent

    def _swapWithSuccessorAndRemove(self, c: TreeNode):
        successor = self._find_min( c.right )
        self._swapNodes( c, successor )

        if c.height == 0:
            self._removeLeaf( c )
        else:
            self._removeBranch( c )

    def _swapNodes(self, node1, node2):

        parent1 = node1.parent
        leftChild1 = node1.left
        rightChild1 = node1.right
        parent2 = node2.parent
        leftChild2 = node2.left
        rightChild2 = node2.right

        # swap heights
        tmp = node1.height
        node1.height = node2.height
        node2.height = tmp

        if parent1:
            if parent1.left == node1:
                parent1.left = node2
            else:
                parent1.right = node2
            node2.parent = parent1
        else:
            self.root = node2
            node2.parent = None

        node2.left = leftChild1
        leftChild1.parent = node2
        node1.left = leftChild2
        node1.right = rightChild2
        if rightChild2:
            rightChild2.parent = node1
        if not (parent2 == node1):
            node2.right = rightChild1
            rightChild1.parent = node2
            parent2.left = node1
            node1.parent = parent2
        else:
            node2.right = node1
            node1.parent = node2

    def remove(self, value: object) -> bool:
        """
            1) The node is a leaf.  Remove it and return.

            2) The node is a branch (has only 1 child). Make the pointer to this node
            point to the child of this node.

            3) The node has two children. Swap items with the successor
            of the node (the smallest item in its right subtree) and
            delete the successor from the right subtree of the node.
        """
        node = self.search( value )

        if node is None:
            return False
        #isLeaf
        if node.height == 0:
            self._removeLeaf( node )
        elif (bool( node.left )) ^ (bool( node.right )):
            self._removeBranch( node )
        else:
            self._swapWithSuccessorAndRemove( node )

        return True

    def contains(self, value: object) -> bool:
        """
        use search to find the node
        """
        return self.search(value) is not None

    def inorder_traversal(self) -> Queue:
        """
        dfs(left) -> enqueue current node's value -> dfs(right)
        """
        que = Queue()

        def _dfs_in_order(node, que):
            if not node:
                return
            _dfs_in_order( node.left, que )
            que.enqueue( node.value )
            _dfs_in_order( node.right, que )

        _dfs_in_order(self.root, que)
        return que

    def postorder_traversal(self) -> Queue:
        """
        dfs(left) -> enqueue current node's value -> dfs(right)
        """
        que = Queue()

        def _dfs_post_order(node, que):
            if not node:
                return
            _dfs_post_order( node.left, que )
            _dfs_post_order( node.right, que )
            que.enqueue( node.value )
        _dfs_post_order(self.root, que)
        return que

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def find_min(self) -> object:
        """
        search left-child
        """
        node = self.root
        if node is None:
            return None

        return self._find_min(node).value

    def find_max(self) -> object:
        """
        search right-child
        """
        node = self.root
        if node is None:
            return None
        while node.right:
            node = node.right
        return node.value

    def is_empty(self) -> bool:
        """
        Determine whether the root exists
        """
        return self.root is None

    def make_empty(self) -> None:
        """
        TODO: Write your implementation
        """
        self.root = None

