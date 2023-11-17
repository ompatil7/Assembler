import nltk
nltk.download("punkt")
asm = open("asm.txt").readlines()
#print(asm)

tokens = []

for line in asm:
    lineToken = nltk.word_tokenize(line)

    for i in range(len(lineToken)):
        lineToken[i] = lineToken[i].upper()
        
    lineToken.append("\n")
    tokens.extend(lineToken)

print(tokens)

#mot,pot,dl,reg
mot = ["MOVER","MOVEM","ADD","SUB","MULT","DIV","BC","COMP","PRINT","READ"]#IS
pot = ["START","END","EQU","ORIGIN","LTORG"]#AD
dl = ["DS","DC"]#DL
reg = ["R1","R2","R3","R4","R5"]


def is_integer(num):
    try:
        num = int(num)
        return True
    
    except ValueError:
        return False

#Symbol table
symTab = []
symadr = []

#literal table
litTab = []
litAdr = []

baseAdr = int(tokens[1])
curAdr = baseAdr - 1

previous = tokens[0]
for token in tokens:
    if token == "DS" or token =="DC" or token == ":":
        symTab.append(previous)

    previous = token

intfile = open("intermediate.txt","w")
comand = ""
litCount = 0
curLitInd = 0 
previous = tokens[0]
for token in tokens:
    if is_integer(token):
        comand = comand + "(C," + token + ")"

    if "ORIGIN" in previous:
        curAdr = int(token)
        comand = str(curAdr) + ")"
        
    if token in symTab:
        index = symTab.index(token) + 1
        comand = comand + "(S," + str(index) + ") "

    if token != "LTORG" and token in pot:
        index = pot.index(token) + 1
        comand = comand + "(AD," + str(index) + ") "

    if "=" in token:
        temp = ""
        for i in token:
            temp += i
            if(i == "="):
                temp = ""
        litCount += 1
        litTab.append(temp)

        index = litTab.index(temp) + 1
        comand = comand + "(L," + str(index) + ") "

    if "DS" in token or "DC" in token or ":" in token:
        symadr.append(curAdr)
    
    if token == "LTORG":
        comand = ""
        for i in range(litCount):
            comand = str(curAdr) + ")" + "(AD,5) _ " + litTab[curLitInd]
            litAdr.append(curAdr)
            print(comand)
            comand = comand + "\n"
            intfile.write(comand)
            curAdr += 1
            curLitInd += 1
            comand = ""

        litCount = 0
        curAdr = curAdr - 1
    
        # comand += str(curAdr) + ")" 

    if token in mot:
        index = mot.index(token) + 1
        comand = comand + "(IS," + str(index) + ") "

    if token in reg:
        comand = comand + token + " "

    if token in dl:
        index = dl.index(token) + 1
        comand = comand + "(DL," + str(index) + ") "

    if "\n" in token:
        if comand == "":
            None
        else:
            print(comand)
            comand = comand + "\n"
            intfile.write(comand)
        curAdr += 1
        comand = str(curAdr) + ")"
        
    previous = token
	
intfile.write("end of code\n")
print(litTab)
print(litAdr)
print(symTab)
print(symadr)


for i in litTab:
    intfile.write(i + " ")
intfile.write("\n")

for i in litAdr:
    intfile.write(str(i) + " ")
intfile.write("\n")

for i in symTab:
    intfile.write(i + " ")
intfile.write("\n")

for i in symadr:
    intfile.write(str(i) + " ")
intfile.write("\n")