
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
    objects[layer].append(o)


def add_objects(l, layer):
    objects[layer] += l


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def clear():
    for o in all_objects():
        del o
    for l in objects:
        l.clear()



def destroy():
    clear()
    objects.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o
