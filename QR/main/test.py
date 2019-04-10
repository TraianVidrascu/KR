matrice = [[1, 2],
           [3, 4]]


def test(list, t, c):
    if t > 1:
        print(list)
        return
    if c > 1:
        return

    new_list = list[:]
    new_list[c] = matrice[t][c]

    test(new_list, t + 1, c)
    test(new_list, t, c + 1)


l = [0,0]
test(l, 0, 0)
print("asd")
print(l)
