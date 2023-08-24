import socket
import geoip2.database

class DNSCountry:
    def __init__(self, geoip_database_path):
        self.cache = {}
        self.reader = geoip2.database.Reader(geoip_database_path)

    def lookup(self, ip_address):
        country_code = self.get_country_code(ip_address)
        dns = socket.getfqdn(ip_address)

        if dns == ip_address:
            dns = "N/A"
            
        if country_code == None:
            country_code = "N/A"
            
        return dns, country_code

    def get_country_code(self, ip_address):
        try:
            response = self.reader.country(ip_address)
            return response.country.iso_code
        except geoip2.errors.AddressNotFoundError:
            return None

    def __del__(self):
        if hasattr(self, 'reader') and self.reader is not None:
            self.reader.close()

