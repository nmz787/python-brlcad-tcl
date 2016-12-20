"""
A simple class counts how many of a certain part-name has been requested, and returns the part-name with the counter appended.
"""


class BrlcadNameTracker(object):
    def __init__(self):
        self.num_parts_in_use_by_part_name = {}

    def get_next_name(self, requesting_object, part_name):
        part_classname = requesting_object.__class__.__name__
        part_name = '{}__{}'.format(part_classname, part_name)
        # get the next instance number for the requested part 
        # TODO: should there be a remove part method, which decrements the key's value?
        # you can remove objects from the brlcad geometry database...
        self.increment_counter_for_name(part_name)
        name_split = part_name.split('.')
        name_prefix = '.'.join(name_split[:-1]) if len(name_split)>1 else name_split[-1]
        name_suffix = '.'+name_split[-1] if len(name_split)>1 else ''
        
        return '{}{}{}'.format(name_prefix, self.num_parts_in_use_by_part_name[part_name], name_suffix)

    def increment_counter_for_name(self, part_name):
        try:
            self.num_parts_in_use_by_part_name[part_name]+=1
        except KeyError:
            # if the key wasn't yet requested, start counting now
            self.num_parts_in_use_by_part_name[part_name]=1
