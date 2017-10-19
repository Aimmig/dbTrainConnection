package dbapi;

import javax.swing.JButton;
import javax.swing.JFileChooser;

/**
 *
 * @author andre
 */
public class XMLFileChooser  extends JFileChooser{
    JButton open;
    
    
    public XMLFileChooser(){
        super();
        open=new JButton();
        this.setDialogTitle("Choose File for saving/loading");
        this.setFileFilter(new XMLFileFilter());
        if(this.showOpenDialog(open)==JFileChooser.APPROVE_OPTION){}
    }
    
    public String isFileXML(){
        if (new XMLFileFilter().accept(this.getSelectedFile())){
            return this.getSelectedFile().getAbsolutePath();
        }
        return "";
    }    
}    
