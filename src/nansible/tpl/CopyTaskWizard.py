from TaskWizardBase import TaskWizardBase


class CopyTaskWizard(TaskWizardBase):
    
    TASK_NAME = 'copy'
    TASK_DESC = 'Copy a file from ansible source to target host'

    def ask_template_questions(self, parms):
        # Get template source file
        parms.source = self._select_source_file('files', allow_dir=True)
        parms.target = self._select_target_path()
        parms.perms = self._ask_file_module_perms()
        
        
    def gen_ansible(self, parms):
        '''Generate task source for ansible'''
        return """\
            copy: src={src_path} dest={target} {perms}
            """.format(
                src_path=parms.source,
                target=parms.target,
                perms=parms.perms)