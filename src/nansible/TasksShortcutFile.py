import os

from SourceFile import SourceFile    
    
class TasksShortcutFile(SourceFile):
    '''tasks.yml -> tasks/main.yml'''
    def compile_to(self, target_root):
        role_path = self.parent.corresponding_target_folder
        tasks_dir_path = os.path.join(target_root, role_path, 'tasks')
        self._mkdir(tasks_dir_path)
        path = os.path.join(tasks_dir_path, 'main.yml')
        self._copy_file_to(path)
