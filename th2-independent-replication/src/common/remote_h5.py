"""Read a remote public-S3 h5ad over HTTPS byte-ranges (stdlib only) — no full download."""
import io, urllib.request

DE_STATS_URL = "https://genome-scale-tcell-perturb-seq.s3.amazonaws.com/marson2025_data/GWCD4i.DE_stats.h5ad"

class HTTPRangeFile(io.RawIOBase):
    def __init__(self, url):
        self.url = url
        r = urllib.request.urlopen(urllib.request.Request(url, method="HEAD"))
        self.size = int(r.headers["Content-Length"]); self.pos = 0
        self.n_reqs = 0; self.n_bytes = 0
    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos
    def tell(self): return self.pos
    def readable(self): return True
    def seekable(self): return True
    def readinto(self, b):
        end = min(self.pos + len(b) - 1, self.size - 1)
        if self.pos > end: return 0
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}"})
        data = urllib.request.urlopen(req).read()
        self.n_reqs += 1; self.n_bytes += len(data)
        b[:len(data)] = data; self.pos += len(data)
        return len(data)

def open_remote(url=DE_STATS_URL):
    import h5py
    f = HTTPRangeFile(url)
    return h5py.File(f, "r"), f
