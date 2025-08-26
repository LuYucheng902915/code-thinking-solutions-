# 707. Desin Linked List
# https://leetcode.cn/problems/design-linked-list/description/

# 自己尝试的双向，带尾指针以及计数器的链表，有许多小 bug，但最终经过修改成功通过
# 这种带尾指针、计数器的双向链表能够将获取长度，在头/尾部插入删除的操作时间复杂度都降低到 O(1)，缺点是处理更复杂一些
# 对链表的操作比较熟悉了
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None


class MyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def get(self, index: int):
        if not 0 <= index < self.length:
            return -1

        current = self.head
        for _ in range(index):
            current = current.next
        return current.val

    def addAtHead(self, val: int) -> None:
        new_node = ListNode(val)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
            self.length += 1
            return

        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
        self.length += 1

    def addAtTail(self, val: int) -> None:
        new_node = ListNode(val)
        if self.length == 0:
            self.addAtHead(val)
            return

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
        self.length += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if not 0 <= index <= self.length:
            return
        if index == 0:
            self.addAtHead(val)
            return
        if index == self.length:
            self.addAtTail(val)
            return

        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        new_node = ListNode(val)
        new_node.prev = prev
        new_node.next = prev.next
        prev.next.prev = new_node
        prev.next = new_node

        self.length += 1

    def deleteAtIndex(self, index: int) -> None:
        if not 0 <= index < self.length:
            return
        if self.length == 1:
            self.head = None
            self.tail = None
            self.length -= 1
            return
        if index == 0:
            self.head = self.head.next
            self.head.prev = None
            self.length -= 1
            return
        if index == self.length - 1:
            self.tail = self.tail.prev
            self.tail.next = None
            self.length -= 1
            return

        current = self.head
        for _ in range(index - 1):
            current = current.next

        current.next = current.next.next
        current.next.prev = current
        self.length -= 1


# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)


# 一个更好的优化就是在按照索引操作时，根据索引的位置选择从列表头还是列表尾开始查找，从而缩短遍历了路径
# 通过双向查找优化，虽然按索引操作算法的理论时间复杂度等级仍然是 O(n)，但优化了其常数因子，使得在最坏情况下的实际遍历次数减少了约一半（遍历几乎整个链表 -> 遍历半个链表）
# 可以证明， 以 get 方法为例，如果查找目标索引完全随机，经过大量次数查找，原来算法平均遍历次数是链表长度的一半，现在的长度大约为链表长度的四分之一
# 总之，对于较长的链表，这种优化显著减少了遍历节点的次数，值得采用
"""
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None

class MyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def _get_node(self, index: int) -> ListNode:
        if index < self.length / 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.length - 1 - index):
                current = current.prev
        return current

    def get(self, index: int) -> int:
        if not 0 <= index < self.length:
            return -1
        return self._get_node(index).val

    def addAtHead(self, val: int) -> None:
        new_node = ListNode(val)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        self.length += 1

    def addAtTail(self, val: int) -> None:
        if not self.head:
            self.addAtHead(val)
            return
        new_node = ListNode(val)
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
        self.length += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if not 0 <= index <= self.length:
            return
        if index == 0:
            self.addAtHead(val)
            return
        if index == self.length:
            self.addAtTail(val)
            return

        next_node = self._get_node(index)
        prev_node = next_node.prev
        new_node = ListNode(val)

        new_node.prev = prev_node
        new_node.next = next_node
        prev_node.next = new_node
        next_node.prev = new_node

        self.length += 1

    def deleteAtIndex(self, index: int) -> None:
        if not 0 <= index < self.length:
            return

        node_to_delete = self._get_node(index)
        prev_node = node_to_delete.prev
        next_node = node_to_delete.next

        if prev_node:
            prev_node.next = next_node
        else:
            self.head = next_node

        if next_node:
            next_node.prev = prev_node
        else:
            self.tail = prev_node

        self.length -= 1
"""
# 为什么会想到采用哨兵节点？动机源于“消除特例”
# 在不使用哨兵节点的代码中，被迫写了大量 if/else 来处理各种边界情况：
# 操作的是否是头节点？ (index == 0)
# #操作的是否是尾节点？ (index == self.length - 1)
# 链表是否为空？ (self.head is None)
# 链表是否只有一个节点？ (self.length == 1)
# 这些判断逻辑散布在 add 和 delete 的各个方法中，不仅让代码显得冗长、重复，而且非常容易出错
# 优秀的软件设计追求 逻辑的统一性。哨兵节点的思想正是为了实现这个目标。开发者会思考：“有没有一种方法，可以让对头、尾、中间节点的操作逻辑完全一样
# 这个问题的答案就是：确保每个“真实”的节点，其前驱（prev）和后继（next）永远不为 None
# 通过创建“假的”头节点和尾节点，来“包住”所有真实的节点，从而使得链表中的每一个真实节点都处于“中间节点”的位置
# 体现了软件工程的权衡，通过两个节点额外的内存空间，看起来是浪费，其实节约了开发时间成本，理解代码成本，维护成本等
# 非常推荐
"""
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None

class MyLinkedList:
    def __init__(self):
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.length = 0

    def _get_node(self, index: int) -> ListNode:
        if index < self.length / 2:
            current = self.head.next
            for _ in range(index):
                current = current.next
        else:
            current = self.tail.prev
            for _ in range(self.length - 1 - index):
                current = current.prev
        return current

    def get(self, index: int) -> int:
        if not 0 <= index < self.length:
            return -1
        return self._get_node(index).val

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.length, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if not 0 <= index <= self.length:
            return

        if index < self.length / 2:
            prev_node = self.head
            for _ in range(index):
                prev_node = prev_node.next
            next_node = prev_node.next
        else:
            next_node = self.tail
            for _ in range(self.length - index):
                next_node = next_node.prev
            prev_node = next_node.prev
            
        new_node = ListNode(val)
        new_node.prev = prev_node
        new_node.next = next_node
        prev_node.next = new_node
        next_node.prev = new_node
        self.length += 1

    def deleteAtIndex(self, index: int) -> None:
        if not 0 <= index < self.length:
            return

        node_to_delete = self._get_node(index)
        prev_node = node_to_delete.prev
        next_node = node_to_delete.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
        
        self.length -= 1
"""
