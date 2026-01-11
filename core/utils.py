


def round_price(price, step):

    remainder = int(price / step)

    rounded_price = remainder * step

    size = len(str(step).split('.')[-1])

    return round(rounded_price, size)



def check_pos(C, B):
    raz = C - B
    return abs(raz)