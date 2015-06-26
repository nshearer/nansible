import os
import gflags

from SourceFolder import SourceFolder

class RootSourceFolder(SourceFolder):
    '''The root of the source tree'''
    
    
    def __init__(self, path):
        super(RootSourceFolder, self).__init__(
            parent = None,
            path = os.path.abspath(path),
            source_tree_path = '.')

    
    def _get_file_type(self, filename):
        if filename == gflags.FLAGS.main:
            return 'MainFile'
        return super(RootSourceFolder, self)._get_file_type(filename)


    def _get_folder_type(self, filename):
        if filename == 'roles':
            return 'RolesFolder'
        if filename == 'projects':
            return 'ProjectsFolder'
        else:
            return SourceFolder._get_folder_type(self, filename)


    def compile_to(self, target_root):
        '''Copy/compile this object into the compiled ansible target'''
        pass


    @property
    def corresponding_target_folder(self):
        '''Path in the target directory to create'''
        return None
    