package dbapi;

import java.io.File;
import javax.swing.filechooser.FileFilter;

/**
 *
 * @author Andre Immig
 * aimmig@students.uni-mainz.de
 */

//class for filtering files of filechooser
public class XMLFileFilter extends FileFilter{
    private final String FileFormat="XML";
    private final char dot='.';
    
    //defines which files to accept in file chooser
    @Override
    public boolean accept(File f){
        if(f.isDirectory()){
            return true;
        }
        return (extension(f).equalsIgnoreCase(FileFormat));
    }    
    
    //Description shown in FileChooser
    @Override
    public String getDescription() {
        return  "Xml format only";
    }
    
    public String extension(File f){
        String FileName=f.getName();
        int indexFile=FileName.lastIndexOf(dot);
        if(indexFile>0 && indexFile<FileName.length()-1){
            return FileName.substring(indexFile+1);
        }
        return "";
    }
    
}
