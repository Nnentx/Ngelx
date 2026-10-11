"""Check arm64 ELF PT_LOAD alignment in APK/AAB; no SDK execution required."""
import sys,struct,zipfile
with zipfile.ZipFile(sys.argv[1]) as z:
 count=0
 for name in z.namelist():
  if '/arm64-v8a/' not in name or not name.endswith('.so'):continue
  data=z.read(name);assert data[:5]==b'\x7fELF\x02',name
  endian='<' if data[5]==1 else '>'
  offset=struct.unpack_from(endian+'Q',data,32)[0]
  size,num=struct.unpack_from(endian+'HH',data,54)
  aligns=[struct.unpack_from(endian+'Q',data,offset+i*size+48)[0] for i in range(num) if struct.unpack_from(endian+'I',data,offset+i*size)[0]==1]
  assert aligns and all(a>=16384 for a in aligns),(name,aligns)
  count+=1;print(name,'PT_LOAD alignment',min(aligns))
 assert count>0
 print(count,'arm64 libraries passed ELF 16 KB alignment; runtime/page packaging verification is separate.')
