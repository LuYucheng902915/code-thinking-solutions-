# 206. Reverse Linked List
# https://leetcode.cn/problems/reverse-linked-list

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# 反转链表的经典解法
# 双指针法
# 时间复杂度 O(n)，空间复杂度 O(1)
# 因为每个节点要反转，一定要指向上一个节点，所以要用第二个指针记录上一个节点
# 因为指向上一个节点后下一个节点信息丢失，所以要临时存储下一个节点
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        current = head

        while current:
            next = current.next
            current.next = prev
            prev = current
            # 这里不能写 prev = prev.next，一定要记住 None.next/val 会报错
            current = next

        return prev


# 递归法（时间、空间复杂度均为 O(n)
# 递归调用的空间开销主要来自于函数调用栈 (Call Stack)
# 每当一个函数调用另一个函数（包括调用自身）时，系统都需要在调用栈上创建一个新的栈帧 (Stack Frame) 来存储该次调用的参数、局部变量和返回地址
# 这种方法会一直递归到链表的最后一个节点，调用栈的深度会达到 N
# 从后往前（回溯）反转 (经典递归解法)
# 这种方法是“纯粹”的递归，也是面试中最常被考察的递归解
# 它的核心思想是：先不处理当前节点，而是信任递归能帮我把后面的所有节点都反转好，只需要在它们反转完毕后，把自己接在末尾就行了
# 相当于对于某个链表，调用递归反转头节点后的链表，并返回头节点后的链表反转后的新头节点
# 只需要把头节点连到反转后链表的最后
class Solution1:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        # 递归的基准条件，链表都类似

        new_head = self.reverseList(head.next)
        head.next = None
        # 这句不能忘记
        # 递归，子列表的头节点是 head.next，返回反转后子链表的头节点
        # 把 head 接到 new_head 为头节点链表的尾部就可以
        # 遍历到新链表的最后一个节点
        # 相当于已知子链表的头节点，把 head 用尾接法接上去,下面的代码就是标准的尾接法
        if not new_head:
            new_head = head
            return new_head
            # 直接 return head

        current = new_head
        # 因为 current 要停在最后一个节点，所以条件是 current.next
        # 如果current是 None，会报错
        # 所以要分类讨论 new_head 是否为 None
        while current.next:
            current = current.next

        current.next = head
        return new_head


# 上面的代码可以通过测试，但有效率更高插入尾部的方法
# 上面的代码在递归每一层都用了 while 循环，使得算法时间复杂度变成了 O(n^2)，效率非常低
# 核心技巧：当 reverseList(head.next) 返回时，head 节点仍然指向着 head.next 节点，而此时的 head.next 节点，恰好就是已经反转好的子链表的最后一个节点
class Solution2:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        递归反转链表 (O(n) 时间复杂度)
        """
        # 基准条件 (Base Case): 链表为空，或只有一个节点，无需反转
        # 由于后面要使用 head.next，必须处理一个节点的情况，保证 head.next 不是 None
        if not head or not head.next:
            return head

        # 递归调用：假设 reverseList 能正确反转 head 后面的部分
        # new_head 是反转后子链表的头节点（也就是原链表的最后一个节点）
        new_head = self.reverseList(head.next)

        # 核心操作：将当前 head 节点连接到反转后子链表的末尾
        # 此时 head.next 仍然指向它原来的下一个节点。
        # 这个原来的下一个节点，经过递归反转，现在变成了子链表的“尾巴”
        # 所以，我们让这个“尾巴”的 next 指针指向 head
        head.next.next = head

        # 断开原头节点的连接，它现在是整个链表的新尾巴
        head.next = None

        # 每一层递归都返回 new_head，它始终是原链表的最后一个节点
        return new_head


# 递归法二（不推荐）
# 使用了尾递归的思想，时间复杂度为 O(n)，空间复杂度在 Python 为 O(n)
# 属于尾递归因为递归调用是函数返回前执行的最后一件事情 (return self._reverse(...))
# 理论上：在支持尾递归优化 (Tail Call Optimization, TCO) 的编程语言（如Scheme）或编译器中，解释器/编译器可以识别出这种情况，并复用当前的栈帧而不是创建新的
# 这样，无论链表多长，调用栈的深度始终为1，空间复杂度可以被优化到 O(1)
# Python 不支持，每次调用都创建新的栈帧，空间复杂度还是 O(n)
class Solution3:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        递归反转链表 (O(n) 时间复杂度)
        从前向后迭代式反转列表，不等待子问题解决，而是递归前进过程中完成指针反转
        由于每一步都需要知道前一个节点，需要一个带有额外参数的辅助函数
        主函数，用于启动递归
        这个写法有点不好，用递归模仿迭代，也要定义两个指针
        Python不支持尾指针优化，这个尾递归算法既不如之前递归算法直观，没有体现递归的精髓，也没有空间复杂度的优势
        比起循环迭代又引入了额外的函数调用，辅助函数的开销
        """
        return self._reverse(head, None)

    def _reverse(
        self, current: Optional[ListNode], prev: Optional[ListNode]
    ) -> Optional[ListNode]:
        # 基准情况：当 current 为 None 时，说明遍历完毕，prev 就是新头节点
        if not current:
            return prev

        # 保存下一个节点，防止链表断裂
        next_node = current.next

        # 执行反转：当前节点的 next 指向前一个节点
        current.next = prev

        # 递归处理下一个节点
        # current 变成下一轮的 prev，next_node 变成下一轮的 current
        return self._reverse(next_node, current)
