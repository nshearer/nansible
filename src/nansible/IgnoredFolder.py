from SourceFile import SourceFile

class IgnoredFolder(SourceFile):
    '''A folder that is not copied to the compiled folder (or recursed)'''
    
    def compile_to(self, target_root):
        '''Copy/compile this object into the compiled ansible target'''
        self.log("Ignoring folder: " + self.source_tree_path)
        
    
    def listdir(self):
        '''List all file and folders under this folder (as SourceFile)'''
        if False:
            yield None
            
    