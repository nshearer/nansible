from TaskWizardBase import TaskWizardBase


class TemplateTaskWizard(TaskWizardBase):
    
    TASK_NAME = 'template'
    TASK_DESC = 'Generate a file from a Jinja2 template file'

    def ask_template_questions(self, parms):
        # Get template source file
        parms.source = self._select_source_file('templates')
        parms.target = self._select_target_path() # /etc/firewall/base-rules.iptables
        parms.perms = self._ask_file_module_perms()
        
        
    def gen_ansible(self, parms):
        '''Generate task source for ansible'''
        return """\
            template: src={src_path} dest={target} {perms}
            """.format(
                src_path=parms.source,
                target=parms.target,
                perms=parms.perms)