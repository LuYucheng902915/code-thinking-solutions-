# 19. Swap Npdes in Pairs
# https://leetcode.cn/problems/swap-nodes-in-pairs/

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val: int = val
        self.next: Optional[ListNode] = next


# 熟悉递归后，这道题秒杀
# 如果链表有奇数个元素，最后一个元素不变，不交换
# 递归写法，时间复杂度 O(N)，空间复杂度 O(N)。（递归的深度大约为 N / 2)
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        # 由于每次处理两个节点，所以要保证 head.next 不是 None
        new_head = self.swapPairs(head.next.next)

        temp = head.next
        head.next = new_head
        temp.next = head

        return temp


# 标准递归写法
class Solution1:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        node1 = head
        node2 = head.next

        node1.next = self.swapPairs(node2.next)
        node2.next = node1

        return node2


# 迭代写法，时间复杂度 O(N)，空间复杂度 O(1)
# 使用虚拟头节点方便
# 比较抽象，一定要仔细画图！不如递归方法直观
# 以两个节点为单位，prev 是上两个节点的后一，已经交换完毕，current 是当前两个节点的前一个
# 所以 current 可能为 None（交换完了）或者 current.next 为 None（剩一个节点，不用交换了），依次得出循环的条件
# 只要画出 prev -> current -> new_prev -> new_current
# 变成 prev -> new_ prev -> current -> new_current
# 代码就很容易写了
"""
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy_node = ListNode(next=head)

        prev = dummy_node
        current = head

        while current and current.next:
            new_prev = current.next
            new_current = new_prev.next
            prev.next = new_prev
            new_prev.next = current
            current.next = new_current
            prev = current
            current = new_current
        
        return dummy_node.next
"""


def function_tmp1(x0):
    return x0 * x0 + 4.0**2.0
