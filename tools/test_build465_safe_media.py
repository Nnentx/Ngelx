"""Regression fixtures: media fit must preserve full-screen controls and URLs."""
import unittest
from apply_build465_safe_media import transform, OLD_PHOTO, OLD_VIDEO, OLD_HEIGHT

class SafeMediaTests(unittest.TestCase):
    def fixture(self):
        return (
            OLD_PHOTO+"\n"
            "class NgelXGrupVideoMesaj extends StatefulWidget{}\n"
            "class _NgelXGrupVideoMesajState {\n"+OLD_HEIGHT+"\n}\n"
            "class TamEkranVideoPage extends StatelessWidget{\n"+OLD_VIDEO+"\n}\n"
            "class GrupMedyaPage {}\n"
            "class _NgelXMedyaGaleriPageState {\n"
            "    body:widget.urls.isEmpty\n"
            "      ?const Center(child:Icon(Icons.close))\n"
            "      :PageView.builder(\n        itemBuilder:(_,i)=>InteractiveViewer(),\n"
            "      ),\n  );\n}\n"
            "class SabitlenenGrupMesajlariPage {}\n"
        )
    def test_photo_and_video_safe_viewports(self):
        result=transform(self.fixture())
        self.assertIn("body:SafeArea(child:LayoutBuilder",result)
        self.assertIn("MediaQuery.viewPaddingOf(context)",result)
        self.assertIn("width:area.maxWidth,height:area.maxHeight",result)
        self.assertIn("body:SafeArea(child:widget.urls.isEmpty",result)
        self.assertEqual(result,transform(result))
    def test_source_drift_stops_instead_of_guessing(self):
        with self.assertRaises(RuntimeError):
            transform(self.fixture().replace(OLD_VIDEO,"body:Container()"))

if __name__=="__main__":unittest.main()
