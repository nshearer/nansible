import os
from SourceFile import SourceFile

class MetaShortcutFile(SourceFile):
    '''meta.yml -> meta/main.yml'''
    def compile_to(self, target_root):
        role_path = self.parent.corresponding_target_folder
        meta_dir_path = os.path.join(target_root, role_path, 'meta')
        self._mkdir(meta_dir_path)
        path = os.path.join(meta_dir_path, 'main.yml')
        self._copy_file_to(path)