import numpy
import numpy as np

from common.p import p

print("""
    ndarray.ndim	    秩，即轴的数量或维度的数量
    ndarray.shape	    数组的维度，对于矩阵，n 行 m 列
    ndarray.size	    数组元素的总个数，相当于 .shape 中 n*m 的值
    ndarray.dtype	    ndarray 对象的元素类型
    ndarray.itemsize	ndarray 对象中每个元素的大小，以字节为单位
    ndarray.flags	    ndarray 对象的内存信息
    ndarray.real	    ndarray 元素的实部
    ndarray.imag	    ndarray 元素的虚部
    ndarray.data	    包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。
""")

arr_24 = np.arange(24)
p(arr_24, "arr_24 = np.arange(24)", "初始化一个24个数的一维数组")

# ndim 属性， 返回数组的维数，即秩
p(arr_24.ndim, "arr_24.ndim", "一维数组的")

# 三维数组
arr_24_to_3 = arr_24.reshape(2, 4, 3)
p(arr_24_to_3.ndim, f"arr_24_to_3 = arr_24.reshape(2, 4, 3)\n{arr_24_to_3}\narr_24_to_3.ndim", "把一维数组处理后可得到一个三维数组")

print("""
ndarray.shape   表示数组的维度，返回一个元组，这个元组的长度就是维度的数目，即 ndim 属性(秩)。比如，一个二维数组，其维度表示"行数"和"列数"。
ndarray.shape   也可以用于调整数组大小。
ndarray.reshape 通常返回的是非拷贝副本，即改变返回后数组的元素，原数组对应元素的值也会改变。
""")

p(np.array([[1, 2, 3], [4, 5, 6]]), "np.array([[1,2,3],[4,5,6]])", "数组的纬度")

# 可以对数组进行调整
arr = np.array([[1, 2, 3], [4, 5, 6]])
arr.shape = (3, 2)
p(arr, "arr = np.array([[1, 2, 3], [4, 5, 6]])\narr.shape = (3, 2)", "将数组调整后可获取与对应纬度一致的数组")

arr2 = np.array([[1, 2, 3], [4, 5, 6]])
arr3 = arr2.reshape(3, 2)
p(arr3, "arr2 = np.array([[1, 2, 3], [4, 5, 6]])\narr3 = arr2.reshape(3, 2)", "reshape函数可以进行相同的操作")

print("""
ndarray.itemsize 以字节的形式返回数组中每一个元素的大小。
例如，一个元素类型为 float64 的数组 itemsize 属性值为 8(float64 占用 64 个 bits，每个字节长度为 8，所以 64/8，占用 8 个字节），
又如，一个元素类型为 complex32 的数组 item 属性为 4（32/8）。
""")
p(np.array([1, 2, 3, 4, 5], dtype=np.int8).itemsize, "np.array([1,2,3,4,5], dtype = np.int8).itemsize",
  "数组的 dtype 为 int8(一个字节) ")
p(np.array([1, 2, 3, 4, 5], dtype=np.float64).itemsize, "np.array([1, 2, 3, 4, 5], dtype=np.float64).itemsize",
  "数组的 dtype 现在为 float64(八个字节)")

print("""
ndarray.flags
ndarray.flags 返回 ndarray 对象的内存信息，包含以下属性：

C_CONTIGUOUS (C)	数据是在一个单一的C风格的连续段中
F_CONTIGUOUS (F)	数据是在一个单一的Fortran风格的连续段中
OWNDATA (O)	        数组拥有它所使用的内存或从另一个对象中借用它
WRITEABLE (W)	    数据区域可以被写入，将该值设置为 False，则数据为只读
ALIGNED (A)	        数据和所有元素都适当地对齐到硬件上
UPDATEIFCOPY (U)	这个数组是其它数组的一个副本，当这个数组被释放时，原数组的内容将被更新
""")
p(np.array([1, 2, 3, 4, 5]).flags, "np.array([1, 2, 3, 4, 5]).flags", "flags 数据")

p(np.array([1, 2, 3, 4, 5]).real, "np.array([1, 2, 3, 4, 5]).real", "数组实部")
p(np.array([1, 2, 3, 4, 5]).imag, "np.array([1, 2, 3, 4, 5]).imag", "数组虚部")

# 创建一个未初始化的随机数组
print("""
numpy.empty(shape, dtype = float, order = 'C')
shape	数组形状
dtype	数据类型，可选
order	有"C"和"F"两个选项,分别代表，行优先和列优先，在计算机内存中的存储元素的顺序, 表面看无区别。
""")
p(np.empty(shape=[3, 2], dtype=int, order="C"), "np.empty(shape=[3, 2], dtype=int, order='C')", "初始化一个随机数组,order为C")
p(np.empty(shape=[3, 2], dtype=int, order="F"), "np.empty(shape=[3, 2], dtype=int, order='F')", "初始化一个随机数组,order为F")

print("""
numpy.zeros
创建指定大小的数组，数组元素以 0 来填充：
shape	数组形状
dtype	数据类型，可选
order	'C' 用于 C 的行数组，或者 'F' 用于 FORTRAN 的列数组
""")

p(np.zeros(5), "np.zeros(5)", "默认浮点数")
p(np.zeros((5,), dtype=np.int8), "np.zeros((5,), dtype = np.int) ", "更改为整数")
p(np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'i4')]),
  "np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'i4')])", "自定义数据类型两个元素")
p(np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'i4'), ('z', 'i4')]),
  "np.zeros((2, 2), dtype=[('x', 'i4'), ('y', 'i4'), ('z', 'i4')])", "自定义数据类型三个元素")

print("""
numpy.ones
创建指定形状的数组，数组元素以 1 来填充：
numpy.ones(shape, dtype = None, order = 'C')
shape	数组形状
dtype	数据类型，可选
order	'C' 用于 C 的行数组，或者 'F' 用于 FORTRAN 的列数组
""")
p(np.ones([2, 2], dtype=int), "np.ones([2,2], dtype = int)", "语法和zeros一致")

print("""
numpy.asarray
numpy.asarray 类似 numpy.array，但 numpy.asarray 参数只有三个，比 numpy.array 少两个。
numpy.asarray(a, dtype = None, order = None)
a	任意形式的输入参数，可以是，列表, 列表的元组, 元组, 元组的元组, 元组的列表，多维数组
dtype	数据类型，可选
order	可选，有"C"和"F"两个选项,分别代表，行优先和列优先，在计算机内存中的存储元素的顺序。
""")

p(np.asarray([1, 2, 3]), "np.asarray([1, 2, 3])", "列表形式")
p(np.asarray((1, 2, 3)), "np.asarray((1, 2, 3))", "元组形式")

print("""
numpy.frombuffer
numpy.frombuffer 用于实现动态数组。
numpy.frombuffer 接受 buffer 输入参数，以流的形式读入转化成 ndarray 对象。
numpy.frombuffer(buffer, dtype = float, count = -1, offset = 0)
buffer 是字符串的时候，Python3 默认 str 是 Unicode 类型，所以要转成 bytestring 在原 str 前加上 b。

buffer	可以是任意对象，会以流的形式读入。
dtype	返回数组的数据类型，可选
count	读取的数据数量，默认为-1，读取所有数据。
offset	读取的起始位置，默认为0。
""")

p(np.frombuffer(b"HHHHHQQQQQ QQ", dtype="S1"), "np.frombuffer(b'HHHHHQQQQQ QQ', dtype='S1')",
  "用字节字符串进行导入，同时格式为1个字符串为一个元素")

print("""
numpy.fromiter
numpy.fromiter 方法从可迭代对象中建立 ndarray 对象，返回一维数组。
numpy.fromiter(iterable, dtype, count=-1)
iterable	可迭代对象
dtype	    返回数组的数据类型
count	    读取的数据数量，默认为-1，读取所有数据
""")

p(np.fromiter(iter(range(10)), dtype=int), "np.fromiter(iter(range(10)), dtype=int)", "可迭代对象转数组，这样可以省下内存")

print("""
numpy.arange
numpy 包中的使用 arange 函数创建数值范围并返回 ndarray 对象，函数格式如下：
numpy.arange(start, stop, step, dtype)
根据 start 与 stop 指定的范围以及 step 设定的步长，生成一个 ndarray。
start	起始值，默认为0
stop	终止值（不包含）
step	步长，默认为1
dtype	返回ndarray的数据类型，如果没有提供，则会使用输入数据的类型。
""")

p(np.arange(6), "np.arange(6)", "生成0-5的数组")
p(np.arange(5, 20, 2), "np.arange(5,20,2)", "设置起始值及步长")

print("""
numpy.linspace
numpy.linspace 函数用于创建一个一维数组，数组是一个等差数列构成的，格式如下：
np.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
start	    序列的起始值
stop	    序列的终止值，如果endpoint为true，该值包含于数列中
num	        要生成的等步长的样本数量，默认为50
endpoint	该值为 true 时，数列中包含stop值，反之不包含，默认是True。
retstep	    如果为 True 时，生成的数组中会显示间距，反之不显示。
dtype	    ndarray 的数据类型
""")

p(np.linspace(1, 10, 10), "np.linspace(1,10,10)", "等差数列一维数组")
p(np.linspace(10, 20, 5, endpoint=False), "np.linspace(10, 20,  5, endpoint =  False)  ", "不包含终止值20")

p(np.linspace(1, 10, 10).reshape([10, 1]), "np.linspace(1,10,10).reshape([10,1])", "设置实例间距")
p(np.linspace(1, 10, 10).reshape([5, 2]), "np.linspace(1,10,10).reshape([5,2])", "设置实例间距2")

print("""
numpy.logspace
numpy.logspace 函数用于创建一个于等比数列。格式如下：
np.logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None)

start	  序列的起始值为：base ** start
stop	  序列的终止值为：base ** stop。如果endpoint为true，该值包含于数列中
num	      要生成的等步长的样本数量，默认为50
endpoint  该值为 true 时，数列中中包含stop值，反之不包含，默认是True。
base	  对数 log 的底数。 默认为10
dtype	  ndarray 的数据类型
""")

p(np.logspace(0, 9, 10, base=2), "np.logspace(0,9,10,base=2)", "对数为2， 指数从0-9")
