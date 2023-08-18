package it.alnao.awsJConsole.window.ec2;

import java.awt.Dimension;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import it.alnao.awsJConsole.window.MainTabs;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.ec2.model.Instance;

//see https://docs.oracle.com/javase/tutorial/uiswing/components/list.html
//see https://docs.oracle.com/javase/tutorial/uiswing/components/table.html
public class Instances {
	public static JPanel createInstancesTab(String profile,Region region) throws FileNotFoundException {
		JPanel p = new JPanel();
		//p.add ( MainTabs.makeTextPanel("Lista istanze EC2 "+ profile) );
		p.add (createListInstancesPanel(profile,region));
		p.add ( MainTabs.makeTextPanel("TODO "+ profile) );
		return p;
	}

	public static JScrollPane createListInstancesPanel(String profile,Region region) throws FileNotFoundException {
		List<Instance> listI = it.alnao.awsJConsole.sdk.ec2.Instances.describeEC2Instances(profile,region);
		String[] columnNames = {"NOME","ID","TIPO","STATO"};//https://docs.oracle.com/javase/tutorial/uiswing/components/table.html
		String[][] data = new String[listI.size()][4];
		//List<String> data=new ArrayList<String>();
		//JTable(Vector rowData, Vector columnNames)
		for (int i=0;i<listI.size();i++) {Instance instance= listI.get(i);
			String name=" ";
			if (instance.tags().size()>0) {
				for (int j=0;j<instance.tags().size();j++) {
					if ( "Name".equals( instance.tags().get(j).key() )) {
						name=instance.tags().get(j).value();
					}
				}
			} 
			data[i][0]=name;
			data[i][1]=instance.instanceId();
			data[i][2]=instance.instanceType().toString();
			data[i][3]=instance.state().name().toString();
			//data.add(name + " " + instance.state().name());
			//instance.instanceId() + " " + name + " " + instance.instanceType() + " " + instance.state().name());
		}		
		
		JTable table = new JTable(data , columnNames){
	        private static final long serialVersionUID = 1L;

	        public boolean isCellEditable(int row, int column) {                
	                return false;               
	        };
	    };
	    table.getColumnModel().getColumn(0).setPreferredWidth(300);
		table.setPreferredSize(new Dimension(600,570));
		
		JScrollPane p = new JScrollPane(table);
		p.setPreferredSize(new Dimension(600,600));
		return p;
		/*
		//see https://docs.oracle.com/javase/tutorial/uiswing/components/list.html
		JList list = new JList(data.toArray()); //data has type Object[]
		list.setSelectionMode(ListSelectionModel.SINGLE_INTERVAL_SELECTION);
		list.setLayoutOrientation(JList.HORIZONTAL_WRAP);
		list.setVisibleRowCount(-1);
		JScrollPane listScroller = new JScrollPane(list);
		listScroller.setPreferredSize(new Dimension(320 *1,70));
		list.setPreferredSize(new Dimension(320 *1,70));
		return listScroller; //JScrollPane
		*/
	}

	
	
}
