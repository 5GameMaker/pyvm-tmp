import io

gpu = component.gpu
def __stdout_drawch(stream, data):
    global gpu
    w, h = gpu.get_resolution()
    if stream.y >= h:
        while stream.y >= h:
            gpu.copy(0, 1, w, h, 0, 0)
            gpu.fill(0, h-1, w, 1, " ")
            stream.y -= 1
    if len(data) == 1:
        if data == "\n":
            stream.y += 1
            stream.x = 0
            if stream.y >= h:
                while stream.y >= h:
                    gpu.copy(0, 1, w+1, h+1, 0, 0)
                    gpu.fill(0, h-1, w, 1, " ")
                    stream.y -= 1
            return
        if data == "\b":
            stream.x -= 1
            if stream.x < 0:
                stream.x = w + stream.x
                stream.y -= 1
                if stream.y < 0:
                    stream.y = h + stream.y
            return
        if data == "\r":
            stream.x = 0
            return
        if data == "\t":
            stream.x = ((stream.x // 8) + 1) * 8
            if stream.x >= w:
                stream.y += 1
                stream.x = 0
                if stream.y >= h:
                    while stream.y >= h:
                        gpu.copy(0, 1, w+1, h+1, 0, 0)
                        gpu.fill(0, h-1, w, 1, " ")
                        stream.y -= 1
            return
        gpu.set(stream.x, stream.y, data)
        stream.x += 1
        if stream.x >= w:
            stream.y += 1
            stream.x = 0
            if stream.y >= h:
                while stream.y >= h:
                    gpu.copy(0, 1, w+1, h+1, 0, 0)
                    gpu.fill(0, h-1, w, 1, " ")
                    stream.y -= 1
        return

def __stdout(stream, data):
    for ch in data:
        __stdout_drawch(stream, ch)

def __stdin(stream, amount):
    data = stream.data[:amount]
    stream.data = stream.data[amount:]
    return data

stdout = io.IOStream("wo", __stdout, None)
stdin = io.IOStream("ro", None, __stdin)
stdout.x, stdout.y = 0, 0
stdin.data = ""
def keyboard_(event):
    stdin.data += event.args[0]
    stdout.write(" \b")

fill = True
should_blink = True
def tick_(_):
    global fill
    if not should_blink: return
    fill = not fill
    stdout.write("#" if not fill else " ")
    stdout.write("\b")
event.listen("key_pushed", keyboard_)
event.listen("tick", tick_)

io.stdout = stdout
io.stdin = stdin

def print(*args, sep="\t", end="\n", file=io.stdout):
    for i in args:
        file.write(str(i))
        file.write(sep)
    file.write(end)

def input(prompt="", echo=True):
    io.stdout.write(prompt)
    _ = ""
    should_blink = True
    while True:
        __ = io.stdin.read(1)
        if __ == "\b":
            if _ == "": continue
            _ = _[:-1]
            io.stdout.write(" \b\b \b")
            continue
        if __ == "\n":
            should_blink = False
            io.stdout.write(" \n")
            return _
        if echo:
            io.stdout.write(__)
        _ += __

globals()["print"] = print
globals()["input"] = input
