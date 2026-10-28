import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_layout', ROOT/'scripts/audit_layout.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class AuditTests(unittest.TestCase):
    def test_review_candidates_and_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'Example.swift').write_text('let bounds = UIScreen.main.bounds\nlet angle = UIDevice.current.orientation\n// UIScreen.main is a comment\nText("Hello")\n')
            (root/'Pods').mkdir()
            (root/'Pods/Vendor.swift').write_text('UIScreen.main.bounds')
            report = audit.audit(root)
            self.assertEqual(report['scannedFiles'], 1)
            self.assertEqual([(e['rule'],e['line']) for e in report['findings']], [('global-screen',1),('orientation',2)])

class CompositionTests(unittest.TestCase):
    def test_opaque_source_pixels_and_overwrite_guard(self):
        from PIL import Image, ImageDraw, ImageChops
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root/'source.png', root/'output.png'
            image = Image.new('RGB',(240,300),(30,40,50))
            ImageDraw.Draw(image).rounded_rectangle((50,50,190,250),radius=20,fill=(200,210,220))
            image.save(source)
            command = [sys.executable,str(ROOT/'scripts/compose_capture.py'),str(source),str(output),'--crop','30,30,210,270','--sample','10,10','--canvas','360,600','--image-box','30,100,330,550']
            subprocess.run(command,check=True,capture_output=True,text=True)
            report = json.loads(output.with_suffix('.json').read_text())
            result = Image.open(output)
            self.assertEqual(result.mode,'RGB')
            self.assertEqual(result.getpixel((0,0)),(30,40,50))
            crop = image.crop((30,30,210,270)).resize(tuple(report['imageSize']),Image.Resampling.LANCZOS)
            x,y = report['imageOrigin'];w,h = report['imageSize']
            self.assertIsNone(ImageChops.difference(crop,result.crop((x,y,x+w,y+h))).getbbox())
            before = output.read_bytes()
            retry = subprocess.run(command,capture_output=True,text=True)
            self.assertNotEqual(retry.returncode,0)
            self.assertEqual(output.read_bytes(),before)

    def test_transparent_source_is_rejected(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory)/'alpha.png', Path(directory)/'output.png'
            Image.new('RGBA',(50,50),(100,100,100,0)).save(source)
            result = subprocess.run([sys.executable,str(ROOT/'scripts/compose_capture.py'),str(source),str(output),'--crop','0,0,50,50','--sample','0,0','--canvas','100,100','--image-box','0,0,100,100'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(output.exists())

if __name__ == '__main__':
    unittest.main()
