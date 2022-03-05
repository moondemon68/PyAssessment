from werkzeug.datastructures import FileStorage

def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['py']

def check_file(file: FileStorage):
    if file.filename == '':
        return True, 'Filename cannot be blank'
    if file and not allowed_file(file.filename):
        return True, 'Extension file not supported'
    return False, ''