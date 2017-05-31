class Cache:
    def __init__(self):
        self.cache = {}

    # end init

    def clear(self):
        self.cache.clear()

    # end clear

    def add(self, key, server_id):
        self.cache[key] = server_id

    # end add

    def get(self, key):
        return self.cache[key]

        # end get

# end Cache
