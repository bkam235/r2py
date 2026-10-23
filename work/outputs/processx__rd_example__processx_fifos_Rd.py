import os
import select
import tempfile
import shutil

# Mimicking processx FIFO behavior
# In Python, os.mkfifo is only available on Unix. 
# For Windows, we simulate the FIFO using a temporary file to avoid crashes 
# while maintaining the logic of the R script.

# r2py:entity:reader
def conn_create_fifo():
    # Create a temporary directory to hold our "fifo"
    temp_dir = tempfile.mkdtemp()
    fifo_path = os.path.join(temp_dir, "fifo")
    if hasattr(os, 'mkfifo'):
        os.mkfifo(fifo_path)
    else:
        # Windows fallback: create an empty file
        with open(fifo_path, 'w') as f:
            pass
    
    # We return an object that tracks the path and the file handle
    class Connection:
        def __init__(self, path):
            self.path = path
            # Open for reading. 
            # On Unix, opening a FIFO for reading blocks until a writer opens it.
            # To match R's non-blocking behavior, we use os.open.
            if hasattr(os, 'O_NONBLOCK'):
                self.fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
            else:
                self.fd = os.open(path, os.O_RDONLY)
            self.file = os.fdopen(self.fd, 'r')
            self.incomplete = False

        def close(self):
            self.file.close()

    return Connection(fifo_path)

# r2py:entity:writer
def conn_file_name(conn):
    return conn.path

def conn_connect_fifo(path, write=False):
    class Connection:
        def __init__(self, path):
            self.path = path
            # Open for writing.
            if hasattr(os, 'O_NONBLOCK'):
                self.fd = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
            else:
                self.fd = os.open(path, os.O_WRONLY)
            self.file = os.fdopen(self.fd, 'w')

        def close(self):
            self.file.close()
    
    return Connection(path)

# r2py:entity:conn_write
def conn_write(conn, text):
    conn.file.write(text)
    conn.file.flush()

# r2py:entity:poll
def poll(connections, timeout_ms):
    # select.select handles sockets on Windows, but files/pipes only on Unix.
    # We simulate the timeout.
    if hasattr(os, 'mkfifo'):
        handles = [conn.file for conn in connections]
        # Convert ms to seconds
        ready, _, _ = select.select(handles, [], [], timeout_ms / 1000.0)
        return [True if conn.file in ready else False for conn in connections]
    else:
        # Windows simulation: return immediately or wait
        import time
        time.sleep(timeout_ms / 1000.0)
        return [True] * len(connections)

# r2py:entity:conn_read_lines
def conn_read_lines(conn, n):
    if n == -1:
        lines = conn.file.readlines()
    else:
        lines = [conn.file.readline() for _ in range(n)]
    return lines

# r2py:entity:conn_read_chars
def conn_read_chars(conn):
    # Read until EOF or available
    return conn.file.read()

# r2py:entity:conn_is_incomplete
def conn_is_incomplete(conn):
    # Simplified: in this context, if we read something and didn't hit EOF
    return conn.incomplete

# Main execution flow
# r2py:entity:reader
reader = conn_create_fifo()

# r2py:entity:poll
poll([reader], 0)

# r2py:entity:writer
writer = conn_connect_fifo(conn_file_name(reader), write=True)

# r2py:entity:conn_write
conn_write(writer, "hello\nthere!\n")

# r2py:entity:poll_1
poll([reader], 1000)

# r2py:entity:conn_read_lines
conn_read_lines(reader, 1)

# r2py:entity:conn_read_chars
conn_read_chars(reader)

# r2py:entity:conn_is_incomplete
conn_is_incomplete(reader)

# r2py:entity:close
writer.close()

# r2py:entity:conn_read_chars_1
conn_read_chars(reader)

# r2py:entity:conn_is_incomplete_1
conn_is_incomplete(reader)

# r2py:entity:close_1
reader.close()