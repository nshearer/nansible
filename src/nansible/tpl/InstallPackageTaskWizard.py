from TaskWizardBase import TaskWizardBase


class InstallPackageTaskWizard(TaskWizardBase):
    
    TASK_NAME = 'install'
    TASK_DESC = 'Install package'

    def ask_template_questions(self, parms):
        # Get template source file
        parms.installer = self.ask_select('installer',
            "Which installer module is to be used",
            options=['apt', 'yum'],
            default='apt')
        parms.name = self.ask_simple('pkg_name',
            "Name of the package")
        
        
    def gen_ansible(self, parms):
        '''Generate task source for ansible'''
        return "%s: name=%s state=present" % (parms.installer, parms.name)