import filesystem

def main(raw, flags, args, env):
    path = filesystem.canonalize(env.get("cwd", "")+"/"+args[0])
    fpath = ""
    for fpart in filesystem.iterate(path):
        fpath = "/" + fpart
        if not filesystem.exists(fpath):
            print(f"cd: no such directory: {fpath}")
            return 1
        if not filesystem.isdirectory(fpath):
            print(f"cd: is not a directory: {fpath}")
            return 1
    env["cwd"] = fpath
