from SourceFile import SourceFile

class IgnoredFile(SourceFile):
    '''A file that is not copied to the compiled folder'''
    
    def compile_to(self, target_root):
        '''Copy/compile this object into the compiled ansible target'''
        self.log("Ignoring file: " + self.source_tree_path)
        
    
    