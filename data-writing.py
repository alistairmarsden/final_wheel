f = open(r'data\wheeldata.txt', "w")
for value in range (50, 950, 50):
    f.write(f"{value}\n")
f.write("loseturn\nbankrupt")
f.close()

a = open(r'dictionary_start.txt', 'r')
b = open(r'data\dictionary.txt','w')
dictionary = [x.strip() for x in a.readlines()]
for word in dictionary:
    b.write(f'{word}\n')
a.close()
b.close()