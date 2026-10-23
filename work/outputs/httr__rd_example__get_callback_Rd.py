import requests

# Mocking the callback system of httr
# r2py:entity:old
class RequestManager:
    def __init__(self):
        self.callbacks = {"request": None, "response": None}

    def set_callback(self, type_val, func):
        old = self.callbacks.get(type_val)
        self.callbacks[type_val] = func
        return old

    def get(self, url):
        # Request callback
        if self.callbacks["request"]:
            req_obj = type('obj', (object,), {'url': url})
            res_val = self.callbacks["request"](req_obj)
            if res_val is not None:
                return res_val
        
        res = requests.get(url)
        
        # Response callback
        if self.callbacks["response"]:
            req_obj = type('obj', (object,), {'url': url})
            self.callbacks["response"](req_obj, res)
            
        return res

mgr = RequestManager()

# r2py:entity:req_logger
def req_logger(req):
    # R's cat adds a newline by default if specified, but we match the R source logic
    print(f"HTTP request to '{req.url}'\n", end="")

old = mgr.set_callback("request", req_logger)
# r2py:entity:g1
g1 = mgr.get("https://httpbin.org")
# r2py:entity:g2
g2 = mgr.get("https://httpbin.org/ip")
# r2py:entity:set_callback
mgr.set_callback("request", old)

# r2py:entity:req_logger2
def req_logger2(req):
    # R's cat("... ") without \n
    print(f"HTTP request to '{req.url}' ... ", end="")

# r2py:entity:res_logger
def res_logger(req, res):
    # R's cat(res$status_code, "\n")
    print(f"{res.status_code}\n", end="")

# r2py:entity:old_req
old_req = mgr.set_callback("request", req_logger2)
# r2py:entity:old_res
old_res = mgr.set_callback("response", res_logger)
# r2py:entity:g3
g3 = mgr.get("https://httpbin.org")
# r2py:entity:g4
g4 = mgr.get("https://httpbin.org/ip")
# r2py:entity:set_callback_1
mgr.set_callback("request", old_req)
# r2py:entity:set_callback_2
mgr.set_callback("response", old_res)

# r2py:entity:replay
def replay(req):
    if req.url == "https://httpbin.org":
        return g3

# r2py:entity:old_req_1
old_req = mgr.set_callback("request", replay)
# r2py:entity:grec
grec = mgr.get("https://httpbin.org")

# Compare date headers. R output shows [1] TRUE
res_date_g3 = g3.headers.get('Date')
res_date_grec = grec.headers.get('Date')
print(f"[1] {res_date_g3 == res_date_grec}")

# r2py:entity:set_callback_3
mgr.set_callback("request", old_req)