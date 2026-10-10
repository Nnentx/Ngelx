"""Verified cleanup with deployed aliases and bounded concurrent inventory reads."""
from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED
import media_cleanup435
media_cleanup435.ORIGINS.update({'ngelx-media.alihancaglar76.workers.dev','ngelx-upload.alihancaglar76.workers.dev'})
def inventory_fast(db,max_docs=100000):
 result={};visited=set();pending={}
 def read_doc(ref):return ref.get(),list(ref.collections())
 # Every independent read must complete successfully. Any failure aborts the
 # inventory rather than treating inaccessible content as unreferenced media.
 with ThreadPoolExecutor(max_workers=16) as pool:
  for collection in db.collections():pending[pool.submit(lambda c:list(c.list_documents()),collection)]=('collection',collection)
  while pending:
   done,_=wait(pending,return_when=FIRST_COMPLETED)
   for future in done:
    kind,ref=pending.pop(future);value=future.result()
    if kind=='collection':
     for document in value:
      if document.path in visited:continue
      visited.add(document.path)
      if len(visited)>max_docs:raise RuntimeError('Inventory limit reached; no deletion allowed')
      pending[pool.submit(read_doc,document)]=('document',document)
    else:
     snap,children=value
     if snap.exists:result[ref.path]=snap
     for child in children:pending[pool.submit(lambda c:list(c.list_documents()),child)]=('collection',child)
 return result
media_cleanup435.inventory=inventory_fast
if __name__=='__main__':media_cleanup435.main()
