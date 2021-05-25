import numpy

from common.p import p

list_1 = [1, 2, 3]
list_2 = [4, 5, 6]
list_3 = [7, 8, 9]
list_123 = [list_1, list_2, list_3]

p(list_1, "list_1 = [1, 2, 3]", "初始化列表1")
p(list_2, "list_2 = [4, 5, 6]", "初始化列表2")
p(list_3, "list_3 = [7, 8, 9]", "初始化列表3")
p(list_123, "list_123 = [list_1, list_2, list_3]", "初始化二维列表")

print(
"""
    numpy.array
    object	数组或嵌套的数列
    dtype	数组元素的数据类型，可选
    copy	对象是否需要复制，可选
    order	创建数组的样式，C为行方向，F为列方向，A为任意方向（默认）
    subok	默认返回一个与基类类型一致的数组
    ndmin	指定生成数组的最小维度
"""
)

# 1维与2维
p(numpy.array(object=list_1), "numpy.array(object=list_1)", "一维数组")
"""
[1 2 3]
"""

p(numpy.array(object=list_123), "numpy.array(object=list_123)", "二维数组")
"""
[[1 2 3]
 [4 5 6]
 [7 8 9]]
"""

# 最小纬度 如ndmin=3 代表最小纬度为3
p(numpy.array(object=list_123, ndmin=2), "numpy.array(object=list_123, ndmin=2)", "使用最小纬度")
"""
[[1 2 3]
 [4 5 6]
 [7 8 9]]
"""

p(numpy.array(object=list_123, ndmin=3), "numpy.array(object=list_123, ndmin=3)", "最小纬度将强行转化")
"""
[[[1 2 3]
  [4 5 6]
  [7 8 9]]]
"""

# dtype 参数，指定一个数据类型
p(numpy.array(object=list_1, dtype=complex), "numpy.array(object=list_1, dtype=complex)", "数据类型")
"""
[1.+0.j 2.+0.j 3.+0.j] 
"""

p(numpy.array(object=list_1, dtype=float), "numpy.array(object=list_1, dtype=float)", "数据类型")
"""
[1. 2. 3.] 
"""

p(numpy.array(object=list_1, dtype=numpy.dtype(numpy.int32)),
  "numpy.array(object=list_1, dtype=numpy.dtype(numpy.int32))", "数据类型")
"""
[1 2 3]
"""
