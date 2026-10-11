"""Sign an already-built AAB locally using a private PKCS12 upload key.
Never upload the key or password file to CI or a public repository.
Usage: python3 tools/sign_play_bundle.py INPUT.aab OUTPUT.aab PRIVATE_KEY_DIRECTORY
"""
import json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import hashes
source,output,key_dir=map(Path,sys.argv[1:]);assert source.is_file() and not output.exists()
credentials=json.loads((key_dir/'NgelX-upload-key-credentials.json').read_text())
keystore=key_dir/'NgelX-upload-key.p12'
_,cert,_=pkcs12.load_key_and_certificates(keystore.read_bytes(),credentials['storePassword'].encode())
assert cert,'Upload certificate missing'
with tempfile.TemporaryDirectory() as directory:
 unsigned=Path(directory)/'unsigned.aab'
 with zipfile.ZipFile(source) as src,zipfile.ZipFile(unsigned,'w') as dst:
  assert 'BundleConfig.pb' in src.namelist() and 'base/manifest/AndroidManifest.xml' in src.namelist()
  for entry in src.infolist():
   name=entry.filename.upper()
   if name.startswith('META-INF/') and (name.endswith(('.SF','.RSA','.DSA','.EC')) or name=='META-INF/MANIFEST.MF'):continue
   with src.open(entry) as stream:dst.writestr(entry,stream.read())
 env=os.environ.copy();env['NGELX_SIGNING_PASSWORD']=credentials['storePassword']
 command=['java','-m','jdk.jartool/sun.security.tools.jarsigner.Main','-keystore',str(keystore),'-storetype','PKCS12','-storepass:env','NGELX_SIGNING_PASSWORD','-keypass:env','NGELX_SIGNING_PASSWORD','-sigalg','SHA256withRSA','-digestalg','SHA-256','-signedjar',str(output),str(unsigned),credentials['keyAlias']]
 result=subprocess.run(command,env=env,capture_output=True,text=True)
 assert result.returncode==0,'Bundle signing failed; secret output suppressed'
 verification=subprocess.run(['java','-m','jdk.jartool/sun.security.tools.jarsigner.Main','-verify',str(output)],capture_output=True,text=True)
 assert verification.returncode==0 and 'jar verified.' in verification.stdout.lower(),verification.stdout
 assert 'unsigned entries' not in verification.stdout.lower(), 'Unsigned entries found'
 print('AAB signed and JAR signature verified. Public upload certificate SHA-256:',cert.fingerprint(hashes.SHA256()).hex())
 print('Self-signed upload certificate is expected; this does not certify Play acceptance or application readiness.')
