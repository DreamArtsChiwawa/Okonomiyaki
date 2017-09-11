with open('dir_list.txt', 'r') as f:
    x = f.readlines()

i = 1
for y in x:
    print('python file_analyze.py ' + y.strip(':\n') + '/*', end='')

    if i % 3 == 0:
        print()

    else:
        print(' & ', end="")
    i += 1
