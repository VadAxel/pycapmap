import socket

class DNSCache:
    def __init__(self):
        self.cache = {}
    
    def lookup(self, ipa):
        name = self.cache.get(ipa, None)
        if name is None:
            name = socket.getfqdn(ipa)
            self.cache[ipa] = name
        return name