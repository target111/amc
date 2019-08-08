def read_file(file):
    lines = [line.strip() for line in file.readlines()]
    combo = [(user.split(":")[0], password.split(":")[1]) for user in lines
             for password in lines]

    return combo


def chunkify(lst, threads):
    return [lst[i::threads] for i in range(threads)]
