import hashlib

def calculate_md5(file_path):
    try:
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest().lower()
    except Exception as e:
        return None