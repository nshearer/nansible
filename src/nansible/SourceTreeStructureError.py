

class SourceTreeStructureError(Exception):
    '''Describe an error with the source file tree'''
    def __init__(self, fileobj, msg):
        emsg = "Error with Source tree"
        emsg += "\n  In file " + str(fileobj)
        emsg += "\n  " + msg
        super(SourceTreeStructureError, self).__init__(msg)