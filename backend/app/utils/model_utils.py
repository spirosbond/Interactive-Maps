"""
Function that takes as input a Pymongo Schema or a list of Schemas and transforms the ObjectID object to String.
This is needed to be able to return the schema in a router without having to define complex serialization methods.
Returns:
    The same object as received but with its ObjectID transformed to a String
"""


def objectid_to_str(model):
    if isinstance(model, list):
        for m in model:
            m["_id"] = str(m["_id"])
    else:
        model["_id"] = str(model["_id"])
    return model
