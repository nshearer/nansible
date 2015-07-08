'''Templates'''

from TemplateTaskWizard import TemplateTaskWizard
from CopyTaskWizard import CopyTaskWizard
from MkdirTaskWizard import MkdirTaskWizard
from InstallPackageTaskWizard import InstallPackageTaskWizard

ALL_TEMPLATES = {
    TemplateTaskWizard.TASK_NAME: TemplateTaskWizard,
    CopyTaskWizard.TASK_NAME: CopyTaskWizard,
    MkdirTaskWizard.TASK_NAME: MkdirTaskWizard,
    InstallPackageTaskWizard.TASK_NAME: InstallPackageTaskWizard,
    }