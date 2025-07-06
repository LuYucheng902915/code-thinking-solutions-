# 59. Spiral Matrix II
# https://leetcode.com/problems/spiral-matrix-ii/

from typing import List


# 时间复杂度为O(n^2)代码模拟螺旋式填充数字，每个位置访问并赋值一次。
# 自己实现的代码，可以通过测试
class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        # Results = [[0] * n] * n #这个一开始是自己写的初始化，是错误的
        # 下面两种都是正确的初始化方式，错误在于[0] * n 会创建一个包含 n 个 0 的列表，例如当 n=3 时，它创建了 [0, 0, 0]
        # [...] * n 这个操作，会将同一个列表对象复制 n 次，而不是创建 n 个独立的列表
        # 这意味着，Results 列表中的每一行都指向内存中完全相同的那个列表。当修改其中任何一行的任何一个元素时，所有行都会跟着一起改变，因为它们本质上是同一个东西

        # 根本原因就在于：整数（int）是不可变对象（Immutable），而列表（list）是可变对象（Mutable）
        # 当 * 被用于一个序列（比如列表）时，它的工作本质是复制引用（或“标签”）。获取序列中每个元素的引用，然后将这些引用重复N次，最后将它们放入一个新的列表中
        # 内层 [0] * n：Python首先执行这个操作，创建了一个列表对象，我们叫它 row_A
        # 外层 [row_A] * n：现在，Python执行外层的乘法。此时，外层列表 [...] 中只包含一个元素：对 row_A 这个列表对象的引用（标签）
        # * n 操作忠实地执行了它的任务：它把这个唯一的引用复制了 n 份，然后把这 n 个一模一样的引用装进了一个新列表里
        # 结果：得到了一个二维列表，但它的每一行其实都指向内存中同一个 row_A

        # 为什么 [0] * n 是安全的？[0]：这个列表包含一个元素：对整数对象 0 的引用
        # * n：操作符同样忠实地将这个对 0 的引用复制了 n 份。所以，你得到的列表 [0, 0, 0] 里面，每个元素确实都指向内存中同一个整数对象 0
        # 因为整数是不可变的！根本没有办法改变 0 这个对象本身
        # 当执行 my_list[0] = 99 这样的操作时：并不是在“修改” 0 这个对象
        # 是在“替换”列表第0个位置的引用。你把原来指向 0 的那个引用，换成了一个指向新对象 99 的引用
        # 这个操作对列表其他位置的元素（它们仍然指向 0）毫无影响

        # 对可变对象（如list, dict）使用 * n：非常危险！因为它创建了多个指向同一个可变对象的引用，修改一个等于修改全部
        # 对不可变对象（如int, str, tuple）使用 * n：通常是安全的。
        # 虽然它也创建了多个指向同一个对象的引用，但由于对象本身不可修改，你只能通过替换引用的方式来改变序列，不会产生联动修改的副作用。

        results = [[0 for _ in range(n)] for _ in range(n)]
        # Results = []
        # for _ in range(n):
        #     Results.append([0] * n)
        count = 0
        index = 0  # index 变量控制着当前正在填充的是从外到内的第几“圈”
        while (n - 2 * index - 1) >= 0:
            length = n - 2 * index - 1
            # length 变量控制着当前“圈”的边长，n - 2 * index - 1 是因为每次填充完一圈后，下一圈的边长会减少 2
            if (length) == 0:  # 处理了当 n 为奇数时，最中心那个元素的特殊情况
                count += 1
                results[index][index] = count

            else:  # 分四段生成每个圈的元素，每段都是length个元素
                for i in range(0, length):
                    count += 1
                    results[index][index + i] = count

                for i in range(0, length):
                    count += 1
                    results[index + i][index + length] = count

                for i in range(0, length):
                    count += 1
                    results[index + length][index + length - i] = count

                for i in range(0, length):
                    count += 1
                    results[index + length - i][index] = count

            index += 1

        return results


# 标准代码，可读性更强，变量可解释性更强，采用循环不变量和每条边相同的规则，本质上与上面代码相同
class Solution1:
    def generateMatrix(self, n: int) -> List[List[int]]:
        nums = [[0] * n for _ in range(n)]
        startx, starty = 0, 0  # 起始点
        loop, mid = n // 2, n // 2  # 迭代次数、n为奇数时，矩阵的中心点
        count = 1  # 计数

        for offset in range(1, loop + 1):  # 每循环一层偏移量加1，偏移量从1开始
            for i in range(starty, n - offset):  # 从左至右，左闭右开
                nums[startx][i] = count
                count += 1
            for i in range(startx, n - offset):  # 从上至下
                nums[i][n - offset] = count
                count += 1
            for i in range(n - offset, starty, -1):  # 从右至左
                nums[n - offset][i] = count
                count += 1
            for i in range(n - offset, startx, -1):  # 从下至上
                nums[i][starty] = count
                count += 1
            startx += 1  # 更新起始点
            starty += 1

        if n % 2 != 0:  # n为奇数时，填充中心点
            nums[mid][mid] = count
        return nums
