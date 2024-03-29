# 1、将元组 (1,2,3) 和集合 {4,5,6} 合并成一个列表。
list_1 = list((1, 2, 3)) + list({4, 5, 6})
# 2、在列表 [1,2,3,4,5,6] 首尾分别添加整型元素 7 和 0。
list_2 = [1, 2, 3, 4, 5, 6]
list_2.insert(0, 0)
list_2.append(7)
print(list_2)
# 3、反转列表 [0,1,2,3,4,5,6,7] 。
list_3 = reversed([0, 1, 2, 3, 4, 5, 6, 7])
# 4、反转列表 [0,1,2,3,4,5,6,7] 后给出中元素 5 的索引号。
list_4 = list(reversed([0, 1, 2, 3, 4, 5, 6, 7])).index(5)
# 5、分别统计列表 [True,False,0,1,2] 中 True,False,0,1,2的元素个数，发现了什么？

# 6、从列表 [True,1,0,‘x’,None,‘x’,False,2,True] 中删除元素‘x’。
# 7、从列表 [True,1,0,‘x’,None,‘x’,False,2,True] 中删除索引号为4的元素。
# 8、删除列表中索引号为奇数（或偶数）的元素。
# 9、清空列表中的所有元素。
# 10、对列表 [3,0,8,5,7] 分别做升序和降序排列。
# 11、将列表 [3,0,8,5,7] 中大于 5 元素置为1，其余元素置为0。
# 12、遍历列表 [‘x’,‘y’,‘z’]，打印每一个元素及其对应的索引号。
# 13、将列表 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 拆分为奇数组和偶数组两个列表。
# 14、分别根据每一行的首元素和尾元素大小对二维列表 [[6, 5], [3, 7], [2, 8]] 排序。
# 15、从列表 [1,4,7,2,5,8] 索引为3的位置开始，依次插入列表 [‘x’,‘y’,‘z’] 的所有元素。
# 16、快速生成由 [5,50) 区间内的整数组成的列表。
# 17、若 a = [1,2,3]，令 b = a，执行 b[0] = 9， a[0]亦被改变。为何？如何避免？
# 18、将列表 [‘x’,‘y’,‘z’] 和 [1,2,3] 转成 [(‘x’,1),(‘y’,2),(‘z’,3)] 的形式。
# 19、以列表形式返回字典 {‘Alice’: 20, ‘Beth’: 18, ‘Cecil’: 21} 中所有的键。
d = {'Alice': 20, 'Beth': 18, 'Cecil': 21}
print([i for i in d.keys()])
# 20、以列表形式返回字典 {‘Alice’: 20, ‘Beth’: 18, ‘Cecil’: 21} 中所有的值。
print([d[i] for i in d.keys()])
# 21、以列表形式返回字典 {‘Alice’: 20, ‘Beth’: 18, ‘Cecil’: 21} 中所有键值对组成的元组。
print(tuple([d[i] for i in d.keys()]))
