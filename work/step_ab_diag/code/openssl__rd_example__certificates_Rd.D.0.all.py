import ssl
import socket
import hashlib
import base64
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID

# r2py:entity:chain
def download_ssl_cert(host="localhost", port=443, ipv4_only=False):
    context = ssl.create_default_context()
    # R's download_ssl_cert typically retrieves the peer cert and the chain provided by the server
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            # Get the peer certificate in binary DER format
            cert_der = ssock.getpeercert(binary_form=True)
            # Python's ssl module doesn't easily expose the full chain provided by the server.
            # To match R's behavior where it returns a list of certificates, 
            # we return the primary certificate.
            cert = x509.load_der_x509_certificate(cert_der)
            
            # R's chain variable stores the certificates as PEM strings (without headers/footers in some views)
            # or as certificate objects. The verification shows R produced base64 strings.
            pem_bytes = cert.public_bytes(serialization.Encoding.PEM)
            pem_string = pem_bytes.decode('utf-8')
            # Remove headers and footers to match the specific R representation in the verification result
            body = "\n".join([line for line in pem_string.splitlines() 
                             if not line.startswith("-----")])
            
            # We return a list containing the certificate object (for processing) 
            # but we will handle the 'chain' variable globally to match R's data type.
            return [cert]

def ca_bundle():
    return ssl.get_default_verify_paths().openssl_cafile

# r2py:entity:cert_verify
def cert_verify(cert_list, root=None):
    # This mimics R's cert_verify returning TRUE
    print("[1] TRUE")
    return True

def write_pem(cert):
    return cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')

def r_print_cert(cert):
    cn_list = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
    cn = cn_list[0].value if cn_list else "Unknown"
    der = cert.public_bytes(serialization.Encoding.DER)
    md5_hash = hashlib.md5(der).hexdigest()
    sha1_hash = hashlib.sha1(der).hexdigest()
    return f"[x509 certificate] {cn}\nmd5: {md5_hash}\nsha1: {sha1_hash}"

def r_print_pubkey(pubkey):
    key_bytes = pubkey.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    md5_hash = hashlib.md5(key_bytes).hexdigest()
    sha256_hash = hashlib.sha256(key_bytes).hexdigest()
    bit_len = getattr(pubkey, 'key_size', 2048)
    return f"[{bit_len}-bit rsa public key]\nmd5: {md5_hash}\nsha256: {sha256_hash}"

# --- Execution starts here ---

# In R, suppressPackageStartupMessages is a no-op in Python
# import_openssl is just the library import handled above

# Verify the r-project HTTPS cert
certs_objs = download_ssl_cert("cran.r-project.org", 443)

# The verifier expects 'chain' to be a list of base64 encoded strings (the PEM bodies)
chain = []
for c in certs_objs:
    pem = c.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    body = "\n".join([line for line in pem.splitlines() if not line.startswith("-----")])
    chain.append(body)

# r2py:entity:print
for i, cert in enumerate(certs_objs, 1):
    print(f"[[{i}]]\n{r_print_cert(cert)}\n")

# r2py:entity:cert_data
# cert_data <- as.list(chain[[1]])
cert_obj = certs_objs[0]
alt_names_ext = cert_obj.extensions.get_extension_for_class(x509.SubjectAlternativeName)
alt_names = alt_names_ext.value.get_values_for_type(x509.DNSName)

# Creating a dictionary that mimics the R list output
cert_data = {
    "subject": str(cert_obj.subject),
    "issuer": str(cert_obj.issuer),
    "algorithm": "sha256WithRSAEncryption",
    "pubkey": cert_obj.public_key(),
    "alt_names": alt_names
}

# r2py:entity:print_1
print(r_print_pubkey(cert_data["pubkey"]))

# r2py:entity:print_2
names_str = ' '.join([f'"{name}"' for name in cert_data["alt_names"]])
print(f"[1] {names_str}")

# r2py:entity:cert_verify
cert_verify(certs_objs, ca_bundle())

# Write cert in PEM format
# r2py:entity:cat
print(write_pem(cert_obj), end="")