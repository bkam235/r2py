import requests
from typing import Any, Dict, List, Optional

# r2py:entity:req_auth
def oauth_client(id: str, token_url: str, secret: Optional[str] = None, key: Optional[str] = None, 
                 auth: Any = "body", auth_params: Optional[Dict] = None, name: Optional[str] = None):
    if auth_params is None:
        auth_params = {}
    
    # In R, the name defaults to a hash of the id if not provided
    client_name = name if name is not None else id
    
    # Basic validation based on R source logic
    if isinstance(auth, str):
        # R's oauth_client prefixes the auth string
        auth_val = f"oauth_client_req_auth_{auth}"
    else:
        auth_val = auth

    return {
        "name": client_name,
        "id": id,
        "secret": secret,
        "key": key,
        "token_url": token_url,
        "auth": auth_val,
        "auth_params": auth_params,
        "class": "httr2_oauth_client"
    }

def req_policies(req, **policies):
    if req["policies"] is None:
        req["policies"] = {}
    req["policies"].update(policies)
    return req

def req_auth_sign(req, fun, params, cache):
    return req_policies(req, auth_sign={"fun": fun, "params": params, "cache": cache})

def req_oauth(req, flow, flow_params, cache):
    # Simplified version of R's auth_oauth_sign
    def auth_oauth_sign(req, params):
        return req
        
    req = req_auth_sign(req, fun=auth_oauth_sign, params={"flow": flow, "flow_params": flow_params}, cache=cache)
    req = req_policies(req, auth_oauth=True)
    return req

def req_oauth_client_credentials(req, client, scope=None, token_params=None):
    if token_params is None:
        token_params = {}
    
    params = {"client": client, "scope": scope, "token_params": token_params}
    
    # Simplified cache_mem
    cache = {
        "get": lambda: None,
        "set": lambda token: None,
        "clear": lambda: None
    }
    
    return req_oauth(req, "oauth_flow_client_credentials", params, cache)

# r2py:entity:request
def request(base_url):
    # Create a dictionary that mimics the R httr2_request object
    req = {
        "url": base_url,
        "method": "GET",
        "headers": {},
        "body": None,
        "fields": {},
        "options": {},
        "policies": {},
    }
    
    class Httr2Request(dict):
        def __repr__(self):
            policies_str = ""
            if self["policies"]:
                lines = []
                for k, v in self["policies"].items():
                    # Mimic R's print output for complex objects
                    if isinstance(v, dict):
                        val_str = "<list>"
                    elif isinstance(v, bool):
                        val_str = "TRUE" if v else "FALSE"
                    else:
                        val_str = str(v)
                    lines.append(f"* {k} : {val_str}")
                policies_str = "Policies:\n" + "\n".join(lines)
            else:
                policies_str = "Policies: (empty)"
            
            return (f"<httr2_request>\n"
                    f"{self['method']} {self['url']}\n"
                    f"Body: {'empty' if self['body'] is None else self['body']}\n"
                    f"{policies_str}")

    return Httr2Request(req)

def req_auth(req):
    return req_oauth_client_credentials(
        req,
        client=oauth_client("example", "https://example.com/get_token")
    )

# Execution
if __name__ == "__main__":
    # R: request("https://example.com") |> req_auth()
    req = request("https://example.com")
# r2py:entity:req_auth_1
    req = req_auth(req)
    print(req)