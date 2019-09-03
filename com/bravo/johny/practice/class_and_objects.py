class tree :
    name = ""
    fruit = ""

    def fruit_name(self):
        print(self.name+" gives : "+self.fruit)

mango = tree()
mango.name = "Mango Tree"
mango.fruit = "Mango"

mango.fruit_name()
