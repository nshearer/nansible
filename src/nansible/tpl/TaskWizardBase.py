from abc import ABCMeta, abstractmethod, abstractproperty
import os
from textwrap import dedent
from glob import glob

from py_wizard.PyMainWizard import PyMainWizard

class WizardException(Exception): pass


# http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class TaskWizardBase(PyMainWizard):
    '''Wizard for generating tasks'''
    __metaclass__ = ABCMeta

    TASK_NAME = 'specify_task_name'
    TASK_DESC = 'Description for user on what this does'
    
    @property
    def task_name(self):
        return self.TASK_NAME
    
    
    def execute(self):
        '''Run the wizard'''
        tasks_file = self._select_tasks_file()
        tasks_indent = self._determine_task_file_indent(tasks_file)

        # Generate source
        parms = Bunch()
        self.ask_template_questions(parms)
        source = dedent(self.gen_ansible(parms)).strip()

        # -- Common Questions -------------------------------------------------

        # Get the ansible name (user friendly description) of the task
        description = self.ask_simple('description',
            "Description of task (printed when ansible runs)",
            optional=True)
        if description is not None:
            source = 'name: %s\n' % (description) + source
            
        # Run as sudo?
        if self.ask_yes_no('sudo', "Run this configuration as sudo?"):
            source = source.rstrip() + "\n" + "sudo: yes"
            
        # Notify service handler?
        notify = self.ask_simple("notify",
            "Run handler after this task?",
            optional=True)
        if notify:
            source = source.rstrip() + "\n" + "notify: " + notify
            
        # -- Append to tasks file ---------------------------------------------
        
        # Indent source to make it a list item
        new_source = list()
        for i, line in enumerate(dedent(source).split("\n")):
            if i == 0:
                new_source.append(tasks_indent + '- ' + line.rstrip())
            else:
                new_source.append(tasks_indent + '  ' + line.rstrip())
        source = "\n".join(new_source).rstrip()

        # Write to file
        print "Appending new task to", tasks_file
        with open(tasks_file, 'at') as fh:
            fh.write("\n" + source + "\n")
                
        
    @abstractmethod
    def ask_template_questions(self):
        '''Hook for task specific wizard to ask questions (without name)'''
        
    @abstractmethod
    def gen_ansible(self, parms):
        '''Generate task source for ansible'''
        
            
    def _determine_task_file_indent(self, path):
        '''Determine what's being used as the indent in the tasks file'''
        indent = None
        with open(path, 'rt') as fh:
            for i, line in enumerate(fh.readlines()[1:]):
                line = line.rstrip()
                if len(line) == 0:
                    pass
                elif line.strip().startswith("#"):
                    pass
                else:
                    line_indent = line[:-1*len(line.strip())]
                    if indent is None:
                        indent = line_indent
                    elif line_indent.startswith(indent):
                        pass
                    elif indent.startswith(line_indent):
                        indent = line_indent
                    else:
                        msg = "Odd indent on line %d of %s"
                        raise WizardException(msg % (i+2, path))
        if indent is None:
            return ' '*4
        return indent
        
        
            
    def _select_tasks_file(self):
        '''Determine which tasks file to update'''
        task_file_candidates = list(glob("*.yml"))
        
        # Have to have a file to update:
        if len(task_file_candidates) == 0:
            raise WizardException("No task files found")
        
        # Probably tasks.yml
        if 'tasks.yml' in task_file_candidates:
            use_tasks_yml = self.ask_yes_no('use_tasks_yml',
                "Update tasks.yml?", default=True)
            if use_tasks_yml:
                return 'tasks.yml'
            
        # Ask which to use
        return self.ask_select('tasks_file',
            "Which file do you want to append to",
            options=task_file_candidates,
            optional=False)
        
        
    def _select_source_file(self, in_dir, allow_dir=False):
        '''Select the source file to use out of the given directory'''
        
        candidates = os.listdir(in_dir)
        source_file = self.ask_select('source_in: %s' % (in_dir),
            "Select source file in %s" % (in_dir),
            options=candidates)
        source_path = os.path.join(in_dir, source_file)
        
        # If Directory:
        if os.path.isdir(source_path):
            if allow_dir:
                recurse = self.ask_yes_no('use dir: %s' % (in_dir),
                    "Recurse into %s?" % (source_path))
            else:
                recurse = True
            
            if recurse:
                sub_file = self._select_source_file(source_path)
                return os.path.join(source_file, sub_file)
            else:
                return source_file
        
        # If File:
        elif os.path.isfile(source_path):
            return source_file
        
        else:
            raise WizardException("Not a file or dir: " + source_path)
        
        
    def _select_target_path(self):
        '''Specify path to save file to'''
        return self.ask_simple('target',
            "Specify path on configure host:")
        
        
    def _ask_file_module_perms(self):
        '''Asks for permissions of file and format in form of file module parms'''
        parms = list()
        
        owner = self.ask_name('owner',
            "Name of owner of the file",
            optional=True)
        if owner is not None:
            parms.append('owner=' + owner)
            
        group = self.ask_name('group',
            "Name of group to own file",
            optional=True)
        if group is not None:
            parms.append('group=' + group)
            
        mode = self.ask_simple('mode',
            "File permissions (mode) of the new file",
            optional=True)
        if mode is not None:
            parms.append('mode=' + mode)
            
        return ' '.join(parms)            
            