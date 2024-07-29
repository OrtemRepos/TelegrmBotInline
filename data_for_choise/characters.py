import json
import random as rnd

class Charecter:
    def __init__(self, name, description, image, mask='<PERSON>'):
        self._name = name
        self._description = description
        self._image = image
        self._mask = mask
    
    def __str__(self) -> str:
        return self._name + self._mask + self._description + self._mask + self._image
    
    def serialize(self):
        return {
            "name": self._name,
            "description": self._description,
            "image": self._image
        }

class CharecterList:
    def __init__(self, name, charecters=[], description=None, image=None, mask='<LIST>') -> None:
        self._charecters = charecters
        self._name = name
        self._description = description
        self._image = image
        self._mask = mask
    
    def add_charecter(self, charecter: Charecter):
        self._charecters.append(charecter)
    
    def add_charecters(self, charecters: list[Charecter]):
        for charecter in charecters:
            self.add_charecter(charecter)
        
    def get_charecters(self):
        return self._charecters
    
    def serialize(self):
        dictonary = [charecter.serialize() for charecter in self._charecters]
        for_save = {"name": self._name, "charecters": dictonary, "description": self._description, "image": self._image}
        return for_save
    @classmethod
    def load_from_file(cls, path):
        with open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        charecters = []
        for charecter in data["charecters"]:
            charecters.append(Charecter(name=charecter["name"], description=charecter["description"], image=charecter["image"]))
        return cls(name=data["name"], charecters=charecters, description=data["description"], image=data["image"])

    
    def __str__(self) -> str:
        out = self._name + self._mask + self._description + self._mask + self._image
        return out
    
    def random_choise(self):
        return rnd.choice(self._charecters)
    
class ListChoise:
    def __init__(self, lists=[]) -> None:
        self._lists = lists
    
    @classmethod
    def load_from_file(cls, path):
        with open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        return cls([CharecterList(**charecter_list) for charecter_list in data])
    
    def get_lists(self):
        return [charecter_list for charecter_list in self._lists if charecter_list._charecters.__len__() > 0]
    def serialize(self, path):
        for_save = [charecter_list.serialize() for charecter_list in self._lists]
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(for_save, fp, indent=4)
    @classmethod
    def load_from_file(cls, path):
        with open(path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        charecter_lists = []
        for charecter_list in data:
            charecters = []
            for charecter in charecter_list["charecters"]:
                charecters.append(Charecter(name=charecter["name"], description=charecter["description"], image=charecter["image"]))
            charecter_lists.append(CharecterList(name=charecter_list["name"], charecters=charecters, description=charecter_list["description"], image=charecter_list["image"]))
        return cls(charecter_lists)


    def add_list(self, name, description=None, image=None):
        chr_list = CharecterList(name, description=description, image=image)
        self._lists.append(chr_list)
    
    def delete_list_by_name(self, name):
        id = self.get_charecter_list_by_name(name)
        self._lists.pop(id)

    def delete_charater_from_list(self, list_id, name):
        
        for charecter in self._lists[list_id]._charecters:
            if charecter._name == name:
                self._lists[list_id]._charecters.remove(charecter)

    def add_charecter_in_list_by_name(self, list_name, name, description=None, image=None):
        id = self.get_charecter_list_by_name(list_name)
        self._lists[id].add_charecter(Charecter(name=name, description=description, image=image))

    def rnd_character_in_list_by_name(self, list_name):
        chr_list = self.get_charecter_list_by_name(list_name)
        return self._lists[chr_list].random_choise()

    def get_charecter_list_by_name(self, name):
        for id in range(len(self._lists)):
            if self._lists[id]._name == name:
                return id
        else:
            raise Exception(f"List with name {name} not found")

    def __str__(self) -> str:
        out = ''
        for charecter_list in self._lists:
            out += str(charecter_list) + '\n'
        return out