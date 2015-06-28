'''Support classes for the nan command'''

from nansible.SourceFile import SourceFile
from nansible.SourceFolder import SourceFolder
from nansible.RolesFolder import RolesFolder
from nansible.RoleFolder import RoleFolder
from nansible.ProjectsFolder import ProjectsFolder
from nansible.ProjectFolder import ProjectFolder
from nansible.ProjectDescriptionFile import ProjectDescriptionFile
from nansible.ProjectRoleFolder import ProjectRoleFolder
from nansible.ProjectRoleTasksFolder import ProjectRoleTasksFolder
from nansible.ProjectTaskFile import ProjectTaskFile
from nansible.TasksShortcutFile import TasksShortcutFile
from nansible.HandlersShortcutFile import HandlersShortcutFile
from nansible.VarsShortcutFile import VarsShortcutFile
from nansible.MetaShortcutFile import MetaShortcutFile
from nansible.AutogenFile import AutogenFile
from nansible.IgnoredFile import IgnoredFile
from nansible.IgnoredFolder import IgnoredFolder

# Setup sub-classes for SourceFile
SourceFile.SUB_CLASSES = {
    'SourceFile':               SourceFile,
    'SourceFolder':             SourceFolder,
    'RolesFolder':              RolesFolder,
    'RoleFolder':               RoleFolder,
    'ProjectsFolder':           ProjectsFolder,
    'ProjectFolder':            ProjectFolder,
    'ProjectDescriptionFile':   ProjectDescriptionFile,
    'ProjectRoleFolder':        ProjectRoleFolder,
    'ProjectRoleTasksFolder':   ProjectRoleTasksFolder,
    'ProjectTaskFile':          ProjectTaskFile,
    'TasksShortcutFile':        TasksShortcutFile,
    'HandlersShortcutFile':     HandlersShortcutFile,
    'VarsShortcutFile':         VarsShortcutFile,
    'MetaShortcutFile':         MetaShortcutFile,
    'AutogenFile':              AutogenFile,
    'IgnoredFile':              IgnoredFile,
    'IgnoredFolder':            IgnoredFolder,
    }

    