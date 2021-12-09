# layer 0: Background0 Objects
# layer 1: Behind tileset Objects
# layer 2: Tileset Objects
# layer 3: Foreground Objects

OL_BACKGROUND = 0
OL_BACK_TILESET = 1
OL_TILESET = 2
OL_CHARACTER = 3
OL_FOREGROUND = 4

objects = [[], [], [], [], []]


def add_object(o, layer):
    global objects
    objects[layer].append(o)


def add_objects(l, layer):
    global objects
    objects[layer] += l


def remove_object(o):
    global objects
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def clear():
    global objects
    for o in all_objects():
        del o
    for l in objects:
        l.clear()


def destroy():
    global objects
    clear()
    objects.clear()


def all_objects():
    global objects
    for i in range(len(objects)):
        # print("objects index: %d" % i)
        # try:
        for o in objects[i]:
            yield o
        # except:
        #     print("objects index: %d" % i)
