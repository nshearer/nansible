'''Templates'''

from TemplateTaskWizard import TemplateTaskWizard
from CopyTaskWizard import CopyTaskWizard
from MkdirTaskWizard import MkdirTaskWizard

ALL_TEMPLATES = {
    TemplateTaskWizard.TASK_NAME: TemplateTaskWizard,
    CopyTaskWizard.TASK_NAME: CopyTaskWizard,
    MkdirTaskWizard.TASK_NAME: MkdirTaskWizard,
    }