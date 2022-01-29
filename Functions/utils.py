"""
Utils python file to hold necessary utility functions.
"""
import itertools

def chunked_iterable(iterable, size):
    """
    This function iterates through a list and returns the list in chunks.
    The chunks are expected to be in in equal size. Otherwise, the function will error
    """
    the_iterable = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(the_iterable, size))
        if not chunk:
            break
        yield chunk
