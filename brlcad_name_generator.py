"""
A simple class counts how many of a certain part-name has been requested, and returns the part-name with the counter appended.
"""

class brlcad_name_generator(object):
    def __init__(self):
        self.num_parts_in_use_by_part_name = {}

    def get_next_name(self, part_name):
        try:
            self.num_parts_in_use_by_part_name[part_name]+=1
        except KeyError:
            self.num_parts_in_use_by_part_name[part_name]=1
        name_split = part_name.split('.')
        name_prefix = '.'.join(name_split[:-1])
        name_suffix = '.'+name_split[-1] if len(name_split)>1 else ''

        return '{}{}{}'.format(name_prefix, self.num_parts_in_use_by_part_name[part_name], name_suffix)
