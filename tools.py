def normal_look(msg):
    a = msg.split('\n')
    b = []
    for i in a:
        if i.replace(" ", "") != '':
            i = " ".join(i.split())
            b.append(i)

    return '\n'.join(b)

