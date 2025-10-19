import java.awt.*;
import java.awt.event.*;
class  CheckboxGroupDemo extends Frame 
{
    Label l1,l2;
    Panel p1;
     CheckboxGroupDemo() 
    {
        setTitle("Checkbox Example");
        setSize(500, 500);
        setLayout(new GridLayout(3,1));
        
        l1=new Label();
        l1.setAlignment(Label.CENTER);
        
        l2=new Label();
        l2.setAlignment(Label.CENTER);
        l2.setSize(350,100);
        
        p1=new Panel();
        p1.setLayout(new FlowLayout());
        add(l1);
        add(l2);
        add(p1);
        setVisible(true);
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });
    }
    void showCheckboxes()
    {
        l1.setText("Check Game:");
        CheckboxGroup Grp=new CheckboxGroup();
        Checkbox chk_cricket=new Checkbox("Cricket",Grp,true);
        Checkbox chk_football=new Checkbox("Football",Grp,false);
        Checkbox chk_hockey=new Checkbox("Hockey",Grp,false);
        p1.add(chk_cricket);
        p1.add(chk_football);
        p1.add(chk_hockey);
        chk_cricket.addItemListener(new ItemListener() {
            public void itemStateChanged(ItemEvent e) {
                if(e.getStateChange()==1)
                {
                    l2.setText("Cricket Checkbox is Checked by User");
                }
                else
                {
                    l2.setText("Cricket Checkbox is Unchecked by User");
                }
            }
        });
        
        chk_football.addItemListener(new ItemListener() {
            public void itemStateChanged(ItemEvent e) {
                if(e.getStateChange()==1)
                {
                    l2.setText("Football Checkbox is Checked by User");
                }
                else
                {
                    l2.setText("Football Checkbox is Unchecked by User");
                }
            }
        });
        
        chk_hockey.addItemListener(new ItemListener() {
            public void itemStateChanged(ItemEvent e) {
                if(e.getStateChange()==1)
                {
                    l2.setText("Hockey Checkbox is Checked by User");
                }
                else
                {
                    l2.setText("Hockey Checkbox is Unchecked by User");
                }
            }
        });
    }
    public static void main(String[] args) {
        CheckboxGroupDemo obj=new  CheckboxGroupDemo(); 
        obj.showCheckboxes();
    }
}
