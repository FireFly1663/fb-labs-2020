import codecs as cs
import math

def filter(textLine):
    abc = "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я".split()
    abc.append(' ')
    for ltr in textLine:
        if ltr not in abc:
            textLine = textLine.replace(ltr, ' ')
    return textLine


def entropy(dataDict):
    entr = 0
    for l in dataDict:
        entr = entr + dataDict[l] * math.log2(dataDict[l])
    return entr * (-1)


File = input('Введите название файла: ')
spaces = int(input('Сколько должно быть пробелов? (0, 1): '))
Steps = int(input('Какой должен быть шаг биграммы? (1, 2): ')) - 1

text = cs.open(File, encoding='utf-8')
letters = dict()
bigram = dict()
letterCounter = 0
bigramCounter = 0
prevChar = 0
isDouble = 1


for k in letters:
    letters[k] = letters[k] / letterCounter
for k in bigram:
    bigram[k] = bigram[k] / bigramCounter


for line in text:
    line = filter(line.lower())
    line = line.strip()
    line = ' '.join(line.split())

    if spaces == 0:
        line = line.replace(' ', '')

    for sym in line:
        letters[sym] = letters.get(sym, 0) + 1

        if Steps: isDouble = letterCounter % 2 == 1

        if letterCounter != 0 and isDouble:
            bigram = prevChar + sym
            bigram[bigram] = bigram.get(bigram, 0) + 1
            prevChar = sym
            bigramCounter = bigramCounter + 1
        elif not isDouble or not Steps:
            prevChar = sym

        letterCounter = letterCounter + 1


# =======================================


print('Letters:')
printSorted(letters)
print('bigram:')
printSorted(bigram)

H1L = round(entropy(letters), 6)
H2B = round(entropy(bigram) / 2, 6)

print('Entropy:')
print('H1L:', H1L)
print('H2B:', H2B)

# =======================================

input()