MAIN_TEMPLATE="""\
---
 
"""


def write_main_file(path):
    '''Create the main playbook that will be called'''
    global MAIN_TEMPLATE
    
    with open(path, 'wt') as fh:
        fh.write(MAIN_TEMPLATE)