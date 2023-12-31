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
import it.alnao.awsJConsole.window.MainTabs;
import it.alnao.awsJConsole.window.Menu;
//import software.amazon.awssdk.auth.credentials.AwsCredentialsProvider;
//import software.amazon.awssdk.profiles.Profile;
import software.amazon.awssdk.regions.Region;

/**
 * 
 * @author Alberto.Nao 
 * @see https://www.alnao.it/aws/ & https://www.alnao.it/javaee/
 * 
 */
public class App {
	private Region defaultRegion=Region.EU_WEST_1;
	
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
				try {
					Set<String> profilesList = Profiles.loadProfilesFromFile();
					new App(profilesList);
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				}
            }
        });
    }  
    
    //app component
    private JFrame frame ;//private JLabel statusLabel;
    private JPanel statusPanel;
    private JPanel contentPane;
    public static final int WIN_W=1000;
    public static final int WIN_H=700;
    
    public App(Set<String> profilesList ) throws FileNotFoundException {
    	contentPane = new JPanel();
        contentPane.setLayout(new BorderLayout());
        contentPane.setPreferredSize(new Dimension(WIN_W,WIN_H));
        contentPane.add(new JLabel("Content"), BorderLayout.CENTER);
        
        frame = new JFrame("Aws J Console");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.setLayout(new BorderLayout());
        frame.setLocationByPlatform(true);
        frame.setSize(200,200);
        frame.setContentPane(contentPane);        
        frame.pack();
        frame.setJMenuBar(Menu.createMenuBar(profilesList  , this ));
        frame.setVisible(true);
        
        updateStatusPanel(Profiles.DEFAULT_PROFILE);
    }
    public JFrame getFrame() {return frame;}
    public String updateStatusPanel(String s) throws FileNotFoundException{
        if (contentPane!=null)
        	frame.remove(contentPane);
        contentPane=createMainPanel(s);
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
        return s;
    }
    private JPanel createMainPanel(String profile) throws FileNotFoundException {
    	JPanel statusPanel = new JPanel();
    	//JLabel statusLabel = new JLabel("Frame with profile: " +profile);
    	//statusPanel.add(statusLabel);
    	Region region=defaultRegion; //TODO: selettore di regioni
    	statusPanel.add(MainTabs.createMainTabs(profile,region));
    	return statusPanel;
    }
}