package it.alnao.awsJConsole.sdk.s3;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import it.alnao.awsJConsole.sdk.Profiles;
import software.amazon.awssdk.core.waiters.WaiterResponse;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.Bucket;
import software.amazon.awssdk.services.s3.model.CreateBucketRequest;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.GetObjectTaggingRequest;
import software.amazon.awssdk.services.s3.model.GetObjectTaggingResponse;
import software.amazon.awssdk.services.s3.model.HeadBucketRequest;
import software.amazon.awssdk.services.s3.model.HeadBucketResponse;
import software.amazon.awssdk.services.s3.model.ListBucketsRequest;
import software.amazon.awssdk.services.s3.model.ListBucketsResponse;
import software.amazon.awssdk.services.s3.model.ListObjectsV2Request;
import software.amazon.awssdk.services.s3.model.ListObjectsV2Response;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.model.S3Exception;
import software.amazon.awssdk.services.s3.model.S3Object;
import software.amazon.awssdk.services.s3.model.Tag;
import software.amazon.awssdk.services.s3.paginators.ListObjectsV2Iterable;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;
import software.amazon.awssdk.services.s3.presigner.model.GetObjectPresignRequest;
import software.amazon.awssdk.services.s3.presigner.model.PresignedGetObjectRequest;
import software.amazon.awssdk.services.s3.waiters.S3Waiter;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.transfer.s3.S3TransferManager;
import software.amazon.awssdk.transfer.s3.model.CompletedFileDownload;
import software.amazon.awssdk.transfer.s3.model.DownloadFileRequest;
import software.amazon.awssdk.transfer.s3.model.FileDownload;
import software.amazon.awssdk.transfer.s3.progress.LoggingTransferListener;
//import software.amazon.awssdk.utils.IoUtils;
//import software.amazon.awssdk.services.s3.model.*;

//see https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/java_s3_code_examples.html
public class Buckets {
    public static void main(String[] args) throws FileNotFoundException {
    	S3Client client = S3Client.builder().build();
    	System.out.println("Start");
    	List<Bucket> listB=getBucketList(client);
    	for (Bucket b : listB) {
    	   System.out.println("Bucket:" + b.name() );
    	}
    	List<S3Object> listO= listBucketObjects(client, listB.get(0).name() ,"");
    	for (S3Object o : listO) {
     	   System.out.println("Object:" + o.key() );
     	}
    	
    	System.out.println("End");
    }
	
	
	
	public static List<Bucket> getBucketList(S3Client s3Client){
		ArrayList<Bucket> l=new ArrayList<Bucket>();
		ListBucketsRequest listBucketsRequest = ListBucketsRequest.builder().build();
		ListBucketsResponse listBuckets = s3Client.listBuckets(listBucketsRequest);
		listBuckets.buckets().stream().forEach(x -> l.add(x));
		return l;
	}
    public static boolean createBucket( S3Client s3Client, String bucketName) {
        try {
            S3Waiter s3Waiter = s3Client.waiter();
            CreateBucketRequest bucketRequest = CreateBucketRequest.builder()
                .bucket(bucketName)
                .build();
            s3Client.createBucket(bucketRequest);
            HeadBucketRequest bucketRequestWait = HeadBucketRequest.builder()
                .bucket(bucketName)
                .build();
            // Wait until the bucket is created and print out the response.
            WaiterResponse<HeadBucketResponse> waiterResponse = s3Waiter.waitUntilBucketExists(bucketRequestWait);
            waiterResponse.matched().response().ifPresent(System.out::println);
            //System.out.println(bucketName +" is ready");
            return true;
        } catch (S3Exception e) {
            System.err.println(e.awsErrorDetails().errorMessage());
            return false;
        }
    }
    //see https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/javav2/example_code/s3/pom.xml
    public Long downloadFile(S3TransferManager transferManager, String bucketName,
            String key, String downloadedFileWithPath) {
		DownloadFileRequest downloadFileRequest =
		DownloadFileRequest.builder()
		.getObjectRequest(b -> b.bucket(bucketName).key(key))
		.addTransferListener(LoggingTransferListener.create())
		.destination(Paths.get(downloadedFileWithPath))
		.build();
		
		FileDownload downloadFile = transferManager.downloadFile(downloadFileRequest);
		
		CompletedFileDownload downloadResult = downloadFile.completionFuture().join();
		//logger.info("Content length [{}]", downloadResult.response().contentLength());
		return downloadResult.response().contentLength();
	}
    public static List<Tag> listTags(S3Client s3, String bucketName, String keyName) {
        try {
            GetObjectTaggingRequest getTaggingRequest = GetObjectTaggingRequest
                .builder()
                .key(keyName)
                .bucket(bucketName)
                .build();
            GetObjectTaggingResponse tags = s3.getObjectTagging(getTaggingRequest);
            List<Tag> tagSet= tags.tagSet();
            return tagSet;
            /*
            for (Tag tag : tagSet) {
                System.out.println(tag.key());
                System.out.println(tag.value());
            }*/
        } catch (S3Exception e) {
            System.err.println(e.awsErrorDetails().errorMessage());
            return null;
        }
    }
    public static String getPresignedUrl(S3Presigner presigner, String bucketName, String keyName ) {

        try {
            GetObjectRequest getObjectRequest = GetObjectRequest.builder()
                .bucket(bucketName)
                .key(keyName)
                .build();

            GetObjectPresignRequest getObjectPresignRequest = GetObjectPresignRequest.builder()
                .signatureDuration(Duration.ofMinutes(60))
                .getObjectRequest(getObjectRequest)
                .build();

            PresignedGetObjectRequest presignedGetObjectRequest = presigner.presignGetObject(getObjectPresignRequest);
            String theUrl = presignedGetObjectRequest.url().toString();
            return theUrl;
            /*
            System.out.println("Presigned URL: " + theUrl);
            HttpURLConnection connection = (HttpURLConnection) presignedGetObjectRequest.url().openConnection();
            presignedGetObjectRequest.httpRequest().headers().forEach((header, values) -> {
             values.forEach(value -> {
                 connection.addRequestProperty(header, value);
              });
            });

            // Send any request payload that the service needs (not needed when isBrowserExecutable is true).
            if (presignedGetObjectRequest.signedPayload().isPresent()) {
                connection.setDoOutput(true);
	
	            try (InputStream signedPayload = presignedGetObjectRequest.signedPayload().get().asInputStream();
	                 OutputStream httpOutputStream = connection.getOutputStream()) {
		                 IoUtils.copy(signedPayload, httpOutputStream);
		            }
	        }
	
	        // Download the result of executing the request.
	        try (InputStream content = connection.getInputStream()) {
	            System.out.println("Service returned response: ");
	            IoUtils.copy(content, System.out);
	            connection.get
	        }
	        */

	    } catch (S3Exception e) { // | IOException
	        e.getStackTrace();
	        return null;
	    }
	 }
    public static List<S3Object> listBucketObjects(S3Client s3Client, String bucketName , String path ) {
    	ArrayList<S3Object> l=new ArrayList<S3Object>();
        try {
            ListObjectsV2Request listReq = ListObjectsV2Request.builder()
                .bucket(bucketName)
                //.maxKeys(1)
                .build();
            ListObjectsV2Response listObjectsV2Response = s3Client.listObjectsV2(listReq);
            List<S3Object> contents = listObjectsV2Response.contents();
            if (path==null || "".equals(path)) {
            	//se root aggiungo le cartelle e i file nella root
            	contents.stream().filter( r -> r.key().endsWith("/") && r.key().indexOf("/")==r.key().lastIndexOf("/") ).forEach(r -> l.add(r) );
            	contents.stream().filter( r -> ! r.key().contains("/") ).forEach(r -> l.add(r) );
            }else{
            	contents.stream().filter( r -> r.key().startsWith(path)).forEach(r -> l.add(r) );
            }
            //ListObjectsV2Iterable listRes = s3Client.listObjectsV2Paginator(listReq);
            //listRes.stream().flatMap(r -> r.contents().stream())
            //    .forEach(content -> l.add(content) /*;System.out.println(" Key: " + content.key() + " size = " + content.size())*/ );
        } catch (S3Exception e) {
            System.err.println(e.awsErrorDetails().errorMessage());
            e.printStackTrace();
            return null;
        }
        return l;
    }
    public static boolean putS3Object(S3Client s3, String bucketName, String objectKey, String objectPath) {
        try {
            Map<String, String> metadata = new HashMap<String,String>();
            metadata.put("x-amz-meta-myVal", "test");
            PutObjectRequest putOb = PutObjectRequest.builder()
                .bucket(bucketName)
                .key(objectKey)
                .metadata(metadata)
                .build();
            s3.putObject(putOb, RequestBody.fromFile(new File(objectPath)));
            //System.out.println("Successfully placed " + objectKey +" into bucket "+bucketName);
        } catch (S3Exception e) {
            System.err.println(e.getMessage());
            return false;
        }
        return true;
    }
}
