from bson.objectid import ObjectId


def objectid_to_str(model):
    """
    Function that takes as input a MongoDB Schema or a list of Schemas and transforms the ObjectID object to String.
    This is needed to be able to return the schema in a router without having to define complex serialization methods.
    Returns:
        The same object as received but with its ObjectID transformed to a String"""
    # Check if provided model is a list
    try:
        # Check if the provided model is a list
        if isinstance(model, list):
            for m in model:
                try:
                    # Ensure the schema has an "_id" key and it is an ObjectId
                    if "_id" in m and isinstance(m["_id"], ObjectId):
                        m["_id"] = str(m["_id"])
                except Exception as e:
                    print(f"Error processing an element in the list: {e}")
        # Or a single schema
        elif isinstance(model, dict):
            try:
                if "_id" in model and isinstance(model["_id"], ObjectId):
                    model["_id"] = str(model["_id"])
            except Exception as e:
                print(f"Error processing the model dictionary: {e}")
        else:
            raise TypeError("Input must be a dictionary or a list of dictionaries.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return model
