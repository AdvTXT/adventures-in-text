def moving(action):
    """If action contains directional information, return (direction, None). Otherwise, returns False."""

    short_dir = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    long_dir = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest']
    for d in long_dir:
        if d in action:
            return ("move", d)
    for d in short_dir:
        if d in action:
            long_d = long_dir[short_dir.index(d)]
            return ("move", long_d)
    return False

def check_noun(location, inventory, noun, *adj):
    """Checks a noun to make sure it exists, and tries to identify which noun is being referred to in the case of a conflict.
        If an adjective is passed in, will try to use that to identify the noun matches more than one object. 
        Returns either the correct noun or an error string."""
        
    contained_objects = [contained.name \
                        for obj in location.objects \
                            for base in obj.__class__.__bases__ if base.__name__ == 'Container' \
                                for contained in obj.objects if obj.is_open]
    room_and_inv_objs = [obj.name for obj in location.objects + inventory]
    all_named_objs = contained_objects + room_and_inv_objs
  
    # if there is only one match for the noun, return it
    if all_named_objs.count(noun) == 1:
        return noun
    try:
        # adj in obj.name is more relevant than adj in the description (e.g. brass_lamp > "The brass lamp is grungy.")
        adj_in_name = [obj for obj in all_named_objects if noun in obj.name and adj in obj.name]
        if len(adj_in_name) == 1:
            return adj_in_name[0]
        # but adj in description is second-best
        adj_in_desc = [obj for obj in all_named_objects if obj.name == noun and adj in str(obj)]
        if len(adj_in_desc) == 1:
            return adj_in_desc[0]
        # if the adjective does not narrow it down, return an error message
        return "That object does not exist."
    except NameError:
        # if adj has not been defined, don't have any other helpful information and must return an error message
        return "That object does not exist."







def parse(action, location, inventory):
    "Given an action, returns (verb, noun)"

    action = action.split()

    if len(action) == 1:
        # assume action is a room action (e.g. look, jump)
        move = moving(action)
        if move: 
            return move
        return (action[0], None)

    if len(action) == 2:
        # assume action is in the form <verb noun> (e.g. get chair)
        # or a movement (e.g. go north)
        if moving(action):
            return moving(action)

        verb, noun = action
        contained_objects = [contained.name \
                            for obj in location.objects \
                                for base in obj.__class__.__bases__ if base.__name__ == 'Container' \
                                    for contained in obj.objects if obj.is_open]
        room_and_inv_objs = [obj.name for obj in location.objects + inventory]
        all_named_objs = contained_objects + room_and_inv_objs

        # if more than one thing has the same name, ask user for more information
        if all_named_objs.count(noun) > 1:
            return "More than one object fits that name."
        # if the object cannot be found in either room.objects or inventory, return error
        elif all_named_objs.count(noun) < 1:
            return "That object does not exist."
        return (verb, noun)

    if len(action) == 3:
        # assume action is in the form <verb adjective noun> (e.g. get brass lamp, get my sword)
        # or in the form <verb preposition noun> (e.g. look in chest, turn on lamp)
        # or in the form <verb-preposition noun preposition> (e.g. turn on lamp)

        prepositions = ['of', 'on', 'in', 'to', 'for', 'with', 'from', 'around', 'under', 'over', 'out', 'off']

        # if adj in prepositions, probably in the form <verb preposition noun> or <verb-preposition noun>


        # if more than one thing has the same name, check the adjective against the description
        if all_named_objs.count(noun) > 1:
            return "More than one object fits that name."
        # if the object cannot be found in either room.objects or inventory, return error
        elif all_named_objs.count(noun) < 1:
            return "That object does not exist."
        return (verb, noun)







