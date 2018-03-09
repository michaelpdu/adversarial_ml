import sys
import os
import uuid
import subprocess
import math
appname = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tlsh'))
from collections import Counter, OrderedDict

javascript = ['abstract','arguments','boolean','break','byte','case','catch','char','class','const','continue','debugger','default','delete','do','double','else','enum','eval','export','extends','false','final','finally','float','for','function','goto','if','implements','import','in','instanceof','int','interface','let','long','native','new','null','package','private','protected','public','return','short','static','super','switch','synchronized','this','throw','throws','transient','true','try','typeof','var','void','volatile','while','with','yield']
javascriptcode =  {word:i for i,word in enumerate(javascript)}

def handle1file(_data):
    result_vector = [0]*256
    for c in _data:
        id = ord(c)
        result_vector[id] = result_vector[id] + 1
    return result_vector

def hashbybase(x,base1):
    x = str(x).strip()
    if x=='': return -1
    import hashlib
    v = hashlib.md5(str(x)).hexdigest()
    rv = int(v[:(1 + (base1 / 256)) * 2], 16) % base1
    return rv

def tokenize(data):
    tokens = []
    vcount = Counter()
    token = []
    for i,e in enumerate(data):
        o1 = ord(e.upper())       
        if (o1>=65 and o1<=90) or (o1>=48 and o1<=57):
            token.append(e)
        else:
            if len(token)>2:
                ts = "".join(token)
                if len(ts)>10: 
                    ts = ts[:8]+str(len(ts))
                vcount.update([ts])            
            token = []

    selected = []
    unknown = []
    selected_code  = ['0']*64
    unknown_code = [0]*256
    for item in vcount.items():
        if item[0].lower() in javascript:            
            selected.append(item[0])
            code = javascriptcode[item[0].lower()]
            selected_code[code] = str(item[1])
        else:
            unknown.append(item[0])    
            code = hashbybase(item[0],256)
            unknown_code[code] = unknown_code[code]+1            

#    print selected
#    print unknown
    
    known64 = ",".join(selected_code)
    unknownhash256 = ",".join( [str(x) for x in unknown_code])
    unknownhist256 = ",".join([str(x) for x in (handle1file("".join(unknown)))])
    
    return ",".join([known64,unknownhash256,unknownhist256])

def disasemble(data):
    struct1 = ''
    value1 = ''
    quoteset = {'"':'"',"'":"'","/":"/"}
    cur = None
    i = 0
    lasti = 0
    while i<len(data):
        if data[i] in quoteset:
            respond = quoteset[data[i]]
            struct1 = struct1+data[lasti:i].strip()
            j = i+1            
            while j<len(data) and respond!=data[j]:
                j = j+1
            if j>=len(data):
                j = len(data)
#                print "possible parse fail without", respond                
            value1 = value1+data[(i+1):j]
            i = j+1
            lasti = i
        else:                
            i = i+1
    return struct1,value1                            

class extractor:

        def getStoreType(self):
                return 'file'

        def getTimeCostTitle(self):
                return "no function here"

        def getTitle(self):
                return "nline,contentsha1,file_entropy,first_line_entropy,filesize"

        def extract(self, file_path):
            data = open(file_path,'r').read()                       
            return self.extractbuf(data)
        def extractbuf(self,data):
            s,v = disasemble(data)
#            print "s",s
#            print "v",v
            vhist256 = handle1file(v)
            vhist256str = ",".join([str(x) for x in vhist256] )
            r = tokenize(s)
#            print r
            return vhist256str+","+tokenize(s)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python extractor.py <samplepath>')
        sys.exit(1)
  
    ex = extractor()
    store_type = ex.getStoreType()
    print(ex.extract(sys.argv[1]))


