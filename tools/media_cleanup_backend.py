"""Use the verified cleanup engine with both deployed legacy Worker aliases."""
import media_cleanup435
media_cleanup435.ORIGINS.update({'ngelx-media.alihancaglar76.workers.dev','ngelx-upload.alihancaglar76.workers.dev'})
if __name__=='__main__':media_cleanup435.main()
