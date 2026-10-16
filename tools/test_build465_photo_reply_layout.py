"""Photos display original aspect ratio; quoted thumbnails stay inside reply."""
import unittest
from apply_build465_photo_reply_layout import (
    transform, START, END, REPLY_START, REPLY_END,
    OLD_PHOTO_LAYOUT, OLD_REPLY,
)

class PhotoReplyLayout(unittest.TestCase):
    def source(self):
        return (
          REPLY_START+"\n Widget build(){\n"+OLD_REPLY+"\n}\n"
          +REPLY_END+"\n"
          +START+"\n Widget build(){\n"+OLD_PHOTO_LAYOUT+"\n}\n"
          +END+"\n"
        )
    def test_original_image_proportions_not_cropped(self):
        result=transform(self.source())
        self.assertIn("fit:BoxFit.contain",result)
        self.assertIn("maxWidth:mediaWidth,maxHeight:mediaHeight",result)
        self.assertIn("width:60,height:60",result)
        self.assertIn("ClipRRect(",result)
        self.assertEqual(result,transform(result))
    def test_changed_image_markup_fails_closed(self):
        with self.assertRaises(RuntimeError):
            transform(self.source().replace("fit:BoxFit.cover","fit:BoxFit.fitWidth"))
if __name__=="__main__":unittest.main()
