import os

from SourceFile import SourceFile

class SourceFolder(SourceFile):
    '''A folder in the source tree'''

    @property
    def isdir(self):
        return True
    
    @property
    def isfile(self):
        return False

    @property
    def corresponding_target_folder(self):
        '''Path in the target directory to create (relative to target root)'''
        
        # See if we can find a parent to get it's corresponding_target_folder
        parent_folder = None
        for parent in self.all_parents:
            if parent.corresponding_target_folder is not None:
                if parent_folder is None:
                    parent_folder = parent.corresponding_target_folder
        
        # Append our folder name to our parents corresponding_target_folder
        if parent_folder is not None:
            return os.path.join(parent_folder, os.path.basename(self.path))
        else:
            return os.path.basename(self.path)
        

    def compile_to(self, target_root):
        '''Copy/compile this object into the compiled ansible target'''
        folder = self.corresponding_target_folder
        target_path = os.path.join(target_root, folder)
        self.log("mkdir %s/" % (target_path))
        os.mkdir(target_path)


    # -- Sub files/folders ----------------------------------------------------        

    def listdir(self):
        '''List all file and folders under this folder (as SourceFile)'''
        for filename in os.listdir(self.path):
            if filename not in ['.', '..']:
                path = os.path.join(self.path, filename)
                source_tree_path = os.path.join(self.source_tree_path, filename)
                
                ftype = None
                if os.path.isdir(path):
                    ftype = self._get_folder_type(filename)
                elif os.path.isfile(path):
                    ftype = self._get_file_type(filename)
                else:
                    print "WARNING: Skipping odd file object: " + path
                    
                if ftype is not None:
                    subclass = self.SUB_CLASSES[ftype]
                    yield subclass(path, source_tree_path, parent=self)


    def _get_folder_type(self, filename):
        return 'SourceFolder'
    
    
    def _get_file_type(self, filename):
        if '.autogen.' in filename:
            return 'AutogenFile'
        return 'SourceFile'


    def walk(self):
        '''Return this object and all objects under it recursively'''
        yield self
        for child in self.listdir():
            if child.isfile:
                yield child
            elif child.isdir:
                for grandchild in child.walk():
                    yield grandchild



