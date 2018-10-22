# yield from and future demo
class Future:
    def __init__(self):
        self.result = None   # 保存结果
        self._callbacks = []  # 保存对 Future 的回调函数

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)

    def __iter__(self):
        """ 让 Future 对象支持 yield from"""
        yield self  # 产出自己
        return self.result   # yield from 将把 result 值返回作为 yield from 表达式的值


def callback1(a, b):
    c = a + b
    c = callback2(c)
    return c


def callback2(c):
    c *= 2
    callback3(c)
    return c


def callback3(c):
    print(c)


def caller(a, b):
    callback1(a, b)


caller(1, 2)  # 输出 6


def callback_1(a, b):
    f = Future()

    def on_callback_1():
        f.set_result(a+b)

    on_callback_1()
    c = yield from f
    return c


def callback_2(c):
    f = Future()

    def on_callback_2():
        f.set_result(c*2)
    on_callback_2()
    c = yield from f
    return c


def callback_3(c):
    f = Future()

    def on_callback_3():
        f.set_result(c)
    on_callback_3()
    yield from f


def caller_use_yield_from(a, b):
    c1 = yield from callback_1(a, b)
    c2 = yield from callback_2(c1)
    yield from callback_3(c2)
    return c2


c = caller_use_yield_from(1, 2)  # coroutine
f1 = c.send(None)   # 产出第一个 future 对象
f2 = c.send(f1.result)  # 驱动运行到第二个 callback
f3 = c.send(f2.result)
try:
    f4 = c.send(None)
except StopIteration as e:
    print(e.value)   # 输出结果 6


# 使用 step 驱动
c = caller_use_yield_from(1, 2)  # coroutine
f = Future()
f.set_result(None)
next_future = c.send(f.result)


def step(future):
    next_future = c.send(future.result)
    next_future.add_done_callback(step)


while 1:
    try:
        step(f)
    except StopIteration as e:
        print(e.value)   # 输出结果 6
        break
