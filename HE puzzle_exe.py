amount_ox = 1
amount_pigs = 14
amount_sheep = 80


def result_check(x, y, z):
    if x * 10 + y * 3 + 0.5 * z == 100:
        return False
    else:
        return True


Bool = result_check(amount_ox, amount_pigs, amount_sheep)

while Bool:
    # print(amount_ox, amount_pigs, amount_sheep)
    if amount_ox >= 10:
        break
    if amount_sheep < 100:
        amount_sheep += 1
    else:
        print("hi")
        if amount_pigs < 33:
            amount_sheep = 1
            amount_pigs += 1
        else:
            amount_sheep = 1
            amount_pigs = 1
            amount_ox += 1
    Bool = result_check(amount_ox, amount_pigs, amount_sheep)

print("{0} ox, {1} pigs and {2} sheep".format(amount_ox, amount_pigs, amount_sheep))
