import hashlib
import uuid

class Utilities:

    def hash_password(password):
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_uuid():
        """Generate a unique UUID4 string"""
        return str(uuid.uuid4())