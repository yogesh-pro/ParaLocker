import random
import pymongo
import certifi
ca = certifi.where()

class ENCODE:
    def __init__(self) -> None:
        self.alphabets = [chr(x) for x in range(97,122)]
    
    def scramble(self,para:None,seed):
        para_lis = [*para]
        random.seed(str(seed))
        random.shuffle(para_lis)
        return "".join(para_lis)


    #function that unshuffle 
    def unscramble(self,shuffled_para:None,seed):
        random.seed(str(seed))
        n = len(shuffled_para)
        perm = [i for i in range(1,n+1)]
        shuffled_para = [*shuffled_para]
        random.shuffle(perm)
        zipped_ls = list(zip(shuffled_para,perm))
        zipped_ls.sort(key=lambda x: x[1])
        _lis =  [a for (a, b) in zipped_ls]
        final = "".join(_lis)
        return final


    def alter(self,para:None,seed:None):
        random.seed(str(seed))
        para = self.scramble(self,para,seed)
        para_lis = [*para]
        for i in range(len(para_lis)):
            para_lis[i] = chr(ord(para_lis[i]) + 3)
        return "".join(para_lis)

    #a function that returns original character every time
    def revert(self,para:None,seed:None):
        random.seed(str(seed))
        para = self.unscramble(self,para,seed)
        para_lis = [*para]
        random.seed(str(seed))
        for i in range(len(para_lis)):
            para_lis[i] = chr(ord(para_lis[i]) - 3)
        return "".join(para_lis)


class MongoDB:
    def __init__(self) -> None:
        pass
    
    
    def insert(self,_dict:None):
        client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.duyrx.mongodb.net/web-paralocker?retryWrites=true&w=majority", tlsCAFile=ca)
        db = client['paralocker']
        coll = db['main']
        return coll.insert_one(_dict)
    
    def find(self,url:None):
        client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.duyrx.mongodb.net/web-paralocker?retryWrites=true&w=majority", tlsCAFile=ca)
        db = client['paralocker']
        coll = db['main']
        # data = [x for x in coll.find_one({},{"url":url})]
        data = coll.find_one({"url":url})
        return data


def main(ca):
    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.duyrx.mongodb.net/web-paralocker?retryWrites=true&w=majority", tlsCAFile=ca)
    db = client['paralocker']
    coll = db['main']
    coll.delete_many({})

