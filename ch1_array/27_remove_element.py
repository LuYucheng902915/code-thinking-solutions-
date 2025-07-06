# 27. Remove Element
# https://leetcode.cn/problems/remove-element/

from typing import List


# 下列算法空间复杂度均为O(1)
# 直接删除元素的方式，O(n^2)的时间复杂度,从后往前删除元素，效率比从前往后删略高
class Solution(object):
    def removeElement(self, nums: List[int], val: int) -> int:
        i = len(nums) - 1

        while i >= 0:
            if nums[i] == val:
                del nums[i]

            i -= 1

        return len(
            nums
        )  # 技巧 del会改变原数组的长度，所以len(nums)可以直接返回删除后数组的长度


# 不使用del自己实现移动元素，O(n^2)的时间复杂度
class Solution1(object):
    def removeElement(self, nums: List[int], val: int) -> int:
        size = len(nums)
        i = size - 1

        while i >= 0:
            if nums[i] == val:
                for j in range(i, size - 1):
                    # 一定要注意第二个是size - 1，j只能取到数组倒数第二个元素的索引
                    nums[j] = nums[j + 1]

                size -= 1

            i -= 1

        return size


# 与第二个完全一样，用for循环，不需要i -= 1
class Solution2(object):
    def removeElement(self, nums, val):
        size = len(nums)

        for i in range(size - 1, -1, -1):
            if nums[i] == val:
                for j in range(i, size - 1):
                    nums[j] = nums[j + 1]

                size -= 1

        return size


# 快慢指针法，赋值次数等于需要保留的元素数量，O(n)的时间复杂度
# 快指针负责遍历整个原始数组，去寻找所有应该被保留下来的新数组的元素（即不等于 val 的元素）
# 慢指针它指向新数组中下一个应该被填充元素的位置。慢指针以及它之前的所有元素，构成了处理后有效的新数组
# 算法结束后慢指针的值就是新数组的长度
class Solution3(object):
    def removeElement(self, nums: List[int], val: int) -> int:
        slow, fast = 0, 0
        size = len(nums)

        while fast < size:
            if nums[fast] != val:
                # 发现了要保存的元素，如果是要删除的元素，就慢指针不变（不保留）。快指针一直加一，访问下一个元素
                nums[slow] = nums[fast]
                slow += 1

            fast += 1

        return slow


# 双指针法，赋值次数等于需要删除的元素数量，但会改变保留的元素的顺序,O(n)的时间复杂度
# 这种方法适用于需要删除的元素较少的情况
# 算法的最后，左/右指针的值就是新数组的长度
class Solution4(object):
    def removeElement(self, nums: List[int], val: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            if nums[left] == val:
                # 如果当前元素等于val，说明它是需要删除的元素
                # 从数组的最右边（right 指针的位置）拿来一个元素，直接覆盖掉当前 nums[left] 的值
                # 右边界向内收缩 (right -= 1)。这么做是因为 nums[right] 的那个元素已经被“用掉”了（移到了左边），所以有效数组的末尾就少了一位
                # 此时 left 指针不移动！因为从右边换过来的新 nums[left] 可能是另一个 val，需要下一轮循环再次对 left 位置进行检查
                right -= 1
            else:
                # 如果当前元素不等于val，说明它是需要保留的元素，不需要用右指针指向的元素覆盖
                # 只需要移动左指针
                left += 1

        return left
