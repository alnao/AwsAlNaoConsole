package it.alnao.awsJConsole.sdk.ec2;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.TreeMap;

import it.alnao.awsJConsole.sdk.Profiles;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.ec2.Ec2Client;
import software.amazon.awssdk.services.ec2.model.DescribeInstancesRequest;
import software.amazon.awssdk.services.ec2.model.DescribeInstancesResponse;
import software.amazon.awssdk.services.ec2.model.Ec2Exception;
import software.amazon.awssdk.services.ec2.model.Instance;
import software.amazon.awssdk.services.ec2.model.Reservation;

public class Instances {
    public static void main(String[] args) throws FileNotFoundException {
    	System.out.println("Start");
    	List<Instance> list=describeEC2Instances(Profiles.DEFAULT_PROFILE,null);
    	for (Instance instance : list) {
    	   System.out.println("Instance:" + instance.instanceId() + " " + instance.tags().get(0).value()
    	   	+ " " + instance.instanceType() + " " + instance.state().name());
    	}
    	System.out.println("End");
    }
    
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
    
    public static TreeMap<String,String> getMapValueIntance(Instance i) {
    	TreeMap<String,String >l=new TreeMap<String,String>();
    	l.put("AmiLaunchIndex",""+i.amiLaunchIndex());
    	l.put("ImageId",""+i.imageId());
    	l.put("InstanceId",""+i.instanceId());
    	l.put("InstanceType",""+i.instanceTypeAsString());
    	l.put("KernelId",""+i.kernelId());
    	l.put("KeyName",""+i.keyName());
    	l.put("LaunchTime",""+i.launchTime());
    	l.put("AmiLaunchIndex",""+i.amiLaunchIndex());
    	l.put("Monitoring",""+i.monitoring());
    	l.put("Placement",""+i.placement());
    	l.put("Platform",""+i.platformAsString());
    	l.put("PrivateDnsName",""+i.privateDnsName());
    	l.put("PrivateIpAddress",""+i.privateIpAddress());
    	l.put("ProductCodes",""+i.productCodes());
    	l.put("PublicDnsName",""+i.publicDnsName());
    	l.put("PublicIpAddress",""+i.publicIpAddress());
    	l.put("RamdiskId",""+i.ramdiskId());
    	l.put("State",""+i.state());
    	l.put("StateTransitionReason",""+i.stateTransitionReason());
    	l.put("VpcId",""+i.vpcId());
    	l.put("Architecture",""+i.architectureAsString());
    	l.put("BlockDeviceMappings",""+i.blockDeviceMappings());
    	l.put("ClientToken",""+i.clientToken());
    	l.put("EbsOptimized",""+i.ebsOptimized());
    	l.put("StateReason",""+i.stateReason());
    	l.put("Tags",""+i.tags());
/*
        case "EnaSupport":
            return Optional.ofNullable(clazz.cast(enaSupport()));
        case "Hypervisor":
            return Optional.ofNullable(clazz.cast(hypervisorAsString()));
        case "IamInstanceProfile":
            return Optional.ofNullable(clazz.cast(iamInstanceProfile()));
        case "InstanceLifecycle":
            return Optional.ofNullable(clazz.cast(instanceLifecycleAsString()));
        case "ElasticGpuAssociations":
            return Optional.ofNullable(clazz.cast(elasticGpuAssociations()));
        case "ElasticInferenceAcceleratorAssociations":
            return Optional.ofNullable(clazz.cast(elasticInferenceAcceleratorAssociations()));
        case "NetworkInterfaces":
            return Optional.ofNullable(clazz.cast(networkInterfaces()));
        case "OutpostArn":
            return Optional.ofNullable(clazz.cast(outpostArn()));
        case "RootDeviceName":
            return Optional.ofNullable(clazz.cast(rootDeviceName()));
        case "RootDeviceType":
            return Optional.ofNullable(clazz.cast(rootDeviceTypeAsString()));
        case "SecurityGroups":
            return Optional.ofNullable(clazz.cast(securityGroups()));
        case "SourceDestCheck":
            return Optional.ofNullable(clazz.cast(sourceDestCheck()));
        case "SpotInstanceRequestId":
            return Optional.ofNullable(clazz.cast(spotInstanceRequestId()));
        case "SriovNetSupport":
            return Optional.ofNullable(clazz.cast(sriovNetSupport()));

        case "VirtualizationType":
            return Optional.ofNullable(clazz.cast(virtualizationTypeAsString()));
        case "CpuOptions":
            return Optional.ofNullable(clazz.cast(cpuOptions()));
        case "CapacityReservationId":
            return Optional.ofNullable(clazz.cast(capacityReservationId()));
        case "CapacityReservationSpecification":
            return Optional.ofNullable(clazz.cast(capacityReservationSpecification()));
        case "HibernationOptions":
            return Optional.ofNullable(clazz.cast(hibernationOptions()));
        case "Licenses":
            return Optional.ofNullable(clazz.cast(licenses()));
        case "MetadataOptions":
            return Optional.ofNullable(clazz.cast(metadataOptions()));
        case "EnclaveOptions":
            return Optional.ofNullable(clazz.cast(enclaveOptions()));
*/
    	return l;
    }
}
