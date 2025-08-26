# 开发商购买土地
# https://kamacoder.com/problempage.php?pid=1044
import sys
from itertools import accumulate

input = sys.stdin.readline


def main1():
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        # 每次循环读取新的一行，分割并转换为整数列表
        # list() 是 Python 的一个内置函数，但更准确地说，它是一个类型构造函数 (Type Constructor)。它的核心功能之一就是接收一个可迭代对象 (iterable)，并将其所有元素“取出”，然后用这些元素构建并返回一个全新的列表
        # map(int, input().split()) 会创建一个 map 对象。这个 map 对象正是一种可迭代对象
        # list() 构造函数拿到了这个 map 对象
        # 它开始对 map 对象进行迭代，就像 for 循环一样，向它索要第一个元素
        # map 对象执行 int('...')，返回第一个整数。list() 把它放进自己正在构建的新列表里
        row = list(map(int, input().split()))
        matrix.append(row)


if __name__ == "__main__":
    main1()


# 自己的解答，可以通过
# 这个问题也是前缀和的典型应用
# 当我们看到问题需要频繁地、重复地查询一个固定数组中不同连续子数组的和
# 就应该立刻想到使用前缀和
# 它的核心思想就是“预处理”。我们通过一次 O(N) 的计算，预先存储了从头开始到每个位置的累加和
# 这样做带来的巨大好处就是，在后续的查询阶段，任何子数组的和都可以通过一次减法
# 在 O(1) 的时间复杂度内得出
# 它是一种典型的“空间换时间”策略，通过一次性的预处理（O(N) 时间和 O(N) 空间）
# 将后续每一次查询的耗时从 O(N) 降到了 O(1)，极大地提高了处理多次查询的效率

# import sys
input = sys.stdin.readline


def main2():
    n, m = map(int, input().split())
    nums = []
    for _ in range(n):
        row = list(map(int, input().split()))
        nums.append(row)
    min_dif = float("inf")
    sum_col = [0 for _ in range(m + 1)]
    for j in range(m):
        sum_temp = 0
        for i in range(n):
            sum_temp += nums[i][j]
        sum_col[j + 1] = sum_col[j] + sum_temp
    for j in range(m):
        if abs(sum_col[-1] - 2 * sum_col[j + 1]) < min_dif:
            min_dif = abs(sum_col[-1] - 2 * sum_col[j + 1])
    sum_row = [0 for _ in range(n + 1)]
    for i in range(n):
        sum_temp = 0
        for j in range(m):
            sum_temp += nums[i][j]
        sum_row[i + 1] = sum_row[i] + sum_temp
    for i in range(n):
        if abs(sum_row[-1] - 2 * sum_row[i + 1]) < min_dif:
            min_dif = abs(sum_row[-1] - 2 * sum_row[i + 1])
    print(min_dif)


if __name__ == "__main__":
    main2()

# 上面这个算法时间复杂度是 O(n * m) 在时间复杂度，
# 由于任何算法都需要读取一次所有n * m 次个区块权值才能计算 O(n * m) 是这个算法理论最低时间复杂度
# 不过，我们还可以对算法进行一些优化，获得实际运行时可能更少的计算次数
# 前缀和保证了每一次切分后，不需要重新求子区域的和
# 首先代码在处理上有一个逻辑问题，那就是for j in range(m):
# 当 j 取 m，含义是 0, m 切分，这不符合题意
# 之前的前缀和由于要计算某些连续元素的和，引入一个前面补0的前缀和数组会更方便
# 通过在最前面补一个 0，我们可以用一个统一的公式 prefix_sum[b + 1] - prefix_sum[a] 来处理所有情况
# 本题不需要计算连续元素的和，自然不需要补0，一定要根据题目选择合理的数据结构
# 其次，由于这个算法不需要计算连续子数组的和，而是比较总前缀和减去部分前缀和乘以二中绝对值最小值
# 这意味着前缀和数组分别为m和n个元素就可以了。更具体说，首先存储 m * n 的所有元素和
# 然后计算1列，前2列，前n-1列和，求所有元素和减去部分和两倍的绝对值的最小值即可
# 对于列也同理。一共希望计算出n-1个列的前缀和，m-1个行的前缀和。最后一个 n 列/ n 行前缀和（所有元素和）是相同的
# 这些可以对矩阵遍历一次就可以全部得到，而之前的代码遍历了两次，效率较低

# 优化后的代码
# import sys
input = sys.stdin.readline


def main3():
    n, m = map(int, input().split())
    nums = [list(map(int, input().split())) for _ in range(n)]
    # 最简洁的一句话推导式生成二维list
    row_sums = [0] * n
    column_sums = [0] * m
    total_sum = 0
    for i in range(n):
        for j in range(m):
            row_sums[i] += nums[i][j]
            column_sums[j] += nums[i][j]
    # 这里先不求前缀和，而是求每行/每列的和并存储，一维化，之后再求前缀和
    # 你没法一个循环就求解行/列方向的前缀和
    # 因为本题只计算绝对值（总和- 2 * 前缀和）的最小值，只要遍历前缀和一次
    # 之前区间和问题面临的是多次任意查询，要保存前缀和
    # 所以本题不用保存前缀和
    total_sum = sum(row_sums)
    min_diff = float("inf")
    current_top_sum = 0
    for i in range(n - 1):
        current_top_sum += row_sums[i]
        diff = abs(total_sum - 2 * current_top_sum)
        if diff < min_diff:
            min_diff = diff
    current_left_sum = 0
    for j in range(m - 1):
        current_left_sum += row_sums[j]
        diff = abs(total_sum - 2 * current_left_sum)
        if diff < min_diff:
            min_diff = diff
        # 更简洁的写法
        # min_diff = min(min_diff, abs(total_sum - 2 * current_left_sum))

    print(min_diff)


if __name__ == "__main__":
    main3()


# nums = [list(map(int, input().split())) for _ in range(n)]
# 这行代码是一个列表推导式 (List Comprehension)，其执行过程可以分解如下：
# 迭代控制：外层的 for _ in range(n): 是迭代控制器。它规定了方括号内的表达式需要被独立执行 n 次，每一次对应输入的一行
# 单行处理表达式：在每一次循环中，都会完整地执行 list(map(int, input().split())) 这个表达式。我们从内到外分析它：
# input(): 调用 sys.stdin.readline()，从标准输入流中读取一行，返回一个字符串，例如 "1 2 3\n"
# .split(): 这是一个字符串方法。当不带参数调用时，它会按任意空白（空格、制表符、换行符等）分割字符串，并返回一个字符串列表。例如，"1 2 3\n".split() 会得到 ['1', '2', '3']。这个列表是一个可迭代对象 (iterable)
# map(int, ...): map 是一个高阶函数，它接收一个函数（int）和一个可迭代对象（上一步得到的 ['1', '2', '3']）作为参数
# 它不会立即执行计算，而是返回一个 map 对象。这个对象是一个迭代器 (iterator)，它封装了“将 int 函数应用于 ['1', '2', '3'] 中每一个元素”的这个操作逻辑。
# map 的第二个参数（.split() 的结果）必须是可迭代的。同时，map 函数本身返回的 map 对象，也同样是可迭代的（更准确地说，它是一个迭代器）
# list(...): 这是一个类型构造函数。它接收一个可迭代对象（这里是 map 对象）作为参数，并通过迭代它来创建一个新的列表。
# 它会触发 map 对象的迭代过程：list 构造函数向 map 对象索要第一个元素，map 对象于是对 '1' 执行 int 函数得到 1 并返回；接着索要第二个，得到 2；以此类推
# list 构造函数将所有从 map 对象中获取到的结果（1, 2, 3）收集起来，构建成一个全新的整数列表 [1, 2, 3]
# 列表推导式将每一次循环中新创建的行列表（如 [1, 2, 3]）收集起来，最终构建成一个包含 n 个行列表的二维列表 nums
# 只要一个东西能被用在 for 循环里，它就是可迭代的。.split() 返回的列表和 map() 返回的 map 对象都符合这个条件


# 暴力+优化解法：复杂度也为O(n*m)
def main4():
    import sys

    input = sys.stdin.read
    data = input().split()

    idx = 0
    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    sum = 0
    vec = []
    for i in range(n):
        row = []
        for j in range(m):
            num = int(data[idx])
            idx += 1
            row.append(num)
            sum += num
        vec.append(row)

    result = float("inf")

    count = 0
    # 行切分
    for i in range(n):
        for j in range(m):
            count += vec[i][j]
            # 遍历到行末尾时候开始统计
            if j == m - 1:
                result = min(result, abs(sum - 2 * count))

    count = 0
    # 列切分
    for j in range(m):
        for i in range(n):
            count += vec[i][j]
            # 遍历到列末尾时候开始统计
            if i == n - 1:
                result = min(result, abs(sum - 2 * count))

    print(result)


if __name__ == "__main__":
    main4()


# 最终格式较好的版本
# import sys

input = sys.stdin.readline


def main5():
    n, m = map(int, input().split())
    nums = [list(map(int, input().split())) for _ in range(n)]

    row_sum = [0 for _ in range(n)]
    column_sum = [0 for _ in range(m)]

    for i in range(n):
        for j in range(m):
            row_sum[i] += nums[i][j]
            column_sum[j] += nums[i][j]

    total_sum = sum(row_sum)
    min_dif = float("inf")

    current_top_sum = 0
    for i in range(n - 1):
        current_top_sum += row_sum[i]
        min_dif = min(min_dif, abs(total_sum - 2 * current_top_sum))

    current_left_sum = 0
    for j in range(m - 1):
        current_left_sum += column_sum[j]
        min_dif = min(min_dif, abs(total_sum - 2 * current_left_sum))

    print(min_dif)


if __name__ == "__main__":
    main5()


# 更加优化的代码 书写更简洁
# import sys

# 使用别名 input 来加速读取，这是一个在算法竞赛中非常常见的技巧
# 它不会影响代码在 LeetCode 等平台上的运行
input = sys.stdin.readline


def main6():
    n, m = map(int, input().split())
    nums = [list(map(int, input().split())) for _ in range(n)]
    # --- 改进 1: 使用列表推导式和 sum() 函数计算每行的和 ---
    # 原写法：使用嵌套for循环，逻辑清晰，但代码稍长
    # 新写法：代码更简洁，意图更明确，读起来像自然语言
    # row 是行向量，sum(row) 就是行和
    row_sum = [sum(row) for row in nums]

    # --- 改进 2: 使用 zip(*nums) 技巧计算每列的和 ---
    # 原写法：使用嵌套for循环，通用且易于理解
    # 新写法：这是一个更高级的Python技巧。zip(*nums)能巧妙地将矩阵转置
    # 把它作为一个技巧记忆，能实现矩阵转置，这不直观，不容易理解
    # 转置后列和就是转置矩阵的行和，很巧妙
    # 然后我们可以方便地对转置后的每一行（即原始矩阵的每一列）求和
    column_sum = [sum(col) for col in zip(*nums)]

    # 虽然访问了数组两次，但使用了列表推导式，不需要初始化数组，并且更简洁，
    # 列表推导式是生成列表的“专业团队”，有python专门实现的底层优化，速度可能更快。
    total_sum = sum(row_sum)
    min_dif = float("inf")

    # 计算所有可能的横向切分
    current_top_sum = 0
    # 我们只切 n-1 刀，所以循环到 n-2 的位置
    for i in range(n - 1):
        current_top_sum += row_sum[i]
        # abs(total_sum - 2 * current_sum) 是计算差值的标准高效公式
        min_dif = min(min_dif, abs(total_sum - 2 * current_top_sum))

    # 计算所有可能的纵向切分
    current_left_sum = 0
    # 我们只切 m-1 刀，所以循环到 m-2 的位置
    for j in range(m - 1):
        current_left_sum += column_sum[j]
        min_dif = min(min_dif, abs(total_sum - 2 * current_left_sum))

    print(min_dif)


# 使用标准的 "入口守卫"，这是一个非常专业的好习惯
if __name__ == "__main__":
    main6()


# 在Python中，当星号 * 被用在函数调用的参数位置时，它的作用是“解包” (Unpack) 一个可迭代对象（比如列表）
# “解包”的意思是，它会把列表的外层容器（方括号[]）“脱掉”，然后把里面的每个元素作为独立的、平级的参数传递给函数
nums = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# 如果我们调用 zip(*nums)，* 会首先作用于 nums，将其解包。所以，zip(*nums) 实际上等价于：
zip([1, 2, 3], [4, 5, 6], [7, 8, 9])
# *nums 将 nums 里的三个列表元素“解”了出来
# zip 函数接收到的不再是一个参数，而是三个独立的列表参数
# zip() 函数接收一个或多个可迭代对象作为参数，然后将它们“压缩”在一起
# 它的工作方式是：从每个传入的参数中，按顺序同时取出第 i 个元素。将取出的这些元素组合成一个元组（tuple）
# 重复这个过程，直到最短的那个输入参数被取完为止
# zip返回值也是一个迭代器对象，也是懒惰的
list_a = ["a", "b", "c"]
list_b = [1, 2, 3]
zipped_items = zip(list_a, list_b)
# 转换为列表查看结果
print(list(zipped_items))
# 输出 [('a', 1), ('b', 2), ('c', 3)]
# zip(*nums) 就巧妙地生成了一个新的可迭代对象，其中每个元素都对应于原始矩阵的一列。这个过程，在效果上就完成了矩阵的“转置”
# 原始矩阵 (3行4列)
matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
# 使用 zip(*matrix) 进行转置
transposed_matrix_iterator = zip(*matrix)
# 为了查看结果，我们将它转换为列表
transposed_list = list(transposed_matrix_iterator)
print("原始矩阵:")
for row in matrix:
    print(row)
print("\n转置后的结果 (4行3列):")
for col_tuple in transposed_list:
    print(col_tuple)

"""
在Python 3中，zip() 和 map() 这类内置函数都遵循惰性求值(Lazy Evaluation)的原则
它们被调用时，返回的并不是一个包含了所有结果的列表(List)，而是一个迭代器(Iterator)对象
这个迭代器对象本身只封装了生成结果所需的状态和转换逻辑
可以理解为一个“配方”或“指令集”——因此其自身的内存占用极小,为O(1)常数级别。它并不会预先计算并存储所有的结果
只有当这个迭代器被“消费”(例如,被 for 循环遍历,或被 list()、tuple() 等类型构造函数强制“物化”)时
它才会按需、逐一地计算并“产出”(yield)每一个结果值。一旦迭代器被完全消费(即遍历到末尾)，它就会被耗尽，无法再次使用
这种按需生成的机制，使得迭代器在处理大规模数据集或无限序列时具有无与伦比的内存效率,是Python中高效编程的一个核心思想
"""

# 更简洁的写法
# import sys
# from itertools import accumulate
input = sys.stdin.readline


def main():
    n, m = map(int, input().split())
    nums = [list(map(int, input().split())) for _ in range(n)]

    row_sum = [sum(row) for row in nums]
    column_sum = [sum(column) for column in zip(*nums)]
    total_sum = sum(row_sum)

    min_dif = float("inf")

    for part_sum in list(accumulate(row_sum))[:-1]:
        min_dif = min(min_dif, abs(total_sum - 2 * part_sum))
    for part_sum in list(accumulate(column_sum))[:-1]:
        min_dif = min(min_dif, abs(total_sum - 2 * part_sum))

    print(min_dif)


if __name__ == "__main__":
    main()

# 使用 itertools.accumulate 来生成前缀和，让代码意图更加“声明式”
# itertools.accumulate 可以生成一个迭代器，里面是累加的和
# accumulate(list)，输入的可迭代对象有多长，它生成的迭代器就能产出多少个值
# 在list()函数逐个消耗这个迭代器时，一个一个地计算并交出（yield）值

# 让我们以 row_sums = [10, 20, 30] 为例，来分解 list(accumulate(row_sums))[:-1] 这行代码：
# it = accumulate(row_sums):
# Python创建了一个accumulate迭代器对象，我们叫它 it
# 此时，it知道它需要处理的数据是 [10, 20, 30]，也知道计算规则是“累加”
# 内存中完全没有 [10, 30, 60] 这个列表。 it只是一个准备好工作的“厨师”
# list(it):
# list()函数开始向it这个“厨师”要“寿司”
# list()：“给我第1个值。” -> it计算并交出
# list()：“给我第2个值。” -> it用内部记住的10，加上row_sums里的20，计算出30并交出
# list()：“给我第3个值。” -> it用内部记住的30，加上row_sums里的30，计算出60并交出
# list()：“还有吗？” -> it发现row_sums已经用完了，于是发出一个“停止”信号
# list()函数收集了所有收到的值，在内存中创建了一个全新的列表 [10, 30, 60]
# [:-1]:
# 最后，对这个刚刚在内存中被物化 (materialize) 出来的列表 [10, 30, 60] 进行切片操作
# 得到最终结果 [10, 30]
# list(迭代器)这个操作会耗尽（exhaust）迭代器。之后，这个迭代器对象虽然还存在于内存中（如果你用一个变量名指向它的话），但它已经“空了”，无法再次提供任何数据
# 迭代器是一次性的
# 迭代器对象内部有一个状态，它会记住下一次应该返回哪个元素。当你通过 for 循环、list()、next()等方式请求数据时，它会交出下一个元素，并把自己的状态指向再下一个。当它交出最后一个元素后，它的状态就变成了“已耗尽”
# 这个过程是单向的、不可逆的。迭代器没有“倒带”或“重置”的功能（除非你重新创建一个）
# 如果一个迭代器需要支持“重置”，那它就必须有能力回到过去
# 要做到这一点，它就必须记住所有已经产生过的值，以备将来“重读”
# 如果迭代器记住了所有值：那它就退化成了一个列表！它会占用大量内存，完全违背了迭代器“用多少，算多少，省内存”的设计初衷
# 迭代器的承诺是：“我只占用极小的内存来记住我下一个该去哪，我不会为你保存过去
# 这个“一次性”的设计让迭代器变得异常强大和通用
# 它可以优雅地表示：无限序列：比如一个可以无限产生素数的生成器。你不可能把所有素数都存在内存里。你只能一个一个地向后获取，这个过程无法“重置”
# 数据流：比如读取一个巨大的文件、接收一个网络数据包、或者传感器传来的实时数据
# 这些数据都是“流式”的，读过一遍就没了，你无法回到过去“重新读取”一个已经处理过的数据包
# 迭代器的“一次性”设计完美地模拟了这种现实世界中的数据流模型
# 单向、一次性的模型非常简单。每个迭代器只需要实现一个__next__()方法，它的任务很纯粹：要么给我下一个值，要么告诉我你已经没了
# 这种简单的约定让整个生态系统变得非常容易构建和理解
# sys.stdin是一个文件类对象，完全符合迭代器的行为。Python 所有文件对象默认都是可迭代的
# 可以被 for 循环遍历，是一次性的，会被耗尽，是惰性的，不会一次性将输入全部读入内存
# 对象被称为迭代器必须满足：
# 实现 __iter__() 方法，并且该方法返回对象自身 (self)
# 实现 __next__() 方法，用来返回流中的下一个元素，并在没有元素时抛出 StopIteration 异常
# sys.stdin概念上，是一个流
# 它们本身就是自己的迭代器，这个对象同时扮演了两种角色——它既是“可迭代对象”，也是“迭代器”
# 可迭代对象 (Iterable)：
# 它的身份：一个数据容器，一个“盒子”。比如列表list、元组tuple、字符串str
# 它的职责：非常单一。当被iter()函数调用时，它的__iter__()方法会创建一个全新的、独立的迭代器对象并把它交出来。它自己不负责一个一个地提供元素
# 比喻：一个装满了玩具的玩具箱。玩具箱本身只是个容器，你问它要玩具，它不会直接给你，而是派一个“机械臂”给你
# 迭代器 (Iterator)：
# 它的身份：一个“工人”，一个“指针”
# 它的职责：记住当前的位置。当被next()函数调用时，它的__next__() 方法会交出下一个元素，并把自己的位置向后移动
# 当没有元素时，抛出 StopIteration 异常
# 比喻：从玩具箱那里派出来的那个“机械臂”。你每按一次按钮（调用next()），机械臂就从箱子里拿出一个玩具给你
# 合二为一的角色（以文件对象和 sys.stdin 为例）
# 它的身份：既是“可迭代对象”，又是“迭代器”
# 它的职责：
# 当被 iter() 函数调用时，它的__iter__() 方法不会创建新对象，而是直接返回它自己 (return self)
# 当被 next() 函数调用时，它的__next__()方法会交出下一个元素
# 比喻：一个自动售货机
# 它本身是一个容器（可迭代对象）
# 你按一下“购买”按钮（调用 iter()），它不会给你一个单独的取货装置，它自己就是那个装置
# 你再按一下“出货”按钮（调用 next()），它就自己吐出一个商品
# Python 迭代协议核心概念总结
# Python 的 for 循环是建立在“迭代协议 (Iteration Protocol)”之上的，该协议明确了两个相辅相成的角色：可迭代对象 (Iterable) 和 迭代器 (Iterator)
# for 循环的底层工作机制如下：
# 首先，for 语句会调用目标对象（如列表）的 __iter__() 方法。任何实现了此方法的对象，都被视为一个可迭代对象。它的核心职责是：被请求时，能提供一个“遍历者”——也就是迭代器
# __iter__() 方法会返回一个迭代器对象。迭代器是真正的“遍历执行者”，它必须实现两个方法：
# __next__()：负责计算并返回序列中的下一个元素。当没有元素时，它必须抛出 StopIteration 异常
# __iter__()：按照协议，它必须返回迭代器对象自身 (self)。这使得迭代器本身也是可迭代的
# for 循环会不断调用这个迭代器对象的 __next__() 方法来获取值，直到捕获到 StopIteration 异常，循环便优雅地结束
# 基于此模型，存在两种情况：
# 对于列表 (list)、元组等容器：它们是可迭代对象，但不是迭代器（自身没有__next__方法）
# 调用 iter(a_list) 会创建一个新的、独立的 list_iterator 对象。因此，容器和它的迭代器是两个不同的对象
# 对于文件对象、sys.stdin 或任何迭代器自身：它们既是可迭代对象，也是自己的迭代器。它们的 __iter__() 方法被设计为直接 return self
# 因此，for 循环从它身上获取的“迭代器”，就是它自己，后续调用的 __next__() 也是它自身的方法
# 这个设计通过将“数据容器”和“遍历状态的追踪者”在概念上分离，实现了高效的惰性求值 (Lazy Evaluation)，使得对巨大或无限数据流的处理成为可能，是Python语言优雅和高效的重要体现
