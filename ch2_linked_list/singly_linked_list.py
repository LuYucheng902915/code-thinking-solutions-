# 除了常用的单向、双向、循环链表，以前还有过没有指针时的静态链表
# 以及针对特殊问题特化的数据结构，例如多重链表和异或链表
# 上面几种不要求掌握，掌握单向、双向和循环链表就足够
# 在现代的编程语言Python中，也很少使用链表，python 本身也没有链表这样的数据结构
# 因为Python 的 list （动态数组）是一个经过高度优化的“全能选手”。对于绝大多数场景，它 O(1) 的随机（任意一个）访问和尾部操作，加上简单易用的特性，已经足够满足需求
# 很少会手动实现和使用传统链表,其优势在于在中间插入/删除元素时间复杂度低（前提是已经获得该节点或前置节点的引用），缺点是访问元素慢
# 当确实需要链表“两端都能快速操作”的特性时（比如实现一个队列）通常使用
# collections.deque：它的底层是用双向链表实现的，可以保证在头部和尾部进行添加和删除操作的时间复杂度都是 O(1)
# 它是 Python 中实现队列和栈等数据结构的官方推荐方式，既高效又方便
# 作为其他数据结构的内部组件，在实现一些更复杂的数据结构时，链表仍然是基石
# 例如，哈希表（字典）在解决哈希冲突时，可能会用到“拉链法”，也就是一个链表


# 与将所有元素存放在一块连续内存中的数组不同，链表的元素在内存中是分散存储的
# 它通过每个元素内部的指针 (pointer)，将这些分散的元素像链条一样串联起来
# 节点 (Node)：链表的基本单元。每个节点通常包含两部分信息：
# 数据域 (Data)：存放元素自身的实际数据（比如数字 10，字符串 "hello"）
# 指针域 (Next)：存放指向下一个节点的内存地址。链表的最后一个节点的指针通常指向一个空值（在 Python 中是 None），表示链条的末端
# 头指针/头节点 (Head)：一个指向链表第一个节点的指针。我们通过头指针就能找到链表的起点，并沿着指针域遍历整个链表

# 注意，如果在编写链表代码时感到混乱，一定要在纸上推演与画图，在纸上把节点和箭头（指针）画出来，模拟算法的指向，手动修改箭头的指向
# 同时一定要注意各个节点的索引，此外对于单链表的插入和删除，一定要找到目标位置的前一个节点，前驱节点


class ListNode:
    """单向链表节点类"""

    def __init__(self, value=0):
        self.val = value
        self.next = None  # 创建节点，默认后面没有节点相连，None代表链表终点标志

    def __repr__(self):
        return f"ListNode({self.val})"

    # 在 Python 中，`__repr__` 是一个内置的“魔法方法”（special method），它的主要作用是为对象提供一个“官方的”字符串表示，通常用于调试和交互式环境
    # __repr__ 是 representation 的缩写。它的完整含义是 "string representation"，即一个对象的“字符串表示形式”
    # 具体来说：当你在 REPL（如 IPython、Python 交互式命令行）里直接输入一个对象名时，会调用它的 `__repr__` 方法来显示结果
    # 在使用内置函数 `repr(obj)` 或者在容器（如列表、字典）里包含该对象时，同样会调用 `__repr__`
    # 如果不定义 `__repr__`，默认输出类似 `<__main__.ListNode object at 0x10f3e3d30>`，可读性和可调试性很差


"""
(base) D:\Codes\Computer Science Fundamentals\Data Structure and Algorithms>python
Python 3.12.3 | packaged by conda-forge | (main, Apr 15 2024, 18:20:11) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from ch2_linked_list.singly_linked_list import ListNode
>>> node = ListNode()
>>> node
ListNode(0)
>>> repr(node)
'ListNode(0)'
"""


class SinglyLinkedList:
    """
    单向链表管理类
    这个类封装了对链表的常用操作
    """

    def __init__(self):
        """初始化一个空链表"""
        self.head = None
        # __init__ 函数规定必须返回None，不返回任何值
        # 在Python中，所有函数都一定有返回值
        # 如果没有明确地用 return 关键字来指定返回值，那么函数在执行完毕后，会自动、隐式地返回 None
        # 只写return/return None/不写return都返回None

    def is_empty(self):
        """检查链表是否为空"""
        # def is_empty(self) -> bool:
        # -> bool：这被称为返回类型提示 (Return Type Hint)
        # 它是在 Python 3.5 版本及以后引入的语法，用来声明这个函数期望返回一个布尔值 (True 或 False)
        # 提高代码可读性，方便静态检查工具
        # def is_empty(self: 'SinglyLinkedList') -> bool:
        # 一般被认为冗余，不写self类型提示
        return self.head is None
        # None 是 Python 中一个非常特殊的、独一无二的对象
        # 代表“无”或“空值”：它的主要作用是表示一个变量没有任何有效的值。它不等于 0，不等于 False，也不等于空字符串 ""
        # 唯一实例 (Singleton)：在整个 Python 程序运行期间，None 这个对象只有一个。所有值为 None 的变量，都指向内存中同一个 None 对象
        # 自有类型：None 的类型是 NoneType，这个类型也只有 None 这一个值
        # 最规范、最推荐的检查一个变量是否为 None 的方式是使用 is 关键字
        # if x is None:
        # is 检查的是两个变量是否指向内存中同一个对象，因为 None 是唯一的，所以用 is 是最恰当的

    def get_length_try(self):
        length = 0
        if self.is_empty():
            return length
        else:
            current = self.head
            while current is not None:
                # 判断条件不是current.next
                length += 1
                current = current.next

        return length

    # 更好的写法
    def __len__(self):
        """
        获取链表长度，使其支持 len(list) 操作
        时间复杂度: O(n)
        """
        # 在 Python 里，如果一个类定义了魔法方法 __len__(self)，那么：
        # 内置函数 len(obj) 就会去调用 obj.__len__()
        # 就可以用 len(your_list) 来得到链表的长度，而不用自己手动遍历一次
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        """
        定义打印链表时的输出，使其支持 print(list)
        时间复杂度: O(n)
        遍历并以 "A -> B -> C -> None" 的格式打印整个链表
        """
        if self.is_empty():
            return "Empty List"
        # 上面三行也可以不要，如果空链表输出只输出None，也可以按下面的代码统一处理。

        vals = []
        current = self.head
        while current:
            vals.append(str(current.val))
            current = current.next

        return " -> ".join(vals) + " -> None"
        # 语法：separator_string.join(iterable)
        # separator_string (分隔符字符串)：这是用来连接元素的字符串
        # 功能是用分隔符把字符串列表元素连接起来，例如["1","2","3"] 会变成 "1->2->3"
        # iterable (可迭代对象)：这是一个包含多个元素的集合，通常是一个列表或元组
        # 一个非常重要的前提是：这个可迭代对象中的所有元素都必须是字符串类型
        # 如果其中有非字符串元素（比如整数），程序会报错TypeError

    def prepend(self, value):
        """
        在链表头部插入新节点 (头插法)
        时间复杂度: O(1)
        """
        new_node = ListNode(value)
        """
        if self.is_empty:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        """
        # 不需要分类讨论
        # 假定空链表，self.head = None, 但 new_node.next 就应该是 None，代表链表只有一个节点
        # prepend 操作的核心永远是修改 head 指针的指向。这个操作流程对于空链表和非空链表是天然统一的
        # 新节点的 next 总是指向“旧的头”（无论旧的头是一个节点还是 None），然后 head 再指向新节点。所以它不需要分类讨论
        # 它的逻辑不依赖于找到某个现有节点
        new_node.next = self.head
        self.head = new_node

    def append(self, value):
        """
        在链表尾部插入新节点 (尾插法)
        时间复杂度: O(n) - 因为需要遍历到链表末尾
        """
        new_node = ListNode(value)
        if self.is_empty():
            self.head = new_node
            return  # 不能忘掉这里要return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node
        # 首先确定 while 的条件，要到最后一个节点，所以是 current.next 为 None,不是 current 为 None
        # 然后将新节点赋值给最后节点的 next
        # 从 head 开始遍历，如果是空链表，head 本身就是 None，此时没有最后一个节点
        # 所以要单独讨论空链表， 否则，current.next 直接报错
        # append 操作的核心是：找到最后一个节点，并修改它的 next 指针
        # 这个核心动作——“找到最后一个节点”——在空链表上是无法执行的

    def insert(self, index, value):
        """
        在指定索引位置插入新节点 (标准版)
        如果 index < 0 或 index > 链表长度，会抛出 IndexError
        这种行为与 Python 内置 list 的 insert 方法更接近（除了负数索引的处理方式）
        推荐写法
        """
        if index < 0:
            raise IndexError("链表索引不能为负数")

        length = len(self)
        if index > length:
            raise IndexError("链表索引超出范围")
        # raise被执行后，insert 函数会终止所有操作，不再执行函数中剩下任何代码
        # 调用处要准备安全网，使用 Python 中标准的错误处理机制—— try...except 语句块 来“接住”并处理这个异常
        # try 块: 把可能会抛出异常的代码，也就是您“怀疑”有风险的操作，放在 try: 的下面。程序会尝试正常执行这里的代码
        # except 块: 把如果真的发生了特定错误，希望执行的“应急预案”代码，放在 except 错误类型: 的下面

        # if not 0 <= index <= len(self):
        #     raise IndexError("Index out of range")
        # 在Python中，a <= b <= c 是一个特殊的语法糖，它被解释器自动转换为：(a <= b) and (b <= c)
        # 可读性高，中间项 b 只需要计算一次
        # raise 关键字的语法作用: raise 关键字的作用是立即中断当前程序的正常执行流程，并“抛出”一个异常信号
        # 一旦执行到 raise 语句，函数会立刻停止运行，并开始沿着“调用栈”向上传播这个异常
        # 它会寻找一个能够“接住”这个异常的 try...except 语句块
        # 如果找到了匹配的 except 块，程序会跳转到该块内执行，错误被处理，程序可以继续运行
        # 如果直到程序顶层都没有找到能处理这个异常的 except 块，程序就会彻底终止，并打印出错误信息和调用栈轨迹（Traceback）
        # 调用栈（Call Stack）是计算机程序在执行期间用来管理函数调用的一种核心数据结构，它遵循后进先出（LIFO）的原则
        # 每当一个函数被调用时，一个包含其局部变量、参数和返回地址的执行上下文，即“栈帧”（Stack Frame），就会被压入调用栈的顶部
        # 当函数执行完毕并返回时，其对应的栈帧会从栈顶被弹出，程序的控制权则根据栈帧中保存的返回地址交还给调用者
        # 这个过程确保了即使在复杂的嵌套调用中，程序的执行流也能有序地进行和返回
        # 当程序中执行了 raise 语句，一个异常（Exception）对象被创建并抛出，这会立即中断程序的常规控制流，并启动一个名为“栈回溯”（Stack Unwinding）的过程
        # 解释器会从调用栈的顶部开始，逐层向后（向下）检查每一个栈帧，寻找能够处理该类型异常的 try...except 语句块
        # 所谓“接住”异常，指的就是在这个回溯过程中，找到了一个与异常类型相匹配的 except 异常处理器（Exception Handler）
        # 一旦找到，栈回溯过程便会停止，程序的控制权立即转移到该 except 块中执行，从而使程序有机会从错误状态中恢复，而不是因未捕获的异常而终止
        # IndexError(...) 异常对象的语法作用: 这是一个类的实例化过程。IndexError 是Python内置的一个异常类，专门用来表示“序列的索引超出了范围”
        # 括号里的字符串，是传递给这个异常对象的错误信息
        # 当这个异常最终被打印到控制台时，这个字符串会显示出来，为调试者提供清晰、具体的错误原因
        if index == 0:
            self.prepend(value)
            return  # 操作完成，直接返回

        # 情况二：在中间或尾部插入
        # 能走到这里，说明 index > 0 且 index <= length，且链表非空
        # 我们只需要找到 index-1 位置的节点即可

        # 思路是首先确认要找的节点是原来索引为 index - 1的节点，从 head 开始走 index - 1 步就能到
        # 但是 head 显然不能为 None，否则无法走下一步，要单独讨论空链表
        # 除此之外如果 index 等于 0，就要在链表头插入，是无法获得索引为 index - 1 节点的
        # 空列表时， index 只有等于 0 才合法，所以 index 为 0 自然包含了空链表情况
        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        # 执行插入
        new_node = ListNode(value)
        new_node.next = prev.next
        prev.next = new_node

    def insert_try(self, index, value):
        """
        在指定索引位置插入新节点
        时间复杂度: O(n) - 这是查找前驱节点的时间复杂度
        插入操作本身时间复杂度是 O(1)
        这里插入索引如果在范围外，会在头/尾插入节点
        后面尝试优化在尾节点插入。把问题弄得很复杂，没有必要
        最好做法就是当输入不合法，索引越界，就抛出异常
        """
        if index <= 0:
            self.prepend(value)
            return

        elif index >= len(self):
            self.append(value)
            return
        # 第一个元素索引为 0
        # 下面是中间插入，插入的索引节点一定有next
        count = 0
        current = self.head
        # while count < index:
        # 错误逻辑，上面注释是错误的代码，下面修改后是正确的
        while count < index - 1:
            current = current.next
            count += 1

        # 循环结束 current 就是第 index 个节点
        new_node = ListNode(value)
        new_node.next = current.next
        current.next = new_node
        # 上面犯了一个经典的逻辑错误，在 index 处插入节点，实际上要找到 index - 1 索引的节点，将新节点放到这个节点的后面
        # index > 0 保证了 index - 1 索引的节点是存在的
        # 这样写可读性不好，下面这个版本更好的表示了前一个节点

    def insert_correct(self, index, value):
        if index <= 0:
            self.prepend(value)
            return

        if index >= len(self):
            self.append(value)
            return

        prev_node = self.head
        for _ in range(index - 1):
            # 要获得索引为 index - 1 的元素，最好的办法就是从第一个索引 0 的元素开始
            # 走 index - 1 步。因为index 大于等于 1，至少走 0 步
            prev_node = prev_node.next

        new_node = ListNode(value)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def insert_optimized(self, index, value):
        # 上一个版本，len(self) 本身遍历了一次链表，这使得插入末尾时，遍历了链表两次
        # 优化思路将检查索引是否越界与遍历查找前驱节点合二为一。只遍历一次
        if index <= 0:
            self.prepend(value)
            return

        # 与之前逻辑一致，如果索引超过链表的长度，我们把它加到链表末尾而不是抛出异常
        # 初始化两个指针，这是因为如果索引超过链表的长度，通过检查当前指针是否为None发现
        # 如果当前指针是None，此时要将新元素插入到前一个元素的后面
        # 对于单向链表，如果不记录前一个元素，是无法返回前一个元素的
        # 这个代码之所以复杂，也是因为要解决索引超过长度，添加到末尾的特殊问题，其实通常索引越界是报错
        # 如果允许抛出异常，那么直接 for 循环到 index - 1，如果发现 prev_node 为 None，直接抛出异常即可

        # prev 用于最终执行插入操作
        # current 用于定位
        prev = None
        current = self.head
        count = 0

        while count < index:  # 还是最多遍历 index - 1 次
            if current is None:
                # index超出了范围
                if prev:  # 确保链表非空
                    new_node = ListNode(value)
                    prev.next = new_node
                else:  # 链表为空， index > 0
                    self.prepend(value)
                return
            prev = current
            current = current.next
            count += 1

        new_node = ListNode(value)
        new_node.next = current
        # 上面这个做法真正做到了避免遍历两次链表，代价是要多维护一个指针，而且逻辑也比较复杂，不推荐
        # 实际实践的时候，真正的优秀做法是给单链表做一个常见的增强，维护一个尾指针和一个计数器
        # 这样可以让 __len__， 头插法和尾插法的时间复杂度都变成 O(1)

    def delete_by_value(self, value):
        """
        删除第一个值为指定值的节点 (常考)
        时间复杂度: O(n) - 因为需要查找该值
        """
        if self.is_empty():
            return

        if self.head.val == value:
            self.head = self.head.next
            return
        prev_node = self.head
        while prev_node.next and prev_node.next.val != value:
            prev_node = prev_node.next
        # 两个条件分布代表是否遍历到链表的最后一个元素和下一个节点是否是要删除的节点
        if prev_node.next:
            prev_node.next = prev_node.next.next
        # prev_node 如果是最后一个节点，说明没有找到，不删除，否则 prev_node.next 一定不是 None
        # 如果没找到，while 循环会一直走到 prev_node 成为倒数第二个节点（或者最后一个节点，如果只有一个节点），直到 prev_node.next 变为 None，此时 if prev_node.next: 条件不成立，也就不会执行删除
        # 这个条件判断用于区分找到还是没找到

        # 删除特定元素，一定要找到其 prev 节点。如果链表为空或者只有头节点，不存在 prev 节点，需要分类讨论
        # 后面会看到对于删除所有特定值的元素，如果删除掉头节点，新的头节点还有可能需要被删除
        # 此时分类讨论就会不方便，使用哑节点（dummy node）思想，更加方便

    def delete_all_by_value(self, value):
        """
        删除所有值为指定值的节点 (常考，体现Dummy Node思想)
        时间复杂度: O(n)
        """
        dummy_head = ListNode(0)
        dummy_head.next = self.head
        current = dummy_head
        # 维护一个虚拟头节点

        while current.next:
            if current.next.val == value:
                current.next = current.next.next
            else:
                current = current.next

        self.head = dummy_head.next

    def delete_by_index_try(self, index):
        """
        删除指定索引位置的节点
        时间复杂度: O(n)
        """
        if self.is_empty():
            return
        # 保证非空
        if index <= 0:
            self.head = self.head.next
            return

        prev = self.head
        # prev一定一开始不是None
        current = prev.next
        count = 0
        while count < index - 1:
            if current is None:
                prev.next = None
                return
            prev = prev.next
            current = current.next
            count += 1

        prev.next = prev.next.next
        # 上面的写法又存在的逻辑错误
        # 当index远大于链表的长度时，当 current 为 None， prev指向前一个，也就是链表的最后一个节点
        # 纠结于在“经典单链表”上实现一个复杂的、单遍的、能处理特殊边界的 delete_by_index 意义不大
        # 默认使用最清晰、最可读的实现方式
        # 如果发现性能瓶颈在于尾部插入，就为单链表增加 tail 指针
        # 下面的函数可读性更好，如果要实现 index 超出范围在头/尾删除，用下面这种写法

    def delete_by_index_cleaner(self, index):
        if self.is_empty():
            return

        if index <= 0:
            self.head = self.head.next
            return

        length = len(self)
        if index >= length - 1:
            # --- 删除最后一个节点的逻辑 ---
            # 如果只有一个节点
            if length == 1:
                self.head = None
                return
            # 找到倒数第二个节点
            prev = self.head
            while prev.next and prev.next.next:
                prev = prev.next
            prev.next = None
        else:
            # --- 删除中间节点的逻辑 ---
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            prev.next = prev.next.next

    def delete_by_index_correct(self, index):
        """
        删除指定索引位置的节点。
        特殊规则：index < 0 删除头节点；index >= 长度 删除尾节点
        错误代码的修正，不遍历两次链表，可以看到逻辑非常复杂
        """

        # 1. 处理空链表
        if self.is_empty():
            return

        # 2. 处理删除头节点 (index <= 0)
        #    也包括只有一个节点时，删除后变为空链表的情况
        if index <= 0:
            self.head = self.head.next
            return

        # 3. 核心逻辑：找到要删除节点的前一个节点 (prev)
        prev = self.head
        # 我们最多走 index-1 步来定位 prev
        # 同时用一个 current 指针来探测是否已到末尾
        current = self.head.next
        count = 0

        while count < index - 1:
            # 如果在找到目标前驱节点之前，current就到头了
            # 这说明 index >= 链表长度
            if current is None:
                # 此时 prev 就是倒数第二个节点（如果链表长度 > 1）
                # 或者 prev 就是头节点（如果链表长度 == 1）
                # 这种情况下，我们直接进入“删除最后一个节点”的逻辑
                # 要删除最后一个节点，我们需要倒数第二个节点
                # 但我们已经遍历到了最后，需要重新找
                # 为了避免二次遍历，我们可以在这里直接处理
                # 此时 prev 就是我们要找的倒数第二个节点

                # 如果 prev.next 为 None，说明 prev 就是最后一个节点了
                # 这种情况发生在链表只有一个节点，但 index > 0
                if prev.next is None:
                    # 实际上这种情况被上面的 index <= 0 和 prev=self.head, current=self.head.next 覆盖了
                    # 如果链表只有一个节点, current 初始化就是 None, 循环一次都不会进
                    # 那么 index=1 就应该删除最后一个节点，也就是头节点
                    self.head = None  # 特殊处理
                    return
                # 如果 prev.next 不是 None，说明 prev 是倒数第二个节点
                # 我们要删除的是 prev.next
                prev.next = None  # 直接将倒数第二个节点的 next 置为 None
                return

            prev = prev.next
            current = current.next
            count += 1

        # 4. 如果循环正常结束，说明是删除中间节点或最后一个节点
        #    此时 prev 指向 index-1, current 指向 index
        #    需要确保 current 不是 None (index 没有越界)
        if current:
            prev.next = current.next
        else:
            # current 为 None，说明 index 恰好等于链表长度
            # 此时 prev 指向的是倒数第二个节点，我们要删除的就是 prev.next
            prev.next = None

    def delete_by_index(self, index):
        """
        删除指定索引位置的节点
        时间复杂度: O(n)
        在index不合法直接报错
        推荐写法
        """
        if not 0 <= index < len(self):
            # 这个判断包含了对空链表的处理，以及要求0 <= index <= len(list) - 1
            raise IndexError("Index out of range.")

        if index == 0:
            self.head = self.head.next
            return

        prev_node = self.head
        for _ in range(index - 1):
            prev_node = prev_node.next

        prev_node.next = prev_node.next.next

    # =========================================================================================
    # === 链表操作的思路与最佳实践总结 ===
    #
    # 经过多次尝试和修正，总结出解决链表问题的核心思想，这套原则不仅适用于链表，也适用于多数数据结构问题。
    #
    # 1. 核心原则：清晰第一，遵循规则
    #    - 思路清晰是首要前提。在动手写代码前，务必明确操作的每一步，尤其理清指针的指向变化。画图推演是最好的方法。
    #    - 索引约定：默认情况下，链表的索引规则与列表(List)保持一致，即头节点的索引为 0。
    #    - 严格遵循题目要求。特别是关于边界条件和索引范围的定义。如果题目没有特殊说明，则遵循标准行为。
    #
    # 2. 标准行为定义 (对齐 Python List)
    #    - 标准删除 (delete): 合法索引范围为 `0` 至 `len(链表) - 1`。对空链表或索引越界的操作，应抛出异常。
    #    - 这与Python内置 list 的 del list[index] 或 list.pop(index) 的行为是完全一致的。
    #    - 标准插入 (insert): 合法索引范围为 `0` 至 `len(链表)`。`index = len(链表)` 表示在尾部追加。超出此范围的索引应抛出异常。
    #    - Python list.insert() 的实际行为:
    #    - 它更加“宽容”。如果 index 大于 len，它不会报错，而是直接在尾部追加。它也支持复杂的负数索引（如 list.insert(-1, val) 是在倒数第一个元素前插入）。
    #    - Python的 list 为了使用的便利性做了一些模糊化处理。上面的标准逻辑上更简单，无歧义，也是值得推荐的。
    #    - 这套“严格”规则，与 Java 的 ArrayList.add(index, element) 和 C# 的 List<T>.Insert(index, item) 的行为是完全一致的。体现了不同语言在严格性与便利性之间的权衡。
    #
    # 3. 实现策略与优化思想
    #    - 可读性 > 微优化: 永远优先采用逻辑最清晰、最易懂的写法。清晰的代码能极大降低自己犯错的概率。
    #      在 LeetCode 这类场景，通常不会因为多一次 O(n) 遍历而超时。为减少一次遍历而把代码写得晦涩复杂，得不偿失。
    #
    #    - 真正的性能优化源于“选择合适的数据结构”，而非“在一个不合适的结构上过度优化”。
    #      - 需要 O(1) 尾部插入 -> 选择“带尾指针的单链表”。
    #      - 需要 O(1) 尾部删除 -> 选择“双向链表”。
    #
    #    - 理解算法题的考察重点: 链表题主要考察对“链表结构”和“指针操作”的理解，例如：
    #      - 是否知道删除操作需要找到“前驱节点”。
    #      - 是否知道可以引入“哑节点 (dummy node)”来优雅地处理边界情况。
    #      - 是否能熟练运用“双指针”、“快慢指针”等技巧。
    #      考察的重点是这些核心概念，而不是把两次遍历优化成一次的“炫技”。
    #
    #    - 对性能的辩证思考: 一个逻辑复杂的单次遍历（如循环内维护多个指针）与两个逻辑简单的遍历相比，
    #      由于指令更复杂、分支预测可能更差等原因，前者的实际性能未必更优。
    #
    # =========================================================================================
    # *****************************************************************************************
    # * 核心洞察：关于 insert 和 delete by index 逻辑统一性的思考
    # *****************************************************************************************
    #
    # 通过对标准版 insert 和 delete 函数的分析，可以发现一个非常重要的设计思想：
    # “通过在函数入口处设立严格的边界检查（如判断索引范围），可以极大地简化和统一函数的核心实现逻辑。”
    #
    # --- 1. insert 方法的逻辑统一之美 ---
    #
    # * 前提：
    #   我们采用标准框架，即通过 `if not 0 <= index <= len(self):` 预先判断并处理所有非法索引。
    #
    # * 统一的实现：
    #   我们只需将 `index == 0` (头插) 作为特殊情况处理。对于所有其他合法情况 (即 1 <= index <= len(self))，
    #   都可以归结为【同一个操作流程】：
    #   1. 找到 `index - 1` 位置的前驱节点 `prev`。
    #   2. 执行统一的指针交换：
    #      new_node.next = prev.next
    #      prev.next = new_node
    #
    # * 精妙之处 (Aha! Moment):
    #   这个逻辑惊人地、且自然地适用于【尾部插入】 (`index == len(self)`) 的情况。
    #   - 当在尾部插入时，循环结束后 `prev` 会指向最后一个节点 (索引为 len-1)。
    #   - 执行 `new_node.next = prev.next` 时，`prev.next` 恰好是 `None`。
    #   - 这使得新节点的 `next` 被正确地设置为 `None`，完美地成为了新的尾节点。
    #   - 这个过程与 `prepend` 在空链表上头插时，`new_node.next = self.head` (此时 head 为 None) 的原理异曲同工。
    #   - 结论: `None` 这个值在两种边界情况（空链表头插、非空链表尾插）下，都自然地融入了统一的逻辑中，
    #     使得我们不再需要为尾部插入编写专门的 `if/else` 分类讨论。
    #
    # --- 2. delete 方法的逻辑一致性 ---
    #
    # * 前提：
    #   我们采用标准的删除索引范围 `0 <= index < len(self)`。
    #
    # * 逻辑的必然简化：
    #   - 正是因为 `delete` 的合法索引最大值是 `len(self) - 1`，
    #     所以我们需要找到的前驱节点 `prev` 的最大索引只会是 `(len-1) - 1 = len-2`。
    #   - 这就带来一个非常重要的保证：对于任何合法的、非头部的删除操作，我们找到的 `prev` 节点，
    #     它的 `prev.next` (也就是要被删除的那个节点) **永远不可能是 `None`**。
    #
    # * 精妙之处 (Aha! Moment):
    #   - 这个保证使得删除操作的核心逻辑 `prev.next = prev.next.next` 对于所有中间和尾部删除的情况，
    #     都是绝对安全的，无需再额外检查 `prev.next` 是否存在。
    #   - 因此，和 `insert` 类似，在处理完头节点删除后，所有其他情况也都可以被一个统一的、简洁的逻辑所覆盖。
    #
    # --- 最终结论 ---
    #
    # 设定清晰、严格的规则（如索引范围），往往不是让问题变得更麻烦，反而能消除大量需要特殊处理的“例外情况”，
    # 让核心代码更加健壮、优雅和高度统一。
    #
    def find_try(self, value):
        """
        查找值为value的节点，返回其索引，找不到返回-1
        时间复杂度: O(n)
        """
        if self.is_empty():
            return -1
        # 这个是不需要的，while current包含了这一点

        current = self.head
        index = 0

        # while current.val != value and current is not None:
        # 经典逻辑错误，会导致找不到值程序出错
        # and遵循短路求值原则，从左到右判断条件
        # 当 current 为 None 的时候,他会先判断current.val != value，报错
        # 程序没有机会判断右边的条件
        # 交换条件后代码就正确了
        while current is not None and current.val != value:
            current = current.next
            index += 1

        if current:
            return index
        else:
            return -1

    def find(self, value):
        """
        查找值为value的节点，返回其索引，找不到返回-1
        时间复杂度: O(n)
        """
        current = self.head
        index = 0
        while current:
            if current.val == value:
                # 把判断拆到两个代码行，更加安全
                # 这样写明确了判断顺序
                # 更防御性，健壮的代码
                return index
            current = current.next
            index += 1
        return -1

    def get(self, index):
        """
        获取指定索引位置的节点的值
        时间复杂度: O(n)
        """
        if not 0 <= index < len(self):
            raise IndexError("Index out of range.")

        current = self.head
        for _ in range(index):
            current = current.next

        return current

    # --- 核心：经典/进阶算法 (面试高频) ---

    def reverse_try(self):
        """
        反转整个链表 (迭代法)
        时间复杂度: O(n)
        """
        if len(self) < 2:
            return

        prev = self.head
        current = prev.next
        while current:
            # 循环条件不能是curren.next，不然比如只有两个元素，那么直接结束，不反转
            # 既然条件是current，那么current.next有可能为None
            # 无论是否current是最后一个节点，current.next = prev都是必须的
            # 先写出通用的四句逻辑，看看如果current是最后一个节点，要不要修改
            # 发现是通用的，无非是使 current 变成了 None，此时原链表最后一个节点存储在prev
            # 如果判断current.next，其实没有必要

            temp = current.next
            current.next = prev
            prev = current
            current = temp

        self.head = prev
        # 还是犯了逻辑问题,这里的问题是没有修改原始头指针的 next
        # current 从第二个结点开始，这是不对的，此时第一个节点的 next 指向第二个节点
        # 所以current必须从第一个，也就是头节点开始
        # 此时头节点需要变成最后的尾节点，next 指向 None，于是只需要 prev 初始化为 None，就可以统一处理
        # 此时如果链表是空链表和单链表，检查发现用统一框架处理，什么也没做，符合实际
        # 链表可以先写出统一的处理代码，再检查边界条件是否符合，还是要额外单独讨论
        # temp 命名为 next_node 可读性更好

    def reverse(self):
        """
        反转整个链表 (迭代法)
        时间复杂度: O(n)
        """
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def find_middle_node(self):
        """
        查找链表的中间节点 (快慢指针法)
        时间复杂度: O(n)
        """
        if self.is_empty:
            return None
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow

    def has_cycle(self):
        """
        判断链表是否有环 (快慢指针法)
        时间复杂度: O(n)
        """
        # 考虑边界条件，首先，由于 fast 是快指针，每次跑两步，所以 while 的循环条件一定是 while fast and fast.next
        # 如果 while 循环结束了， 说明链表有结尾，一定没有环（有环的单链表遍历不会停止）
        # 接下来考虑判断条件，判断 slow 和 fast 是否相等。应该移动前判断还是移动后判断
        # 考虑初始条件，slow 初始一定是head， fast 是和 slow 相同还是 slow 的 next
        # 如果都是 head, 那么必须先移动再比较，初始条件检查链表非空即可
        # 如果初始不同，可以先比较再移动，初始条件还需要额外保证链表有两个节点
        # 尝试一下两种写法
        """
        if self.is_empty():
            return False
        """
        # 基本实现正确，但是上面这句包括在了后面的代码中，仍然可以省略
        # 注意当空链表， fast 是 None，不会判断 fast.next，短路求值会把整个表达式设置为 False
        # 然后退出循环，返回False，所以第一句代码是冗余的，但为了清晰的边界条件和提高可读性，也可以保留
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
        """
        if not self.head or not self.head.next:
            # 类似的，这里其实判断不为空链表，即 slow.next 不报错即可，利用了 and 运算符的短路求值
            return False
        slow = self.head
        fast = slow.next
        while fast and fast.next:
            if slow == fast:
                return True
            slow = slow.next
            fast = fast.next.next
        return False
        """

    @staticmethod
    def merge_sorted_lists(l1: "SinglyLinkedList", l2: "SinglyLinkedList"):
        """
        (静态方法) 合并两个有序链表
        时间复杂度: O(m+n)，m和n分别为两个链表的长度
        """
        dummy = ListNode(0)
        current = dummy

        p1 = l1.head
        p2 = l2.head

        while p1 and p2:
            if p1.val <= p2.val:
                current.next = p1
                p1 = p1.next
            else:
                current.next = p2
                p2 = p2.next
            current = current.next

        # 连接剩余的节点
        current.next = p1 if p1 else p2

        # 创建一个新的链表对象来返回结果
        merged_list = SinglyLinkedList()
        merged_list.head = dummy.next
        return merged_list

    # 为什么这个方法前面要加 @staticmethod？
    # 简单来说：因为 merge_sorted_lists 这个函数的功能，逻辑上与 SinglyLinkedList 类紧密相关，但它又不需要访问任何一个具体的链表实例（即不需要 self 参数）
    # 它的任务是接收两个外部传入的链表 l1 和 l2 作为参数，然后返回一个全新的、合并后的链表
    # 在整个过程中，它完全没有读取或修改某一个特定链表实例的内部状态（比如 self.head）。它是一个独立的操作
    # 在文件顶部直接定义 def merge_sorted_lists(l1, l2): ... 将其写在类的外面在功能上是等价的
    # 但是，把它作为类的静态方法，是一种更好的代码组织方式。因为“合并两个有序链表”这个操作，在概念上是属于“链表”这个范畴的
    # 将它放在 SinglyLinkedList 类内部，可以让所有与链表相关的逻辑都聚合在一起，使得代码结构更清晰，也更容易被其他开发者找到和使用（通过 SinglyLinkedList.merge_sorted_lists(...) 来调用）
    # : "SinglyLinkedList" 用于参数的类型声明
    # 为什么要带引号，核心概念，前向引用
    # Python解释器读取类 class SinglyLinkedList: 定义时，它是从上到下执行的
    # 当它读到 def merge_sorted_lists(l1: "SinglyLinkedList", ...): 这一行时，SinglyLinkedList 这个类本身还没有被完整地创建和定义好
    # 如果您不加引号，直接写成 l1: SinglyLinkedList，Python会试图立即查找一个名为 SinglyLinkedList 的已定义对象，但此时它还不存在，于是就会抛出 NameError 的错误
    # 把类型名称写成字符串 "SinglyLinkedList"，就是在使用一种叫做“前向引用”的技巧
    # 这等于在告诉Python：“嘿，这个参数 l1 的类型是一个叫做 SinglyLinkedList 的东西，但先别急着去找它，因为现在正在定义它
    # 只需要先把这个名字（字符串）记下来，等整个类都定义完毕之后，再回头来解析它到底是什么类型。”
    # 这样就完美地解决了“在定义一个东西时，又需要引用这个东西本身”的问题


if __name__ == "__main__":
    # --- 1. 基础操作演示 ---
    print("--- 1. 基础操作 ---")
    ll = SinglyLinkedList()
    ll.append(10)
    ll.append(30)
    ll.prepend(5)
    ll.insert(2, 20)  # 在索引2的位置插入20
    print("当前链表:", ll)
    print("链表长度:", len(ll))
    print("获取索引为3的元素:", ll.get(3))
    print("查找元素10的索引:", ll.find(10))
    print("-" * 20)

    # --- 2. 删除操作演示 ---
    print("--- 2. 删除操作 ---")
    ll.append(30)
    print("添加重复元素后:", ll)
    ll.delete_by_value(5)  # 删除头部
    print("删除第一个5后:", ll)
    ll.delete_all_by_value(30)  # 删除所有30
    print("删除所有30后:", ll)
    ll.delete_by_index(1)  # 删除索引1的元素(20)
    print("删除索引1的元素后:", ll)
    print("-" * 20)

    # --- 3. 经典算法演示 ---
    print("--- 3. 经典算法 ---")
    ll.append(20)
    ll.append(30)
    ll.append(40)
    print("当前链表:", ll)

    # 反转
    ll.reverse()
    print("反转后:", ll)

    # 找中间节点
    middle_node = ll.find_middle_node()
    print("中间节点是:", middle_node)

    # 判断是否有环
    print("是否有环:", ll.has_cycle())
    # 人为制造一个环来测试
    if len(ll) > 2:
        ll.head.next.next.next = ll.head.next  # 20 -> 30
    print("制造环后，是否有环:", ll.has_cycle())
    print("-" * 20)

    # --- 4. 合并有序链表演示 ---
    print("--- 4. 合并有序链表 ---")
    list1 = SinglyLinkedList()
    list1.append(1)
    list1.append(3)
    list1.append(5)

    list2 = SinglyLinkedList()
    list2.append(2)
    list2.append(4)
    list2.append(6)

    print("List 1:", list1)
    print("List 2:", list2)
    merged = SinglyLinkedList.merge_sorted_lists(list1, list2)
    print("合并后:", merged)
    print("-" * 20)
# 部分的递归算法见题目中解答，还要研究双向链表和循环链表，以及带尾指针单链表的操作
