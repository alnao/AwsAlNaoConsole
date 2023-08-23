package it.alnao.awsJConsole.window.ec2;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.awt.Dimension;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.TreeMap;

import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;

import it.alnao.awsJConsole.App;
import it.alnao.awsJConsole.window.MainTabs;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.ec2.model.Instance;

//see https://docs.oracle.com/javase/tutorial/uiswing/components/list.html
//see https://docs.oracle.com/javase/tutorial/uiswing/components/table.html
public class Instances {
	public static final int MAIN_PANEL_W=500;
	JPanel p=null;
	JScrollPane p2=null;
	
	public Instances() {
		//TODO: per ora non serve fare nulla
	}
	public JPanel createInstancesTab(String profile,Region region) throws FileNotFoundException {
		this.p = new JPanel(); //JFrame();
		//p.add ( MainTabs.makeTextPanel("Lista istanze EC2 "+ profile) );
		p.add (createListInstancesPanel(profile,region));

		JComponent c=MainTabs.makeTextPanel("Seleziona una istanza del profilo: "+ profile);
		p2=new JScrollPane(c);
		p2.setPreferredSize(new Dimension(App.WIN_W-30-MAIN_PANEL_W,App.WIN_H-50));
		p.add (  p2 );
		p.setVisible(true);
		return p;
	}

	public JScrollPane createListInstancesPanel(String profile,Region region) throws FileNotFoundException {
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
	    table.getColumnModel().getColumn(0).setPreferredWidth(200);
	    table.getColumnModel().getColumn(1).setPreferredWidth(150);
	    table.getColumnModel().getColumn(2).setPreferredWidth(65);
	    table.getColumnModel().getColumn(3).setPreferredWidth(60);
		table.setPreferredSize(new Dimension(MAIN_PANEL_W-10,App.WIN_H-50));
		
		table.addMouseListener(new java.awt.event.MouseAdapter() {
		    @Override
		    public void mouseClicked(java.awt.event.MouseEvent evt) {
		    	JTable target = (JTable) evt.getSource();
		        int row = target.rowAtPoint(evt.getPoint());
		        int col = target.columnAtPoint(evt.getPoint());
		        System.out.println("Click on" + row + "-" + col);
		        if (row<0) { return;  }
	            Instance i=listI.get(row);
	            p.remove(p2);
	            p2=createDetailInstancesPanel(profile, region, i);
	            p.add (  p2 );
	            p2.validate();
	            p2.repaint();
	            p.validate();
	            p.repaint();
		    }
		});
		
		JScrollPane p = new JScrollPane(table);
		p.setPreferredSize(new Dimension(MAIN_PANEL_W-5,App.WIN_H-50));
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

	
	public JScrollPane createDetailInstancesPanel(String profile,Region region,Instance instance) {
		int w_panel=App.WIN_W-30-MAIN_PANEL_W-5;
		JPanel pp=new JPanel();
		GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
		pp.setLayout(new GridLayout(6, 1, 1, 2)); /* aumentare 2 se aggiunti sotto-pannelli */
		JComponent c1= MainTabs.makeTextPanel("Istanza: "+ instance.imageId() );
		c1.setPreferredSize(new Dimension(w_panel,1));
        gbc.gridx = 0;
        gbc.gridy = 0;
		pp.add ( c1 ,gbc);
		String name=" ";
		if (instance.tags().size()>0) {
			for (int j=0;j<instance.tags().size();j++) {
				if ( "Name".equals( instance.tags().get(j).key() )) {
					name=instance.tags().get(j).value();
				}
			}
		} 
		JComponent c2n=MainTabs.makeTextPanel("Nome: "+ name );
		c2n.setPreferredSize(new Dimension(w_panel,1));
        gbc.gridy = 1;
		pp.add ( c2n ,gbc);
		JComponent c2=MainTabs.makeTextPanel("Stato: "+ instance.state().nameAsString() );
		c2.setPreferredSize(new Dimension(w_panel,1));
        gbc.gridy = 2;
		pp.add ( c2 ,gbc);
		//elenco proprietà in tabella
		TreeMap<String,String> t=it.alnao.awsJConsole.sdk.ec2.Instances.getMapValueIntance(instance);
		String[] columnNames = {"NOME","VALORE"};//https://docs.oracle.com/javase/tutorial/uiswing/components/table.html
		String[][] data = new String[t.keySet().size()][2];
		for (int i=0;i<t.keySet().size();i++) {
			data[i][0]=(String) t.keySet().toArray()[i];
			data[i][1]=t.get(data[i][0]);
		}		
		JTable table = new JTable(data , columnNames){
	        private static final long serialVersionUID = 1L;
	        public boolean isCellEditable(int row, int column) {                
	                return false;               
	        };
	    };
	    table.getColumnModel().getColumn(0).setPreferredWidth(150);
	    table.getColumnModel().getColumn(1).setPreferredWidth(330);
		table.setPreferredSize(new Dimension(w_panel,400));
		JScrollPane ppt = new JScrollPane(table);
		ppt.setPreferredSize(new Dimension(w_panel,420));
        gbc.gridy = 3;
		pp.add(ppt,gbc);
		//tabella tag
		JComponent c2t=MainTabs.makeTextPanel("TAG "+ name );
		c2t.setPreferredSize(new Dimension(w_panel,1));
        gbc.gridy = 4;
		pp.add ( c2t ,gbc);
		String[] columnNamesT = {"NOME","VALORE"};//https://docs.oracle.com/javase/tutorial/uiswing/components/table.html
		String[][] dataT = new String[instance.tags().size()][2];
		for (int i=0;i<instance.tags().size();i++) {
			dataT[i][0]=instance.tags().get(i).key();
			dataT[i][1]=instance.tags().get(i).value();
		}	
		JTable tableT = new JTable(dataT , columnNamesT){
	        private static final long serialVersionUID = 1L;
	        public boolean isCellEditable(int row, int column) {                
	                return false;               
	        };
	    };
	    tableT.getColumnModel().getColumn(0).setPreferredWidth(150);
	    tableT.getColumnModel().getColumn(1).setPreferredWidth(330);
	    tableT.setPreferredSize(new Dimension(w_panel,100));
		JScrollPane pptag = new JScrollPane(tableT);
		pptag.setPreferredSize(new Dimension(w_panel,100));
        gbc.gridy = 5;
		pp.add(pptag,gbc);
		p2 = new JScrollPane( pp  );
		pp.setLayout(new BoxLayout(pp, BoxLayout.Y_AXIS));
		p2.setPreferredSize(new Dimension(w_panel+5,App.WIN_H-50));		
		return p2;		
	}	
	

}
