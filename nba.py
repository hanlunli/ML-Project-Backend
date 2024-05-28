import csv

def csv_to_dict(csv_file):
    result = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            key = row.pop('Rk')
            processed_row = {}
            for k, v in row.items():
                try:
                    processed_row[k] = float(v)
                except ValueError:
                    processed_row[k] = v
            result[key] = processed_row
    return result

csv_file = 'nba.csv'
data = csv_to_dict(csv_file)

def sortfunc():
    tempdict = []
    tempdict.append([data["1"]["Player"],data["1"]['PTS']])
    for i in range(2,len(data)):
        current = [data[f"{i+1}"]["Player"],data[f"{i+1}"]["PTS"]]
        spot = binary_spot_search(current, tempdict)
        tempdict.insert(spot, current)
    end(tempdict)

def binary_spot_search(value, dict):
    found = False
    unchange = dict
    while not found:
        length = len(dict)
        pos = length//2
        middle = dict[pos]
        if value[1] == middle[1]:
            found = True
            return unchange.index(middle)
        elif value[1] > dict[-1][1]:
            temp = dict[-1]
            temp1 = unchange.index(temp)
            found = True
            return temp1+1
        elif value[1] < dict[0][1]:
            found = True
            return 0
        elif middle[1] < value[1]:
            if len(dict) == 1:
                found = True
                return unchange.index(dict[0])
            dict = dict[pos:]
        elif value[1] < middle[1]:
            if len(dict) == 1:
                found = True
                return unchange.index(dict[0])+1
            dict = dict[:pos]

def listflip(list1):
    list2 = []
    for i in range(len(list1)):
        list2.append(list1[-1*(i+1)])
    return list2

def end(dict):
    dict1 = listflip(dict)
    for i in range(len(dict1)):
        print(f"{dict1[i][0]}: {dict1[i][1]}")

sortfunc()
