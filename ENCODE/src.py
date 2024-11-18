import random
import pymongo
import certifi
import string

ca = certifi.where()


class ENCODE:
    def __init__(self):
        pass

    def create_key_square(self, key: str):
        key = "".join(dict.fromkeys(key.replace("j", "i").lower()))  # Remove duplicates
        alphabets = "abcdefghiklmnopqrstuvwxyz"  # Exclude 'j'
        key_square = key + "".join([ch for ch in alphabets if ch not in key])
        return [key_square[i:i+5] for i in range(0, 25, 5)]

    def find_position(self, char, key_square):
        for i, row in enumerate(key_square):
            if char in row:
                return i, row.index(char)
        return None

    def playfair_encrypt(self, plaintext: str, key_square):
        plaintext = plaintext.lower().replace("j", "i").replace(" ", "")
        if len(plaintext) % 2 != 0:
            plaintext += 'x'  # Padding for odd-length

        encrypted = []
        for i in range(0, len(plaintext), 2):
            a, b = plaintext[i], plaintext[i+1]
            row1, col1 = self.find_position(a, key_square)
            row2, col2 = self.find_position(b, key_square)

            if row1 == row2:  # Same row
                encrypted.append(key_square[row1][(col1 + 1) % 5])
                encrypted.append(key_square[row2][(col2 + 1) % 5])
            elif col1 == col2:  # Same column
                encrypted.append(key_square[(row1 + 1) % 5][col1])
                encrypted.append(key_square[(row2 + 1) % 5][col2])
            else:  # Rectangle swap
                encrypted.append(key_square[row1][col2])
                encrypted.append(key_square[row2][col1])

        return ''.join(encrypted)

    def playfair_decrypt(self, ciphertext: str, key_square):
        decrypted = []
        for i in range(0, len(ciphertext), 2):
            a, b = ciphertext[i], ciphertext[i+1]
            row1, col1 = self.find_position(a, key_square)
            row2, col2 = self.find_position(b, key_square)

            if row1 == row2:  # Same row
                decrypted.append(key_square[row1][(col1 - 1) % 5])
                decrypted.append(key_square[row2][(col2 - 1) % 5])
            elif col1 == col2:  # Same column
                decrypted.append(key_square[(row1 - 1) % 5][col1])
                decrypted.append(key_square[(row2 - 1) % 5][col2])
            else:  # Rectangle swap
                decrypted.append(key_square[row1][col2])
                decrypted.append(key_square[row2][col1])

        return ''.join(decrypted)

    def scramble(self, para: str, seed: str) -> str:
        key_square = self.create_key_square(seed)
        return self.playfair_encrypt(para, key_square)

    def unscramble(self, scrambled_para: str, seed: str) -> str:
        key_square = self.create_key_square(seed)
        return self.playfair_decrypt(scrambled_para, key_square)


class MongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.duyrx.mongodb.net/web-paralocker?retryWrites=true&w=majority", tlsCAFile=ca)
        self.db = self.client["paralocker"]
        self.coll = self.db["main"]

    def insert(self, data: dict):
        try:
            return self.coll.insert_one(data).inserted_id
        except Exception as e:
            print(f"Error inserting data: {e}")
            return None

    def find(self, query: dict):
        try:
            return self.coll.find_one(query)
        except Exception as e:
            print(f"Error finding data: {e}")
            return None

    def delete_all(self):
        try:
            result = self.coll.delete_many({})
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting data: {e}")
            return None


def main():
    # MongoDB setup
    connection_uri = "mongodb+srv://admin:admin@cluster0.duyrx.mongodb.net/web-paralocker?retryWrites=true&w=majority"
    database = "paralocker"
    collection = "main"
    mongo_db = MongoDB(connection_uri, database, collection)

    # Clear the database collection
    # deleted_count = mongo_db.delete_all()
    # print(f"Deleted {deleted_count} documents from the collection.")
