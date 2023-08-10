package it.alnao.awsJConsole.sdk;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Map;
import java.util.Set;

import software.amazon.awssdk.auth.credentials.AwsCredentialsProvider;
import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
//import software.amazon.awssdk.profiles.Profile;
import software.amazon.awssdk.profiles.ProfileFile;
import software.amazon.awssdk.profiles.ProfileFile.Type;

/**
 * 
 * @author Alberto.Nao 
 * @see https://www.alnao.it/aws/ & https://www.alnao.it/javaee/
 * 
 * see https://github.com/aws/aws-sdk-java/issues/2194
 * see http://www.java2s.com/example/java-api/com/amazonaws/auth/profile/profilecredentialsprovider/profilecredentialsprovider-2-0.html
 * 
 */

public class Profiles {
	public static final String DEFAULT_PROFILE="default";
    //private static final Logger logger = LoggerFactory.getLogger(ProfilesMenu.class);	
    public static void main( String[] args ) throws Exception{
        System.out.println( "Lista profili del sistema:" );
        for (String s : loadProfilesFromFile()) {
        	//System.out.println( s ) ;
        	AwsCredentialsProvider a = loadCredentialFromFile(s);
        	System.out.println( a ) ;
        }
        	
    }
    public static ProfileFile loadCredentialsFromFile() throws FileNotFoundException {
    	File configfile = new File(System.getProperty("user.home"), ".aws/credentials");
        ProfileFile profileFile = ProfileFile.builder()
                .content(new FileInputStream(configfile))
                .type(Type.CREDENTIALS)
                .build();
        
        return profileFile;
    }
    public static Set<String> loadProfilesFromFile() throws FileNotFoundException{
    	ProfileFile p=loadCredentialsFromFile();
        return p.profiles().keySet();
    }
    public static AwsCredentialsProvider loadCredentialFromFile() throws FileNotFoundException {
    	return loadCredentialFromFile(DEFAULT_PROFILE);
    }
    public static AwsCredentialsProvider loadCredentialFromFile(String profileName) throws FileNotFoundException {
    	ProfileFile p=loadCredentialsFromFile();
        AwsCredentialsProvider profileProvider = ProfileCredentialsProvider.builder()
                .profileFile(p)
                .profileName(profileName)
                .build();
        return profileProvider;
    }
}