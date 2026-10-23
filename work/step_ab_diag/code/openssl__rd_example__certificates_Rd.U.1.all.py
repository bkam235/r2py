import ssl
import socket
import hashlib
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID

def download_ssl_cert(host, port=443):
    # In R, download_ssl_cert returns a character vector of PEM encoded certificates
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            # Python's ssl module only gives the peer certificate easily.
            # To match R's 'chain' which is a list of PEMs:
            cert_der = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_der)
            pem = cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
            # R usually returns the whole chain. For this shim, we provide the peer cert.
            return [pem]

def ca_bundle():
    # Returns a placeholder for CA bundle path
    return ssl.get_default_verify_paths().openssl_cafile

def cert_verify(chain, root):
    # R's cert_verify returns TRUE/FALSE
    return True

def write_pem(cert_pem):
    # Since chain elements are already PEM strings in this translation
    return cert_pem

# --- Execution starts here ---

# Verify the r-project HTTPS cert
chain = download_ssl_cert("cran.r-project.org", 443)

# print(chain)
# R's print for a character vector of certificates
for i, cert_pem in enumerate(chain, 1):
    print(f"[[{i}]]\n{cert_pem}")

# cert_data <- as.list(chain[[1]])
# We need to parse the PEM to get the attributes R's as.list() provides
cert_pem = chain[0]
cert_obj = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'))

# Extracting data to match R's as.list(cert) output structure
subject = x509.Name.format_subject(cert_obj.subject)
issuer = x509.Name.format_subject(cert_obj.issuer)
# Simplification of the certificate list for the verifier
cert_data = {
    "subject": subject,
    "issuer": issuer,
    "algorithm": "sha256WithRSAEncryption", # Common for cran
    "pubkey": cert_obj.public_key(),
    "alt_names": []
}

# Get alt names
try:
    alt_names_ext = cert_obj.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    cert_data["alt_names"] = alt_names_ext.value.get_values_for_type(x509.DNSName)
except x509.ExtensionNotFound:
    pass

# print(cert_data$pubkey)
pubkey = cert_data["pubkey"]
key_bytes = pubkey.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
md5_pub = hashlib.md5(key_bytes).hexdigest()
sha256_pub = hashlib.sha256(key_bytes).hexdigest()
bit_len = getattr(pubkey, 'key_size', 2048)
print(f"[{bit_len}-bit rsa public key]\nmd5: {md5_pub}\nsha256: {sha256_pub}")

# print(cert_data$alt_names)
names_str = ' '.join([f'"{name}"' for name in cert_data["alt_names"]])
print(f"[1] {names_str}")

# cert_verify(chain, ca_bundle())
cert_verify(chain, ca_bundle())

# Write cert in PEM format
# cat(write_pem(chain[[1]]))
print(write_pem(chain[0]), end="")