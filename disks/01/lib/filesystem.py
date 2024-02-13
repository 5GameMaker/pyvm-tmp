mounts = {}
_list = list

class FSException(Exception): pass

def mount(hdd, path):
    global mounts
    if hdd in [i[1] for i in mounts.items()]:
        raise FSException("Filesystem already mounted at: "+dict([_list(reversed(i)) for i in mounts.items()])[hdd])
    if path in mounts:
        raise FSException("Path is already used by mounted filesystem")
    if exists(path) and not path == "/":
        raise FSException("Path exists on a real file system")
    if not exists(parent(path)) and not path == "/":
        raise FSException("Parent directory is invalid: "+path)
    mounts[path] = hdd

def cleanse(path):
    if path == "": return "/"
    if path.endswith("/"): path = cleanse(path[:-1])
    return path

def canonalize(path):
    formed_path = []
    for n, i in enumerate(path.split("/")):
        if i == "":
            continue
        elif i == ".":
            continue
        elif i == "..":
            formed_path = formed_path[:-1]
        else:
            formed_path.append(i)
    return cleanse("/" + "/".join(formed_path))

def iterate(path):
    path = canonalize(path)
    for item in path.split("/"):
        yield item

def parent(path):
    return "/"+"/".join(_list(iterate(path))[:-1])

def to_real_path(path):
    real_path = [components.hdd, ""]
    for i in iterate(path):
        real_path[1] += "/"+i
        if real_path[1] in mounts:
            real_path = [mounts[real_path[1]], ""]
    return real_path

def exists(path):
    drive, path = to_real_path(path)
    return drive.exists(path)

def list(path):
    drive, path = to_real_path(path)
    flist = _list(drive.list(path))
    for mountpoint in mounts:
        if mounts[mountpoint] == drive: continue
        if canonalize(path).startswith(canonalize(mountpoint)): continue
        if canonalize(parent(mountpoint)) == canonalize(path):
            flist.append(["dir", mountpoint.split("/")[-1]])
    for i in flist: yield i

def open(path):
    if not exists(path): raise FSException(f"No such file or directory: {path}")
    drive, path = to_real_path(path)
    return drive.open(path)
