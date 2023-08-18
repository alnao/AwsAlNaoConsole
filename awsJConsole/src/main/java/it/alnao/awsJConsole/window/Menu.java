package it.alnao.awsJConsole.window;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;
import java.lang.reflect.Method;
import java.util.Set;

import javax.swing.ButtonGroup;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.JSeparator;

import it.alnao.awsJConsole.App;
import it.alnao.awsJConsole.sdk.Profiles;

/**
 * 
 * @author Alberto.Nao 
 * @see https://www.alnao.it/aws/ & https://www.alnao.it/javaee/
 * 
 * see menu https://docs.oracle.com/javase/tutorial/uiswing/components/menu.html
 */
public class Menu {
    public static JMenuBar createMenuBar(Set<String> profilesList, App app) {
    	
    	JMenuBar menuBar;
    	JMenu menu, menuF, menuH;
    	JRadioButtonMenuItem rbMenuItem;
    	menuBar = new JMenuBar();
    	
    	//FILE menu
    	menuF = new JMenu("File");
    	menuBar.add(menuF);
    	JMenuItem miFileNone = new JMenuItem("None");
    	JSeparator sep1 = new JSeparator();
    	JMenuItem miFileExit = new JMenuItem("Exit");
    	miFileExit.addActionListener(new ActionListener() {
    		  @Override
    		  public void actionPerformed(ActionEvent e) {
    			  System.exit(0);
    		  }
    		});
    	menuF.add(miFileNone);
    	menuF.add(sep1);
    	menuF.add(miFileExit);
    	
    	//PROFILES menu
    	menu = new JMenu("Profiles");
    	menuBar.add(menu);
    	//menu.addSeparator();
    	ButtonGroup group = new ButtonGroup();
    	for (final String prof : profilesList) {
        	rbMenuItem = new JRadioButtonMenuItem(prof);
        	if (Profiles.DEFAULT_PROFILE.equals(prof))
        		rbMenuItem.setSelected(true);
        	rbMenuItem.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent arg0) {
                	try {
						app.updateStatusPanel(prof);
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					}
              	}
            });
        	group.add(rbMenuItem);
        	menu.add(rbMenuItem);
    	}
    	
    	//ABOUT menu
    	menuH = new JMenu("Help");
    	menuBar.add(menuH);
    	JMenuItem miFileA = new JMenuItem("About");
    	miFileA.addActionListener(new ActionListener() {
    		  @Override
    		  public void actionPerformed(ActionEvent e) {
    			    JOptionPane.showMessageDialog(
    			    	app.getFrame(), "Aws J Console -- see www.alnao.it");
    		  }
    		});
    	menuH.add(miFileA);
    	
    	return menuBar;
    }
}
