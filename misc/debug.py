from talon.engine import engine

VERBOSE = False

def listener(topic, m):
    if topic == "cmd" and m["cmd"]["cmd"] == "g.load" and m["success"] == True:
        print("[grammar reloaded]")
    else:
        if VERBOSE:
            print(topic, m)
        elif topic == 'phrase' and 'words' in m and m['cmd'] != 'p.hypothesis':
            try:
                print(topic, m['phrase'], m['parsed'])
            except:
                print()
                print(topic, m)
                raise


engine.register("", listener)
