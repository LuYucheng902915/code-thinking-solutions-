# 创建一个空列表
empty_list: list[int] = []  # 直接使用小写的 list 关键字来作为类型提示,Python3.9之后
print("空列表:", empty_list)

# from typing import List
# empty_list: List[int] = []
# 旧版本为了保证代码好的向后兼容性

# 创建一个包含数字的列表
numbers = [1, 2, 3, 4, 5]
print("数字列表:", numbers)

# 创建一个包含字符串的列表
fruits = ["apple", "banana", "cherry"]
print("水果列表:", fruits)

# 创建一个包含不同类型元素的混合列表
mixed_list = [1, "apple", 3.14, True]
print("混合类型列表:", mixed_list)

# 访问列表中的第一个元素
first_fruit = fruits[0]
print("第一个水果:", first_fruit)

# 访问列表中的第三个元素
third_fruit = fruits[2]
print("第三个水果:", third_fruit)

# 访问列表中的最后一个元素
last_fruit = fruits[-1]
print("最后一个水果:", last_fruit)

# 修改列表中的元素
fruits[1] = "orange"
print("将第二个水果改为orange后:", fruits)

# 在列表末尾添加元素
fruits.append("banana")
print("在末尾添加banana后:", fruits)

# 在指定位置插入元素
fruits.insert(1, "strawberry")
print("在第二个位置插入strawberry后:", fruits)

# 删除指定位置的元素
del fruits[1]
print("删除第二个元素后:", fruits)

# 弹出指定位置的元素，并返回该元素
removed_fruit = fruits.pop(2)
print("弹出第三个元素:", removed_fruit)
print("弹出元素后的列表:", fruits)

# 删除列表中第一个匹配的元素
fruits.remove("banana")
print("删除第一个banana后:", fruits)

# 获取列表长度
num_of_fruits = len(fruits)
print("水果数量:", num_of_fruits)

# 判断元素是否在列表中
print("apple是否在水果列表中:", "apple" in fruits)
print("banana是否不在水果列表中:", "banana" not in fruits)

# 列表排序（升序）
fruits = ["apple", "orange", "cherry", "banana"]
fruits.sort()
print("升序排序后的水果列表:", fruits)

# 列表排序（降序）
fruits.sort(reverse=True)
print("降序排序后的水果列表:", fruits)

# 合并另一个列表
fruits.extend(["kiwi", "mango"])
print("合并kiwi和mango后的水果列表:", fruits)

# 按元素长度排序
fruits.sort(key=len)
print("按长度排序后的水果列表:", fruits)

# 反转列表
fruits.reverse()
print("反转后的水果列表:", fruits)

# 复制列表
fruits_copy = fruits.copy()
print("水果列表的副本:", fruits_copy)

# 清空列表
fruits.clear()
print("清空后的水果列表:", fruits)

# 其他常用操作补充：

# 统计某个元素出现的次数
numbers = [1, 2, 3, 2, 4, 2, 5]
count_2 = numbers.count(2)
print("数字2在numbers中出现的次数:", count_2)

# 查找某个元素第一次出现的索引
index_3 = numbers.index(3)
print("数字3在numbers中的索引位置:", index_3)

# 列表切片
slice_numbers = numbers[1:4]
print("numbers的第2到第4个元素切片:", slice_numbers)

# 列表推导式（生成新列表）
squared = [x**2 for x in numbers]
print("numbers中每个元素的平方:", squared)
