"""
Landscape class for biosim

This class creates and applies function that
make up for the behavior for the landscapes.
So if animals can go there, how much vegetation, etc.

.. note:: All params for landscapes can be found under their class,
          as well as in the task file.

"""
from biosim.animals import Herbivore, Carnivore
import random as rd


class OneGrid:
    """
    Class describing individual cells of different landscape types.
    As well as storing animals and their params in the cell
    """
    def __init__(self, cord):
        """
        Initiates instance for one cell
        :param cord: the coordinates for the cell

        self.fodder: the amount of available fodder

        self.livable: checks whether an cell is livable or not

        self.population_herb: all herbivores in that cell

        self.population_carn: all carnivores in that cell

        self.population_sum_herb: number of herbivores in that cell

        self.population_sum_carn: number of carnivores in that cell
        """
        self.fodder = 0
        self.cord = cord
        self.livable = True
        self.population_herb = []
        self.population_carn = []
        self.population_sum_herb = None
        self.population_sum_carn = None

    def cell_set_params(cls, params):
        """
        Takes an dictionary of parameters and replaces default param

        :param params: dictionary containing f_max value
        """
        for parameter in params:
            if parameter in cls.params:
                cls.params[parameter] = params[parameter]

    def cell_add_population(self, population=None):
        """
        Adds a population to the landscape location, and turns it in to an animal object

        :param population: the population to add to the map
        :type population: is a dictionary containing location, and population for given location
        """
        if not self.livable:
            raise TypeError('Cannot add animals to water cell')
        else:
            for animal in population:
                if animal['species'] == 'Herbivore':
                    self.population_herb.append(Herbivore(animal['age'], animal['weight']))
                elif animal['species'] == 'Carnivore':
                    self.population_carn.append(Carnivore(animal['age'], animal['weight']))

    def cell_sum_of_animals(self):
        """
        Calculates the sum of herbivores and carnivores in the cell
        """
        self.population_sum_herb = len(self.population_herb)
        self.population_sum_carn = len(self.population_carn)

    def cell_calculate_fitness(self):
        """
        Uses the calculate fitness function from animals
        to calculate the fitness of each animal in cell
        """
        for animal in self.population_herb:
            animal.calculate_fitness()

        for animal in self.population_carn:
            animal.calculate_fitness()

    def cell_add_fodder(self):
        self.fodder = self.params['f_max']

    def cell_feeding_herbivore(self):
        """
        Herbivores in a cell eat in descending order of fitness.
        the eat a set amount of fodder every year
        """
        self.cell_calculate_fitness()
        self.population_herb.sort(key=lambda x: x.fitness, reverse=True)
        for herbivore in self.population_herb:
            if self.fodder == 0:
                break
            elif self.fodder >= herbivore.params['F']:
                herbivore.weight_gained_from_eating(herbivore.params['F'])
                self.fodder = self.fodder - herbivore.params['F']
            elif 0 < self.fodder < herbivore.params['F']:
                herbivore.weight_gained_from_eating(self.fodder)
                self.fodder = 0

    def cell_feeding_carnivore(self):
        """
        Uses the calculated probability from animals and lets each carnivore kill the herbivores
        if the herbivore is killed it is removed from the population before the next
        carnivore eats
        """
        self.cell_calculate_fitness()
        self.population_herb.sort(key=lambda x: x.fitness, reverse=True)

        rd.shuffle(self.population_carn)
        for predator in self.population_carn:
            appetite = predator.params['F']
            amount_eaten = 0

            for prey in self.population_herb:
                prob = predator.carnivore_kill_prob(prey)
                if rd.random() < prob:
                    fodder = prey.weight
                    if amount_eaten + fodder < appetite:
                        prey.is_dead = True
                        predator.weight_gained_from_eating(fodder)
                        amount_eaten += fodder
                    elif amount_eaten + fodder > appetite:
                        prey.is_dead = True
                        fodder = appetite - amount_eaten
                        predator.weight_gained_from_eating(fodder)
                        break
                    elif amount_eaten + fodder == appetite:
                        prey.is_dead = True
                        predator.weight_gained_from_eating(fodder)
                        break
                    predator.calculate_fitness()
            population_herb = [herb for herb in self.population_herb if herb.is_dead is False]
            self.population_herb = population_herb

    def cell_procreation(self):
        """
        Uses calculation to figure out if an animal receives a child or not.
        there has to be at least two of the same species to get children.
        animals can max get one children each year
        """
        self.cell_sum_of_animals()
        new_born_herbs = []
        num_herb = self.population_sum_herb
        for herb in self.population_herb:
            new_born_herb = herb.birth(num_herb)
            if new_born_herb is not None:
                new_born_herbs.append(new_born_herb)
            num_herb -= 1
        self.population_herb += new_born_herbs

        new_born_carns = []
        num_carn = self.population_sum_carn
        for carn in self.population_carn:
            new_born_carn = carn.birth(num_carn, species='carn')
            if new_born_carn is not None:
                new_born_carns.append(new_born_carn)
            num_carn -= 1
        self.population_carn += new_born_carns

    def cell_migration(self):
        """
        Check witch animal shall move and which shall stay
        """
        for herb in self.population_herb:
            herb.migrate()

        for carn in self.population_carn:
            carn.migrate()

    def cell_migration_remove(self):
        """
        Removes animals from their previous place to
        so that animals dont get duplicated
        """
        population_herb = [herb for herb in self.population_herb if herb.has_migrated is False]
        self.population_herb = population_herb

        population_carn = [carn for carn in self.population_carn if carn.has_migrated is False]
        self.population_carn = population_carn

    def cell_aging(self):
        """
        At birth, each animal has age a = 0 .
        age increases by one year for each year that passes
        """
        for animal in self.population_herb:
            animal.grow_one_year()
            animal.has_migrated = False

        for animal in self.population_carn:
            animal.grow_one_year()
            animal.has_migrated = False

    def cell_weight_lost(self):
        """
        Calculates the weight lost by all animals in cell
        """
        if self.population_herb is not None:
            for herb in self.population_herb:
                herb.lose_weight()

        if self.population_carn is not None:
            for carn in self.population_carn:
                carn.lose_weight()

    def cell_death(self):
        """
        This func kills and removes both carnivores and herbivores in each cell
        """
        for herb in self.population_herb:
            herb.death()

        for carn in self.population_carn:
            carn.death()

        population_herb = [herb for herb in self.population_herb if herb.is_dead is False]
        self.population_herb = population_herb

        population_carn = [carn for carn in self.population_carn if carn.is_dead is False]
        self.population_carn = population_carn

    def cell_age_weight_and_fitness(self):
        """
        Adds the age weight and fitness for each of the animals into dictionary with list as value
        """
        herb_age_weight_fitness = {
            'age': [],
            'weight': [],
            'fitness': []
        }

        carn_age_weight_fitness = {
            'age': [],
            'weight': [],
            'fitness': []

        }

        for herb in self.population_herb:
            herb_age_weight_fitness['age'].append(herb.age)
            herb_age_weight_fitness['weight'].append(herb.weight)
            herb_age_weight_fitness['fitness'].append(herb.fitness)

        for carn in self.population_carn:
            carn_age_weight_fitness['age'].append(carn.age)
            carn_age_weight_fitness['weight'].append(carn.weight)
            carn_age_weight_fitness['fitness'].append(carn.fitness)

        return herb_age_weight_fitness, carn_age_weight_fitness


class Lowland(OneGrid):
    """
    lowland subclass

    params = {'f_max': 800}
    """
    params = {
        'f_max': 800
    }

    def __init__(self, cord=None):
        super().__init__(cord)
        self.fodder = 0
        self.livable = True

    def __repr__(self):
        return f'Lowland,Food:{self.fodder},Total animals:{self.population_sum_carn + self.population_sum_herb}'


class Highland(OneGrid):
    """
    highland subclass

    params = {'f_max': 300}
    """
    params = {
        'f_max': 300
    }

    def __init__(self, cord=None):
        super().__init__(cord)
        self.fodder = 0
        self.livable = True

    def __repr__(self):
        return f'Highland,Food:{self.fodder},Total animals:{self.population_sum_carn + self.population_sum_herb}'


class Dessert(OneGrid):
    """
    dessert subclass

    params = {'f_max': 0}
    """
    params = {
        'f_max': 0
    }

    def __init__(self, cord=None):
        super().__init__(cord)
        self.fodder = 0
        self.livable = True

    def __repr__(self):
        return f'Dessert,Food:{self.fodder},Total animals:{self.population_sum_herb + self.population_sum_carn}'


class Water(OneGrid):
    """
    water subclass

    params = {'f_max': 0}
    """
    params = {
        'f_max': 0
    }

    def __init__(self, cord=None):
        super().__init__(cord)
        self.fodder = 0
        self.livable = False

    def __repr__(self):
        return f'Water,Food:{self.fodder},Uninhabitable'
