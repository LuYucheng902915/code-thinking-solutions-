# 209. Minimum Size Subarray Sum
# https://leetcode.cn/problems/minimum-size-subarray-sum/

import bisect
from typing import List

# bisect 是 Python 的一个标准库（Standard Library），不需要用 pip 安装
# 只要环境中安装了 Python，就可以通过 import bisect 导入标准库

# bisect 模块的核心功能是在已排序的序列（主要是列表）中，高效地执行二分查找（Binary Search），并维持其排序状态
# 有一个很长的、已排序的列表，现在需要频繁地向其中插入新元素，同时还要保持列表的有序状态
# 常规的低效做法：my_list.append(new_item) 然后再 my_list.sort()。append 很快（O(1)），但 sort() 很慢（O(NlogN)）。每次都重排整个列表，开销巨大
# bisect 的高效做法：bisect 模块使用二分查找来定位插入点，这个过程非常快（O(logN)）。然后执行插入操作（O(N)）。对于频繁插入的场景，这远比“追加再排序”要高效
# bisect 模块主要提供了两组核心功能，每组都有 _left 和 _right 两个版本

# 查找插入点：bisect.bisect_left() 和 bisect.bisect_right()
# 这两个函数只告诉你新元素应该插入到哪个索引位置，但不会真的执行插入操作
# bisect.bisect_left(a, x):
# 功能：在已排序的列表 a 中，查找 x 合适的插入点，并返回该点的索引。这个插入点是所有大于或等于 x 的元素中最左边（第一个）的位置
# 如果 x 大于 a 中所有元素，返回的是列表的长度 len(a)
# 这个返回值非常有意义，因为它正好是新元素应该被插入的索引位置，相当于执行 list.append() 的效果（或者说按索引插入列表，如果索引等于列表长度，就是在列表末尾添加元素）
# bisect.bisect_right(a, x) (它还有一个别名 bisect.bisect(a, x))：
# 功能：与 _left 类似，但如果 x 已经存在，它会返回现有元素右侧的插入点索引
# 可以理解为：它返回的索引是所有严格大于 x 的元素中中最左边元素的索引
# 如果列表有很多元素在排序上与插入的元素相等，left 把插入元素放在最左边，right 把插入元素放在最右边

# 查找并插入：bisect.insort_left() 和 bisect.insort_right()
# 这两个函数是“查找并执行”的版本，它们会自动完成插入操作
# bisect.insort_left(a, x):
# 功能：找到 x 的左侧插入点，并直接将 x 插入到列表 a 中，保持列表有序
# bisect.insort_right(a, x) (别名 bisect.insort(a, x)):
# 功能：找到 x 的右侧插入点，并直接将 x 插入到列表 a 中
# insort_left(a, x) 内部调用 bisect_left(a, x) 来得到一个索引 i，然后执行 a.insert(i, x)
# insort_right(a, x) 内部调用 bisect_right(a, x) 来得到一个索引 j，然后执行 a.insert(j, x)

# insort_left/right 不返回任何值（或者说，它返回 None）
# 这是一个 Python 中非常重要的设计约定（Design Convention）
# 一个函数或方法，如果它直接修改（in-place modification）一个可变对象（比如列表），那么它应该返回 None
# 为了明确地区分两种操作：返回一个新对象的函数，比如内置函数 sorted(a)，它会返回一个新的排好序的列表，而原列表 a 保持不变
# 直接修改原对象的函数/方法：比如列表方法 a.sort()，它会直接在 a 上进行排序，不创建新列表，因此它返回 None。bisect.insort_left(a, x) 就属于这一类

# insort_left/right 对于 Python 内置类型组成的列表，插入位置不同，结果相同
# 这是因为 Python 内置类型的比较，比如元组，会从左到右逐个元素比较。如果第一个元素相同，就比较第二个，以此类推
# 因此除非两个对象完全相同，否则比较结果总是不等的，于是这些相同的元素，插入在最左边还是最右边结果看起来没有区别

# Python的排序工具（包括 bisect 和 sort）在进行比较时，只依赖于小于号 < 操作符（在类中对应 __lt__ 特殊方法）
# 它不使用 >、== 或其他比较符。所有的排序决策都基于 a < b 的返回结果是 True 还是 False
# 由此可以推导出排序意义上的相等（Equivalence）：当 not (a < b) 和 not (b < a) 同时成立时，排序算法就认为 a 和 b 在排序上是等价的。在Student 例子中，只要两个学生分数相同，它们就是等价的
# bisect_left(a, x): 它在寻找第一个不小于 x 的位置。其内部循环在查找第一个索引 i，使得 not (a[i] < x) 为 True
# bisect_right(a, x): 它在寻找第一个严格大于 x 的位置。内部循环在查找第一个索引 i，使得 x < a[i] 为 True

# Python 作为面向对象语言，可以自定义比较的规则，比如下面的例子，可以通过定义类的特殊方法（比如 __lt__，即小于 < 操作符）
# 这告诉 Python,例如比较对象时，可以只比较特定的属性，忽略其他属性。这使得两个内容不完全相同的对象，在排序意义上“相等了”
# 此时在 left 还是 right 插入，结果就有了明显的区别，下面的例子形象说明了这一点

numbers = [10, 20, 20, 20, 30, 40]
target = 20
# 使用 bisect_left 查找 20 的插入点
# 它会返回第一个 20 的索引
idx_left = bisect.bisect_left(numbers, target)
print(f"在 {numbers} 中，20 的左侧插入点索引是: {idx_left}")  # -> 1
# 使用 bisect_right 查找 20 的插入点
# 它会返回最后一个 20 右侧的索引
idx_right = bisect.bisect_right(numbers, target)
print(f"在 {numbers} 中，20 的右侧插入点索引是: {idx_right}")  # -> 4

my_list = [10, 20, 30, 40]
n = len(my_list)  # n 等于 4
# 查找一个比所有元素都大的数，比如 50
idx_left = bisect.bisect_left(my_list, 50)
idx_right = bisect.bisect_right(my_list, 50)
print(f"列表长度是: {n}")
print(f"bisect_left(50) 返回: {idx_left}")  # -> 4
print(f"bisect_right(50) 返回: {idx_right}")  # -> 4
# 如果真的在这个索引位置插入，效果就是 append
my_list.insert(n, 50)
print(f"插入后列表: {my_list}")  # -> [10, 20, 30, 40, 50]


# 定义一个简单的学生类
class Student:
    def __init__(self, score, name):
        self.score = score
        self.name = name

    # 关键：我们只让Python根据分数来比较大小 (<)
    def __lt__(self, other):
        return self.score < other.score

    # 定义一个清晰的打印格式，显示名字和内存地址以区分不同对象
    def __repr__(self):
        return f"({self.score}, '{self.name}')"


# 1. 准备一个已按分数排好序的列表
# 为了区分，我们明确地创建每个对象
s1 = Student(75, "Alice")
s2 = Student(75, "Bob")
s3 = Student(90, "David")
students = [s1, s2, s3]
print(f"原始列表: {students}\n")
# 2. 创建一个新学生，分数也是75
# 对于排序来说，new_s 和 s1, s2 是“相等”的，因为 75 < 75 不成立
new_s = Student(75, "Eve")
# --- 实验开始 ---
# 3. 使用 insort_left
# 它会寻找第一个不小于 new_s 的位置，也就是 s1 的位置 (索引 0)
students_left = students.copy()
bisect.insort_left(students_left, new_s)
print(f"insort_left 结果: {students_left}")
# 新来的 'Eve' 被插在了所有老75分学生的前面
# 4. 使用 insort_right
# 它会寻找第一个严格大于 new_s 的位置，也就是 s3 的位置 (索引 2)
students_right = students.copy()
bisect.insort_right(students_right, new_s)
print(f"insort_right 结果: {students_right}")
# 新来的 'Eve' 被插在了所有老75分学生的后面


# 暴力法，O(N^2) 的时间复杂度
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        # min_len = float("inf") 导致类型检测错误
        # 下面这样写逻辑正确且不会引起静态类型检查错误
        min_len = n + 1

        for i in range(n):
            current_sum = 0
            for j in range(i, n):
                current_sum += nums[j]
                if current_sum >= target:
                    min_len = min(min_len, j - i + 1)
                    break

        # return min_len if min_len != float("inf") else 0
        # 上面的写法虽然实际逻辑不会返回 float，但是静态类型检查会报错
        return min_len if min_len != n + 1 else 0


# 滑动窗口法，O(N) 的时间复杂度
# 由于右指针从头到尾遍历整个数组，左指针在满足条件时向右移动，因此每个元素最多被访问两次（一次由右指针，一次由左指针）
# 因此，整体时间复杂度为 O(N)
class Solution1:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        min_len = n + 1
        current_sum = 0
        left = 0

        for right in range(n):
            current_sum += nums[right]

            while current_sum >= target:
                # 这里 while 是重点，不是 if，左指针可以移动多次
                min_len = min(min_len, right - left + 1)
                current_sum -= nums[left]
                left += 1

        return min_len if min_len != n + 1 else 0


# 结合前缀和的二分查找, O(NlogN) 的时间复杂度
class Solution2:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        min_len = n + 1
        prefix_sums = [0] * (n + 1)

        for i in range(n):
            prefix_sums[i + 1] = prefix_sums[i] + nums[i]

        for i in range(n):  # i 代表从 nums[i] 开始的子数组
            s = target + prefix_sums[i]
            # s 代表需要找到 >= target 的最小前缀和
            # 使用二分查找找到第一个大于等于 s 的前缀和的位置
            # bisect_left 返回的是第一个大于等于 s 的元素的索引
            # 如果没有找到，则返回 len(prefix_sums)
            # 在前缀和数组中，prefix_sums[j] - prefix_sums[i] 这个计算结果，精确地对应了原数组 nums 中子数组 nums[i:j]
            # nums[i:j] 包含了从索引 i 到 j-1 的所有元素，因此其长度为 j - i，而不是 j - i + 1，这一点一定要注意
            # 内层仍然可以通过循环的方法， j 从 i + 1 遍历到 n，当 prefix_sums[j] - prefix_sums[i] >= target 时
            # 说明从 i 到 j - 1 的子数组满足条件,此时检查 j - i 是否为当前最小长度。但这样做内层最坏会是 O(N)，所以整体时间复杂度为 O(N^2)
            # 二分查找由于前缀和数组递增（有序），可以将内层的查找时间复杂度降为 O(logN)，因此整体时间复杂度为O(NlogN)，但是代码不那么容易理解
            j = bisect.bisect_left(prefix_sums, s)

            if j != len(prefix_sums):
                min_len = min(min_len, j - i)

        return min_len if min_len != n + 1 else 0
