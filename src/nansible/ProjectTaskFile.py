from SourceFile import SourceFile
    
class ProjectTaskFile(SourceFile):
    '''One of the special task files for projects
    
    disabled.yml - Run when project is disabled
    enabled.yml - Run when project is enabled
    disabled_or_enabled.yml - Run when project is either enabled or disabled
    purfed.yml - Run when project is in purged status
    '''
    
    ENABLED = 'enabled'
    DISABLED = 'disabled'
    PURGED = 'purged'
    
    FILENAMES= {
        'disabled.yml':             (DISABLED, ),
        'enabled.yml':              (ENABLED, ),
        'disabled_or_enabled.yml':  (ENABLED, DISABLED),
        'purged.yml':               (PURGED),
        }
