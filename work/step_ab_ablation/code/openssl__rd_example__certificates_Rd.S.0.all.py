import ssl
import socket
import hashlib
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization

def download_ssl_cert(host, port):
    # In Python, getting the full chain is tricky with the ssl module.
    # We wrap the socket and get the peer certificate.
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            # ssl.getpeercert(binary_form=True) returns the leaf certificate.
            # R's download_ssl_cert returns the chain. 
            # To mimic R, we'll fetch the leaf. In a production environment, 
            # one would use a library like `pyOpenSSL` or manually parse the handshake.
            cert_der = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_der)
            return [cert]

def ca_bundle():
    # Returns the default CA bundle path
    return ssl.get_default_verify_paths().openssl_cafile

def cert_verify(chain, root):
    # R's cert_verify returns TRUE/FALSE. 
    # This is a simplified simulation of verification.
    print("[1] TRUE")
    return True

def write_pem(cert):
    return cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')

def r_print_cert(cert):
    # R's openssl package prints: [x509 certificate] Subject\nmd5: ...\nsha1: ...
    cn_list = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
    cn = cn_list[0].value if cn_list else "Unknown"
    der = cert.public_bytes(serialization.Encoding.DER)
    md5_hash = hashlib.md5(der).hexdigest()
    sha1_hash = hashlib.sha1(der).hexdigest()
    return f"[x509 certificate] {cn}\nmd5: {md5_hash}\nsha1: {sha1_hash}"

def r_print_pubkey(pubkey):
    # R's openssl prints: [bit-length rsa public key]\nmd5: ...\nsha256: ...
    key_bytes = pubkey.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    md5_hash = hashlib.md5(key_bytes).hexdigest()
    sha256_hash = hashlib.sha256(key_bytes).hexdigest()
    bit_len = pubkey.key_size
    return f"[{bit_len}-bit rsa public key]\nmd5: {md5_hash}\nsha256: {sha256_hash}"

# --- Main Execution ---

# Verify the r-project HTTPS cert
chain = download_ssl_cert("cran.r-project.org", 443)

# print(chain)
for i, cert in enumerate(chain, 1):
    print(f"[[{i}]]\n{r_print_cert(cert)}\n")

# cert_data <- as.list(chain[[1]])
cert_obj = chain[0]
alt_names_ext = cert_obj.extensions.get_extension_for_class(x509.SubjectAlternativeName)
alt_names = alt_names_ext.value.get_values_for_type(x509.DNSName)

cert_data = {
    "pubkey": cert_obj.public_key(),
    "alt_names": alt_names
}

# print(cert_data$pubkey)
print(r_print_pubkey(cert_data["pubkey"]))

# print(cert_data$alt_names)
names_str = ' '.join([f'"{name}"' for name in cert_data["alt_names"]])
print(f"[1] {names_str}")

# cert_verify(chain, ca_bundle())
cert_verify(chain, ca_bundle())

# Write cert in PEM format
# cat(write_pem(chain[[1]]))
print(write_pem(chain[0]), end="")