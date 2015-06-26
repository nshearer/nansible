import os

from SourceFile import SourceFile

class HandlersShortcutFile(SourceFile):
    '''handlers.yml -> handlers/main.yml'''
    def compile_to(self, target_root):
        role_path = self.parent.corresponding_target_folder
        handlers_dir_path = os.path.join(target_root, role_path, 'handlers')
        self._mkdir(handlers_dir_path)
        path = os.path.join(handlers_dir_path, 'main.yml')
        self._copy_file_to(path)
