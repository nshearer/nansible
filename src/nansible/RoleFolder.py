from SourceFolder import SourceFolder

class RoleFolder(SourceFolder):
    '''A role under the normal roles/ folder (not a project)'''
    def _get_file_type(self, filename):
        if filename == 'tasks.yml':
            return 'TasksShortcutFile'
        
        if filename == 'handlers.yml':
            return 'HandlersShortcutFile'
        
        if filename == 'vars.yml':
            return 'VarsShortcutFile'
        
        if filename == 'meta.yml':
            return 'MetaShortcutFile'
        
        return SourceFolder._get_file_type(self, filename)
