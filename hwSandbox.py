import requests
#from IPython.display import Image

# recreate your pokemon class here
class Encounter_Pokemon():

    def __init__(self, name):
        self.name = name
        self.abilities = []
        self.types = []
        self.weight = None
        self.image = None
        self.pokenum = None

    def throw_pokeball(self):
        catch_attempt = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.name}')
        if catch_attempt.status_code == 200:
            print('Pokemon successfully caught')
            data = catch_attempt.json()
            self.name = data["name"] # this will allow for passing in either a full name or an integer index during the prior API call
            self.weight = data["weight"]
            self.abilities = [this_ability["ability"]["name"] for this_ability in data["abilities"]]
            self.types = [this_type["type"]["name"] for this_type in data["types"]]
            self.image = data["sprites"]['front_default']
            self.pokenum = data["id"]
        else:
            print(f'Error, status code {catch_attempt.status_code}')
        
    def successful_evolution(self):
        evo_attempt = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.name}')
        if evo_attempt.status_code == 200:
            print('Bum dum bum dum bum dum baaaa')
            data = evo_attempt.json()
            self.name = data["name"] # this will allow for passing in either a full name or an integer index during the prior API call
            self.weight = data["weight"]
            self.abilities = [this_ability["ability"]["name"] for this_ability in data["abilities"]]
            self.types = [this_type["type"]["name"] for this_type in data["types"]]
            self.image = data["sprites"]['front_default']
            self.pokenum = data["id"]
        else:
            print(f'Error on retrieving evolution info, status code {evo_attempt.status_code}')
            
    def i_choose_you(self):
        display(Image(self.image, width = 100))
        
    def wants_to_evolve(self):
        get_evo_data = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{self.pokenum}/')
        if get_evo_data.status_code == 200:
            print(f'{self.name} wants ...')
            tempData = get_evo_data.json()
            self.find_evo_data(tempData["evolution_chain"]["url"])
        else:
            print(f'Error on species page retrieval, status code {get_evo_data.status_code}')

    def find_evo_data(self, found_url):
        get_evo_data = requests.get(found_url)
        if get_evo_data.status_code == 200:
            print("...to evolve!")
            self.try_to_evolve(get_evo_data.json())
        else:
            print(f'Error on evo chain retrieval, status code {get_evo_data.status_code}')

    # I'm going to do the original max 2 evolutions. I know there are baby pokemon now, and super
    # evolutions, and so on, so I'm not sure what the maximum total possible evolutions are from
    # like baby to something special, probably 4? This is proof of concept anyway. Traversing
    # the chain 4 levels seems obnoxious. I'd love to hear the more pythony way to do this, though.
    # Should I be making a traverse_chain() method?
    def try_to_evolve(self, evo_data):
        # pokemon is bottom level, goes to next level if next level exists
        if self.name == evo_data["chain"]["species"]["name"]:
            # if next level exists:
            if evo_data["chain"]["evolves_to"]:
                self.oldName = self.name
                self.name = evo_data["chain"]["evolves_to"][0]["species"]["name"]
                self.successful_evolution()
                print(f'Congratulations, your {self.oldName} evolved into {self.name}')
            else:
                print(f"Sorry, your {self.name} can't evolve any further.")
        # pokemon is middle level, goes to next level if next level exists
        elif self.name == evo_data["chain"]["evolves_to"][0]["species"]["name"]:
            # if next level exists:
            if evo_data["chain"]["evolves_to"][0]["evolves_to"]:
                self.oldName = self.name
                self.name = evo_data["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
                self.successful_evolution()
                print(f'Congratulations, your {self.oldName} evolved into {self.name}')
            else:
                print(f"Sorry, your {self.name} can't evolve any further.")
        # we'll assume there are at most three evolutions for now, I see we could go deeper, I'm
        # sure there's way more efficient code out there for doing all this
        else:
            print(f"Sorry, your {self.name} can't evolve any further.")
        

my_pokemon = Encounter_Pokemon('gastly')
my_pokemon.throw_pokeball()
print(my_pokemon.name)
print("pokemon num: ",my_pokemon.pokenum)
print("abilities: ",my_pokemon.abilities)
my_pokemon.wants_to_evolve()
print(my_pokemon.name)
print("pokemon num: ",my_pokemon.pokenum)
print("abilities: ",my_pokemon.abilities)
my_pokemon.wants_to_evolve()
print(my_pokemon.name)
print("pokemon num: ",my_pokemon.pokenum)
print("abilities: ",my_pokemon.abilities)
my_pokemon.wants_to_evolve()

my_pokemon = Encounter_Pokemon('moltres')
my_pokemon.throw_pokeball()
my_pokemon.wants_to_evolve()