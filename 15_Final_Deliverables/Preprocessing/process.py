with open('eng_dataset.txt') as f:
    lines = f.readlines()


def remove_line(l):
    l = [i for i in l if i != '\n' ]
    return l

text = remove_line(lines)
# hindi = []
# english = []
hin_dic ={}
eng_dic={}
for i in  range(1,19):
    hin_dic[str(i)] = []
    eng_dic[str(i)] = []

for i in range(0,len(text),2):
    if '–' in text[i]:
        temp1 = text[i].split()[2]
        temp2 = text[i].split()[4]
        chapter = temp1.split('.')[0]
        verse = temp1.split('.')[1]
        # vers2 = temp2.split('.')[1]
        data = text[i+1][:-2]
        # print(data)
        # print(temp2)
        # print(text[i].split())
        eng_dic[chapter].append(data)
        # eng_dic[verse] = data
        # english.append(eng_dic)

    else:
        temp = text[i].split()[2]
        chapter = temp.split('.')[0]
        verse = temp.split('.')[1]
        data = text[i+1][:-2]
        # print(temp)
        eng_dic[chapter].append(data)


    # dic[i]
with open('hin_dataset.txt') as f:
    lines = f.readlines()


def remove_line(l):
    l = [i for i in l if i != '\n' ]
    return l

text = remove_line(lines)

for i in range(0,len(text),2):
    if '–' in text[i]:
        temp1 = text[i].split()[2]
        temp2 = text[i].split()[4]
        chapter = temp1.split('.')[0]
        verse = temp1.split('.')[1]
        # vers2 = temp2.split('.')[1]
        data = text[i+1].split('n')[0][:-1]
        # print(temp2)
        # print(text[i].split())
        hin_dic[chapter].append(data)

    else:
        temp = text[i].split()[2]
        chapter = temp.split('.')[0]
        verse = temp.split('.')[1]
        data = text[i+1].split('.')[0][:-1]
        # print(temp)
        hin_dic[chapter].append(data)

    # print(hin_dic[i])
# final_hindi = []
# for i in hindi:
#     # print(i)
#     temp = []
#     for key in i.keys():
#         temp.append(i[key])
#     final_hindi.append(temp)
# print(len(final_hindi))
# # for i in final_hindi:
# #     print(len(i))

# import json
 
# # Data to be written

# print(eng_dic["18"])
# file1 = open("hindi.txt","a")

# # file1.writelines(L)
# # file1.close()
# for i in hin_dic.keys():
#     file1.writelines(hin_dic[i])
#     file1.write(r'\n')

# file2 = open("english.txt","a")

# # file1.writelines(L)
# # file1.close()
e =[]
for i in eng_dic.keys():
    e.append(eng_dic[i])

h =[]
for i in hin_dic.keys():
    h.append(hin_dic[i])

# for i in e :
#     print(len(i))
# print(len(e))
# with open('hindi.txt', 'w') as f:
#     for i in range(len(h)):
#         for j in range(len(h[i])):
#             f.write(h[i][j] + "\n")
#         f.write('\n')

# with open('english.txt', 'w') as f:
#     for i in range(len(e)):
#         for j in range(len(e[i])):
#             f.write(e[i][j] + "\n")
#         f.write('\n')


from googletrans import Translator

def get_translation(data, dest):
    translator = Translator()
    text = translator.translate(data, dest).text
    return text
# g = []
# for i in range(18):
#     temp = []
#     for j in range(len(h[i])):
#         dd = get_translation(h[i][j],"gu")
#         temp.append(dd)
#     g.append(temp)

# with open('gujarati.txt', 'w') as f:
#     for i in range(len(g)):
#         for j in range(len(g[i])):
#             f.write(g[i][j] + "\n")
#         f.write('\n')


# m = []
# for i in range(18):
#     temp = []
#     for j in range(len(h[i])):
#         dd = get_translation(h[i][j],"mr")
#         temp.append(dd)
#     m.append(temp)

# with open('marathi.txt', 'w') as f:
#     for i in range(len(m)):
#         for j in range(len(m[i])):
#             f.write(m[i][j] + "\n")
#         f.write('\n')

# b = []
# for i in range(18):
#     temp = []
#     for j in range(len(h[i])):
#         dd = get_translation(h[i][j],"bn")
#         temp.append(dd)
#     b.append(temp)

# with open('bengali.txt', 'w') as f:
#     for i in range(len(b)):
#         for j in range(len(b[i])):
#             f.write(b[i][j] + "\n")
#         f.write('\n')

# t = []
# for i in range(18):
#     temp = []
#     for j in range(len(h[i])):
#         dd = get_translation(h[i][j],"ta")
#         temp.append(dd)
#     t.append(temp)

# with open('tamil.txt', 'w') as f:
#     for i in range(len(t)):
#         for j in range(len(t[i])):
#             f.write(t[i][j] + "\n")
#         f.write('\n')

p = []
for i in range(18):
    temp = []
    for j in range(len(h[i])):
        dd = get_translation(h[i][j],"pa")
        temp.append(dd)
    p.append(temp)

with open('punjabi.txt', 'w') as f:
    for i in range(len(p)):
        for j in range(len(p[i])):
            f.write(p[i][j] + "\n")
        f.write('\n')

# with open('english.txt', 'w') as f:
#     for i in range(len(e)):
#         f.write('\n')
#         for j in range(len(e[i])):
#             f.write(e[i][j])
    # file1.write('\\n')


# for i in eng_dic.keys:
 
# # Serializing json
# json_object = json.dumps(hin_dic, indent=4)
 
# # Writing to sample.json
# with open("hindi.json", "w") as outfile:
#     outfile.write(json_object)

# # Serializing json
# json_object = json.dumps(eng_dic, indent=4)
 
# # Writing to sample.json
# with open("english.json", "w") as outfile:
#     outfile.write(json_object)