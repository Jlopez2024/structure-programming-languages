def first(list):
    try:
        return list[0]
    except:
        return None

def tail(list):
    return list[1:]

def lower(list, n):
    if list == []:
        return []
    else:
        if first(list) < n:
            return [first(list)] + lower(tail(list),n)
        else:
            return lower(tail(list), n)

def equals(list, n):
    if list == []:
        return []
    else:
        if first(list) == n:
            return [first(list)] + equals(tail(list),n)
        else:
            return equals(tail(list), n)


def upper(list, n):
    if list == []:
        return []
    else:
        if first(list) > n:
            return [first(list)] + upper(tail(list),n)
        else:
            return upper(tail(list), n)

def sort(list):
    if list == []:
        return []
    else:
        return sort(lower(list, first(list))) + equals(list, first(list)) + sort(upper(list, first(list)))

if __name__ == "__main__":
    print(sort([3,5,1,6,8,7,2,7,1,2,2]))