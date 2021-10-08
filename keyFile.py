import os
from os.path import exists as file_exists

def keyUpdate(locs: list): #funciton for saving data to json
    

    print('Type \'exit\' to exit.\n') #Enter keys and url
    j = 0
    values = []
    while 'exit' not in values and j < len(locs):
        values.append(input(locs[j] + ': '))
        j += 1
    
    if 'exit' in values:
        return

    with open('.env', 'w+') as file:
        for i in range(len(locs)):
            file.write(locs[i] + '==' + values[i] + '\n')
    return

def loadKeys():
    if fileCheck(): #if file exists load existing data
        with open('.env', 'r') as f:
            for line in f.readlines():
                try:
                    key, value = line.split('==')
                    os.environ[key] =  value[:-1]
                except ValueError:
                    print('FILE ERROR\n*************\nPlease run setupt \'-s\' or \'--setup\'')
                    return
    return

def fileCheck() -> bool:
    if file_exists('.env'):
        return True
    else:
         print('KEY4 ERROR\n*************\nPlease run setupt \'-s\' or \'--setup\'')
         return False
    