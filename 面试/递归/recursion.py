import sys

"""
    - 递归基本原理：
        递归函数特性：
        -- 必须有一个明确的结束条件；
        -- 每次进入更深一层递归时，问题规模相比上次递归都应有所减少
        -- 相邻两次重复之间有紧密的联系，前一次要为后一次做准备（通常前一次的输出就作为后一次的输入）。
        -- 递归效率不高，递归层次过多会导致栈溢出（在计算机中，函数调用是通过栈（stack）这种数据结构实现的，每当进入一个函数调用，
           栈就会加一层栈帧，每当函数返回，栈就会减一层栈帧。由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出）
"""


def function1(n):
    """
        一般递归
         每次执行将多了一个函数推入，每一级递归都需要调用函数, 会创建新的栈,随着递归深度的增加, 创建的栈越来越多

        function1(5)
        5 + function1(4)
        5 + 4 + function1(3)
        5 + 4 + 3 + function1(2)
        5 + 4 + 3 + 2 + function1(1)
        5 + 4 + 3 + 3
        5 + 4 + 6
        5 + 10
        15

        递归过程如 ->
            -- 去的过程：
                n = 5
                     n = 4
                           n = 3
                                n = 2
                                     n = 1
                                            n = 0
                                            n = 0   -- 返回的过程
                                     n = 1
                                n = 2
                           n = 3
                     n = 4
                n = 5
        执行完毕
    """
    if n == 1:
        return 1
    return n + function1(n - 1)


"""
从内存角度（本质）来分析：每调用一次函数，都会单独开辟一份栈帧空间，递归函数就是不停的开辟和释放栈帧空间的过程，
具体来理解下：一个普通函数从执行到结束，就是一个开辟空间和释放空间的过程；而递归函数是在调用最外层函数时，先开辟一个最外层空间，
每调用一次自身，就会在最外层空间内，再自己开辟本次的空间（所以递归耗内存）（还有一种说法是，不断的本次空间的基础上再开辟空间，
等于是不断的嵌套，其实这两种说法本质上是一样的，因为信息都可以做到不共享），空间之间如果不通过参数传递或者用return 返回值，信息是不共享的

"""


def function2(n, total=0):
    """
    尾递归
    每一级调用直接返回函数的返回值更新调用栈,而不用创建新的调用栈, 类似迭代的实现, 时间和空间上均优化了一般递归
    function2(5)
    function2(4, 5)
    function2(3, 9)
    function2(2, 12)
    function2(1, 14)
    function2(0, 15)
    即计算之前会把计算结果推到下一个function2
    """
    if n == 0:
        return total
    return function2(n - 1, total + n)


"""
基础的python 的递归是有限制的，大概是1000左右，所以无法进行深递归
所以可以下列模块
sys.setrecursionlimit(30000)
print(function2(20000))
"""

"""
装饰器处理
"""


class TailRecurseException(Exception):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    This function decorates a function with tail call
    optimization. It does this by throwing an exception
    if it is it's own grandparent, and catching such
    exceptions to fake the tail call optimization.
    This function fails if the decorated
    function recurses in a non-tail context.
    """

    def func(*args, **kwargs):
        f = sys._getframe()
        # 为什么是grandparent, 函数默认的第一层递归是父调用,
        # 对于尾递归, 不希望产生新的函数调用(即:祖父调用),
        # 所以这里抛出异常, 拿到参数, 退出被修饰函数的递归调用栈!(后面有动图分析)
        if f.f_back and f.f_back.f_back \
                and f.f_back.f_back.f_code == f.f_code:
            # 抛出异常
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    # 捕获异常, 拿到参数, 退出被修饰函数的递归调用栈
                    args = e.args
                    kwargs = e.kwargs

    func.__doc__ = g.__doc__
    return func


@tail_call_optimized
def function3(n, acc=1):
    # calculate a factorial
    if n == 0:
        return acc
    return function3(n - 1, n * acc)


print(function3(10000))
