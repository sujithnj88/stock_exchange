import secrets
import base64
from http.cookies import SimpleCookie
import datetime

class NseCookie:
    def __init__(self) -> None:
        self.cookie = SimpleCookie()

        self.cookie["bm_sv"] = "A773781A2A942AFE7569CF4A3D45DFF3~YAAQREYDF6zmghCSAQAArWQoGxmDz678NiCeuGJ5qU62Xg6vTr8dd620eEj8LdvRSSSAUoixxBnvnXLD0DxvZNe+3PeithzWVEl4b5rB/PmGi4cUD4Si0OcEiZ0HZF7+2E/CxAILzlbzDqV4VVIwq5W80xVV9wSQLZeRJjNgESqgi71JoxjSaRUyrGtESxcEnadvS1PBpolE6y74OXjdGRjN/xLGwsVsDXKREQ+XU2eEBPPwWh+A0ZoY9fHx7eai9D8="
        # Set cookie attributes
        self.cookie["bm_sv"]["domain"] = ".nseindia.com"
        self.cookie["bm_sv"]["path"] = "/"
        self.cookie["bm_sv"]["secure"] = True
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=1)  # 1 day from now
        self.cookie["bm_sv"]["expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
