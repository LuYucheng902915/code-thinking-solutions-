# https://leetcode.cn/problems/intersection-of-two-linked-lists-lcci/

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


# 两种思路
# 思路一，计算两个链表的长度，然后将长链表的指针向前移动到剩余节点数与短链表相同
# 接下来两个指针同时向前移动，只要移动过程指向同一个节点，就找到了答案
# 时间复杂度 O(m + n)，空间复杂度 O(1)
class Solution1:
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:
        """
        思路一：计算两个链表的长度，让长链表的指针先走长度差步，
        然后两个指针同步前进，首次相遇点即为交点。
        """
        if not headA or not headB:
            return None
        # 上面这句代码不要也是正确的，但可以保留，一个是后面思考的时候可以简化思考，直接考虑两个链表都非空的处理
        # 此外如果输入是一个空链表加上一个长链表，这个判断避免了遍历长链表
        # 1. 计算两个链表的长度
        lenA, lenB = 0, 0
        pA, pB = headA, headB
        while pA:
            lenA += 1
            pA = pA.next
        while pB:
            lenB += 1
            pB = pB.next

        # 重置指针到头部
        pA, pB = headA, headB

        # 2. 将较长链表的指针向前移动，以对齐它们的起跑线
        if lenA > lenB:
            for _ in range(lenA - lenB):
                pA = pA.next
        else:
            for _ in range(lenB - lenA):
                pB = pB.next

        # 3. 两个指针同步前进，直到它们相遇
        while pA != pB:
            pA = pA.next
            pB = pB.next

        # 如果相遇，pA就是交点；如果不相交，最终pA和pB会同时到达None
        return pA


# 思路二
# 比较巧妙，但时间复杂度不变，本身并不会有显著性能优势，但写的代码会比较简洁
# 使用两个指针 pA 和 pB，分别从 headA 和 headB 开始遍历
# 当 pA 遍历到链表 A 的末尾时，让它指向链表 B 的头部；同样，当 pB 遍历到链表 B 的末尾时，让它指向链表 A 的头部
# 这样，两个指针最终会在相交点相遇
# 设链表 A 不相交的部分长度为 a，链表 B 不相交的部分长度为 b，相交的公共部分长度为 c
# 指针 pA 的行走路径：先走完 A (a+c)，然后从 B 的头部开始走
# 指针 pB 的行走路径：先走完 B (b+c)，然后从 A 的头部开始走
# 在交点相遇时：pA 走过的总路程 = a + c + b，pB 走过的总路程 = b + c + a
# 既然路程相等，速度也一样（每次一步），它们必然会在走完这段路程时相遇在同一个点，这个点就是交点
# 如果不相交呢，此时 c = 0
# pA 的路程：走完 a，再走完 b。总路程 a+b
# pB 的路程：走完 b，再走完 a。总路程 b+a
# 它们走完各自的总路程后，会同时到达终点 None
class Solution2:
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:
        """
        思路二：双指针法。让两个指针分别遍历两个链表，
        当一个指针到达末尾时，就从另一个链表的头部重新开始。
        这样可以保证两个指针走过的总路程相同，若有交点则必定在交点相遇。
        路径 A -> B 和 路径 B -> A 的长度都是 len(A) + len(B)。
        """
        if not headA or not headB:
            return None

        pA, pB = headA, headB

        while pA != pB:
            # 如果pA走到了尽头，就让他去走链表B的路
            # 否则，就正常走一步
            pA = pA.next if pA else headB

            # pB同理
            pB = pB.next if pB else headA
            # 注意由于如果不相交，要比较两个 None，所以 pA 和 pB 都要走到 None

        # 循环结束时，pA和pB要么在交点相遇，要么都为None
        return pA


# 空间换时间的方法，利用一个哈希集合作为辅助数据，来快速判断节点是否被访问过
# 时间复杂度 O(M + N)，空间复杂度 O(M)，M 为 A 的长度。
class Solution3:
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:
        # 如果 A 或者 B 是空链表，都会最终返回 None，所以开始不需要任何判断
        nodes_in_A = set()

        # 遍历链表 A，将节点添加到集合中
        current_A = headA
        while current_A:
            nodes_in_A.add(current_A)
            current_A = current_A.next

        # 遍历链表 B，检查每个节点是否已存在于集合中
        current_B = headB
        while current_B:
            if current_B in nodes_in_A:
                # 如果存在，说明找到了第一个相交节点，立即返回
                return current_B
            current_B = current_B.next

        # 如果遍历完 B 都没有找到，则说明没有交点
        return None
