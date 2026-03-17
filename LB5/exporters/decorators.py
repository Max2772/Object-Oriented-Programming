import base64
import io
import zipfile
from pathlib import Path
from typing import List

from LB5.exporters.abstract_exporter import Exporter
from LB5.types.dto.delivery_result import DeliveryResult


class ExporterDecorator(Exporter):
    def __init__(self, exporter: Exporter, internal_filename: str):
        self._exporter = exporter
        self.internal_filename = internal_filename

    def save(self, data: bytes, file_path: str):
        with open(file_path, "wb") as f:
            f.write(data)
        print(f"Экспорт {self.internal_filename} в файл {file_path}")

    def export(
            self,
            results: List[DeliveryResult],
            file_path: str = None
    ) -> bytes:
        return self._exporter.export(results, file_path)


class CompressedExporter(ExporterDecorator):
    def __init__(
            self,
            exporter: Exporter,
            internal_filename: str,
    ):
        super().__init__(exporter, internal_filename)

    def export(
            self,
            results: List[DeliveryResult],
            file_path: str = None
    ) -> bytes:
        data = self._exporter.export(results)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(self.internal_filename, data)

        compressed_data = zip_buffer.getvalue()
        if file_path:
            self.save(
                compressed_data,
                file_path
            )

        return compressed_data


class EncryptedExporter(ExporterDecorator):
    def __init__(
            self,
            exporter: Exporter,
            key: str,
            internal_filename: str
    ):
        super().__init__(exporter, internal_filename)
        self.key = key.encode()

    def _xor(self, data: bytes) -> bytes:
        return bytes(b ^ self.key[i % len(self.key)] for i, b in enumerate(data))

    def export(
            self,
            results: List[DeliveryResult],
            file_path: str = None
    ) -> bytes:
        data = self._exporter.export(results)
        encrypted = base64.b64encode(self._xor(data))

        if file_path:
            self.save(
                encrypted,
                file_path
            )

        return encrypted

    def decrypt(
            self,
            encrypted_data: bytes,
            file_path: str = None
    ) -> bytes:
        decrypted_data = self._xor(base64.b64decode(encrypted_data))
        if file_path:
            self.save(
                decrypted_data,
                file_path
            )
        return decrypted_data
