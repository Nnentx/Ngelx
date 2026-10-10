"""Verified cleanup with deployed aliases and bounded concurrent inventory reads."""
from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED
import os,threading
import media_cleanup435
media_cleanup435.ORIGINS.update({'ngelx-media.alihancaglar76.workers.dev','ngelx-upload.alihancaglar76.workers.dev'})
class CleanupReadBudgetExceeded(RuntimeError):pass
_read_budget=int(os.environ.get('NGELX_CLEANUP_READ_BUDGET','10000'))
_reads_used=0
_budget_lock=threading.Lock()
def _reserve_reads(count):
 global _reads_used
 with _budget_lock:
  if _reads_used+count>_read_budget:raise CleanupReadBudgetExceeded('Cleanup read budget exhausted; durable jobs remain queued')
  _reads_used+=count
def inventory_fast(db,max_docs=100000):
 result={};visited=set();pending={}
 def read_doc(ref):return ref.get(retry=None,timeout=20),list(ref.collections(retry=None,timeout=20))
 def read_collection(collection):
  refs=[]
  for ref in collection.list_documents(page_size=100,retry=None,timeout=20):
   # Reserve conservatively for both listing and document fetch. Never keep
   # retrying quota errors or regard a budget-truncated inventory as complete.
   _reserve_reads(2);refs.append(ref)
  return refs
 # Every independent read must complete successfully. Any failure aborts the
 # inventory rather than treating inaccessible content as unreferenced media.
 with ThreadPoolExecutor(max_workers=16) as pool:
  for collection in db.collections():pending[pool.submit(read_collection,collection)]=('collection',collection)
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
     for child in children:pending[pool.submit(read_collection,child)]=('collection',child)
 return result
media_cleanup435.inventory=inventory_fast
if __name__=='__main__':
 try:media_cleanup435.main()
 except CleanupReadBudgetExceeded:
  print('::warning::Cleanup paused at its read budget; incomplete scans never authorize media deletion. Durable jobs retry next run.')
 except Exception as error:
  from google.api_core.exceptions import ResourceExhausted
  if not isinstance(error,ResourceExhausted):raise
  print('::warning::Firestore quota unavailable; live cleanup verification deferred. Durable jobs remain queued. No deletion based on incomplete inventory.')
