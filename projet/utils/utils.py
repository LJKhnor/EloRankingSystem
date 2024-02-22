def processColor(ranking,rankings_tupple):
    length = rankings_tupple.__len__()
    gradient = ["lightgreen", "lightyellow", "salmon"]
    gradient_length = gradient.__len__()
    j=0

    for i in range(length):
        if ranking[0] == rankings_tupple[i][0]:
            j=i

    if j == 0:
        return gradient[0]
    elif j == length-1:
        return gradient[2]
    else:
        return gradient[1]

