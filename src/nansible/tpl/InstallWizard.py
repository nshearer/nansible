import os
import stat
import re
from pwd import getpwuid
from grp import getgrgid
from textwrap import dedent
import shutil

from TaskWizardBase import TaskWizardBase, WizardException
from TaskWizardBase import append_to_task

class FileRecord(object):
    def __init__(self, path):
        self.path = path
        self.owner = None
        self.group = None
        self.mode = None
    def __eq__(self, fl):
        if fl.path == self.path:
            if str(fl.owner) == str(self.owner):
                if str(fl.group) == str(self.group):
                    if str(fl.mode) == str(self.mode):
                        return True
        return False
    def __ne__(self, fl):
        return not self == fl
        
        
def find_files(search_path):
    for dirpath, dirnames, filenames in os.walk(search_path):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            try:
                fl = FileRecord(path)
                st = os.stat(fl.path)
                fl.owner = getpwuid(st.st_uid).pw_name
                fl.group = getgrgid(st.st_gid).gr_name
                fl.mode = oct(stat.S_IMODE(st.st_mode))
                if fl.__class__ is tuple:
                    pass
                yield fl
            except OSError, e:
                print "Ignoring %s: %s" % (path, str(e))


def remove_prefix(subject, prefix):
    if subject.startswith(prefix):
        return subject[len(prefix):]
    raise Exception("'%s' doesn't start with '%s'" % (subject, prefix))


class InstallWizard(TaskWizardBase):
    
    TASK_NAME = 'install'
    TASK_DESC = 'Multi-task wizard for installing a new service'

    def _calc_autosave_path(self):
        return '/tmp/nan.answers'

    def execute(self):
        role_name = self.ask_name('role_name',
            "Name of a role to create for this service")
        
        # Sanity checks
        if 'roles' not in os.listdir('.'):
            raise WizardException("Run in a directory with a roles directory")
        if role_name in os.listdir('roles/'):
            raise WizardException("Role %s already exists" % (role_name))
        
        # List packages to be installed
        pkgs = self.ask_list('pkgs',
            "List packages to be installed")
        
        # Scan for files
        print "Scanning for existing files"
        existing_files = {fl.path: fl for fl in find_files('/etc')}
        existing_file_paths = set([fl.path for fl in existing_files.values()])
        
        # Install packages
        msg = "Packages are ready to be installed.  "
        msg += "Install them manually:"
        for pkg in pkgs:
            msg += "\n $ sudo apt-get install %s" % (pkg)
        self.ask_action('install', msg)
        
        # Scan for new files
        print "Scanning for new files"
        after_files = {fl.path: fl for fl in find_files('/etc')}
        after_file_paths = set([fl.path for fl in after_files.values()])
        
        new_file_paths = after_file_paths - existing_file_paths
        
        # Create directories needed
        os.makedirs('roles/%s/files' % (role_name))
        os.makedirs('roles/%s/templates' % (role_name))
        
        # Create file stubs
        tasks_path = 'roles/%s/tasks.yml' % (role_name)
        with open(tasks_path, 'wt') as fh:
            print >>fh, "---"
            print >>fh, " "*4 + "#" + tasks_path
        
        handlers_path = 'roles/%s/handlers.yml' % (role_name)
        with open(handlers_path, 'wt') as fh:
            print >>fh, "---"
            print >>fh, " "*4 + "#" + handlers_path

        installer = self.ask_simple("installer",
            "Name of the ansible installer module",
            default='apt')
        
        sudo = self.ask_yes_no('sudo',
            "Use sudo?")

        # Add tasks to install packages
        for pkg in pkgs:
            src = '%s: name=%s state=present' % (installer, pkg)
            if sudo:
                append_to_task(src, 'sudo: yes')
            self._append_task_to_file(tasks_path, src)
            
        # Determine services
        services = list()
        pat = re.compile('^\/etc\/init\.d\/([^\/]+)$')
        for path in new_file_paths:
            m = pat.match(path)
            if m:
                service = m.group(1)
                if self.ask_yes_no('is_service:' + service,
                                   "Is %s a new service?"):
                    services.append(service)

        # Create handlers to restart services
        for service in services:
            src = "name: restart %s" % (service)
            src += "\nservice: name=%s state=restarted" % (service)
            if sudo:
                src += "\nsudo: yes"
            self._append_task_to_file(handlers_path, src)
        default_service = None
        if len(services) > 0:
            default_service = self.ask_select('default_service',
                "Select the default service to restart",
                options = services)
            
        # Find configuration files
        for path in new_file_paths:
            if '/init.d/' not in path and not path.startswith('/etc/rc'):
                self.inform_user("New config file: " + path)
                
                # Do we want to keep this file?
                keep = self.ask_yes_no('keep:'+path,
                    "Copy %s to ansible for deployment?" % (path))
                if keep:
                    file_type = self.ask_select('type:'+path,
                        "What type of file should %s be?" % (path),
                        options=['template', 'file'])
                    
                    # Determine where to save file
                    saved_path = None
                    while saved_path is None or not saved_path.startswith('roles/'):
                        saved_filename = os.path.basename(path)
                        if file_type == 'template':
                            saved_filename = saved_filename + '.j2'
                        saved_path = os.path.join('roles',
                                                  role_name,
                                                  file_type + 's',
                                                  saved_filename)
                        saved_path = self.ask_simple('save:'+path,
                            "Where should %s be saved?" % (path),
                            default=saved_path)
                        saved_filename = os.path.basename(saved_path)
                    
                    shutil.copy(path, saved_path)
                    
                    # Write task to deploy file
                    print "Existing file permissions for %s:" % (path)
                    print "owner: ", after_files[path].owner
                    print "group: ", after_files[path].group
                    print "mode:  ", after_files[path].mode
                    
                    if file_type == 'template':
                        src = dedent("""\
                            template: src={src_path} dest={target} {perms}
                            """).format(
                                src_path=remove_prefix(saved_path,
                                    prefix='roles/%s/templates/' % (role_name)),
                                target=path,
                                perms=self._ask_file_module_perms())
                    elif file_type == 'file':
                        src = dedent("""\
                            template: src={src_path} dest={target} {perms}
                            """).format(
                                src_path=remove_prefix(saved_path,
                                    prefix='roles/%s/files/' % (role_name)),
                                target=path,
                                perms=self._ask_file_module_perms())
                    if default_service is not None:
                        src = append_to_task(src, 'notify: restart %s' % (default_service))
                    if sudo:
                        src = append_to_task(src, 'sudo: yes')
                    self._append_task_to_file(tasks_path, src)
                    
        # Start services
        for service in services:
            enabled = self.ask_yes_no('enabled:'+service,
                "Start %s on boot?" % (service),
                default=True)
            start = self.ask_yes_no('start:'+service,
                "Start %s on deploy?" % (service),
                default=True)
            if start or enabled:
                src = 'service: name=%s' % (service)
                if start:
                    src += ' state=started'
                if enabled:
                    src += ' enabled=yes'
                if sudo:
                    src = append_to_task(src, 'sudo: yes')
                self._append_task_to_file(tasks_path, src)
                    

    def ask_template_questions(self, parms):
        pass
        
    def gen_ansible(self, parms):
        '''Generate task source for ansible'''
        pass