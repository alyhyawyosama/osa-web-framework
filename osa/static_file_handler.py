"""
The StaticFileHandler class is designed for educational purposes to demonstrate how to serve static files in a web application.
It includes features such as caching, ETag generation, and optional content compression.
Below is a detailed description of its abilities:

Abilities

1. Serving Static Files:
   - The serve method handles requests for static files.
        It checks if the requested file exists and serves it to the client.
        If the file is not found, it raises a 404 Not Found error.

2. Caching:
   - The class supports caching of static files to improve performance. 
   - The cache_enabled attribute controls whether caching is enabled.
   - The cache_max_age attribute specifies the maximum age for cached responses.

3. ETag Generation:
   - The class generates both strong and weak ETags for static files to facilitate efficient caching and validation.
   - Strong ETags are generated based on the file content using SHA-256 hashing.
   - Weak ETags are generated based on the file size and modification time using MD5 hashing.
   - The If-None-Match header is used to validate ETags and return 304 Not Modified responses when appropriate.

4. Content Compression:
   - The class supports optional gzip compression for compressible file types (e.g., HTML, CSS, JavaScript, plain text).
   - The compress_enabled attribute controls whether compression is enabled.
   - The _gzip_compress method compresses the file content using gzip.

5. MIME Type Detection:
   - The _guess_mimetype method detects the MIME type of the requested file based on its extension.

7. Response Headers:
   - The class sets appropriate response headers, including Last-Modified, ETag, Content-Encoding, and Cache-Control, to optimize client-side caching and performance.
Read more about ETags and caching here:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag
    https://www.rfc-editor.org/rfc/rfc7232#section-2.1
    https://stackoverflow.com/questions/56663203/etag-weak-vs-strong-example
"""

import os
import mimetypes
from hashlib import md5, sha256
from datetime import datetime
from io import BytesIO
import gzip
from webob import Response, Request
from osa.exceptions import HTTPException

class StaticFileHandler:
    def __init__(self, static_dir="static", cache_enabled=True, cache_max_age=3600, compress_enabled=True):
        self.static_dir = os.path.abspath(static_dir)
        self.cache_enabled = cache_enabled
        self.cache_max_age = cache_max_age
        self.compress_enabled = compress_enabled
        self._cache = {}

    def serve(self, path, request: Request):
        file_path = self._get_full_path(path)

        if not os.path.isfile(file_path):
            raise HTTPException(404, "File not found")

        if self.cache_enabled and path in self._cache:
            response = self._get_cached_response(path, request)
        else:
            response = self._create_response(file_path, request)
            if self.cache_enabled:
                self._cache_response(path, response)

        return response

    def _get_full_path(self, path):
        # Prevent directory traversal attacks
        safe_path = os.path.normpath(path).lstrip(os.sep) # Remove leading slashes and normalize path .e.g, /../file.txt -> file.txt
        full_path = os.path.join(self.static_dir, safe_path)

        if not full_path.startswith(self.static_dir):
            raise HTTPException(403, "Forbidden")
        return full_path

    def _create_response(self, file_path, request):
        file_size = os.path.getsize(file_path)
        file_mtime = self._get_last_modified(file_path)

        # Generate strong and weak ETags
        # strong_etag = self._generate_strong_etag(file_path) # Strong ETag based on file content (not used in this implementation)
        weak_etag = self._generate_weak_etag(file_size, file_mtime)

        # If-None-Match: Optimized response using ETag
        if request.if_none_match and ( weak_etag in request.if_none_match):
            return Response(status=304)  # Not modified

        with open(file_path, 'rb') as f:
            content = f.read()

        # Optionally compress the content (gzip) based on file type and client support
        compressible_types = {"text/html", "text/css", "application/javascript", "text/plain"}
        content_type = self._guess_mimetype(file_path)

        if self.compress_enabled and "gzip" in request.accept_encoding and content_type in compressible_types:
            content = self._gzip_compress(content)
            encoding = 'gzip'
        else:
            encoding = None

        response = Response(body=content)
        response.content_type = content_type
        response.content_length = len(content)
        response.headers['Last-Modified'] = file_mtime
        response.headers['ETag'] = weak_etag

        if encoding:
            response.headers['Content-Encoding'] = encoding

        if self.cache_enabled:
            response.headers['Cache-Control'] = f"public, max-age={self.cache_max_age}"

        return response

    def _cache_response(self, path, response):
        self._cache[path] = response

    def _get_cached_response(self, path, request):
        cached_response = self._cache[path]

        # Handle If-None-Match to return 304 Not Modified if ETag matches
        if request.if_none_match and cached_response.headers.get('ETag') in request.if_none_match:
            return Response(status=304)

        return cached_response

    def _guess_mimetype(self, file_path):
        mimetype, _ = mimetypes.guess_type(file_path)
        return mimetype or 'application/octet-stream' # Default to binary data if MIME type is not recognized

    def _get_last_modified(self, file_path):
        """
        Returns the last modified time of the file in GMT format.
        """
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp).strftime('%a, %d %b %Y %H:%M:%S GMT')
        # used to convert a Unix timestamp into a human-readable date and time string in a specific format.:
        # datetime.fromtimestamp(timestamp):
        # This function converts a Unix timestamp (which is the number of seconds since January 1, 1970) into a datetime object.
        # The timestamp variable should be a float or integer representing the Unix timestamp.
        # .strftime('%a, %d %b %Y %H:%M:%S GMT'):

        # The strftime method formats the datetime object into a string according to the specified format.
        # The format string '%a, %d %b %Y %H:%M:%S GMT' specifies the desired output format:
        # %a: Abbreviated weekday name (e.g., Mon, Tue).
        # %d: Day of the month as a zero-padded decimal number (e.g., 01, 02).
        # %b: Abbreviated month name (e.g., Jan, Feb).
        # %Y: Year with century as a decimal number (e.g., 2023).
        # %H: Hour (24-hour clock) as a zero-padded decimal number (e.g., 00, 01).
        # %M: Minute as a zero-padded decimal number (e.g., 00, 01).
        # %S: Second as a zero-padded decimal number (e.g., 00, 01).
        # GMT: Literal string "GMT" indicating the time zone.

    def _generate_strong_etag(self, file_path):
        """
        Generates a strong ETag based on the file content.
        """
        with open(file_path, 'rb') as f:
            file_content = f.read()
        return sha256(file_content).hexdigest()

    def _generate_weak_etag(self, file_size, file_mtime):
        """
        Generates a weak ETag based on the file size and modification time.
        """
        etag = f"W/{file_size}-{file_mtime}"
        return md5(etag.encode()).hexdigest()

    def _gzip_compress(self, content):
        buf = BytesIO()
        with gzip.GzipFile(fileobj=buf, mode='wb') as f:
            f.write(content)
        return buf.getvalue()
