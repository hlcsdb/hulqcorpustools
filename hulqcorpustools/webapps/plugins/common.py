from pathlib import Path

from werkzeug.utils import secure_filename
from werkzeug.wrappers.request import Request
from werkzeug.datastructures import FileStorage

ALLOWED_EXTENSIONS = {'.txt', '.docx', '.doc'}
def secure_allowed_filelist(_filelist: Request.files):
    allowed_files = filter(allowed_file, _filelist)
    secured_files = map(secure_names, allowed_files)
    secured_files = list(secured_files)
    return secured_files

def allowed_file(_file: FileStorage):
    if Path(_file.filename).suffix in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
    
def secure_names(_file: FileStorage):
    _file.filename = secure_filename(_file.filename)
    return _file

def save_secured_allowed_files_to_path(
        _files: Request.files,
        _key: str,
        upload_dir: Path | str,
        ):
    """filter unacceptable filetypes, secure filenames, and save to secure path

    Arguments:
        _files: werkzeug Request.files
        _key: request key corresponding to form file submission (i.le. from html input.name)
        upload_dir: Path or str to where the files should be saved

    Returns:
        list of werkzeug.datastructures.FileStorage with filenames replaced with secure, full paths to where they are saved
    """
    secured_files = secure_allowed_filelist(_files.getlist(_key))
    for _file in secured_files:
        save_filename = Path(upload_dir).joinpath(_file.filename)
        _file.filename = save_filename
        _file.save(save_filename)
    return secured_files