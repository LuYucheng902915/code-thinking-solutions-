# 142. 环形链表 II
# https://leetcode.cn/problems/linked-list-cycle-ii/

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# --- 方法一：快慢指针法 (Floyd 判环算法) ---
# 这是本题的标准最优解，思路巧妙，空间复杂度为 O(1)。
#
# 核心思想:
# 算法分为两个阶段：
# 1. 判断环的存在并找到相遇点：使用一个慢指针(slow)每次走一步，一个快指针(fast)每次走两步。
#    如果链表有环，fast 最终会在环内追上 slow，两者相遇。如果 fast 走到链表末尾(None)，则无环。
# 2. 寻找环的入口：当快慢指针相遇后，将任意一个指针（例如 ptr）重新指向链表头部 head，
#    另一个指针（例如 slow）留在相遇点。然后两个指针都以每次一步的速度前进，它们再次相遇的地方就是环的入口。
#
# 时间复杂度: O(N)
#   - 两个指针在链表中的移动次数不会超过链表长度的常数倍，因此是线性时间。
#
# 空间复杂度: O(1)
#   - 只使用了 slow, fast, ptr 等有限几个指针变量，与链表规模无关。
#
# 数学原理证明 (为什么第二阶段的相遇点是环的入口):
#   - 设定几个变量:
#     - 链表头(head)到环入口(entrance)的距离为 a。
#     - 环的周长为 b。
#     - 环入口(entrance)到快慢指针相遇点(meet)的距离为 c。
#
#   - 在第一阶段相遇时:
#     - 慢指针走过的路程: s_slow = a + c
#     - 快指针走过的路程: s_fast = a + n*b + c (n 为快指针在环内比慢指针多走的圈数)
#
#   - 因为快指针的速度是慢指针的 2 倍，所以路程也是 2 倍:
#     - s_fast = 2 * s_slow
#     - a + n*b + c = 2 * (a + c)
#     - a + n*b + c = 2a + 2c
#     - n*b = a + c
#
#   - 这个公式 n*b = a + c 非常关键，我们可以对它进行变换:
#     - a = n*b - c
#     - a = (n-1)*b + (b - c)
#
#   - 这个变换后的公式 a = (n-1)*b + (b - c) 告诉我们一个惊人的事实:
#     - "从链表头(head)到环入口(entrance)的距离 a" 恰好等于
#       "从相遇点(meet)走 (n-1) 圈环，再走 b-c 的距离"。
#     - (b-c) 是什么？它正是从相遇点(meet)沿着环走回到环入口(entrance)的距离。
#
#   - 因此，如果一个指针 ptr 从 head 出发，另一个指针 slow 从 meet 点出发，都以相同的速度前进，
#     ptr 走了 a 步到达 entrance，而 slow 走了 a 步（即 (n-1)圈 + (b-c)步）后，也恰好到达 entrance。
#     所以，它们的相遇点就是环的入口。
class Solution_Optimal:
    def detectCycle(self, head):
        slow, fast = head, head

        # 阶段一：判断是否有环，并找到相遇点
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                # 找到相遇点，跳出循环
                break
        else:
            # 如果循环正常结束，说明 fast 走到了尽头，无环
            return None

        # 阶段二：寻找环的入口
        # 将一个新指针 ptr 置于链表头部
        ptr = head
        # ptr 和 slow 指针以相同速度前进，相遇点即为环入口
        while ptr != slow:
            ptr = ptr.next
            slow = slow.next

        return ptr


# --- 方法二：哈希表法 ---
# 这是最直观、最容易想到的解法。
#
# 核心思想:
#   遍历链表，使用一个哈希集合(Set)来存储所有已经访问过的节点。
#   在遍历过程中，如果遇到的节点已经存在于哈希集合中，那么这个节点就是
#   第一个被重复访问的节点，也就是环的入口。
#
# 时间复杂度: O(N)
#   - N 是链表的节点数。每个节点最多被访问和插入哈希集合一次。
#   - 哈希集合的 add 和 in 操作的平均时间复杂度为 O(1)。
#
# 空间复杂度: O(N)
#   - 在最坏情况下（链表无环或环非常大），需要存储所有 N 个节点。
class Solution_HashSet:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited = set()
        current = head

        while current:
            if current in visited:
                return current

            visited.add(current)
            current = current.next

        return None


# --- 方法三：列表法 ---
# 这是哈希表法的一个变体，用列表代替哈希集合。
# 主要用于教学，以展示不同数据结构带来的巨大性能差异。
#
# 核心思想:
#   与哈希表法完全相同，只是存储已访问节点的容器换成了列表(List)。
#
# 时间复杂度: O(N^2)
#   - 循环 N 次。在第 k 次循环中，`in` 操作需要遍历一个长度为 k 的列表，耗时 O(k)。
#   - 总时间约为 1 + 2 + ... + (N-1) = N*(N-1)/2，所以是 O(N^2)。
#   - 对于大数据量，此方法会超时。
#
# 空间复杂度: O(N)
#   - 同样需要存储所有访问过的节点。
class Solution_List:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited = []
        current = head

        while current:
            # list 的 'in' 操作是线性扫描，非常耗时
            if current in visited:
                return current

            visited.append(current)
            current = current.next

        return None
