import numpy as np
import re
import nltk
# i = input("Enter the Sentence you want to tag: ")
# file = input("File name: ")
# fil = open("sumba.txt.txt", 'r')
fil = open("test.txt", 'r')
# output = open('output.txt', 'a')
number = 0



# print(inp)
file1 = "./Assignment2/hmmmodel.txt"
f = open(file1, 'r')
tags = ['Begin']
transition = []
emmission = []
for line in f:
    # line = f.readline().rstrip()
    # print(line)
    
    line = line.rstrip().split()
    if len(line) == 0:
        continue
    # print(line)
    if line[0] == "Tags":
        tags = line[1:]
        # tags.pop(0)
        # print(tags)
    elif line[0] == "Transition":
        while(1):
            ad = []
            itr = f.readline()
            # print(itr)
            if itr == "\n":
                # print(transition)
                break
            itr = itr.rstrip()
            temp = itr. split()

            ad.append(temp[0])
            ad.append(temp[2])
            ad.append(temp[4])
            # print(ad)
            transition.append(ad)
    elif line[0] == "Emission":
        while(1):
            itr = f.readline()
            # print(itr)
            if itr == "\n":
                # print(emmission)
                break
            itr = itr.rstrip()
            
            temp = "".join(itr.split())
            
            itr = (re.split('[(=)|\n]', temp))
            itr.pop(-2)
            itr.pop(0)
            # print(itr)
            emmission.append(itr)
        
dictPOS = {itr[0] : {i : 0 for i in tags} for itr in transition} 
# print(dictPOS)
dictWords = {itr[0] : {i : 0 for i in tags} for itr in emmission}
normalTotal = {itr[0] : 0.0 for itr in emmission}
normalPOS = {itr[0] : 0.0 for itr in transition}
    
    # dictPOS = {}
for itr in transition:
    dictPOS[itr[0]][itr[1]] = itr[2]
    normalPOS[itr[0]] += float(itr[2])

for itr in emmission:
    dictWords[itr[0]][itr[1]] = itr[2]
    normalTotal[itr[0]] += float(itr[2])
for key in dictWords:
    for itr in dictWords[key]:
        # print(itr, key)
        dictWords[key][itr] = float(dictWords[key][itr]) / normalTotal[key]
for key in dictPOS:
    for itr in dictPOS[key]:
        dictPOS[key][itr] = float(dictPOS[key][itr]) / normalPOS[key]
for l1 in fil:
    inp = nltk.tokenize.word_tokenize(l1)
    pos = {i : " " for i in range(len(inp))}
    obs = {itr : {i : [] for i in range(len(inp))} for itr in tags}
    for i in range(len(inp)):
        # print(inp[i])
        for itr in tags:
            # print(inp[i], itr)
            maxi = 0.0

            if i == 0:
                obs[itr][i].append('Begin')
                if inp[i] in dictWords.keys():
                    obs[itr][i].append(float(dictWords[inp[i]][itr]) * float(dictPOS['Begin'][itr]))    
                elif inp[i].lower() in dictWords.keys():
                    obs[itr][i].append(float(dictWords[inp[i].lower()][itr]) * float(dictPOS['Begin'][itr]))           
                else:
                    obs[itr][i].append(float(dictPOS['Begin'][itr]))
                
            else:
                t = ""
                
                for x in tags:
                    if inp[i] in dictWords.keys():
                        # print('yes')
                        s = float(obs[x][i-1][1]) * float(dictWords[inp[i]][itr]) * float(dictPOS[x][itr])
                        if s == 0 and float(dictWords[inp[i]][itr]) != 0:
                            s = float(obs[x][i-1][1]) * float(dictWords[inp[i]][itr])
                        
                        
                    elif inp[i].lower() in dictWords.keys():
                        # print('yes low')
                        s = float(obs[x][i-1][1]) * float(dictWords[inp[i].lower()][itr]) * float(dictPOS[x][itr])
                        if s == 0 and float(dictWords[inp[i].lower()][itr]) != 0:
                            s = float(obs[x][i-1][1]) * float(dictWords[inp[i].lower()][itr])
                    else:
                        # print('yes')
                        s = float(obs[x][i-1][1]) * float(dictPOS[x][itr])
                    if(s > maxi):
                        maxi = s
                        t = x
                    # if maxi == 0:
                    #     if inp[i] in dictWords.keys() and float(dictWords[inp[i]][itr]) > 0 and float(obs[x][i-1][1]) > 0:
                    #         t = x
                    #         maxi = 
                    #     if inp[i].lower() in dictWords.keys() and float(dictWords[inp[i].lower()][itr]) > 0 and float(obs[x][i-1][1]) > 0:
                    #         t = x
                # print(maxi, t)
                # if t == "":
                #     print (inp[i])
                obs[itr][i].append(t)
                obs[itr][i].append(maxi)

    # for d in obs:
    #     print(d, obs[d])
    t = ""    
    maxi = 0 
    for i in range(len(inp)-1, -1, -1):  
        # print(inp[i], t)  
        if(i == len(inp)-1):
            for itr in tags:
                if obs[itr][i][1] > maxi:
                    obs[itr][i][1] = maxi
                    t = obs[itr][i][0]
                    pos[i] = itr
                
        else:
            pos[i] = t
            t = obs[t][i][0]
                
    for key in pos:
        print(pos[key], end = " ")
    print()
    # print(number, pos)
    number = number + 1
