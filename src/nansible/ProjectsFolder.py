from SourceFolder import SourceFolder

class ProjectsFolder(SourceFolder):
    '''Projects Directory (/projects)'''
    
    def _get_file_type(self, filename):
        if filename == 'project.yml':
            return 'ProjectDescriptionFile'
        return 'IgnoredFile'

    def _get_folder_type(self, filename):
        return 'ProjectFolder'


    def compile_to(self, target_root):
        pass # TODO
    
    @property
    def corresponding_target_folder(self):
        '''Path in the target directory to create (relative to target root)'''
        #return None # Projects doesn't really have a counterpart in target
        return 'projects'
    
