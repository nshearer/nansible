import os

from SourceFile import SourceFile

class VarsShortcutFile(SourceFile):
    '''vars.yml -> vars/main.yml'''
    def compile_to(self, target_root):
        role_path = self.parent.corresponding_target_folder
        vars_dir_path = os.path.join(target_root, role_path, 'vars')
        self._mkdir(vars_dir_path)
        path = os.path.join(vars_dir_path, 'main.yml')
        self._copy_file_to(path)
