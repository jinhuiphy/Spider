import json
f0=open('line.json','r',encoding='utf-8')
F0=open('linestation.txt','r',encoding='utf-8')
F=open('data.json','w',encoding='utf-8')
station=[]
for line in F0.readlines():
    station.append(line.replace('\n',''))
h=f0.readlines()
j=len(h)
for b0 in range(j):
    s={}
    b=0
    jsondata=json.loads(h[b0])
    k0=0
    for k in jsondata:
        if k0==0:
            s[k] = jsondata[k]
        else:
            print(k)
            if jsondata[k] in station:
                s['station'+str(b)]=jsondata[k]
                b+=1
        k0+=1
    json.dump(s,F, ensure_ascii=False)
    F.write('\n')


