
class KeyValueStore:

    def __init__(self):
        self.keys_set = set()
        self.keys_dict = dict()

    def put(self, key, value):
        print('Message received with the key: ' + key)
        self.keys_set.add(key)
        self.keys_dict[key] = value
        return True

    def get(self, key):
        if key not in self.keys_set:
            return "failed", False
        return self.keys_dict[key],True

    def doCommit(self, key, value):
        self.keys_set.add(key)
        self.keys_dict[key] = value
        return True
    
    def askVote(self,key):
        if key not in self.keys_set:
            return "failed"
        return self.keys_dict[key]
    
    def addSlave(self,port):
        return True


store_service = KeyValueStore()
