range_iter = iter(range(10))
for i in range_iter:
    print('for loop produced', i)
    if i % 4 == 0:
        j = next(range_iter)
        print('But we can advance the iterator manually, too:', j)