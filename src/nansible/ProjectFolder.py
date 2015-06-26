from SourceFolder import SourceFolder

class ProjectFolder(SourceFolder):
    '''Folder for a specific project (/projects/[name])'''

    def _get_folder_type(self, filename):
        return 'ProjectRoleFolder'
    
    def _get_file_type(self, filename):
        if filename == 'project.yml':
            return 'ProjectDescriptionFile'
        return 'IgnoredFile'


    # Don't create a folder in compiled for this
    def compile_to(self, target_root):
        pass
    @property
    def corresponding_target_folder(self):
        '''Path in the target directory to create (relative to target root)'''
        return None
