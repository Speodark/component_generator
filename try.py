def add_to_dict(lst, value, dct):
    for i in range(len(lst) - 1):
        key = lst[i]
        if key in dct:
            dct = dct[key]
        else:
            dct[key] = {}
            dct = dct[key]
    dct[lst[-1]] = value

list1 = ['hello', 'good', 'nice']
value = 5
dictionary = {'go':3, 'hello':{'to':3}}
add_to_dict(list1, value, dictionary)
print(dictionary)
