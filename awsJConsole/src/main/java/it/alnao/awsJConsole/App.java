package it.alnao.awsJConsole;


import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;
//import java.util.ArrayList;
import java.util.Set;

//import javax.swing.BorderFactory;
//import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JRadioButtonMenuItem;
//import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

import it.alnao.awsJConsole.sdk.Profiles;
//import software.amazon.awssdk.auth.credentials.AwsCredentialsProvider;
//import software.amazon.awssdk.profiles.Profile;


/**
 * 
 * @author Alberto.Nao 
 * @see https://www.alnao.it/aws/ & https://www.alnao.it/javaee/
 * 
 */
public class App {
    
    
    public static void main(String[] args) {
    	//logger.info("Application 03_ProfilesMenu start");
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
            	//Regions region = Regions.EU_WEST_1;
            	Set<String> profilesList;
				try {
					profilesList = Profiles.loadProfilesFromFile();
					new App(profilesList);
				} catch (FileNotFoundException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
                
            }
        });
    }  
    //app component
    private JFrame frame ;
    private JLabel statusLabel;
    private JPanel statusPanel;
    private JPanel contentPane;
    public App(Set<String> profilesList ) {
    	//see menu https://docs.oracle.com/javase/tutorial/uiswing/components/menu.html
    	JMenuBar menuBar;
    	JMenu menu, submenu;
    	JMenuItem menuItem;
    	JRadioButtonMenuItem rbMenuItem;
    	JCheckBoxMenuItem cbMenuItem;
    	menuBar = new JMenuBar();
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
                	//logger.info("load profile " + prof);
                	updateStatusPanel(prof);
                	
              	}
            });
        	group.add(rbMenuItem);
        	menu.add(rbMenuItem);
    	}
    	
    	contentPane = new JPanel();
        contentPane.setLayout(new BorderLayout());
        contentPane.setPreferredSize(new Dimension(320 * 4,700));
        contentPane.add(new JLabel("Content"), BorderLayout.CENTER);
        
        frame = new JFrame("AlNao JConsole");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.setLayout(new BorderLayout());
        frame.setLocationByPlatform(true);
        frame.setSize(200,200);
        frame.setContentPane(contentPane);        
        frame.pack();
        frame.setJMenuBar(menuBar);
        frame.setVisible(true);
        
        updateStatusPanel(Profiles.DEFAULT_PROFILE);
    }
    private void updateStatusPanel(String s){
        if (contentPane!=null)
        	frame.remove(contentPane);
        contentPane=createBucketPanel(s);
        frame.setContentPane(contentPane); 
        
    	if (statusPanel!=null)
    		frame.remove(statusPanel);
    	/*
        statusPanel = new JPanel();
        statusPanel.setBorder(BorderFactory.createEmptyBorder(1, 5, 1, 0));
        statusPanel.setPreferredSize(new Dimension(frame.getWidth(), 16));
        statusPanel.setLayout(new BoxLayout(statusPanel, BoxLayout.X_AXIS));
        statusLabel = new JLabel("Buckets Frame with profile: " +s);
        statusLabel.setHorizontalAlignment(SwingConstants.LEFT);
        statusPanel.add(statusLabel);
        frame.add(statusPanel, BorderLayout.NORTH);//SOUTH
        */
        frame.validate();
        frame.repaint();
    }
    private JPanel createBucketPanel(String profile) {
    	JPanel statusPanel = new JPanel();
    	JLabel statusLabel = new JLabel("Frame with profile: " +profile);
    	statusPanel.add(statusLabel);
    	return statusPanel;
    }
}