def coro1():
    """定义一个简单的基于生成器的协程作为子生成器"""
    word = yield 'hello'
    yield word
    return word    # 注意这里协程可以返回值了，返回的值会被塞到 StopIteration value 属性 作为 yield from 表达式的返回值


def coro2():
    """委派生成器，起到了调用方和子生成器通道的作用，请仔细理解下边的描述。
    委派生成器会在 yield from 表达式处暂停，调用方可以直接发数据发给子生成器，
    子生成器再把产出的值发给调用方。
    子生成器返回后， 解释器抛出 StopIteration异常， 并把返回值附加到异常对象上，此时委派生成器恢复
    """
    # 子生成器返回后，解释器抛出 StopIteration 异常，返回值被附加到异常对象上，此时委派生成器恢复
    result = yield from coro1()  # 这里 coro2 会暂停并把调用者的 send 发送给 coro1() 协程，coro1() 返回后其return 的值会被赋值给 result
    print('coro2 result', result)


def main():  # 调用方，用来演示调用方通过委派生成器可以直接发送值给子生成器值。这里main 是调用者，coro2 是委派生成器，coro1 是子生成器
    c2 = coro2()  # 委派生成器
    print(next(c2))   # 这里虽然调用的是 c2 的send，但是会发送给 coro1, 委派生成器进入 coro1 执行到第一个 yield 'hello' 产出 'hello'
    print(c2.send('world'))  # 委派生成器发送给 coro1，word 赋值为 'world'，之后产出 'world'
    try:
        # 继续 send 由于 coro1 已经没有 yield 语句了，直接执行到了 return 并且抛出 StopIteration
        # 同时返回的结果作为 yield from 表达式的值赋值给左边的 result，接着 coro2() 里输出 "coro2 result world"
        c2.send(None)
    except StopIteration:
        pass


main()
