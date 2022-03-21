class Connection():
    """Wrapper class to encapsulate the Postgresql Database Url properties"""

    def __init__(self, username, password, host, port, database):
        self.Username = username
        self.Password = password
        self.Host = host
        self.Port = port
        self.Database = database
    
    @staticmethod
    def Map(url: str):
        """
            Maps a standard Postgresql connection* string to a usable set of properties

            *(postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...])
        """

        protocol = 'postgresql://'
        userspecPortion = url[protocol.rindex('/') - 1:url.rfind('@')]
        userspec = userspecPortion.split(':')
        username = userspec[0]
        password = userspec[1]
        networkLocationPortion = url[url.rfind('@') + 1:url.rfind('/')]
        networkLocation = networkLocationPortion.split(':')
        host = networkLocation[0]
        port = networkLocation[1]
        database = url[url.rfind('/') + 1:len(url)]

        return Connection(username, password, host, port, database)