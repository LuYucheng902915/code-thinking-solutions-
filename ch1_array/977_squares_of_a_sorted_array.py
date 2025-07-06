# 977. Squares of a Sorted Array
# https://leetcode.cn/problems/squares-of-a-sorted-array/

from typing import List


# 直接排序法(O(nlogn))
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        return sorted(x * x for x in nums)
        # 上面那句sorted的参数是一个生成器，里面省略了一个括号，函数调用唯一参数为生成器时，生成器括号可以省略
        # sorted是一个内置函数，接收任意可迭代对象作为参数
        # 但是对于排序函数，你必须要先知道所有数据
        # 一个懒惰的生成器一次只能生成一个值，所以sorted函数接收生成器作为参数，必须消费这个生成器，把里面的元素取出来
        # 放入sorted函数内部的一个临时列表中，然后再排序
        # 所以这三种写法实现上类似，都必须先生成一个列表，然后对列表排序，性能也基本类似
        # 第一种写法列表是sorted函数内部隐式创建的，另外两种是显式创建的
        # 生成器几乎不需要开销，而且还可能由于让sorted()函数更直接地控制整个迭代和填充过程，开销更小
        # 第一种写法最简洁，是推荐的写法
        # return sorted([x * x for x in nums])
        # 上面这句是列表推导式生成列表，再排序
        # return sorted(list(x * x for x in nums))
        # 上面这句将生成器转换为列表后再排序，但这种写法意义不大


# 直接排序法写法二
class Solution1:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        for i in range(len(nums)):
            nums[i] *= nums[i]
        nums.sort()
        return nums


# 直接排序写法三
class Solution2:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        ans = []
        for num in nums:
            ans.append(num**2)
        ans.sort()
        # 列表的.sort()方法，只接受列表作为对象，会就地修改列表本身，使其有序，返回值是None
        return ans


# 直接排序写法四
class Solution3:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        new = [x * x for x in nums]
        new.sort()
        return new
        # list.sort()改变原列表，sorted(list)不改变列表


# 双指针法，O(n)的时间复杂度
class Solution4:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        size = len(nums)
        left, right = 0, size - 1
        write_idx = size - 1
        results = [0] * size  # 这是生成全0列表的标准写法
        # results = [0 for _ in range(size)]，在这个简单场景下，第一种更常用

        while left <= right:  # write_idx >= 0也可以，等价条件，这里选择与后面一致的写法
            left_square = nums[left] * nums[left]
            right_square = nums[right] * nums[right]
            if left_square > right_square:
                results[write_idx] = left_square
                left += 1
            else:
                results[write_idx] = right_square
                right -= 1

            write_idx -= 1

        return results


# 双指针法，最后反转列表，可以减少一个变量write_idx，改为append方法添加元素
class Solution5:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        # 根据list的先添加排序在前原则
        # 将nums的平方按从大到小的顺序添加进新的list
        # 最后反转list
        results = []  # 注意使用append，就不能用results = [0] * len(nums)，必须初始化空列表
        # 否则结果的results变成size*2长，末尾有size个零元素
        left, right = 0, len(nums) - 1
        while left <= right:
            if abs(nums[left]) > abs(nums[right]):
                results.append(nums[left] ** 2)
                left += 1
            else:
                results.append(nums[right] ** 2)
                right -= 1
        return results[::-1]


# 进一步优化
class Solution6:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        """
        整体思想：有序数组的绝对值最大值永远在两头，比较两头，平方大的插到新数组的最后
        1. 优化所有元素为非正或非负的情况
        2. 头尾平方的大小比较直接将头尾相加与0进行比较即可
        3. 新的平方排序数组的插入索引可以用倒序插入实现(针对for循环, while循环不适用)
        """
        # 特殊情况, 元素都非负（优化1）
        if nums[0] >= 0:
            return [num**2 for num in nums]  # 按顺序平方即可
        # 最后一个非正，全负有序的
        if nums[-1] <= 0:
            return [num**2 for num in nums[::-1]]  # 倒序平方后的数组
        # 这里返回不能写return (num**2 for num in nums)
        # 这样返回一个生成器对象，不是list，会报错
        # 但返回sorted(num**2 for num in nums)是可以的
        # sorted函数的参数虽然是生成器，但sorted()函数返回结果是list。
        # (x**2 for x in nums) 这部分（注意是圆括号）创建了一个“懒惰的”生成器，它本身不进行计算
        # sorted() 函数接收到这个生成器后，会把它“耗尽”——即，从生成器中取出所有的值（逐个计算平方），存储到一个临时列表里

        # 一般情况, 有正有负
        left = 0  # 原数组头索引
        right = len(nums) - 1  # 原数组尾部索引
        results = [0] * len(nums)  # 新建一个等长数组用于保存排序后的结果
        # write_idx = len(nums) - 1  # 新的排序数组(是新数组)尾插索引, 每次需要减一（优化3优化了）

        for write_idx in range(len(nums) - 1, -1, -1):
            # (优化3，倒序，不用单独创建变量，更加pythonic风格的写法)
            # if nums[left] ** 2 >= nums[right] ** 2:
            if nums[left] + nums[right] <= 0:  # (优化2)
                results[write_idx] = nums[left] ** 2
                left += 1
                # end_index -= 1  (优化3)
            else:
                results[write_idx] = nums[right] ** 2
                right -= 1
                # end_index -= 1  (优化3)
        return results
