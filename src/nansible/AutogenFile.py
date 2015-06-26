import os
import sys
import tempfile
import subprocess
import stat
import shutil

from SourceFile import SourceFile

class AutogenFile(SourceFile):
    '''Runs a script to generate files to include in the ansible tree
    
    Autogen scripts will be executed in a temporary directory with the
    parameters:
      $1 - The full path to the source root
      $2 - The relative path of the directory the autogen scripts was found in
           (relative to source root, e.g.: roles/tasks/)
      
    curdir will be switched to the temp directory
    
    Any files written to the temp directory will be copied into the target
    '''
    def compile_to(self, target_root):
        
        # Make sure script is executable
        st = os.stat(self.path)
        os.chmod(self.path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP)
        
        # Create temporary folder
        run_dir = tempfile.mkdtemp()
        start_dir = os.path.abspath(os.curdir)
        os.chdir(run_dir)
        rtncode = 0
        
        try:
        
            # Run script
            self.log("---- Executing %s in %s ----" % (
                self.source_tree_path, run_dir))
            cmd = [
                self.path,
                self.root.path,
                os.path.dirname(self.source_tree_path),
                ]
            rtncode = subprocess.check_call(cmd,
                stdout=sys.stdout, stderr=sys.stderr)
            self.log("---- End of Script Output ------------------")
        
            # Copy files out of run dir
            if rtncode == 0:
                for dirpath, dirnames, filenames in os.walk('.'):
                    for dirname in dirnames:
                        path = os.path.join(dirpath, dirname)
                        target_path = os.path.join(target_root, path)
                        self._mkdir(target_path)
                    for filename in filenames:
                        path = os.path.join(dirpath, filename)
                        target_path = os.path.join(target_root, path)
                        self._copy_file_to(target_path, path)
        finally:
            # Clean up
            os.chdir(start_dir)
            shutil.rmtree(run_dir)
        
