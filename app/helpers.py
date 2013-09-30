def filter_factory(filter_terms, member_to_check):
    """creates a filter using list of terms
    if empty list or list containing none passed
    the filter returns true on every call"""
    nones_in_filter_terms = len([el for el in filter_terms if el is None])
    if nones_in_filter_terms == len(filter_terms):
        return lambda x: True
    def my_filter(obj):
        if member_to_check not in obj.__dict__:
            raise Exception('Object does not contain attribute we are filtering on')
        else:
            return obj.__dict__[member_to_check] in filter_terms
    return my_filter
