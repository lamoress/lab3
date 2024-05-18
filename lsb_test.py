import unittest
from PIL import Image
import os
from lsb import encode_lsb, decode_lsb, psnr

class TestSteganography(unittest.TestCase):

    def setUp(self):
        self.original_image_path = "1.bmp"
        self.secret_file_path = "test_secret.txt"
        self.encoded_image_path = "encoded_image.bmp"
        self.decoded_file_path = "decoded_file.txt"

        with open(self.secret_file_path, 'w', encoding='utf-8') as f:
            f.write("Secret Message")

    def tearDown(self):
        if os.path.exists(self.encoded_image_path):
            try:
                os.remove(self.encoded_image_path)
            except PermissionError:
                pass
        if os.path.exists(self.decoded_file_path):
            os.remove(self.decoded_file_path)
        if os.path.exists(self.secret_file_path):
            os.remove(self.secret_file_path)

    def test_encode_lsb(self):
        result = encode_lsb(self.original_image_path, self.secret_file_path)
        self.assertEqual(result, "Done")
        self.assertTrue(os.path.exists(self.encoded_image_path))

    def test_decode_lsb(self):
        encode_result = encode_lsb(self.original_image_path, self.secret_file_path)
        self.assertEqual(encode_result, "Done")
        result = decode_lsb(self.encoded_image_path)
        self.assertEqual(result, "Файл успешно извлечен.")
        self.assertTrue(os.path.exists(self.decoded_file_path))
        
        with open(self.secret_file_path, 'rb') as original, open(self.decoded_file_path, 'rb') as decoded:
            self.assertEqual(original.read(), decoded.read())

    def test_psnr(self):
        encode_result = encode_lsb(self.original_image_path, self.secret_file_path)
        self.assertEqual(encode_result, "Done")
        original_image = Image.open(self.original_image_path)
        encoded_image = Image.open(self.encoded_image_path)
        psnr_value = psnr(original_image, encoded_image)
        self.assertTrue(psnr_value > 30)
        original_image.close()
        encoded_image.close()

if __name__ == '__main__':
    unittest.main()
