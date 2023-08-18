package it.alnao.awsJConsole.sdk.ec2;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;

import it.alnao.awsJConsole.sdk.Profiles;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.ec2.Ec2Client;
import software.amazon.awssdk.services.ec2.model.DescribeInstancesRequest;
import software.amazon.awssdk.services.ec2.model.DescribeInstancesResponse;
import software.amazon.awssdk.services.ec2.model.Ec2Exception;
import software.amazon.awssdk.services.ec2.model.Instance;
import software.amazon.awssdk.services.ec2.model.Reservation;

public class Instances {
    public static List<Instance> describeEC2Instances( Ec2Client ec2){
    	ArrayList<Instance> list=new ArrayList<Instance>();
        String nextToken = null;
        try {
            do {
                DescribeInstancesRequest request = DescribeInstancesRequest.builder().maxResults(6).nextToken(nextToken).build();
                DescribeInstancesResponse response = ec2.describeInstances(request);
                for (Reservation reservation : response.reservations()) {
                    for (Instance instance : reservation.instances()) {
                    	list.add(instance);
                    }
                }
                nextToken = response.nextToken();
            } while (nextToken != null);

        } catch (Ec2Exception e) {
            System.err.println(e.awsErrorDetails().errorCode());
            return list;
        }
        return list;
    }
    
    public static List<Instance> describeEC2Instances(String profile, Region region) throws FileNotFoundException{
    	if (region==null)
    		region = Region.EU_WEST_1; //default irland
        Ec2Client ec2 = Ec2Client.builder()
            .region(region)
            .credentialsProvider( Profiles.loadCredentialFromFile(profile) )
            .build();
       List<Instance> list=describeEC2Instances(ec2);
       return list;
    }
    public static void main(String[] args) throws FileNotFoundException {
    	System.out.println("Start");
    	List<Instance> list=describeEC2Instances(Profiles.DEFAULT_PROFILE,null);
    	for (Instance instance : list) {
    	   System.out.println("Instance:" + instance.instanceId() + " " + instance.tags().get(0).value()
    	   	+ " " + instance.instanceType() + " " + instance.state().name());
    	}
    	System.out.println("End");
    }
}
