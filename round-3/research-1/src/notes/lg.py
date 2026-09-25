"""Local regex grep over fetched texts: python3 notes/lg.py <file> <pattern> [max] [ctx]"""
import re,sys
f,pat=sys.argv[1],sys.argv[2]
n=int(sys.argv[3]) if len(sys.argv)>3 else 12
c=int(sys.argv[4]) if len(sys.argv)>4 else 250
t=re.sub(r'\s+',' ',open(f,errors='ignore').read())
for i,m in enumerate(re.finditer(pat,t,re.I)):
    if i>=n:break
    print('...',t[max(0,m.start()-c):m.end()+c],'\n')
