# 区间和问题
# https://kamacoder.com/problempage.php?pid=1070

# 我们在这个问题中初次接触ACM格式的输入输出，注意输入输出格式，这里要写一个完整的程序

import sys

# 将 sys.stdin.readline 赋值给 input，后续可以直接使用 input()，写法更简洁
# 并且它的速度比内置的 input() 函数快，将input()重定义，这是常用的技巧
input = sys.stdin.readline

n = int(input())
# n_line = sys.stdin.readline().strip(),.strip() 方法会移除字符串两端的空白字符（包括换行符）
# n = int(n_line), int() 函数在转换字符串为整数时，可以自动处理字符串两端的空白字符（包括换行符 \n）
# 所以 .strip() 在这种特定情况下可以省略，让代码再短一点。

array = [int(input()) for _ in range(n)]
# 读取n行单元素最简单的写法，列表推导式
# 这是一种pythonic的写法，更简洁，一行代码就可以实现下面四行的功能
# Python解释器有专门底层优化，比for循环加append效率高，推荐使用这种写法

array = []
for _ in range(n):
    element = int(sys.stdin.readline().strip())
    array.append(element)

for line in sys.stdin:
    # 这个循环会一直读取，直到标准输入结束 (EOF, End of File)
    a, b = map(int, line.split())
    #  将一行中的字符串（如 "0 1"）按空格分割，并把分割后的两部分都转换为整数

for line in sys.stdin:
    # 去掉每行末尾的换行符
    line = line.strip()
    # 如果是空行，则跳过
    if not line:
        continue
    a, b = map(int, line.split())
    # 更鲁棒一些的写法，不过编程考试中，假定输入是完全符合题目要求的，不需要考虑鲁棒性


# 一个可以通过测试的简单实现：
# import sys
def solve():
    input = sys.stdin.readline
    n = int(input())
    array = [int(input()) for _ in range(n)]

    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + array[i]

    for line in sys.stdin:  # sys.stdin 包含了输入,按行划分,到输入结束(EOF)为止
        a, b = map(int, line.split())
        # .split() 是字符串的一个方法，它的作用是把一个字符串按照指定的分隔符（默认是空格）分割成一个字符串列表。
        # 得到一个字符串列表，列表每个元素还是字符串
        # map() 是一个非常强大的内置函数，它的语法是 map(function, iterable)。它的作用是：将 function（第一个参数）这个“魔法”依次施加到 iterable（第二个参数，比如我们上一步得到的列表）的每一个元素上
        # map() 并不会立刻返回一个列表，而是返回一个“map 对象”。这个对象非常“懒惰”，它知道如何去执行映射，但只有在需要时才会真正去做
        # 得到一个 map 对象。我们可以把它想象成一个“待办事项”列表，内容是：["对 '5' 执行 int()", "对 '10' 执行 int()"]。
        # 这是 Python 的“解包 (Unpacking)”语法。当你把一个可迭代对象（比如列表、元组，或者我们上一步得到的 map 对象）赋值给多个变量时，Python 会自动地从可迭代对象中按顺序取出元素，然后依次赋给左边的变量。
        # 这个过程会触发 map 对象去执行它的“待办事项”。
        # Python 看到左边有两个变量 a 和 b，于是它向 map 对象索要第一个元素。
        # map 对象执行它的第一个待办事项 int('5')，得到整数 5，然后把它交给 Python。Python 将 5 赋值给 a。
        print(prefix_sum[b + 1] - prefix_sum[a])


solve()

# 更好格式的实现：
# import sys
input = sys.stdin.readline  # 注意不能写成readline()


def main1():
    n_str = input()
    n = int(n_str)

    array = [int(input()) for _ in range(n)]

    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + array[i]

    for line in sys.stdin:
        a, b = map(int, line.split())
        # line.split()，不要误写成input().split()
        # 一定要注意是int 不是int()
        # 当写下 int() 时，Python 会立刻执行这个函数调用。int()没有参数返回0，这句代码变成map(0,...)报错
        # map的第一个参数是一个函数名，表示要对后面的可迭代对象进行什么函数操作
        # 它不会立刻把所有工作都做完。它返回一个“待办事项”列表（即 map 对象）
        # 只有当真正需要从这个对象中取出结果时（比如用 list() 转换它，或者用 for 循环遍历它）
        # 它才会去执行那个操作，处理一个，返回一个。在编程中，我们把这种特性称为惰性求值(Lazy Evaluation)
        print(prefix_sum[b + 1] - prefix_sum[a])


if __name__ == "__main__":
    main1()


# 最终版本
# import sys
input = sys.stdin.readline


def main():
    n = int(input())
    array = [int(input()) for _ in range(n)]
    prefix_sum = [0] * (n + 1)

    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + array[i]

    for line in sys.stdin:
        a, b = map(int, line.split())
        print(prefix_sum[b + 1] - prefix_sum[a])


if __name__ == "__main__":
    main()

# 暴力方法：假定m组查询，每次查询O(n)，整体时间复杂度O(m*n)，空间复杂度O(n)空间存储数组，额外空间O(1)
# 前缀和解法：计算前缀和，O(n)空间存储数组，额外O(n)空间存储前缀和数组。求前缀和的时间复杂度为O(n)
# 具体来说读取n行时间复杂度O(n)，创建前缀和数组时间复杂度O(n)，n次循环计算前缀和数组，每次都是一次加法，时间复杂度O(n)
# 查询m次，每次查询复杂度O(1)，总时间复杂度为O(m+n),额外空间复杂度O(n)
# 空间换时间思想


# sys.stdin 是 Python sys 模块中的一个核心对象，它代表了程序的标准输入流（Standard Input Stream）
# 从技术上讲，它是一个类文件对象（File-like Object），通常是 io.TextIOWrapper 的一个实例，该实例封装了一个带缓冲的二进制流

# 其关键性质如下：
# 流式（Stream-based）: sys.stdin 并非一个一次性存储所有数据的容器（如列表），而是一个数据流
# 数据是按需、顺序地从源（如键盘或管道）流向程序，并被消耗。

# 可迭代性（Iterable）: 该对象实现了迭代协议
# 允许通过 for line in sys.stdin: 的方式进行逐行迭代，这是处理行分隔输入的标准模式。

# 缓冲机制（Buffered）: 输入通常是带缓冲的。
# 在与终端交互的模式下，它一般是行缓冲（line-buffered）的，即操作系统会累积用户的键盘输入
# 直到遇到换行符（\n，通常由Enter键产生）后，才将整行数据发送至程序的输入流

# 消耗性与不可查找性（Consumptive & Non-seekable）: 作为连接到终端（TTY）等非随机访问设备的流
# sys.stdin 通常是不可查找的（seekable()返回False）
# 这意味着数据一旦被读取，流的内部位置指示器便会前移，已读数据不能被重新读取。它是一个单向、一次性的数据通道

# 核心操作方法
# 逐行迭代（推荐方法）
# 语法: for line in sys.stdin:
# 描述: 这是处理标准输入最常用且内存效率最高的方式
# 该循环会阻塞，直到新的一行数据可用，然后将其作为字符串（包含尾随的换行符 \n）赋给循环变量
# 循环在接收到文件结束符（EOF）时自动终止

# 单行读取
# 语法: sys.stdin.readline()
# 描述: 从流中读取并返回单独的一行。返回的字符串包含尾随的换行符 \n（如果存在）
# 当流结束时，再次调用将返回一个空字符串 ""

# 全量读取
# 语法 1: sys.stdin.read()
# 描述: 读取并返回从当前位置到流末尾（EOF）的所有剩余数据，作为一个单一的字符串。

# 语法 2: sys.stdin.readlines()
# 描述: 读取并返回所有剩余行，作为一个字符串列表，列表中的每个元素都是一行（包含尾随的换行符 \n）
# 性能警告: 全量读取方法会将全部输入加载到内存中，对于大规模输入存在导致 MemoryError 的风险
# 因此除非输入量可控，否则不推荐使用

# sys.stdin 流的生命周期由输入源决定。当从终端读取时，流的结束由用户发送 EOF (End-of-File) 信号来标记
# sys.stdin 是 Python 中与标准输入进行交互的、基于流的接口
# 它作为一个带缓冲、不可查找的类文件对象，最理想的操作模式是通过逐行迭代来处理输入，这种方式兼具代码简洁性和内存效率
