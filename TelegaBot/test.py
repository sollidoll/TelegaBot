keys = {'Евро':'EUR',
        'Доллар':'USD',
        'Рубль':'RUB'}

quote = input()
base = input()

if quote not in keys or base not in keys:
    print('Error')
else:
    print(keys.get(quote), keys.get(base))