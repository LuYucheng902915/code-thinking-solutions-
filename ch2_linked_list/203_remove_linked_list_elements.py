# 203. Remove Linked List Elements
# https://leetcode.cn/problems/remove-linked-list-elements/

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# Leetcode传入的参数 head 是链表的 head 节点，Optional 说明节点值可以为 None，即空链表


class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        # 这是开始自己的一个写法，不够精炼，逻辑上更直观
        dummy_node = ListNode(next=head)

        prev = dummy_node
        current = head  # 当前检查的节点
        while current:
            if current.val == val:
                prev.next = prev.next.next
                # prev.next = current.next是可读性更好的写法
                current = current.next
            else:
                current = current.next
                prev = prev.next
        # 既然if 和 else 都执行了 current = current.next
        # 将它提取出来更好
        # current = current.next
        # 发现要删除的节点，prev 不变，prev.next 跳过 current，current 变成下一个节点，继续检查新的 current，prev不变
        # 如果 current 保留，prev 和 current 同时前进
        # 这里其实把所有的 current 都用 prev.next 代替，就不需要两个指针，也就是下一个解法
        head = dummy_node.next
        return head


class Solution1:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        # 标准的迭代写法
        dummy_node = ListNode(next=head)
        current = dummy_node

        while current.next:
            if current.next.val == val:
                current.next = current.next.next
            else:
                current = current.next

            # current = current.next
            # 错误写法，非常重要，一定要注意只有不删除才 current = current.next
            # 删除后要重新检查 current.next 的值，可能还等于 val，也可能删除掉最后一个，current.next 是 None 了
            # 此时，如果用错误写法，删除了最后一个节点后，直接 current = current.next ，会让 current 变成 None
            # 下一次 while 循环条件判断时直接报错

        head = dummy_node.next

        return head


class Solution2:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        if not head:
            return None

        head.next = self.removeElements(head.next, val)

        if head.val == val:
            return head.next
        else:
            return head


# 递归解法。其核心思想是：
# 基准情况 (Base Case): 如果链表为空 (head is None)，则无需操作，直接返回 None
# 递推关系: 假设 removeElements 能够正确处理除了头节点之外的剩余部分 (head.next)
# 先调用 self.removeElements(head.next, val) 来获得一个已经移除了所有 val 的子链表
# 并将其接在当前头节点的后面
# 返回结果: 在处理完子链表后，再判断当前的头节点 (head) 是否需要删除
# 如果 head.val == val，那么应该跳过当前节点，返回 head.next。
# 否则，保留当前节点，返回 head。
# 注意: 在实际工程中，对于长度可能很长的链表，递归有栈溢出的风险，通常迭代是更优的选择。


# 熟练后写的一个不使用虚拟头节点的做法，轻松做对
# 这种方法的核心是分情况讨论：对头节点的删除和对非头节点的删除
# 处理头节点：循环移动 head 指针，直到它指向一个值不为 val 的节点，或者整个链表为空。这样就处理了所有需要删除的前导节点
# 之所以要虚拟头节点，原因就是头节点没有前驱节点，不容易删除，所以这里如果先一直删除头节点，得到的链表要么空，要么头节点不需要删除，那么就不需要头节点的前去点击了
# 后面处理是类似的，因为要指向前驱节点，然后判断下一个节点的值是否为 val，所以 head 必须不是 None
# 因为优先判断 head 是否为 None，所以避免了 None.next 的出现
class Solution3:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        while head and head.val == val:
            head = head.next
        if not head:
            return head

        prev = head
        while prev.next:
            if prev.next.val == val:
                prev.next = prev.next.next
            else:
                prev = prev.next

        return head
