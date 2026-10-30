import java.nio.file.*; import java.io.*; import java.security.*; import java.security.cert.*;
public class TrustStore { public static void main(String[] args) throws Exception {
KeyStore ks=KeyStore.getInstance("JKS"); char[] password="changeit".toCharArray(); ks.load(null,password); int i=0;
try(InputStream in=Files.newInputStream(Path.of(args[0]))) { for(java.security.cert.Certificate cert:CertificateFactory.getInstance("X.509").generateCertificates(in)) ks.setCertificateEntry("system-ca-"+(i++),cert); }
try(OutputStream out=Files.newOutputStream(Path.of(args[1]))) { ks.store(out,password); } System.out.println("TRUST_ROOTS "+i);
}}
