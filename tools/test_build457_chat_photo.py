import unittest
from apply_build457_chat_photo import (
    PRIVATE_METHOD, PRIVATE_END, PHOTO_CLASS, NEXT_CLASS,
    SAVE_ANCHOR, RENDER_ANCHOR, WRAP_OLD, transform,
)

class ChatPhoto457(unittest.TestCase):
    def fixture(self):
        return (PHOTO_CLASS + "\n"
                "Widget build()=>NgelXAgResmi(\n"
                +RENDER_ANCHOR+"\n"
                ");\n}\n"
                +NEXT_CLASS+"\n"
                +PRIVATE_METHOD+"\n"
                +SAVE_ANCHOR+"\n"
                "await ngelxBatchCommitDogrula(batch:batch,marker:mesajRef);\n"
                "}\n"
                +PRIVATE_END+"\n"
                "child:"+WRAP_OLD+"\n")

    def test_save_stage_is_after_upload_but_before_firestore_batch(self):
        result=transform(self.fixture())
        save=result.index("Fotoğraf mesajı kaydediliyor…")
        upload=result.index("Duration(minutes:2)")
        commit=result.index("ngelxBatchCommitDogrula")
        self.assertLess(upload,save)
        self.assertLess(save,commit)
        self.assertIn("onPressed:retry",result)
        self.assertIn("NgelXSohbetFotoOnizleme(url:medyaUrl)",result)
        self.assertNotIn(WRAP_OLD,result)
        self.assertEqual(transform(result),result)

    def test_unknown_preview_fails_closed(self):
        with self.assertRaises(ValueError):
            transform(self.fixture().replace(RENDER_ANCHOR, "error:unknown,"))

    def test_unknown_save_fails_closed(self):
        with self.assertRaises(ValueError):
            transform(self.fixture().replace(SAVE_ANCHOR,"changed save pipeline"))

if __name__=="__main__":
    unittest.main()
