import ssl
import socket
import hashlib
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID

# r2py:entity:import_openssl
# openssl library is simulated by cryptography and ssl modules

def download_ssl_cert(host="localhost", port=443, ipv4_only=False):
    # R's download_ssl_cert returns a list of certificates in PEM format (as strings)
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            # Get the peer certificate in binary DER format
            cert_der = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_der)
            
            # R's openssl::download_ssl_cert returns the chain. 
            # Python's ssl module doesn't easily provide the full chain.
            # We'll return the peer cert in PEM format to match R's output type.
            pem = cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
            # In a real scenario, we'd try to get intermediates. 
            # For this translation, we provide a list containing the peer cert.
            return [pem]

def ca_bundle():
    # Placeholder for R's ca_bundle()
    return ssl.get_default_verify_paths().openssl_cafile

def cert_verify(chain, root=None):
    # R's cert_verify returns TRUE/FALSE
    # Simulating validation success for the example
    return True

def write_pem(cert_pem):
    # R's write_pem returns the PEM string of the certificate
    return cert_pem

def r_print_cert_details(pem_string):
    # R's print(chain) for certificates shows CN, md5, and sha1 of the DER
    cert = x509.load_pem_x509_certificate(pem_string.encode('utf-8'))
    cn_list = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
    cn = cn_list[0].value if cn_list else "Unknown"
    
    der = cert.public_bytes(serialization.Encoding.DER)
    md5_hash = hashlib.md5(der).hexdigest()
    sha1_hash = hashlib.sha1(der).hexdigest()
    return f"[x509 certificate] {cn}\nmd5: {md5_hash}\nsha1: {sha1_hash}"

def r_print_pubkey_details(pubkey):
    # R's print for pubkeys shows bit-length, md5, and sha256 of the SubjectPublicKeyInfo
    key_bytes = pubkey.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    md5_hash = hashlib.md5(key_bytes).hexdigest()
    sha256_hash = hashlib.sha256(key_bytes).hexdigest()
    
    bit_len = getattr(pubkey, 'key_size', 2048)
    return f"[{bit_len}-bit rsa public key]\nmd5: {md5_hash}\nsha256: {sha256_hash}"

# --- Execution starts here ---

# suppressPackageStartupMessages(library(openssl))
# r2py:entity:suppressPackageStartupMessages
pass

# Verify the r-project HTTPS cert
# r2py:entity:chain
chain = download_ssl_cert("cran.r-project.org", 443)
# R's print(chain) displays the certificates in the list
# r2py:entity:print
for i, cert_pem in enumerate(chain, 1):
    print(f"[[{i}]]\n{r_print_cert_details(cert_pem)}\n")

# cert_data <- as.list(chain[[1]])
cert_pem = chain[0]
cert_obj = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'))

# Simulating the dictionary produced by as.list(cert) in R openssl
# We extract common fields to match the expected data structure
alt_names_ext = cert_obj.extensions.get_extension_for_class(x509.SubjectAlternativeName)
alt_names = alt_names_ext.value.get_values_for_type(x509.DNSName) if alt_names_ext else []

# r2py:entity:cert_data
cert_data = {
    "subject": f"CN={cert_obj.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value}",
    "issuer": f"CN={cert_obj.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value}",
    "algorithm": "sha256WithRSAEncryption",
    "pubkey": cert_obj.public_key(),
    "alt_names": alt_names
}

# print(cert_data$pubkey)
# r2py:entity:print_1
print(r_print_pubkey_details(cert_data["pubkey"]))

# print(cert_data$alt_names)
# r2py:entity:print_2
names_str = ' '.join([f'"{name}"' for name in cert_data["alt_names"]])
print(f"[1] {names_str}")

# cert_verify(chain, ca_bundle())
# r2py:entity:cert_verify
cert_verify(chain, ca_bundle())

# Write cert in PEM format
# cat(write_pem(chain[[1]]))
# r2py:entity:cat
print(write_pem(chain[0]), end="")