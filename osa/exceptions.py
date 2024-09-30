from http import HTTPStatus

class HTTPException(Exception):
    def __init__(self, status_code: int, status_code_value: str=None ,description: str=None ):
        assert status_code in HTTPStatus.__members__.values() , f"Invalid status code {status_code}"
        self.status_code = HTTPStatus(status_code)
        self.message = status_code_value if status_code_value else self.status_code.phrase
        self.description = description if description else self.status_code.description
        
    @property
    def status(self):
        return self.status_code.value
    
    @property
    def phrase(self):
        return f"{self.message}" 
    
    def __str__(self):
        return f"{self.status} {self.phrase} "

def abort(status_code, message=None):
    """
    Function to abort the request with a specific status code and message
    """
    raise HTTPException(status_code, message)