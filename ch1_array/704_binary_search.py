# 704. Binary Search
# https://leetcode.com/problems/binary-search/

# 本题注意开始确定区间的方式，左闭右闭区间和左闭右开区间，后面保持一致性
# 左闭右闭区间left <= right，right = middle - 1，left = middle + 1
# 左闭右开区间left < right，right = middle，left = middle + 1
# 保持使用middle = left + (right - left) // 2防溢出的好习惯

from typing import List

# List是一个类型提示，表示nums和target以及返回值的类型是列表和整数
# 从 Python 3.9 版本开始，不再需要从 typing 模块导入大写的 List、Dict 等类型，可以直接使用小写的内置容器类型（如 list, dict, tuple 等）来进行类型提示
# def search(self, nums: list[int], target: int) -> int:
# from typing import List以及def search(self, nums: List[int], target: int) -> int:可以保证后向兼容性
# 当一个新版本的软件或系统，能够正确地处理、运行或打开用旧版本创建的数据或代码时，我们就说这个新版本是“向后兼容”的
# 主体是新版本，它回头“向后”看，去兼容旧版本的东西
# 当一个旧版本的软件或系统，能够正确地处理、运行或打开用新版本创建的数据或代码时，我们就说这个旧版本是“向前兼容”的
# 这通常非常困难


# 左闭右闭区间, O(log n)的时间复杂度
class Solution(object):
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            middle = left + (right - left) // 2

            if nums[middle] > target:
                right = middle - 1
            elif nums[middle] < target:
                left = middle + 1
            else:
                return middle

        return -1


# 左闭右开区间
class Solution2(object):
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)

        while left < right:
            middle = left + (right - left) // 2

            if nums[middle] > target:
                right = middle
            elif nums[middle] < target:
                left = middle + 1
            else:
                return middle

        return -1
