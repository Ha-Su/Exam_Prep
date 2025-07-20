MODULE_MAP = {
    "Human Computer Interaction": "HCI",
    "Serious Games": "SG",
}

def get_module(module: str) -> str | None:
    # If it's a key, return the mapped value
    if module in MODULE_MAP:
        return MODULE_MAP[module]
    # Otherwise see if it's one of the values, and return its key
    for key, val in MODULE_MAP.items():
        if val == module:
            return key
    return None
ret = get_module("Human Computer Interaction")
print(ret)