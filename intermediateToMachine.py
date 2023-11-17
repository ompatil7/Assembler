import nltk

intr = open("intermediate.txt").readlines() #line by line list

code = []

curindex = 0
while intr[curindex] != "end of code\n":
    code.append(intr[curindex])
    curindex += 1

curindex += 1
litTab = nltk.word_tokenize(intr[curindex])
print(litTab)

curindex += 1
litAdr = nltk.word_tokenize(intr[curindex])
print(litAdr)

curindex += 1
symTab = nltk.word_tokenize(intr[curindex])
print(symTab)

curindex += 1
symAdr = nltk.word_tokenize(intr[curindex])
print(symAdr)

def is_integer(s):
    try:
        s = int(s)
        return True
    except ValueError:
        return False

reg = ["R1","R2","R3","R4","R5"]
tokens = []
for line in code:
    linetoken = nltk.word_tokenize(line)
    linetoken.append("\n")
    tokens.extend(linetoken)

print(tokens)

macFile = open("machine.txt","w")
previous = tokens[0]
comand = ""
tokenindex = 0

while tokenindex < len(tokens):
    if comand == "" and is_integer(tokens[tokenindex]):
        comand += tokens[tokenindex] + ") " 

    if "_" in tokens[tokenindex]:
        comand += "_ "

    if previous == "_" and is_integer(tokens[tokenindex]):
        comand += tokens[tokenindex] + " "
    
    if "AD" in tokens[tokenindex] or "IS" in tokens[tokenindex] or "C" in tokens[tokenindex]:
        temp = ""
        for i in tokens[tokenindex]:
            temp += i
            if i == ",":
                temp = ""
        
        temp += " "
        comand += temp

    if tokens[tokenindex] in reg:
        index = reg.index(tokens[tokenindex]) + 1
        comand += str(index) + " "

    if "L" in tokens[tokenindex] and "DL" not in tokens[tokenindex]: 
        temp = ""
        for i in tokens[tokenindex]:
            temp += i
            if i == ",":
                temp = ""
        
        index = int(temp) - 1
        comand += litAdr[index] + " "

    if "DL" in tokens[tokenindex]:
        tempToken = nltk.word_tokenize(comand)
        comand = tempToken[0] + ") _ _ _"
        while "\n" not in tokens[tokenindex]:
            tokenindex += 1

    if "S" in tokens[tokenindex] and "IS" not in tokens[tokenindex]: 
        temp = ""
        for i in tokens[tokenindex]:
            temp += i
            if i == ",":
                temp = ""
        
        index = int(temp) - 1
        comand += symAdr[index] + " "

    if "\n" in tokens[tokenindex]:
        print(comand)
        comand += "\n"
        macFile.write(comand)
        comand = ""

    previous = tokens[tokenindex]
    tokenindex += 1