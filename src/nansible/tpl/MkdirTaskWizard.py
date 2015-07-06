from TaskWizardBase import TaskWizardBase


class MkdirTaskWizard(TaskWizardBase):
    
    TASK_NAME = 'mkdir'
    TASK_DESC = 'Create a directory on the remote host'

    def ask_template_questions(self, parms):
        # Get template source file
        parms.target = self._select_target_path()
        parms.perms = self._ask_file_module_perms()
        
        
    def gen_ansible(self, parms):
        '''Generate task source for ansible'''
        return """\
            file: path={target} state=directory {perms}
            """.format(
                target=parms.target,
                perms=parms.perms)