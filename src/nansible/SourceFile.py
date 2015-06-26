import os
import shutil
import gflags

from SourceTreeStructureError import SourceTreeStructureError

class SourceFile(object):
    '''A file in the source tree'''

    SUB_CLASSES=None

    def __init__(self, path, source_tree_path, parent):
        '''Init 

        @param path: Path to file on disk
        @param source_tree_path: Path relative to source tree root (./)
        @param parent: Parent object
        '''
        self.__path = path
        self.__source_tree_path = source_tree_path
        self.__parent = None

        if parent is not None:
            self.__parent = parent

    @property
    def path(self):
        '''Path to file object on disk'''
        return self.__path
    
    
    @property
    def name(self):
        '''Name of the file'''
        return os.path.basename(self.path)
    

    @property
    def source_tree_path(self):
        '''Path to file object relative to source tree root'''
        path = self.__source_tree_path
        if len(path) > 2 and path.startswith("./"):
            path = path[2:]
        return path
    
    def __str__(self):
        return self.__source_tree_path
    
    def __repr__(self):
        return "%s('%s', '%s')" % (self.__class__.__name__,
                                   self.__path, self.__source_tree_path)

    @property
    def parent(self):
        return self.__parent
    
    @property
    def all_parents(self):
        '''Yield all parents, starting from most immediate, up to root'''
        next_parent = self.parent
        while next_parent is not None:
            yield next_parent
            next_parent = next_parent.parent
    
    
    @property
    def root(self):
        '''Root object of source tree (RootSourceFolder)'''
        if self.parent is None:
            return self
        else:
            return self.parent.root

    @property
    def isdir(self):
        return False
    
    @property
    def isfile(self):
        return True

    def compile_to(self, target_root):
        '''Copy/compile this object into the compiled ansible target'''
        if self.parent.corresponding_target_folder is not None:
            target_path = os.path.join(
                target_root,
                self.parent.corresponding_target_folder,
                os.path.basename(self.source_tree_path))
            self._copy_file_to(target_path)
        
        
    def _copy_file_to(self, path, source_path=None):
        '''Copy this file to the compiled directory
        
        @param path: Full path to copy the file to
        @param source_path: Path to copy from (assumed to be this file if None)
        '''
        if source_path is None:
            source_path = self.path
        if os.path.exists(path):
            msg = "Conflict: Target file already exists: " + path
            raise SourceTreeStructureError(self, msg)
        self.log("%s -> %s" % (source_path, path))
        shutil.copy2(source_path, path)
    
    
    def _mkdir(self, path):
        # Auto create 1 parent
        parent = os.path.dirname(path)
        if not os.path.exists(parent):
            os.mkdir(parent)
        # Create dir (ignore existing)
        if not os.path.exists(path):
            os.mkdir(path)
    
    
    def log(self, msg):
        if gflags.FLAGS.verbose:
            print "  " + msg


