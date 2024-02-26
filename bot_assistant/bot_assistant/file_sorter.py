import sys
import re
import shutil
from pathlib import Path


class FileSorter:
    JPEG_IMAGES = []
    PNG_IMAGES = []
    JPG_IMAGES = []
    SVG_IMAGES = []
    AVI_VIDEO = []
    MP4_VIDEO = []
    MOV_VIDEO = []
    MKV_VIDEO = []
    DOC_DOCUMENTS = []
    DOCX_DOCUMENTS = []
    TXT_DOCUMENTS = []
    PDF_DOCUMENTS = []
    XLSX_DOCUMENTS = []
    PPTX_DOCUMENTS = []
    MP3_AUDIO = []
    OGG_AUDIO = []
    WAV_AUDIO = []
    AMR_AUDIO = []
    ARCHIVES = []
    ZIP_ARCHIVES = []
    GZ_ARCHIVES = []
    TAR_ARCHIVES = []
    MY_OTHER = []

    REGISTER_EXTENSION = {
        'JPEG': JPEG_IMAGES,
        'PNG': PNG_IMAGES,
        'JPG': JPG_IMAGES,
        'SVG': SVG_IMAGES,
        'AVI': AVI_VIDEO,
        'MP4': MP4_VIDEO,
        'MOV': MOV_VIDEO,
        'MKV': MKV_VIDEO,
        'DOC': DOC_DOCUMENTS,
        'DOCX': DOCX_DOCUMENTS,
        'TXT': TXT_DOCUMENTS,
        'PDF': PDF_DOCUMENTS,
        'XLSX': XLSX_DOCUMENTS,
        'PPTX': PPTX_DOCUMENTS,
        'MP3': MP3_AUDIO,
        'OGG': OGG_AUDIO,
        'WAV': WAV_AUDIO,
        'AMR': AMR_AUDIO,
        'ZIP': ZIP_ARCHIVES,
        'GZ': GZ_ARCHIVES,
        'TAR': TAR_ARCHIVES,
    }

    FOLDERS = []
    EXTENSIONS = set()
    UNKNOWN = set()

    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

    TRANS = {}

    for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(cyrillic)] = latin
        TRANS[ord(cyrillic.upper())] = latin.upper()

    @staticmethod
    def get_extension(name: str) -> str:
        return Path(name).suffix[1:].upper()

    @staticmethod
    def normalize(name: str) -> str:
        base_name, dot, extension = name.rpartition(".")
        translate_name = re.sub(r'\W', '_', base_name.translate(FileSorter.TRANS))
        return f"{translate_name}{dot}{extension}"

    def handle_images(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_video(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_documents(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_audio(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_other(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        file_name.replace(target_folder / self.normalize(file_name.name))

    def handle_archive(self, file_name: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / self.normalize(file_name.name.replace(file_name.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
        except shutil.ReadError:
            folder_for_file.rmdir()
            return
        file_name.unlink()

    def scan(self, folder: Path):
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                    self.FOLDERS.append(item)
                    self.scan(item)
                continue

            extension = self.get_extension(item.name)
            full_name = folder / item.name
            if not extension:
                self.MY_OTHER.append(full_name)
            else:
                try:
                    ext_reg = self.REGISTER_EXTENSION[extension]
                    ext_reg.append(full_name)
                    self.EXTENSIONS.add(extension)
                except KeyError:
                    self.UNKNOWN.add(extension)
                    self.MY_OTHER.append(full_name)

    def go(self, folder_path: str):
        folder_process = Path(folder_path)
        self.main(folder_process)

    def main(self, folder: Path):
        self.scan(folder)
        for file in self.JPEG_IMAGES:
            self.handle_images(file, folder / 'images' / 'JPEG')
        for file in self.PNG_IMAGES:
            self.handle_images(file, folder / 'images' / 'PNG')
        for file in self.JPG_IMAGES:
            self.handle_images(file, folder / 'images' / 'JPG')
        for file in self.SVG_IMAGES:
            self.handle_images(file, folder / 'images' / 'SVG')
        for file in self.AVI_VIDEO:
            self.handle_video(file, folder / 'video' / 'AVI')
        for file in self.MP4_VIDEO:
            self.handle_video(file, folder / 'video' / 'MP4')
        for file in self.MOV_VIDEO:
            self.handle_video(file, folder / 'video' / 'MOV')
        for file in self.MKV_VIDEO:
            self.handle_video(file, folder / 'video' / 'MKV')
        for file in self.DOC_DOCUMENTS:
            self.handle_documents(file, folder / 'documents' / 'DOC')
        for file in self.DOCX_DOCUMENTS:
            self.handle_documents(file, folder / 'documents' / 'DOCX')
        for file in self.TXT_DOCUMENTS:
            self.handle_documents(file, folder / 'documents' / 'TXT')
        for file in self.PDF_DOCUMENTS:
            self.handle_documents(file, folder / 'documents' / 'PDF')
        for file in self.XLSX_DOCUMENTS:
            self.handle_documents(file, folder / 'documents' / 'XLSX')
        for file in self.PPTX_DOCUMENTS:
            self.handle_documents(file, folder / 'documents' / 'PPTX')
        for file in self.MP3_AUDIO:
            self.handle_audio(file, folder / 'audio' / 'MP3')
        for file in self.OGG_AUDIO:
            self.handle_audio(file, folder / 'audio' / 'OGG')
        for file in self.WAV_AUDIO:
            self.handle_audio(file, folder / 'audio' / 'WAV')
        for file in self.AMR_AUDIO:
            self.handle_audio(file, folder / 'audio' / 'AMR')
        for file in self.ZIP_ARCHIVES:
            self.handle_archive(file, folder / 'archives' / 'ZIP')
        for file in self.GZ_ARCHIVES:
            self.handle_archive(file, folder / 'archives' / 'GZ')
        for file in self.TAR_ARCHIVES:
            self.handle_archive(file, folder / 'archives' / 'TAR')
        for file in self.MY_OTHER:
            self.handle_other(file, folder / 'MY_OTHER')


def exit_bot() -> None:
    print("Good bye!")
    sys.exit()


if __name__ == "__main__":
    print("Hello my name is Otto. How can I help you?")
    folder_path = input("Enter the path to the folder: ")
    sorter = FileSorter()
    sorter.go(folder_path)
    exit_bot()
