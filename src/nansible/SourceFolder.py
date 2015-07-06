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
        self._mkdir(target_path)


    # -- Sub files/folders ----------------------------------------------------        

    def listdir(self):
        '''List all file and folders under this folder (as SourceFile)'''
        folders = list()
        files = list()
        
        for filename in sorted(os.listdir(self.path)):
            if filename not in ['.', '..']:
                path = os.path.join(self.path, filename)
                if os.path.isdir(path):
                    folders.append(filename)
                elif os.path.isfile(path):
                    files.append(filename)
                else:
                    print "WARNING: Unknown file object type: " + path
                
        for foldername in folders:
            path = os.path.join(self.path, foldername)
            source_tree_path = os.path.join(self.source_tree_path, foldername)
            ftype = self._get_folder_type(foldername)
            if ftype is not None:
                subclass = self.SUB_CLASSES[ftype]
                yield subclass(path, source_tree_path, parent=self)
        
        for filename in files:
            path = os.path.join(self.path, filename)
            source_tree_path = os.path.join(self.source_tree_path, filename)
            ftype = self._get_file_type(filename)
            if ftype is not None:
                subclass = self.SUB_CLASSES[ftype]
                yield subclass(path, source_tree_path, parent=self)


    def _get_folder_type(self, filename):
        if filename == 'roles':
            return 'RolesFolder'
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



