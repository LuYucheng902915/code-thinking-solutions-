# 1002. Find Common Characters
# https://leetcode.cn/problems/find-common-characters/

import math
from collections import Counter


# 思路一，本题自己实现的思路，做法完全正确
# 时间复杂度为 O(NL)，L 为单词的平均长度或最大长度（在分析中最坏情况时通常指最大长度）
# 第一个循环创建所有 Counter，需要遍历所有单词的所有字符，成本是 O(NL)
# 第二个循环遍历最多 26 个字符， 循环内部在循环遍历 N 个 Counter，每次操作 get 方法时间复杂度是 O(1)
# 所以第二个循环的时间成本为 O(NC)，C 为字符集的大小（这里是 26），实际 C 也可能比 26 小
# 假设 L >> C，总时间复杂度 O(NL + NC) = O（NL），意味着算法的运行时间与输入中所有单词的总字符数大致成正比
# 空间复杂度是存储了 N 个 Counter 字典，每个 Counter 字典最多包含 26 个键值对（题目要求全小写字母）
# 空间复杂度为 O(NC)，简化也可以认为是 O(N)
# 使用第一个单词而不是最短的单词作为基准是完全正确的，最短的单词一方面是需要 O(N) 的开销来找到最短的单词
# 另一方面最短单词不一定包含最少的不重复字符的数量，并不一定能有效提高运行速度
# 这里提高效率的主要目的是减少第二个循环的循环次数
# 一个可行的优化是选择 Counts 中最短的字典作为基准
# 注意字典是可以求 len 的，返回字典中键值对（key-value pair）的数量。这个操作的时间复杂度是 O(1)，这个数被记录在字典内部
# 虽然找到 len() 最短的 Counter 额外遍历一次 counts 列表，额外产生 O(N) 时间复杂度
# 但只要不是 counts 中所有字典长度都相等，或者第一个单词对应的 Counter 恰好是最短的
# 这样优化都能减少第二个 for 循环循环次数，而且第二个循环内部操作 min(), .get() 比单纯地找最短 Counter 的操作 (len()) 要更复杂一些（即常数因子更大）
# 这样优化在性能上是划算的，一个 O(N) 的简单循环，去换取另一个更复杂的 O(NK) 循环，这里 K 是节约的循环次数
# 第二个优化是对 101 这个数字的优化，这个数字依赖于题目约束，不是好的编程实践，可以使用 baseline 中字符的频率来初始化 Counter
class Solution:
    def commonChars(self, words: list[str]) -> list[str]:
        counts = []
        for word in words:
            counts.append(Counter(word))

        # 以第一个单词的字符作为基准
        # baseline_cou = counts[0]
        # 优化，以 counts 中最短的作为 baseline
        baseline_cou = min(counts, key=len)
        results = []

        for key in baseline_cou:
            # number = 101
            # 优化，以 baseline 中字符频率来设置 number
            # number = baseline_cou.get(key)
            # 上面这句静态类型检查会报错，因为 get 可能返回 None，虽然在这个代码里不可能返回 None
            number = baseline_cou[key]
            for count in counts:
                number = min(number, count.get(key, 0))

            for _ in range(number):
                results.append(key)
            # 另一种写法
            # if number > 0:
            #     results.extend([key] * number)

        return results


# 思路二，对上面的做法可以优化空间复杂度，不需要存储所有单词的 Counter 对象，只需要维护一个到目前为止的最小频率的 Counter
# 优化后空间复杂度 O(L + C) 或者 O(L)，大大降低了空间占用
# 注意空间复杂度衡量的不是程序运行期间总共分配过多少内存，而是程序在任意时刻所占用的内存峰值（Peak Memory Usage）
# 这个方法产生的 Counter 会因为无人引用被 Python 的垃圾回收机制回收，从而是空间复杂度更好的方法
# 实际上可能不会立刻被回收，但讨论的空间复杂度也是一个理论模型。
# 它衡量的是为了让算法逻辑上能正确运行，所需要保持“存活”的可达（Reachable）内存的最大值与输入规模 N 之间的关系
# 在Python中计算一个算法的空间复杂度，就是计算可达对象的峰值辅助空间
# “存活/可达内存” 是一个动态的、运行时的概念。在有垃圾回收的语言（如Python, Java）中，一个变量或对象只要在当前的执行上下文中是“可达的”（即有变量名引用它），它就不会被回收，它就是“存活”的
# 辅助空间 (Auxiliary Space)：关注的是算法为了完成计算而额外使用的内存，通常不包括存储输入数据本身所占用的空间
class Solution1:
    def commonChars(self, words: list[str]) -> list[str]:
        # 用第一个单词的频率作为初始的最小频率
        min_counts = Counter(words[0])

        # 遍历从第二个单词开始的剩余单词
        for i in range(1, len(words)):
            current_counts = Counter(words[i])
            # 更新 min_counts，只保留两个 Counter 中都存在的键
            # 并且值的交集是取两者中的最小值
            # 这可以通过'&'操作符优雅地实现
            min_counts &= current_counts
            # # 手动实现交集逻辑：
            # for char in list(min_counts.keys()):
            #     min_counts[char] = min(min_counts[char], current_counts.get(char, 0))

        # # 使用 Counter.elements() 方法可以更方便地构建结果
        # return list(min_counts.elements())

        # 手动构建结果列表
        results = []
        for char, count in min_counts.items():
            results.extend([char] * count)

        return results


# 思路三，纯数组模拟法，同样由于题目限定了 26 个小写字母，依然可以只使用数组来避免哈希操作的开销
# 时间复杂度为 O(NL)，空间复杂度就是一个 26 个元素的数组，为 O(26)/O(1)
class Solution2:
    def commonChars(self, words: list[str]) -> list[str]:
        # 初始化一个最小频率数组，所有值设为一个“无穷大”的数
        # float('inf') 是比任何数都大的浮点数，比用101更好
        min_freq = [math.inf] * 26

        for word in words:
            char_freq = [0] * 26
            for char in word:
                char_freq[ord(char) - ord("a")] += 1

            # 更新全局最小频率
            for i in range(26):
                min_freq[i] = min(min_freq[i], char_freq[i])

        # 构建结果
        results = []
        for i in range(26):
            if min_freq[i] != math.inf:
                # chr(i + ord('a')) 将索引转换回字符
                results.extend([chr(i + ord("a"))] * int(min_freq[i]))

        return results


# Python 语言学习：
# list.extend(iterable)
# 它接收一个可迭代对象（比如列表、元组、字符串，或者 Counter.elements() 的返回结果），然后将该对象中的每一个元素逐个地添加到列表的末尾
# append() 只会把接收到的对象作为一个整体添加到列表末尾
"""
my_list = ["a", "b"]
another_list = ["c", "d"]

# 使用 extend
my_list.extend(another_list)
print(my_list)  # 输出: ['a', 'b', 'c', 'd'] (另一个列表的元素被拆开加入)

# 如果使用 append
my_list = ["a", "b"]  # 重置
my_list.append(another_list)
print(my_list)  # 输出: ['a', 'b', ['c', 'd']] (另一个列表被当成一个元素加入)
"""
# Counter.elements()
# 作用：这个方法会返回一个迭代器 (iterator)，该迭代器会“展开”Counter。它会把每个元素按照其计数的次数逐个地产出
# 应用场景：当你需要把一个频率字典还原成一个包含重复元素的序列时，这个方法非常方便
"""
from collections import Counter

final_counts = Counter({'l': 2, 'e': 1, 'b': 3})

# elements() 返回一个迭代器
elements_iterator = final_counts.elements()

# 我们可以把它转换成列表来查看内容
result_list = list(elements_iterator)
print(result_list) # 输出可能是: ['l', 'l', 'e', 'b', 'b', 'b'] (顺序不保证)
"""
# min_counts &= current_counts (Counter 的交集运算)
# 作用：对于 Counter 对象，& 操作符被重载（overloaded）了，用来计算两个 Counter 的交集 (intersection)。&= 是其原地（in-place）版本
# Python 使用特殊/魔术/双下划线方法 (Special/Magic/Dunder Methods)来定义重载，比如 __and__ 方法
# 当写下 a & b 这样的表达式时，Python 解释器实际上会去尝试调用对象 a 的一个特殊方法：a.__and__(b)
# 如果 a 的类定义了 __and__ 方法，那么 a & b 的结果就是调用这个方法后返回的值
# 如果 a 的类没有定义 __and__ 方法，Python 就会抛出 TypeError，告诉你这个操作不被支持
# & 作用域两个整数代表按位与，作用于两个集合代表求集合交集
# 作用于计数器 Counter 时（& 只能作用在 Counter 这一特数的计数器字典，因为实现这个子类时为其实现了 & 操作符的功能）
# 可以把 Counter 视为多重集合，& 就是求两个多重集合的交集，结果中只包含两个 Counter 共同拥有的元素；结果中每个元素的计数值，是取它在两个 Counter 中计数的最小值
# 交集的含义：结果会是一个新的 Counter，它只包含两个原始 Counter 共同拥有的键。并且，每个键对应的值是取两个 Counter 中该键计数的最小值
# Counter里的值可以是负数或 0，没有严格规定，虽然通常是正数，既可以手动赋值，也可以使用 .subtract() 方法
# Counter 的减法有两种，行为不同，这一点非常重要
# 操作符： c1 - c2 会创建一个新的 Counter，并且只保留结果为正数的计数
# .subtract() 方法：c1.subtract(c2) 会原地修改 c1，进行纯粹的数学减法，结果可以是负数或零
# min_counts &= current_counts 就是在不断地“削减” min_counts，让它保留与下一个单词的共用部分
"""
from collections import Counter

c1 = Counter(['a', 'a', 'b'])  # Counter({'a': 2, 'b': 1})
c2 = Counter(['a', 'b', 'b', 'c']) # Counter({'b': 2, 'a': 1, 'c': 1})

# 使用 `-` 操作符
result_operator = c1 - c2
# 'a': 2-1=1
# 'b': 1-2=-1 (被丢弃)
# 'c': 0-1=-1 (被丢弃)
print(result_operator) # 输出: Counter({'a': 1})

# 使用 .subtract() 方法
# 我们用 c1 的一个副本来操作，以免修改原始 c1
c1_copy = c1.copy()
c1_copy.subtract(c2)
# 'a': 2-1=1
# 'b': 1-2=-1
# 'c': 0-1=-1
print(c1_copy) # 输出: Counter({'a': 1, 'b': -1, 'c': -1})
"""
"""
from collections import Counter

# c1 代表单词 "bella"
c1 = Counter("bella")  # -> Counter({'l': 2, 'b': 1, 'e': 1, 'a': 1})

# c2 代表单词 "label"
c2 = Counter("label")  # -> Counter({'l': 2, 'a': 1, 'b': 1, 'e': 1})

# c3 代表单词 "roller"
c3 = Counter("roller") # -> Counter({'r': 2, 'l': 2, 'o': 1, 'e': 1})

# 计算 c1 和 c2 的交集
intersection_1_2 = c1 & c2
print(intersection_1_2) # 输出: Counter({'l': 2, 'b': 1, 'e': 1, 'a': 1})

# 在上一个交集的基础上，再和 c3 计算交集
final_intersection = intersection_1_2 & c3
print(final_intersection) # 输出: Counter({'l': 2, 'e': 1})
"""
