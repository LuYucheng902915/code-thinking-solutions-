class ListNode:
    def __init__(self, value=0):
        self.val = value
        self.next = None

    def __repr__(self):
        return f"ListNode({self.val})"


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def __len__(self):
        length = 0
        current = self.head
        while current:
            length += 1
            current = current.next
        return length

    def __str__(self):
        if self.is_empty:
            return "Empty List"

        vals = []
        current = self.head
        while current:
            vals.append(str(current.val))
            current = current.next

        return " -> ".join(vals) + " -> None"

    def prepend(self, value):
        new_node = ListNode(value)
        new_node.next = self.head
        self.head = new_node

    def append(self, value):
        new_node = ListNode(value)
        if self.is_empty():
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def insert(self, index, value):
        if not 0 <= index <= len(self):
            raise IndexError("Index out of range")

        if index == 0:
            self.prepend(value)
            return

        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        new_node = ListNode(value)
        new_node.next = prev.next
        prev.next = new_node
