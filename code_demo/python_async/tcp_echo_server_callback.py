"""
python3 selectos 模块演示：
"""
import selectors
import socket

sel = selectors.DefaultSelector()  # 定义一个 selector


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)   # 注意这里的 setblocking 为 False
    sel.register(conn, selectors.EVENT_READ, read)   # 注册监听可读事件的回调


def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)  # 取消对 conn socket 的事件监听
        conn.close()


sock = socket.socket()
sock.bind(('localhost', 1234))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)    # sock 可读的时候执行 accept 回调

while True:
    events = sel.select()   # 等待直到监听的socket 有注册的事件发生
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
