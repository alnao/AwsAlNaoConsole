package it.alnao.awsJConsole.window;

import java.awt.Dimension;
import java.io.FileNotFoundException;

import javax.swing.*;
import javax.swing.event.MenuKeyEvent;
import javax.swing.plaf.DimensionUIResource;

import it.alnao.awsJConsole.App;
import it.alnao.awsJConsole.window.ec2.Instances;
import it.alnao.awsJConsole.window.s3.Buckets;
import software.amazon.awssdk.regions.Region;

//https://docs.oracle.com/javase/tutorial/uiswing/components/tabbedpane.html
public class MainTabs {

	public static JComponent makeTextPanel(String t) {
		JTextPane textPane = new JTextPane();
		textPane.setText(t);
		//StyledDocument doc = textPane.getStyledDocument();
		//addStylesToDocument(doc);
		return textPane;
	}
	
	
	public static JTabbedPane createMainTabs(String profile,Region region) throws FileNotFoundException {
		JTabbedPane tabbedPane = new JTabbedPane();
		tabbedPane.setPreferredSize(new Dimension(App.WIN_W-10,App.WIN_H-40));
		//ImageIcon icon = createImageIcon("images/middle.gif");

		JComponent panel1 = makeTextPanel("Profilo: " + profile);
		tabbedPane.addTab("Profilo: " + profile, panel1);
		tabbedPane.setMnemonicAt(0, MenuKeyEvent.VK_1);

//EC2	//JComponent panel2 = makeTextPanel("Ec2");
		tabbedPane.addTab("Ec2", new Instances().createInstancesTab(profile,region));
		//tabbedPane.addTab("Tab 2", icon, panel2,"Does twice as much nothing");
		tabbedPane.setMnemonicAt(1, MenuKeyEvent.VK_2);

		tabbedPane.addTab("S3",new Buckets().createInstancesTab(profile, region));
		tabbedPane.setMnemonicAt(2, MenuKeyEvent.VK_3);

		JComponent panel4 = makeTextPanel("TODO"); //(has a preferred size of 410 x 50).
		panel4.setPreferredSize(new DimensionUIResource(410, 50));
		tabbedPane.addTab("TODO", panel4);
		tabbedPane.setMnemonicAt(3, MenuKeyEvent.VK_4);
		
		return tabbedPane;
	}
	
	
}
