

import asttokens #использовать нельзя(
import keyword
import argparse


# вспомогательные функции

# алгоритм обезличивания переменных и функций

def Goto_Noname(tokens):
    index = 1
    words = []
    index2 = 1
    func = []
    for ind in range(len(tokens)-1):
        if tokens[ind][0] == 1:
            if not (keyword.iskeyword(tokens[ind][1])):
                if (tokens[ind][1] in words):
                    
                    tokens[ind][1] = 'per'
                elif (tokens[ind][1] in func):
                    
                    tokens[ind][1] = 'func'

                elif tokens[ind+1][1] == '(':
                    func.append(tokens[ind][1])
                    tokens[ind][1] = 'func'  
                    index2 += 1
                else:
                    words.append(tokens[ind][1])
                    tokens[ind][1] = 'per'  
                    index += 1
    return tokens

# запись программы в файл

def Draw_to_file(fileTo, result):

        fileTo.write((str(result)+"%"))
        fileTo.write('\n')

# возвращает список токенов и список строк токенов(двумерный массив)

def From_Programm_To_Tokens(From_Path):

    # открытие входного файла
    file = open(From_Path, 'r')
    fileFrom = ''.join(file)

    # переход к списку токенов
    my_tokens = asttokens.ASTTokens(fileFrom, parse=True)
    tokens = my_tokens.tokens

    # избавление от лишней информации(оставляю только тип токена и имя)
    for ind in range(len(tokens)):
        tokens[ind] = tokens[ind][:2]
    token = list(map(list, tokens))

    # удаляю "призрачный" токен пустой строки ''
    for ind in range(len(token)-1, -1, -1):
        if token[ind][0] == 6:
            token.pop(ind)

    # обезличиваю имена(index -> per1, count -> per2)
    tokens = Goto_Noname(token)

    # сбор списка токенов по строкам программы
    strings_tokens = []
    string = []
    for el in tokens:
        if el[0] != 4:
            string.append(el)
        else:
            strings_tokens.append(string)
            string = []

    # подготавливаю токены к подсчёту расстояния
    for ind in range(len(tokens)):
        tokens[ind] = tokens[ind][1]

    file.close()

    return tokens, strings_tokens

# подсчёт расстояния Левенштейна

def Levenshtein(tokens1, tokens2):
    matrix = [[0 for i in range(len(tokens1))] for j in range(len(tokens2))]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == 0 and j == 0:
                matrix[i][j] = 0
            elif i == 0 and j > 0:
                matrix[i][j] = j
            elif i > 0 and j == 0:
                matrix[i][j] = i
            else:
                matrix[i][j] = min(
                    matrix[i][j-1]+1, matrix[i-1][j]+1, matrix[i-1][j-1]+(tokens1[j] != tokens2[i]))
    return (matrix[-1][-1])


def comparing(From1, From2, scores_file):

    tokens= From_Programm_To_Tokens(From1)
    tokens2= From_Programm_To_Tokens(From2)

    result = Levenshtein(tokens, tokens2)
    result = (1-round(result/max(len(tokens), len(tokens2)), 3))*100
    # вывод программы в файл, если путь есть
    Draw_to_file(scores_file,result)


def main():
    ''' Увы не смог довести до конца
    parser = argparse.ArgumentParser(
        description="compare files and put ans into file scores.txt")
    parser.add_argument("file_With_Paths", type=str,
                        help="file with paths where the files are for comparison")
    parser.add_argument("file_To", type=str,
                        help="file where to put the answers")
    # args - обьект типа namespase имеет два параметра - file_With_Path и file_To
    args = parser.parse_args()
    '''
    print("Введите путь до файла с путями и путь до выходного файла")
    file_with_path,file_to = input().split()
    Paths = open(file_with_path, "r")
    scores = open(file_to, "w")
    scores.write("Im here\n")
    while True:
        # считываем строку
        line = Paths.readline()
        # прерываем цикл, если строка пустая
        if not line:
            break

        line.replace("/","\\")
        # разделяю строку на два пути
        arr = line.split()
        Path_From, Path_From2 = arr[0], arr[1]
        #print(Path_From,Path_From2)
        comparing(Path_From, Path_From2, scores)
    
    Paths.close()
    scores.close()

main()