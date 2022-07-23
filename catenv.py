
#
# CatENV
#
# Defintions
#

#
# Configuration
#

enable_FAA = False
quiet_mode = False
output_to_message = False
cmem = {}

def deserialize(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def serialize(path, object):
    with open(path, 'wb') as f:
        pickle.dump(object, f)

def wsleep(text):
    for x in text:
        if x.isalpha():
            time.sleep(random.choice([0.3, 0.4, 0.5]))
        elif x.isdigit():
            time.sleep(random.choice([0.7, 0.2, 0.5]))
        else:
            time.sleep(random.choice([0.1, 0.9]))

def rep(text):
    try:
        if len(text) < 60:
            wsleep(text)
        vk.messages.send(peer_id=pid, message=text, random_id=randid())
    except Exception as e:
        l(f"Не удалось отправить сообщение: {e}")

def randid():
    return random.randint(-2147483647, 2147483647)

def percent(frst, scnd):
    coef = 100 / frst
    gets = scnd * coef
    return gets

def succ():
    if quiet_mode:
        pass
    else:
        print("[ \033[92mok\033[0m ]")

def failcomplete():
    if quiet_mode:
        pass
    else:
        print("[\033[31mfail\033[0m]")

def procmsg(text):
    if quiet_mode:
        pass
    else:
        rows, columns = os.popen('stty size', 'r').read().split()
        intm = int(columns) - 13 - len(text)
        txt = " " * intm
        print("\033[94m>>>\033[0m " + text + "..." + txt, end="")

def output(text): # Alternative to print()
    if quiet_mode:
        pass
    else:
        if not output_to_message:
            sys.stdout.write(str(text) + '\n')
        else:
            message(str(text))

def writeto(text, target, enable_FAA=enable_FAA):
    if enable_FAA:
        if target not in gv("files"):
            sv("files", gv("files") | {str(target): text})
    else:
        file = open(str(target), 'w', encoding='utf-8')
        file.write(str(text))
        file.close()

def getavatar(id):
    return vk.users.get(user_ids=id, fields="photo_400_orig")[0]["photo_400_orig"]

def readff(file, enable_FAA=enable_FAA): # Read From File
    if enable_FAA:
        if file not in gv("files"):
            Ff = open(file, 'r', encoding='UTF-8')
            Contents = Ff.read()
            Ff.close()
            sv("files", gv("files") | {file: Contents})
            return Contents
        else:
            return gv("files")[file]
    else:
        try:
            Ff = open(file, 'r', encoding='UTF-8')
            Contents = Ff.read()
            Ff.close()
            return Contents
        except:
            return None

def pluswrite(text, target, enable_FAA=enable_FAA):
    if enable_FAA:
        if target not in gv("files"):
            #file = open(str(target), 'a', encoding='utf-8')
            #file.write(str(text))
            #file.close()
            sv("files", gv("files") | {str(target): readff(target, enable_FAA=False) + str(text)})
        else:
            sv("files", gv("files") | {str(target): readff(target) + str(text)})
    else:
        file = open(str(target), 'a', encoding='utf-8')
        file.write(str(text))
        file.close()

def gv(var):
    global cmem
    try:
        return cmem[var]
    except:
        return "Error: variable not found"

def sv(var, val):
    global cmem
    #if {var: val} not in cmem:
    cmem[var] = val
    #else:
    #    pass


if enable_FAA:
    sv("files", {})

from threading import Thread
from time import sleep
def memcheck(g: dict[str, any]):
    global memgun_changes
    last: dict[str, any] = g
    while True:
        new: dict[str, any] = globals().copy()
        for k, v in new.items():
            if k != 'memgun_changes':
                if k not in list(last.keys()):
                    memgun_changes += f"new: {k} = {v}\n"
                elif last[k] != new[k]:
                    memgun_changes += f'change: {k} = {last[k]} -> {new[k]}\n'
        last = new
#thrm = Thread(target=memcheck, args=[globals().copy()])
#thrm.start()


def getfiles(path):
    buf = ""
    for x in os.listdir(path):
        buf += readff(path + x)
    return buf

def l(text):
    print(f"[{time.ctime()}] {text}")
    pluswrite(f"[{time.ctime()}] {text}", "log/mainlog.txt")
