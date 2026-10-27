import struct,zipfile,hashlib,json,sys
from pathlib import Path
p=Path(sys.argv[1]);b=p.read_bytes()
u16=lambda d,o:struct.unpack_from('<H',d,o)[0]
u32=lambda d,o:struct.unpack_from('<I',d,o)[0]
u64=lambda d,o:struct.unpack_from('<Q',d,o)[0]
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 names=z.namelist();assert any(n.startswith('lib/arm64-v8a/') for n in names)
 assert 'assets/flutter_assets/assets/ludo582/stats_header.png' in names
 assert 'assets/flutter_assets/assets/ludo582/lobby_header.png' in names
 xml=z.read('AndroidManifest.xml')
strings=[];attributes={};o=8
while o<len(xml):
 kind,header,size=struct.unpack_from('<HHI',xml,o)
 assert size>=8
 if kind==1:
  count=u32(xml,o+8);flags=u32(xml,o+16);start=u32(xml,o+20)
  for i in range(count):
   a=o+start+u32(xml,o+header+4*i)
   if flags&0x100:
    def length8(a):
     n=xml[a];return (((n&127)<<8)|xml[a+1],a+2) if n&128 else (n,a+1)
    _,a=length8(a);length,a=length8(a);strings.append(xml[a:a+length].decode())
   else:
    length=u16(xml,a);a+=2
    if length&0x8000:length=((length&0x7fff)<<16)|u16(xml,a);a+=2
    strings.append(xml[a:a+2*length].decode('utf-16-le'))
 elif kind==0x102 and strings[u32(xml,o+20)]=='manifest':
  start=u16(xml,o+24);width=u16(xml,o+26);count=u16(xml,o+28)
  for i in range(count):
   a=o+16+start+i*width;name=strings[u32(xml,a+4)];raw=u32(xml,a+8);datatype=xml[a+15];data=u32(xml,a+16)
   attributes[name]=strings[raw] if raw!=0xffffffff else strings[data] if datatype==3 else data
 o+=size
assert attributes['package']=='com.nnentx.ngelx_app',attributes
assert attributes['versionCode']==582 and attributes['versionName']=='1.0.352',attributes
# Confirm that the downloaded signing certificate matches the installed app's CI-verified signer.
eocd=b.rfind(b'PK\x05\x06');assert eocd>=0
cd=u32(b,eocd+16);assert b[cd-16:cd]==b'APK Sig Block 42'
start=cd-u64(b,cd-24)-8;assert u64(b,start)==u64(b,cd-24)
o=start+8;cert_sha=None

def take(d,o):
 n=u32(d,o);return d[o+4:o+4+n],o+4+n
while o<cd-24:
 size=u64(b,o);ident=u32(b,o+8);value=b[o+12:o+8+size]
 if ident in (0x7109871a,0xf05368c0):
  signers,_=take(value,0);signer,_=take(signers,0);signed,_=take(signer,0)
  _,a=take(signed,0);certs,_=take(signed,a);cert,_=take(certs,0)
  cert_sha=hashlib.sha256(cert).hexdigest();break
 o+=8+size
assert cert_sha=='be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa',cert_sha
print(json.dumps({'package':attributes['package'],'version':attributes['versionName'],'build':attributes['versionCode'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'certificate_sha256':cert_sha,'reference_assets':True}))
