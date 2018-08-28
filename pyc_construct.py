from struct import pack
def p32(i):
    return pack("<i", i)

def string(d, fout):
    l = len(d)
    fout.write(b"s")
    if(type(d)==type("1")):
        if(d!="" and d[0]=="'"):
            d = d.strip("'")
            l -= 2
        d = d.encode()
    l = p32(l)
    fout.write(l)
    fout.write(d)

def tumple(d, fout):
    l = p32(len(d))
    fout.write(b"(")
    fout.write(l)
    for s in d:
        string(s, fout)

def tumple_line(i, l, fout):
    fout.write(b'(')

    fout.write(p32(l))
    while(data[i][:5]!="names"):
        # print(data[i])
        if(data[i]=="None"):
            fout.write(b"N")
        elif(data[i]=="code"):
            i = analyse("code", i+1, fout)-1
        elif(data[i][0]=='('):
            analyse("tumple", i, fout)
        elif(data[i][0]=="'"):
            string(data[i][1:-1], fout)
        else:
            fout.write(b"i")
            fout.write(p32(int(data[i])))
        i += 1
    return i

def calc_len(i):
    l = 0
    n = 1
    while(n):
        if(data[i].find("argcount")!=-1):
            n += 1
        if(n==1):
            l += 1
        # print(n, l, data[i])
        if(data[i][:6]=="lnotab"):
            n -= 1


        i += 1
    return l-8


def analyse(kind, i, fout):
    # print(data[i])
    global data
    if(kind=="code"):
        fout.write(b"c")
        argcount = int(data[i].split(' ')[1])
        i += 1
        fout.write(p32(argcount))
        nlocals = int(data[i].split(' ')[1])
        i += 1
        fout.write(p32(nlocals))
        stacksize = int(data[i].split(' ')[1])
        i += 1
        fout.write(p32(stacksize))
        flags = int(data[i].split(' ')[1], 16)
        i += 1
        fout.write(p32(flags))
        i = analyse("co_code", i, fout)
        i = analyse("consts", i, fout)
        i = analyse("names", i, fout)
        i = analyse("varnames", i, fout)
        i = analyse("freevars", i, fout)
        i = analyse("cellvars", i, fout)
        i = analyse("filename", i, fout)
        i = analyse("name", i, fout)
        i = analyse("firstlineno", i, fout)
        i = analyse("lnotab", i, fout)
    if(kind=="co_code"):
        if(len(data[i].split(' '))==1):
            s = ""
            while(data[i]!="consts"):
                i += 1
                s += data[i]
            s = s.replace("consts", "")
        else:
            s = data[i].split(" ")[1]
            i += 1
        try:
            s = bytes.fromhex(s)
        except:
            s = bytes.fromhex("0"+s)
        string(s, fout)
        i += 1
    if(kind=="consts"):
        l = calc_len(i)
        i = tumple_line(i, l, fout)
    if(kind in ["names", "varnames", "freevars", "cellvars", "tumple"]):
        if(data[i][0]!="("):
            data[i] = "".join(data[i].split(' ')[1:])

        d = data[i].replace("(", "").replace(")", "").replace(" ", "").split(",")
        if(d[-1]==""):
            d.pop(-1)
        tumple(d, fout)
        i += 1
    if(kind in ["filename", "name"]):
        d = data[i].split(" ")[1].replace("'", "")

        string(d, fout)
        i += 1
    if(kind=="firstlineno"):
        d = int(data[i].split(" ")[1])
        fout.write(p32(d))
        i += 1
    if(kind=="lnotab"):
        try:
            s = data[i].split(" ")[1]
        except:
            s = ""
        try:
            s = bytes.fromhex(s)
        except:
            s = bytes.fromhex("0"+s)
        string(s, fout)
        i += 1

    return i


if(__name__=="__main__"):
    fout = open("output.pyc", "wb")
    with open("opcode.txt","r", encoding='utf-8') as f:
        data = f.readlines()
        # utf-8格式的opcode使用下述语句解析，因为showfile重定向的结果出来是utf-8格式的orz
        # data = f.read().replace("\x00", "").split("\n\n")
    for i in range(len(data)):
        data[i] = data[i].strip()
    print(data)
    magic = bytes.fromhex(data[0].split(" ")[1])
    moddate = bytes.fromhex(data[1].split(" ")[1])
    fout.write(magic)
    fout.write(moddate)
    t = analyse("code", 3, fout)
    print("all lines:", t)
    fout.close()
