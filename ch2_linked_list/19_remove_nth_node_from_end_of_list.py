# 19. Remove nth Node from End of List
# https://leetcode.cn/problems/remove-nth-node-from-end-of-list

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# 这道题有两种方法
# 第一种是计算长度法，从头到尾走一遍，计算出链表总长度 L
# 从头再走一遍，走 L - n - 1 步，到达要删除节点的前一个节点
# 第二种是快慢指针法，通过让一个指针先走，来制造一个固定的“距离”，然后两个指针同步前进，直到快指针到终点


# 自己解答，做对了，也是最优解法
# 题目规定了 n 的范围为 1 <= n <= 链表长度
# 时间复杂度为 O(L)，L为链表长度，空间复杂度为 O(1)
# 双指针法。虽然有两个循环，但每个指针都最多从头到尾遍历列表一次，没有重复扫描，所以属于单遍扫描的方法
# 其实从指针移动次数角度看，由于一次遍历使用了两个指针，可以分析得到两种方法移动次数是差不多的，这里单遍扫描的优点不在运行时间上
# 如果数据是流式的，它不支持回头再读，这是在实际应用中单遍扫描方法最大的优势
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy_node = ListNode(next=head)
        slow, fast = dummy_node, dummy_node
        # 同样引入哑节点避免分类讨论
        # 关键是要让快指针 flag 变成 None 的时候，慢指针刚好停在要删除节点的前一个节点
        # 根据这个原则设计快慢指针的距离
        for _ in range(n):
            fast = fast.next

        while fast.next:
            slow = slow.next
            fast = fast.next

        slow.next = slow.next.next

        head = dummy_node.next
        return head
        # return dummy_node.next


# 下面是计算长度法，也是 O(L)的时间复杂度
# 题目规定了链表长度大于等于 1
class Solution2:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy_node = ListNode(next=head)

        length = 0
        current = head
        while current:
            current = current.next
            length += 1

        prev = dummy_node
        for _ in range(length - n):
            prev = prev.next

        prev.next = prev.next.next
        head = dummy_node.next
        return head
