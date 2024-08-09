from random import choice, randint
import yaml

prefix = '$'

#     <<<< rarer <<<<
#prob = [256, 128, 64, 32, 16, 8, 4, 2]
#an = ["Rainbow", "Rock", "Firefly", "Lucky", "Unusual", "Rare", "Uncommon", "Common"]


#optype 1 - write || optype 0 - read
def data_manager(uid: str, name: str, optype: bool, modif: str):
    with open(f"users/{uid}.yml", "r") as file:
        data: dict = yaml.safe_load(file)
    if modif:
        mod: str = str(modif.removeprefix("-" or "+"))
        prfx: str = str(modif[0])

    if optype and name != ("effects" or "auras"):
        if prfx == "-":
            data[name] = data[name] - int(mod)
        else:
            data[name] = data[name] + int(mod)

    elif name == "auras":
        if prfx == "-":
            try:
                data["auras"].remove(str(mod))
            except KeyError:
                return f"There are no {mod}s in <@{uid}>'s inventory"
        else:
            data["auras"].add(str(mod))

#effects - (prefix)(effect)(duration)
#           +luck010

    elif name == "effects":
        effect: str = str(mod[:-3])
        duration: int = int(mod[-3:])
        if prfx == "+":
            if data["effects"].get(effect):
                data["effects"].update({effect: int(data["effects"].get(effect)) + duration})
            else:
                data["effects"].update({effect: duration})
        else:
            data["effects"].pop(effect)

    elif not optype:
        return data.get(name)

    with open(f"users/{uid}.yml", "w") as file:
        yaml.dump(data, file, default_flow_style=False)


def roll(uid: str) -> str:
    data_manager(uid, name="rolls", optype=True, modif="+1")
    return data_manager(uid, name="rolls", optype=False, modif="")


def get_response(user_input: str, uid: str) -> str:
    msg: str = user_input.lower()

    if msg == prefix + 'ping':
        return f"pong"

    elif 'im not gay' in msg:
        return ':billed_cap:'

    elif msg == prefix + "femboy":
        rand = randint(1, 100)
        return f"You are {rand}% femboy!"

    elif msg == prefix + "racist":
        if uid == ("434677190408405005" or "1191909315393630208" or "588273713095639040"):
            print(f'(fake roll {uid})')
            return "You are 100% racist!"
        else:
            print('(real roll)')
            rand = randint(1, 100)
            return f"You are {rand}% racist!"

    elif msg == prefix + "roll":
        return roll(uid)

#indev
    elif (prefix + "data") in msg:
        print("debugging")
