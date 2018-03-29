f0=open('export.txt','r',encoding='utf-8')
f=open('WebMercator.txt','r',encoding='utf-8')
F=open('BusStation.txt','r',encoding='utf-8')
F0=open('linestation.txt','w',encoding='utf-8')
stations=f0.readlines()
station=len(stations)
h=[]
a=0
for data in range(station):
    h.append(stations[data][0:12])
    #print(h)
number=[]
datastation=[]
w=f.readlines()
k=len(w)
for d in range(k):
    if w[d][0:12] in h:
        number.append(d)
        datastation.append(w[d][0:12])
        #print(w[d][0:14])
F_data=F.readlines()
F_station=[]
n=len(number)
print(number)
for t in range(n):
    F0.write(F_data[number[t]])
    F_station.append(F_data[number[t]])


