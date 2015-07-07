'''Templates'''

from TemplateTaskWizard import TemplateTaskWizard
from CopyTaskWizard import CopyTaskWizard
from MkdirTaskWizard import MkdirTaskWizard
from InstallWizard import InstallWizard

ALL_TEMPLATES = {
    TemplateTaskWizard.TASK_NAME: TemplateTaskWizard,
    CopyTaskWizard.TASK_NAME: CopyTaskWizard,
    MkdirTaskWizard.TASK_NAME: MkdirTaskWizard,
    InstallWizard.TASK_NAME: InstallWizard,
    }