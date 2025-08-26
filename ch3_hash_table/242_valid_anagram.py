# 242. Valid Anagram
# https://leetcode.cn/problems/valid-anagram/

import collections


# 思路一，如果两个字符串是字母异位词，将字符串排序后，得到的新字符串应该完全相同，这个方法支持输入字符串包含 Unicode 字符
# Python 的 sorted() 函数在对字符串进行排序时，会根据字符的 Unicode 码点（code point）的顺序来进行排序
# 每个 Unicode 字符，无论是英文字母、中文汉字、日文假名还是表情符号（Emoji），都有一个唯一的码点值
# 当对一个字符串 s 调用 sorted(s) 时，它会执行以下操作
# 将字符串 s 视为一个可迭代的字符序列
# 对这个序列中的所有字符进行排序
# 返回一个包含排序后字符的列表 (list)
# 字符串 (str) 是不可变 (immutable) 类型，因此它没有 .sort() 方法
# 时间复杂度 O(NlogN)，空间复杂度是 O(N)，因为 sorted 函数内部必须在内存创建一个字符列表
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        return sorted(s) == sorted(t)


# 思路二，哈希表法（字典）来统计每个字符串中各个字符出现的次数
# 这里产生两个字典分别统计两个字符串，然后比较这两个字典，注意 Python 中比较字典相等只关心是否具有完全相同的键值对，而与键值对的顺序完全无关
# 时间复杂度是 O(N)，检查长度是否相等是 O(1) 的操作 (注意字符串求长是 O(1) 的操作)，遍历两个字符串是都是 O(N) 的操作，比较字典相等，与字典的键的数量成正比，总的来说，是 O(N) 时间复杂度，假定字符串长度远大于字符串中不同字符的数量
# 空间复杂度就是 O(C)/O(1)，C为字符串不同字符的数量，因为使用两个哈希表存储字符的频率。该方法同样完全适用于包含 Unicode 字符的输入字符串，字典支持以 Unicode 字符作为键
class Solution1:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            # 获取一个字符串 str 的长度，即 len(s)，其时间复杂度是 O(1)，Python 的字符串对象在内部直接保存了自身的长度信息
            return False

        word_in_s: dict[str, int] = {}
        # word_in_s = dict()
        for char in s:
            if char in word_in_s:
                word_in_s[char] += 1
            else:
                word_in_s[char] = 1
        # 如果直接 word_in_s[char] += 1
        # 第一次碰到一个未见过的字符时
        # 程序执行 word_in_s[char] = word_in_s[char] + 1
        # 程序计算右边表达式的值，发现要访问一个字典中不存在的键，于是就会抛出 KeyError 错误

        word_in_t: dict[str, int] = {}
        for char in t:
            if char in word_in_t:
                word_in_t[char] += 1
            else:
                word_in_t[char] = 1

        if word_in_t == word_in_s:
            return True

        return False


# 思路三，对上面的哈希表法进行一定的优化
# 可以先用一个哈希表记录第一个字符串的字符频率，然后遍历第二个字符串，将对应字符的计数减一
# 先遍历 s 来增加计数，然后遍历 t 来减少计数
# 如果减少的过程中发现字符不在哈希表中或者计数已经为 0，说明 t 包含了 s 没有的字符或者某个字符数量多于 s，于是不可能是异位词
# 如果遍历 t 正常结束，由于两个字符串长度相等，说明 t 中字符都在 s 中且数量匹配，所以不再需要检查计数是否全 0
# 时间和空间复杂度与思路二一致，也能处理 Unicode 字符。
# import collections
class Solution2:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        # 使用 collections.Counter 会更简洁
        # Collections 是一个 Python 的标准库模块（module）。这个模块包含了很多非常有用的、经过优化的特殊容器数据类型，Counter 就是其中之一
        # 而 Counter 本身是一个类（class），Counter 是一个专门用来计数的字典子类
        # 它的核心作用是接收一个可迭代对象（比如字符串、列表等），然后快速统计出该对象中每个元素出现的次数（即频率），并以“元素: 次数”的键值对形式存储起来
        # Counter 是一个字典，可以像操作普通字典一样操作
        # Counter 和普通字典的一个重要区别是。如果访问一个不存在的键，普通字典会抛出 KeyError，而 Counter 会返回 0
        # most_common(n) 方法，这是一个非常有用的独有方法，可以返回一个列表，包含出现次数最多的 n 个元素及其计数，按从多到少的顺序排列
        # Counter 对象之间可以像数学集合一样进行加、减等运算
        """
        counter = collections.Counter("mississippi")
        # 找出出现次数最多的 2 个字母
        print(counter.most_common(2)) # 输出: [('i', 4), ('s', 4)]
        # 如果不提供 n，则返回所有元素
        print(counter.most_common()) # 输出: [('i', 4), ('s', 4), ('p', 2), ('m', 1)]

        c1 = collections.Counter("apple")     # {'a': 1, 'p': 2, 'l': 1, 'e': 1}
        c2 = collections.Counter("apply")     # {'a': 1, 'p': 2, 'l': 1, 'y': 1}
        # 加法：合并计数
        print(c1 + c2)  # Counter({'p': 4, 'a': 2, 'l': 2, 'e': 1, 'y': 1})
        # 减法：减去计数（结果保留正数计数）
        print(c1 - c2)  # Counter({'e': 1})
        """
        return collections.Counter(s) == collections.Counter(t)

        # 手动实现
        """
        counter = {}
        for char in s:
            counter[char] = counter.get(char, 0) + 1
        # 这里 couter 与 collections.Counter(s)内容完全一致
        # dict.get(key, default) 方法非常适合这个场景。它会尝试获取 key 对应的 value，如果 key 不存在，它不会报错，而是会返回指定的 default 值  

        for char in t:
            # 如果 t 中的字符不在 counter 中，或者计数已经是 0
            if char not in counter or counter[char] == 0:
                return False
            counter[char] -= 1

        return True
        """


# 思路四，在题目输入全部是小写字母的前提下，完全可以用长度 26 的数组来代替哈希表，这样常数时间的开销会更小，避免了求哈希值和处理哈希冲突的开销
# 通常会更快，时间复杂度仍为 O(N)， 空间复杂度仍为 O(C)/O(1)
# 缺点是这个方法无法处理字符串中含有 Unicode 字符的情况，输入必须是小写字母
class Solution3:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        counts = [0] * 26  # 创建一个长度为26的数组，索引0-25对应a-z

        for char in s:
            counts[ord(char) - ord("a")] += 1
        # ord() 是 "ordinal"（序数）的缩写。它的作用是：接收一个长度为 1 的字符串（即单个字符），返回代表该字符的 Unicode 码点的整数
        for char in t:
            index = ord(char) - ord("a")
            if counts[index] == 0:
                return False
            counts[index] -= 1

        return True


# 思路五，暴力求解法，逐个检查字符串 s 中的每个字符，看是否能在 t 中找到并“抵消”掉一个匹配的字符
# 将字符串 t 转换成一个字符列表 t_list，因为列表是可变的，方便进行删除操作
# 遍历字符串 s 中的每一个字符 char_s。对于每一个 char_s，在 t_list 中进行查找
# 如果找到了，就从 t_list 中移除该字符，然后跳出内层查找，继续处理 s 的下一个字符
# 如果在 t_list 中没有找到 char_s，说明 t 中没有足够的匹配字符，直接返回 False
# 如果外层循环能顺利完成（即 s 中的所有字符都在 t 中找到了归宿），则返回 True
# 时间复杂度：O(N^2)。外层循环遍历 s 需要 O(N)。内层循环中，在列表 t_list 中查找 (in) 和删除 (.remove()) 操作的平均时间复杂度都是 O(N)
# 空间复杂度：O(N)。需要创建一个 t 的列表副本，消耗 O(N) 的额外空间
class Solution4:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        t_list = list(t)  # 将 t 转换成列表以便于移除元素

        for char_s in s:
            try:
                # list.remove(x) 会移除列表中第一个值为 x 的元素
                # 如果找不到，会抛出 ValueError
                t_list.remove(char_s)
            except ValueError:
                # 在 t_list 中找不到 char_s，说明不匹配
                return False

        return True
