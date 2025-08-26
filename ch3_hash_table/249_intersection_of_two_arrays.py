# 249. Intersection of Two Arrays
# https://leetcode.cn/problems/intersection-of-two-arrays/


# 思路一，最地道和 Pythonic 的写法，三句话搞定
# 时间复杂度: O(M + N), M 和 N 分别是两个列表的长度
# 空间复杂度: O(M + N), 最坏情况下存储两个集合
# 这个解法非常简洁，它把哈希表的底层思想（创建集合、查找）和集合运算都封装起来
class Solution:
    def intersection(self, nums1: list[int], nums2: list[int]) -> list[int]:
        set1 = set(nums1)
        set2 = set(nums2)
        return list(set1 & set2)


# Python 3.7 后，字典有了顺序的概念
# Python 官方标准严格规定了字典的顺序必须与插入顺序一致
# 当用 for 循环遍历字典的时候，遍历的顺序是固定的
# 这提高了代码的可预测性和可调试性
# 对于集合，Python 官方没有相关规定，使用的哈希算法是默认开启哈希随机化来确保安全的
# 集合的顺序是无法预测的（不过如果一个终端反复运行，此时使用同一个哈希随机种子，如果有遍历集合元素的操作，遍历的顺序是不变的，这经过了实验验证）
# 但只要在不同终端运行同一个代码，遍历顺序也是不固定的，不能假定集合有任何顺序


# 思路二，手动实现哈希表（集合的查找），不适用 & 运算符，而是手动模拟查找过程
# 将空间复杂度优化到了 O(min(M, N))
class Solution1:
    def intersection(self, nums1: list[int], nums2: list[int]) -> list[int]:
        # 为了优化空间，总是用较短的数组来构建哈希集合
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1  # 交换，让 nums1 成为较短的那个

        lookup_set = set(nums1)
        result_set = set()  # 用集合来存储结果，自动处理唯一性

        for num in nums2:
            if num in lookup_set:
                result_set.add(num)

        return list(result_set)


# 思路三，排序加上双指针法
# 这是一个不使用哈希表，在特定情况下（例如内存限制严格）非常有用的经典算法
# 时间复杂度为 O(NlogN + MlogM)，空间复杂度为 O(1)
class Solution2:
    def intersection(self, nums1: list[int], nums2: list[int]) -> list[int]:
        nums1.sort()
        nums2.sort()

        p1, p2 = 0, 0
        result: list[int] = []

        while p1 < len(nums1) and p2 < len(nums2):
            if nums1[p1] < nums2[p2]:
                p1 += 1
            elif nums1[p1] > nums2[p2]:
                p2 += 1
            else:  # 相等
                # 保证结果的唯一性，只有当结果列表为空或当前元素与最后一个元素不同时才添加
                if not result or nums1[p1] != result[-1]:
                    result.append(nums1[p1])
                p1 += 1
                p2 += 1

        return result
