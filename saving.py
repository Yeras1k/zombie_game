import os, json, pygame

def load_existing_save(savefile):
    with open(os.path.join(savefile), 'r+') as file:
        saves = json.load(file)
    return saves

def write_save(data):
    with open(os.path.join(os.getcwd(),'save.json'), 'w') as file:
        json.dump(data, file)

def load_save():
    try:
        save = load_existing_save('save.json')
    except:
        save = create_save()
        write_save(save)
    return save

def create_save():
    new_save = {
    "HEALTH": 150,
    "COIN_COUNT": 0,
    "RELOAD": 3000
    }

    return new_save