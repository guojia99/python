import numpy
import numpy as np

from common.p import p

print("""
    bool_	布尔型数据类型（True 或者 False）
    int_	默认的整数类型（类似于 C 语言中的 long，int32 或 int64）
    intc	与 C 的 int 类型一样，一般是 int32 或 int 64
    intp	用于索引的整数类型（类似于 C 的 ssize_t，一般情况下仍然是 int32 或 int64）
    int8	字节（-128 to 127）
    int16	整数（-32768 to 32767）
    int32	整数（-2147483648 to 2147483647）
    int64	整数（-9223372036854775808 to 9223372036854775807）
    uint8	无符号整数（0 to 255）
    uint16	无符号整数（0 to 65535）
    uint32	无符号整数（0 to 4294967295）
    uint64	无符号整数（0 to 18446744073709551615）
    float_	float64 类型的简写
    float16	半精度浮点数，包括：1 个符号位，5 个指数位，10 个尾数位
    float32	单精度浮点数，包括：1 个符号位，8 个指数位，23 个尾数位
    float64	双精度浮点数，包括：1 个符号位，11 个指数位，52 个尾数位
    complex_	complex128 类型的简写，即 128 位复数
    complex64	复数，表示双 32 位浮点数（实数部分和虚数部分）
    complex128	复数，表示双 64 位浮点数（实数部分和虚数部分）
""")

print("""
    字符代码前缀
    b	布尔型
    i	(有符号) 整型
    u	无符号整型 integer
    f	浮点型
    c	复数浮点型
    m	timedelta（时间间隔）
    M	datetime（日期时间）
    O	(Python) 对象
    S, a	(byte-)字符串
    U	Unicode
    V	原始数据 (void)
""")

print("""
    数据类型对象
    numpy.dtype(object, align, copy)
    object - 要转换为的数据类型对象
    align - 如果为 true，填充字段使其类似 C 的结构体。
    copy - 复制 dtype 对象 ，如果为 false，则是对内置数据类型对象的引用
""")

p(numpy.dtype(numpy.int32), "numpy.dtype(numpy.int32)", "数据类型定义")
"""
int32
"""

# int8, int16, int32, int64 四种数据类型可以使用字符串 'i1', 'i2','i4','i8' 代替
p(numpy.dtype("i8"), "numpy.dtype('i8')", "使用特殊字符串进行定义")
"""
int64 
"""

# 可以按照字节顺序标注
p(np.dtype('<i4'), "np.dtype('<i4')", "通过标注均可")
"""
int32 
"""
p(np.dtype('<u8'), "np.dtype('>i8')", "通过标注均可")
"""
uint64 
"""

# 结构化数据类型
p(np.dtype([('age', np.int32)]), "np.dtype(['age', np.int32])", "定义数据类型结构体")
"""
[('age', '<i4')] 
"""
# 该结构可用于实际存取
dt = np.dtype([('age', np.int32)])
list_1 = [(10,), (11,), (12,)]
p(np.array(object=list_1, dtype=dt),
  "dt = np.dtype([('age', np.int32)])\nlist_1 = [(10, ), (11, ), (12, )]\nnp.array(object=list_1, dtype=dt)",
  "存储中也可对应提取")
"""
[(10,) (11,) (12,)] 
"""

# 可以定义一个复杂的结构体
device = [
    ('name', 'S20'), ('data_point', 'f4'), ('number', 'i4')
]
device_dt = np.dtype(device)
list_2 = [
    (123, 123, 123), (456, 456, 456)
]
device_arr = np.array(object=list_2, dtype=device_dt)
p(device_arr,
  "device = [\n    ('name', 's20'), ('data_point', 'f4'), ('number', 'i4')\n]\ndevice_dt = np.dtype(device)\nlist_2 = [\n    (123, 123, 123), (456, 456, 456)\n]\ndevice_arr = np.array(object=list_2, dtype=device_dt)",
  "复杂结构体")
"""
[(b'123', 123., 123) (b'456', 456., 456)] 
"""
