from SourceFolder import SourceFolder

class RolesFolder(SourceFolder):
    '''roles/ folder containing normal ansible roles'''
    def _get_folder_type(self, filename):
        return 'RoleFolder'
