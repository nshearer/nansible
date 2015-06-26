import os

from RoleFolder import RoleFolder

class ProjectRoleFolder(RoleFolder):
    '''A role folder in a project'''
    
    def _get_folder_type(self, filename):
        if filename == 'tasks':
            return 'ProjectRoleTasksFolder'
        return super(ProjectRoleFolder, self)._get_folder_type(filename)

    @property
    def project_name(self):
        return self.parent.name

    
    @property
    def corresponding_target_folder(self):
        '''Path in the target directory to create (relative to target root)'''
        return 'roles/%s__%s' % (self.project_name, self.name)
        
    
