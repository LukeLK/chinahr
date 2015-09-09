__author__ = 'bitfeng'


import os

lines = []
for line in open('/Users/bitfeng/Downloads/chinahr-2.csv', 'r'):
    lines.append(line)

indu = [v.strip().strip(',') for v in lines[1:12]]
#print indu

t = {i.split(',')[0]: [i.split(',')[1], i.split(',')[2]] for i in indu}
t['1003'] = ['1014', '1022']
#print t

re = {}

for k in t.keys():
    re[k] = []
    for i in range(int(t[k][1])-int(t[k][0])+1):
        re[k].append(str(int(t[k][0])+i))

#print re

industry = []

for k in re.keys():
    for v in re[k]:
        industry.append(k+'_'+v)
#print industry
#print len(industry)



pro = [v.strip().strip(',') for v in lines[16:74]]

pro[6] = '1001,1007,1087,1110'


t = {i.split(',')[0]+'_'+i.split(',')[1]: [i.split(',')[2], i.split(',')[3]] for i in pro}
#t['1003'] = ['1014', '1022']
#print t

re = {}

for k in t.keys():
    re[k] = []
    for i in range(int(t[k][1])-int(t[k][0])+1):
        re[k].append(str(int(t[k][0])+i))

#print re

profession = []

for k in re.keys():
    for v in re[k]:
        profession.append(k+'_'+v)
#print profession
#print len(profession)



loc = [v.strip().strip(',') for v in lines[78:]]

print loc


t = {i.split(',')[0]: [i.split(',')[1], i.split(',')[2]] for i in loc}
#t['1003'] = ['1014', '1022']
#print t

re = {}

for k in t.keys():
    re[k] = []
    for i in range(int(t[k][1])-int(t[k][0])+1):
        re[k].append(str(int(t[k][0])+i))

#print re

location = []

for k in re.keys():
    for v in re[k]:
        location.append(k+'_'+v)

location.append('34')
location.append('35')
location.append('36')
location.append('37')

#print location
#print len(location)

print len(industry)*len(profession)

start_url = open('/Users/bitfeng/spiders/chinahr/chinahr_start_urls.txt', 'wb')
print type(industry)
start_url.write(','.join(industry)+'\n')
start_url.write(','.join(profession)+'\n')
start_url.write(','.join(location)+'\n')
start_url.close()


test = 'http://www.chinahr.com/so/0/0-0-0-0-0-0-0-1001_1001_1001-1001_1001-0-0-0-0-0-18_193-0/p0'
print test.split('/')[-2]

head = 'http://www.chinahr.com/so/0/0-0-0-0-0-0-0'
body = '0-0-0-0-0'
tail = '0/p0'

urlsFile = open('/Users/bitfeng/spiders/chinahr/chinahr_start.txt', 'wb')

urls = []

for pro in profession:
    for loc in location:
            urls.append('-'.join([head, pro, body, '0', loc, tail]))

urls.sort()

for line in urls:
    urlsFile.write(line+'\n')
urlsFile.close()

print urls[0:5]
print len(urls)

