package it.alnao.awsJConsole.window.s3;

import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridLayout;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.TreeMap;

import javax.swing.BoxLayout;
import javax.swing.JComponent;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;

import it.alnao.awsJConsole.App;
import it.alnao.awsJConsole.window.MainTabs;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.ec2.model.Instance;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.Bucket;
import software.amazon.awssdk.services.s3.model.S3Object;

public class Buckets {
	public static final int MAIN_PANEL_W=350;
	JPanel p=null;
	JScrollPane p2=null;
	
	public Buckets() {
		//TODO: per ora non serve fare nulla
	}
	public JPanel createInstancesTab(String profile,Region region) throws FileNotFoundException {
		this.p = new JPanel(); //JFrame();
		//p.add ( MainTabs.makeTextPanel("Lista istanze EC2 "+ profile) );
		p.add (createListPanel(profile,region));

		JComponent c=MainTabs.makeTextPanel("Seleziona un bucket del profilo: "+ profile);
		p2=new JScrollPane(c);
		p2.setPreferredSize(new Dimension(App.WIN_W-30-MAIN_PANEL_W,App.WIN_H-75));
		p.add (  p2 );
		p.setVisible(true);
		return p;
	}
	public JScrollPane createListPanel(String profile,Region region) throws FileNotFoundException {
		S3Client client = S3Client.builder().build();
		List<Bucket> listB=it.alnao.awsJConsole.sdk.s3.Buckets.getBucketList(client);

		String[] columnNames = {"NOME"};//https://docs.oracle.com/javase/tutorial/uiswing/components/table.html
		String[][] data = new String[listB.size()][1];
		for (int i=0;i<listB.size();i++) {Bucket bu= listB.get(i);
			data[i][0]=bu.name();
			//System.out.println(bu.toString());
		}		
		
		JTable table = new JTable(data , columnNames){
	        private static final long serialVersionUID = 1L;

	        public boolean isCellEditable(int row, int column) {                
	                return false;               
	        };
	    };
	    table.getColumnModel().getColumn(0).setPreferredWidth(200);
	    //table.getColumnModel().getColumn(1).setPreferredWidth(150);
	    //table.getColumnModel().getColumn(2).setPreferredWidth(65);
	    //table.getColumnModel().getColumn(3).setPreferredWidth(60);
		table.setPreferredSize(new Dimension(MAIN_PANEL_W-10,App.WIN_H-100));
		
		table.addMouseListener(new java.awt.event.MouseAdapter() {
		    @Override
		    public void mouseClicked(java.awt.event.MouseEvent evt) {
		    	JTable target = (JTable) evt.getSource();
		        int row = target.rowAtPoint(evt.getPoint());
		        int col = target.columnAtPoint(evt.getPoint());
		        //System.out.println("Click on" + row + "-" + col);
		        if (row<0) { return;  }
	            Bucket b=listB.get(row);
	            p.remove(p2);
	            p2=createDetailPanel(profile, region, b ,"");
	            p.add (  p2 );
	            p2.validate();
	            p2.repaint();
	            p.validate();
	            p.repaint();
		    }
		});
		JScrollPane p = new JScrollPane(table);//table
		p.setPreferredSize(new Dimension(MAIN_PANEL_W-5,App.WIN_H-100));
		return p;
	}
	public JScrollPane createDetailPanel(String profile,Region region,Bucket bu, String path) {
		int w_panel=App.WIN_W-30-MAIN_PANEL_W-5;
		JPanel pp=new JPanel();
		GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
		pp.setLayout(new GridLayout(6, 1, 1, 2)); /* aumentare 2 se aggiunti sotto-pannelli */
		JComponent c1= MainTabs.makeTextPanel("Bucket: "+ bu.name() );
		c1.setPreferredSize(new Dimension(w_panel,1));
        gbc.gridx = 0;
        gbc.gridy = 0;
		pp.add ( c1 ,gbc);
		String name=" ";
		/* TODO path
		JComponent c2n=MainTabs.makeTextPanel("Nome: "+ name );
		c2n.setPreferredSize(new Dimension(w_panel,1));
        gbc.gridy = 1;
		pp.add ( c2n ,gbc);
		JComponent c2=MainTabs.makeTextPanel("Stato: "+ instance.state().nameAsString() );
		c2.setPreferredSize(new Dimension(w_panel,1));
        gbc.gridy = 2;
		pp.add ( c2 ,gbc);
		*/
		//elenco oggetti
		S3Client client = S3Client.builder().build();
		List<S3Object> listO=it.alnao.awsJConsole.sdk.s3.Buckets.listBucketObjects(client,bu.name(),path);
		String[] columnNames = {"NOME","DIM","CREATED"};//https://docs.oracle.com/javase/tutorial/uiswing/components/table.html
		String[][] data = new String[listO.size()][3];
		for (int i=0;i<listO.size();i++) {S3Object o=listO.get(i);
			data[i][0]=o.key();
			data[i][1]=""+o.size()/1024;
			data[i][2]=o.lastModified().toString().replace("T", " ").replace("Z", "");
		}		
		JTable table = new JTable(data , columnNames){
	        private static final long serialVersionUID = 1L;
	        public boolean isCellEditable(int row, int column) {                
	                return false;               
	        };
	    };
	    table.getColumnModel().getColumn(0).setPreferredWidth(350);
	    table.getColumnModel().getColumn(1).setPreferredWidth(50);
	    table.getColumnModel().getColumn(2).setPreferredWidth(125);
		table.setPreferredSize(new Dimension(w_panel,500));
		JScrollPane ppt = new JScrollPane(table);
		ppt.setPreferredSize(new Dimension(w_panel,520));
        gbc.gridy = 3;
		pp.add(ppt,gbc);
		/*
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
		*/
		p2 = new JScrollPane( pp  );
		pp.setLayout(new BoxLayout(pp, BoxLayout.Y_AXIS));
		p2.setPreferredSize(new Dimension(w_panel+5,App.WIN_H-100));		
		return p2;
	}
}
