from SourceFolder import SourceFolder
from ProjectTaskFile import ProjectTaskFile
    
class ProjectRoleTasksFolder(SourceFolder):
    '''tasks/ in a role folder in a project'''
    
    def _get_file_type(self, filename):
        if filename in ProjectTaskFile.FILENAMES.keys():
            return 'ProjectTaskFile'
        return super(ProjectRoleTasksFolder, self)._get_file_type(filename)
