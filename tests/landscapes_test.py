from biosim.landscapes import Lowland, Highland, Dessert, Water
import pytest


@pytest.mark.parametrize('class_with_animals', [Lowland, Highland, Dessert])
class TestAnimalLandscapes:
    """
    This class test all land types witch support animals and have the same behavior
    """
    params_herb = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'phi_age': 0.6,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10
    }

    params_carn = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 40.0,
        'phi_age': 0.3,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.8,
        'F': 50,
        'DeltaPhiMax': 10
    }

    def add_animals(self, class_with_animals, animals_nr_herb=20, animals_weight_herb=20, animals_age_herb=5,
                    animals_nr_carn=20, animals_weight_carn=20, animals_age_carn=5):
        """
        Easy way to add animals in all tests
        :param class_with_animals: classes that are livable
        :param animals_nr_herb: the start number of herbivore
        :param animals_weight_herb: the start weight of herbivore
        :param animals_age_herb: the start age of herbivore
        :param animals_nr_carn: the start number for carnivore
        :param animals_weight_carn:the start weight of carnivore
        :param animals_age_carn:the start age of carnivore
        :return:
        """
        self.animals_nr_herb = animals_nr_herb
        self.animals_weight_herb = animals_weight_herb
        self.animals_age_herb = animals_age_herb
        self.animals_nr_carn = animals_nr_carn
        self.animals_weight_carn = animals_weight_carn
        self.animals_age_carn = animals_age_carn
        self.herb_list = [{'species': 'Herbivore', 'age': self.animals_age_herb, 'weight': self.animals_weight_herb}
                          for _ in range(self.animals_nr_herb)]
        self.carn_list = [{'species': 'Carnivore', 'age': self.animals_age_carn, 'weight': self.animals_weight_carn}
                          for _ in range(self.animals_nr_carn)]

        landscapes_with_animals = class_with_animals
        landscapes_with_animals.cell_add_population(self.herb_list)
        landscapes_with_animals.cell_add_population(self.carn_list)
        landscapes_with_animals.cell_sum_of_animals()

    def test_add_population_herbivores(self, class_with_animals):
        """
        Test that adding animals works in all cells with herbivores.
        :param class_with_animals: All the landscapes that are livable
        """
        landscapes_with_animals = class_with_animals()

        start_population_herb = landscapes_with_animals.population_sum_herb
        self.add_animals(landscapes_with_animals)
        end_population_herb = landscapes_with_animals.population_sum_herb
        assert start_population_herb is None
        assert end_population_herb == self.animals_nr_herb

    def test_add_population_carnivores(self, class_with_animals):
        """
        Test that adding animals works in all cells with carnivores.
        :param class_with_animals: All the landscapes that are livable
        """
        landscapes_with_animals = class_with_animals()

        start_population_carn = landscapes_with_animals.population_sum_carn
        self.add_animals(landscapes_with_animals)
        end_population_carn = landscapes_with_animals.population_sum_carn
        assert start_population_carn is None
        assert end_population_carn == self.animals_nr_carn

    def test_aging_herbivore(self, class_with_animals):
        """
        Test that herbivore age, once per called upon
        :param class_with_animals: All the landscapes that are livable
        """
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals)

        total_age_before_herb = 0
        for animal in landscapes_with_animals.population_herb:
            total_age_before_herb += animal.age
        average_age_before_herb = total_age_before_herb / self.animals_nr_herb

        _nr_years = 2
        for _ in range(_nr_years):
            landscapes_with_animals.cell_aging()

        total_age_after_herb = 0
        for animal in landscapes_with_animals.population_herb:
            total_age_after_herb += animal.age
        average_age_after_herb = total_age_after_herb / self.animals_nr_herb

        assert average_age_before_herb == self.animals_age_herb
        assert average_age_after_herb == self.animals_age_herb + _nr_years

    def test_aging_carnivore(self, class_with_animals):
        """
        Test that carnivore age, once per called upon
        :param class_with_animals: All the landscapes that are livable
        """
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals)

        total_age_before_carn = 0
        for animal in landscapes_with_animals.population_carn:
            total_age_before_carn += animal.age
        average_age_before_carn = total_age_before_carn / self.animals_nr_carn

        _nr_years = 2
        for _ in range(_nr_years):
            landscapes_with_animals.cell_aging()

        total_age_after_carn = 0
        for animal in landscapes_with_animals.population_carn:
            total_age_after_carn += animal.age
        average_age_after_carn = total_age_after_carn / self.animals_nr_carn

        assert average_age_before_carn == self.animals_age_carn
        assert average_age_after_carn == self.animals_age_carn + _nr_years

    def test_death_herbivore(self, class_with_animals):
        """
        Test that when herbivore die, they get removed.
        Animals die with certain when weight = 0
        :param class_with_animals: All the landscapes that are livable
        """
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_weight_herb=0, animals_weight_carn=0)

        start_population_herb = landscapes_with_animals.population_sum_herb
        landscapes_with_animals.cell_death()
        landscapes_with_animals.cell_sum_of_animals()
        end_population_herb = landscapes_with_animals.population_sum_herb

        assert start_population_herb == self.animals_nr_herb
        assert end_population_herb == 0

    def test_death_carnivore(self, class_with_animals):
        """
        Test that when carnivore die, they get removed.
        Animals die with certain when weight = 0
        :param class_with_animals: All the landscapes that are livable
        """
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_weight_herb=0, animals_weight_carn=0)

        start_population_carn = landscapes_with_animals.population_sum_carn
        landscapes_with_animals.cell_death()
        landscapes_with_animals.cell_sum_of_animals()
        end_population_carn = landscapes_with_animals.population_sum_carn

        assert start_population_carn == self.animals_nr_carn
        assert end_population_carn == 0

    def test_procreation_max_herbivore(self, class_with_animals, mocker):
        """
        Test that if there are more than one animal, the number of animals will increase.
        Here all animals will get a child except the last one "the male".
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        :return:
        """
        mocker.patch('random.random', return_value=0)  # Sett the prob, so its guaranteed they get children
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_weight_herb=50, animals_weight_carn=50)
        # Setts a high weight, because if it is to low the mother cant give birth

        start_population_herb = landscapes_with_animals.population_sum_herb
        landscapes_with_animals.cell_procreation()
        landscapes_with_animals.cell_sum_of_animals()
        end_population_herb = landscapes_with_animals.population_sum_herb

        assert start_population_herb == self.animals_nr_herb
        assert end_population_herb == self.animals_nr_herb*2 - 1  # There has to be one "male" that can't give birth

    def test_procreation_max_carnivore(self, class_with_animals, mocker):
        """
        Test that if there are more than one animal, the number of animals will increase.
        Here all animals will get a child except the last one "the male".
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        :return:
        """
        mocker.patch('random.random', return_value=0)  # Sett the prob, so its guaranteed they get children
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_weight_herb=50, animals_weight_carn=50)
        # Setts a high weight, because if it is to low the mother cant give birth

        start_population_carn = landscapes_with_animals.population_sum_carn
        landscapes_with_animals.cell_procreation()
        landscapes_with_animals.cell_sum_of_animals()
        end_population_carn = landscapes_with_animals.population_sum_carn

        assert start_population_carn == self.animals_nr_carn
        assert end_population_carn == self.animals_nr_carn*2 - 1  # There has to be one "male" that can't give birth

    def test_procreation_min_herbivore(self, class_with_animals, mocker):
        """
        Test that if the prob for getting children is 0. That no animals are added
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        :return:
        """
        mocker.patch('random.random', return_value=1)  # Sett the prob, so its guaranteed they dont get children
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_weight_herb=50, animals_weight_carn=50)
        # Setts a high weight, because if it is to low the mother cant give birth

        start_population_herb = landscapes_with_animals.population_sum_herb
        landscapes_with_animals.cell_procreation()
        landscapes_with_animals.cell_sum_of_animals()
        end_population_herb = landscapes_with_animals.population_sum_herb

        assert start_population_herb == self.animals_nr_herb
        assert end_population_herb == self.animals_nr_herb

    def test_procreation_min_carnivore(self, class_with_animals, mocker):
        """
        Test that if the prob for getting children is 0. That no animals are added
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        :return:
        """
        mocker.patch('random.random', return_value=1)  # Sett the prob, so its guaranteed they dont get children
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_weight_herb=50, animals_weight_carn=50)
        # Setts a high weight, because if it is to low the mother cant give birth

        start_population_carn = landscapes_with_animals.population_sum_carn
        landscapes_with_animals.cell_procreation()
        landscapes_with_animals.cell_sum_of_animals()
        end_population_carn = landscapes_with_animals.population_sum_carn

        assert start_population_carn == self.animals_nr_carn
        assert end_population_carn == self.animals_nr_carn

    def test_carnivore_kills_herb_prob_max(self, class_with_animals, mocker):
        """
        Test that if the kill prob is true. The herbivores are killed and removed
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        :return:
        """
        mocker.patch('random.random', return_value=0)
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_age_herb=40, animals_weight_herb=1, animals_weight_carn=50)
        # Sett high age and low weight, so the fitness on herb is low.

        start_population_herb = landscapes_with_animals.population_sum_herb
        landscapes_with_animals.cell_feeding_carnivore()
        landscapes_with_animals.cell_sum_of_animals()
        end_population_herb = landscapes_with_animals.population_sum_herb

        assert start_population_herb == self.animals_nr_herb
        assert end_population_herb == 0

    def test_carnivore_kill_herb_prob_min(self, class_with_animals, mocker):
        """
        Test that if the kill prob is False. The herbivores are not killed nor removed
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        :return:
        """
        mocker.patch('random.random', return_value=1)
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_age_herb=40, animals_weight_herb=1, animals_weight_carn=50)
        # Sett high age and low weight, so the fitness on herb is low.

        start_population_herb = landscapes_with_animals.population_sum_herb
        landscapes_with_animals.cell_feeding_carnivore()
        landscapes_with_animals.cell_sum_of_animals()
        end_population_herb = landscapes_with_animals.population_sum_herb

        assert start_population_herb == self.animals_nr_herb
        assert end_population_herb == self.animals_nr_herb

    def test_carnivore_eat_amount(self, class_with_animals, mocker):
        """
        Test that carnivores feed and
        carnivores gain weight.
        Checks the average weight, so if just one animal has another value
        we will know
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        :return:
        """
        mocker.patch('random.random', return_value=0)
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals, animals_age_herb=40, animals_weight_herb=1, animals_weight_carn=50)

        total_weight_before_eat = 0
        for animal in landscapes_with_animals.population_carn:
            total_weight_before_eat += animal.weight
        average_weight_before_eat = total_weight_before_eat / self.animals_nr_carn

        landscapes_with_animals.cell_feeding_carnivore()
        landscapes_with_animals.cell_sum_of_animals()

        total_weight_after_eat = 0
        for animal in landscapes_with_animals.population_carn:
            total_weight_after_eat += animal.weight
        average_weight_after_eat = total_weight_after_eat / self.animals_nr_carn

        assert average_weight_before_eat == self.animals_weight_carn
        assert average_weight_after_eat == self.animals_weight_carn + \
               self.params_carn['beta'] * self.animals_weight_herb

    def test_migration_prob_max(self, class_with_animals, mocker):
        """
        Test that the migration works.
        From the task, and the fitness formula, we kan calculate that with the sett weight and age value
        the migration value is calculated: fitness * mu = 0.182765.
        So any random value lower, vil make all animals migrate, anything over vil stop all animals from migrating
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        :return:
        """
        mocker.patch('random.random', return_value=0)
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals)

        landscapes_with_animals.cell_migration()
        animals_migrating = 0
        animals_not_migrating = 0
        for animal in landscapes_with_animals.population_herb:
            if animal.has_migrated is True:
                animals_migrating += 1
            else:
                animals_not_migrating += 1

        for animal in landscapes_with_animals.population_carn:
            if animal.has_migrated is True:
                animals_migrating += 1
            else:
                animals_not_migrating += 1

        landscapes_with_animals.cell_sum_of_animals()
        landscapes_with_animals.cell_migration_remove()
        landscapes_with_animals.cell_sum_of_animals()

        assert animals_migrating == self.animals_nr_herb + self.animals_nr_carn
        assert animals_not_migrating == (self.animals_nr_herb + self.animals_nr_carn) - animals_migrating
        assert landscapes_with_animals.population_sum_herb + landscapes_with_animals.population_sum_carn == 0

    def test_migration_prob_zero(self, class_with_animals, mocker):
        """
        Test that the migration works
        :param class_with_animals: All the landscapes that are livable
        :param mocker: Lets us control random value
        """
        mocker.patch('random.random', return_value=10)
        landscapes_with_animals = class_with_animals()
        self.add_animals(landscapes_with_animals)

        landscapes_with_animals.cell_migration()
        animals_migrating = 0
        animals_not_migrating = 0
        for animal in landscapes_with_animals.population_herb:
            if animal.has_migrated is True:
                animals_migrating += 1
            else:
                animals_not_migrating += 1

        for animal in landscapes_with_animals.population_carn:
            if animal.has_migrated is True:
                animals_migrating += 1
            else:
                animals_not_migrating += 1

        landscapes_with_animals.cell_sum_of_animals()
        landscapes_with_animals.cell_migration_remove()
        landscapes_with_animals.cell_sum_of_animals()

        assert animals_migrating == 0
        assert animals_not_migrating == (self.animals_nr_herb + self.animals_nr_carn) - animals_migrating
        assert landscapes_with_animals.population_sum_herb == self.animals_nr_herb
        assert landscapes_with_animals.population_sum_carn == self.animals_nr_carn


@pytest.mark.parametrize('class_with_fodder', [Highland, Lowland])
class TestFodderLandscapes:
    """
    Test the two classes that have fodder
    """
    params_herb = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'phi_age': 0.6,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10
    }

    params_carn = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 40.0,
        'phi_age': 0.3,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.8,
        'F': 50,
        'DeltaPhiMax': 10
    }

    def add_animals(self, class_with_fodder, animals_nr_herb=20, animals_weight_herb=20, animals_age_herb=5,
                    animals_nr_carn=20, animals_weight_carn=20, animals_age_carn=5):
        """
        Easy way to add animals in all tests
        :param class_with_fodder: classes that are livable
        :param animals_nr_herb: the start number of herbivore
        :param animals_weight_herb: the start weight of herbivore
        :param animals_age_herb: the age weight of herbivore
        :param animals_nr_carn: the start number for carnivore
        :param animals_weight_carn:the start weight of carnivore
        :param animals_age_carn:the age weight of carnivore
        :return:
        """
        self.animals_nr_herb = animals_nr_herb
        self.animals_weight_herb = animals_weight_herb
        self.animals_age_herb = animals_age_herb
        self.animals_nr_carn = animals_nr_carn
        self.animals_weight_carn = animals_weight_carn
        self.animals_age_carn = animals_age_carn
        self.herb_list = [{'species': 'Herbivore', 'age': self.animals_age_herb, 'weight': self.animals_weight_herb}
                          for _ in range(self.animals_nr_herb)]
        self.carn_list = [{'species': 'Carnivore', 'age': self.animals_age_carn, 'weight': self.animals_weight_carn}
                          for _ in range(self.animals_nr_carn)]

        landscapes_with_fodder = class_with_fodder
        landscapes_with_fodder.cell_add_population(self.herb_list)
        landscapes_with_fodder.cell_add_population(self.carn_list)
        landscapes_with_fodder.cell_sum_of_animals()

    def test_feeding_herb(self, class_with_fodder):
        """
        Test that herbivores gain weight when eating
        :param class_with_fodder: All classes that have available fodder
        """
        landscapes_with_fodder = class_with_fodder()
        self.add_animals(landscapes_with_fodder)

        total_weight_before = 0
        for animal in landscapes_with_fodder.population_herb:
            total_weight_before += animal.weight
        average_weight_before_eat = total_weight_before / self.animals_nr_herb

        landscapes_with_fodder.cell_add_fodder()
        landscapes_with_fodder.cell_feeding_herbivore()

        total_weight_after = 0
        for animal in landscapes_with_fodder.population_herb:
            total_weight_after += animal.weight
        average_weight_after_eat = total_weight_after / self.animals_nr_herb

        assert average_weight_before_eat == self.animals_weight_herb
        assert average_weight_after_eat == self.animals_weight_herb + self.params_herb['F'] * self.params_herb['beta']

    def test_regrowth(self, class_with_fodder):
        """
        Test that regrowth works in right cells
        :param class_with_fodder: All classes that have available fodder
        """
        landscapes_with_fodder = class_with_fodder()
        self.add_animals(landscapes_with_fodder)

        landscapes_with_animals_fodder_before = landscapes_with_fodder.fodder
        landscapes_with_fodder.cell_add_fodder()
        landscapes_with_animals_fodder_before_eating = landscapes_with_fodder.fodder
        landscapes_with_fodder.cell_feeding_herbivore()
        landscapes_with_animals_fodder_after_eating = landscapes_with_fodder.fodder
        landscapes_with_fodder.cell_add_fodder()
        landscapes_with_animals_fodder_regrows = landscapes_with_fodder.fodder

        assert landscapes_with_animals_fodder_before == 0
        assert landscapes_with_animals_fodder_before_eating == landscapes_with_fodder.params['f_max']
        assert landscapes_with_animals_fodder_after_eating == landscapes_with_fodder.params['f_max'] - \
               (self.animals_nr_herb * self.params_herb['F'])
        assert landscapes_with_animals_fodder_regrows == landscapes_with_fodder.params['f_max']

    def test_feed_with_fitness_order(self, class_with_fodder):
        """
        Test that they feed by fitness order.
        Adds two animals with different fitness
        :param class_with_fodder: All classes that have available fodder
        :return:
        """

        landscapes_with_fodder = class_with_fodder()
        landscapes_with_fodder.params['f_max'] = 20
        start_weight_high_fitness = 50
        start_age_high_fitness = 1
        nr_herbs = 2
        start_weight_low_fitness = 1
        start_age_low_fitness = 50
        self.add_animals(landscapes_with_fodder,
                         animals_nr_herb=nr_herbs,  # Fitness around 0.98
                         animals_age_herb=start_age_high_fitness,
                         animals_weight_herb=start_weight_high_fitness)
        self.add_animals(landscapes_with_fodder,
                         animals_nr_herb=nr_herbs,  # Fitness around 0.001
                         animals_age_herb=start_age_low_fitness,
                         animals_weight_herb=start_weight_low_fitness)

        landscapes_with_fodder.cell_add_fodder()
        landscapes_with_fodder.cell_feeding_herbivore()
        landscapes_with_fodder.cell_sum_of_animals()

        for animal in landscapes_with_fodder.population_herb:
            if animal.fitness > 0.5:  # The animal with high fitness will gain weight
                assert animal.weight == start_weight_high_fitness + (self.params_herb['F'] * self.params_herb['beta'])
            else:  # The animal with low fitness stay the same
                assert animal.weight == 1

        Lowland.params['f_max'] = 800
        Highland.params['f_max'] = 300


@pytest.mark.parametrize('class_dessert', [Dessert])
class TestDessert:
    """
    Test the dessert landscape
    """
    def add_animals(self, class_dessert, animals_nr_herb=20, animals_weight_herb=20, animals_age_herb=5,
                    animals_nr_carn=20, animals_weight_carn=20, animals_age_carn=5):
        """
        Easy way to add animals in all tests
        :param class_dessert: classes that are livable
        :param animals_nr_herb: the start number of herbivore
        :param animals_weight_herb: the start weight of herbivore
        :param animals_age_herb: the age weight of herbivore
        :param animals_nr_carn: the start number for carnivore
        :param animals_weight_carn:the start weight of carnivore
        :param animals_age_carn:the age weight of carnivore
        :return:
        """
        self.animals_nr_herb = animals_nr_herb
        self.animals_weight_herb = animals_weight_herb
        self.animals_age_herb = animals_age_herb
        self.animals_nr_carn = animals_nr_carn
        self.animals_weight_carn = animals_weight_carn
        self.animals_age_carn = animals_age_carn
        self.herb_list = [{'species': 'Herbivore', 'age': self.animals_age_herb, 'weight': self.animals_weight_herb}
                          for _ in range(self.animals_nr_herb)]
        self.carn_list = [{'species': 'Carnivore', 'age': self.animals_age_carn, 'weight': self.animals_weight_carn}
                          for _ in range(self.animals_nr_carn)]

        landscapes_dessert = class_dessert
        landscapes_dessert.cell_add_population(self.herb_list)
        landscapes_dessert.cell_add_population(self.carn_list)
        landscapes_dessert.cell_sum_of_animals()

    def test_feeding_herb(self, class_dessert):
        """
        Test that animals dont gain weight when eating.
        Because there are no fodder, so they cant gain weight
        :param class_dessert: The dessert class
        """
        landscapes_dessert = class_dessert()
        self.add_animals(landscapes_dessert)

        total_weight_before = 0
        for animal in landscapes_dessert.population_herb:
            total_weight_before += animal.weight
        average_weight_before_eat = total_weight_before / self.animals_nr_herb

        landscapes_dessert.cell_add_fodder()
        landscapes_dessert.cell_feeding_herbivore()

        total_weight_after = 0
        for animal in landscapes_dessert.population_herb:
            total_weight_after += animal.weight
        average_weight_after_eat = total_weight_after / self.animals_nr_herb

        assert average_weight_before_eat == self.animals_weight_herb
        assert average_weight_after_eat == self.animals_weight_herb

    def test_regrowth(self, class_dessert):
        """
        Test that regrowth works in right cells.
        :param class_dessert: The dessert class
        """
        landscapes_dessert = class_dessert()
        self.add_animals(landscapes_dessert)

        landscapes_with_animals_fodder_before = landscapes_dessert.fodder
        landscapes_dessert.cell_add_fodder()
        landscapes_with_animals_fodder_before_eating = landscapes_dessert.fodder
        landscapes_dessert.cell_feeding_herbivore()
        landscapes_with_animals_fodder_after_eating = landscapes_dessert.fodder
        landscapes_dessert.cell_add_fodder()
        landscapes_with_animals_fodder_regrows = landscapes_dessert.fodder

        assert landscapes_with_animals_fodder_before == 0
        assert landscapes_with_animals_fodder_before_eating == 0
        assert landscapes_with_animals_fodder_after_eating == 0
        assert landscapes_with_animals_fodder_regrows == 0


@pytest.mark.parametrize('class_water', [Water])
class TestWater:
    """
    Test the water class
    """
    def add_animals(self, class_water, animals_nr_herb=20, animals_weight_herb=20, animals_age_herb=5,
                    animals_nr_carn=20, animals_weight_carn=20, animals_age_carn=5):
        """
        Easy way to add animals in all tests
        :param class_water: classes that are livable
        :param animals_nr_herb: the start number of herbivore
        :param animals_weight_herb: the start weight of herbivore
        :param animals_age_herb: the age weight of herbivore
        :param animals_nr_carn: the start number for carnivore
        :param animals_weight_carn:the start weight of carnivore
        :param animals_age_carn:the age weight of carnivore
        :return:
        """
        self.animals_nr_herb = animals_nr_herb
        self.animals_weight_herb = animals_weight_herb
        self.animals_age_herb = animals_age_herb
        self.animals_nr_carn = animals_nr_carn
        self.animals_weight_carn = animals_weight_carn
        self.animals_age_carn = animals_age_carn
        self.herb_list = [{'species': 'Herbivore', 'age': self.animals_age_herb, 'weight': self.animals_weight_herb}
                          for _ in range(self.animals_nr_herb)]
        self.carn_list = [{'species': 'Carnivore', 'age': self.animals_age_carn, 'weight': self.animals_weight_carn}
                          for _ in range(self.animals_nr_carn)]

        landscapes_water = class_water
        landscapes_water.cell_add_population(self.herb_list)
        landscapes_water.cell_add_population(self.carn_list)
        landscapes_water.cell_sum_of_animals()

    def test_add_population(self, class_water):
        """
        Test that adding animals causes an error, because water is not livable.
        :param class_water: The dessert class
        """
        landscapes_water = class_water()
        with pytest.raises(Exception):
            self.add_animals(landscapes_water)
