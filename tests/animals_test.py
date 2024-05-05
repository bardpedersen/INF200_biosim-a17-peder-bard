from biosim.animals import Herbivore, Carnivore
import pytest


@pytest.mark.parametrize('both_species', [Herbivore, Carnivore])
class TestBothAnimals:
    def test_grow_one_year(self, both_species):
        """
        Test that herbivores age one time per year
        :param both_species: is both herbivores and carnivores
        :return:
        """
        species = both_species()
        age = species.age
        _nr_years = 10
        for _ in range(_nr_years):
            species.grow_one_year()
            assert species.age == age + 1
            age += 1

    def test_weight_gained_from_eating(self, both_species):
        """
        Test that animal weight increases each time they eat
        :param both_species: is both herbivores and carnivores
        :return:
        """
        species = both_species()
        amount_of_fodder = 10
        for i in range(amount_of_fodder):
            weight = species.weight + species.params['beta']*i
            species.weight_gained_from_eating(i)
            assert species.weight == weight

    def test_lose_weight_each_year(self, both_species):
        """
        Test that animals lose weight each year
        :param both_species: is both herbivores and carnivores
        :return:
        """
        species = both_species()
        _nr_years = 10
        for _ in range(_nr_years):
            weight = species.weight - both_species.params['eta'] * species.weight
            species.lose_weight()
            assert species.weight == weight

    def test_calculate_fitness_weight_zero(self, both_species):
        """
        Tests the fitness calculation is zero, when weight is zero
        :param both_species: is both herbivores and carnivores
        :return:
        """
        species = both_species()
        species.weight = 0
        species.calculate_fitness()
        assert species.fitness == 0

    def test_death_zero_weight(self, both_species):
        """
        Test that they die when weight is zero
        :param both_species:
        :return:
        """
        species = both_species()
        species.weight = 0
        species.death()
        assert species.is_dead is True

    def test_migrated(self, both_species, mocker):
        """
        Test so animals will migrate if the chance is high.
        Sett low age and high weight to increases fitness
        as well as high mu
        :param both_species: is both herbivores and carnivores
        :return:
        """
        species = both_species()
        mocker.patch('random.random', return_value=0)
        species.params['mu'] = 10
        species.age = 1
        species.weight = 50
        species.migrate()
        assert species.has_migrated is True

    def test_has_migrated(self, both_species):
        """
        Test so animals cant migrate twice in one year
        :param both_species: is both herbivores and carnivores
        :return:
        """
        species = both_species()
        species.has_migrated = True
        species.migrate()
        assert species.has_migrated is False


@pytest.mark.parametrize('herbivore', [Herbivore])
class TestHerbivores:
    def test_calculate_fitness(self, herbivore):
        """
        Tests the fitness calculation.
        :param herbivore: THe class Herbivore
        :return:
        """
        species = herbivore()
        species.weight = 10
        species.age = 10
        species.calculate_fitness()
        assert species.fitness == pytest.approx(0.4999999996)

    def test_death_not_dead(self, herbivore, mocker):
        """
        Tests the death function is false when not dead
        :param herbivore: THe class Herbivore
        :param mocker: Lets us sett the random value
        :return:
        """
        species = herbivore()
        species.weight = 10
        species.age = 10
        mocker.patch('random.random', return_value=0.21)  # death prob = 20%
        species.death()
        assert species.is_dead is False

    def test_death_dead(self, herbivore, mocker):
        """
        Tests the death function is true when dead
        :param herbivore: THe class Herbivore
        :param mocker: Lets us sett the random value
        :return:
        """
        species = herbivore()
        species.weight = 10
        species.age = 10
        mocker.patch('random.random', return_value=0.19)
        species.death()
        assert species.is_dead is True

    def test_birth_prob_low_weight(self, herbivore, mocker):
        """
        Tests birth with low weight
        :param herbivore: THe class Herbivore
        :param mocker: Lets us sett the random value
        :return:
        """
        species = herbivore()
        mocker.patch('random.random', return_value=0.78)  # set slightly lower than prob carn birth so birth happens
        mocker.patch('random.gauss', return_value=8)

        species.weight = 9.5  # smaller
        species.calculate_fitness()
        new_born_herb = species.birth(100)  # large N value to show that probability is zero
        assert new_born_herb is None

    def test_birth(self, herbivore, mocker):
        """
        Tests birth with normal weight
        :param herbivore: THe class Herbivore
        :param mocker: Lets us sett the random value
        :return:
        """
        species = herbivore()
        w_child = 8
        mocker.patch('random.random', return_value=0.78)  # set slightly lower than prob carn birth so birth happens
        mocker.patch('random.gauss', return_value=8)
        species.weight = 34
        species.calculate_fitness()
        new_born_herb = species.birth(100)
        assert new_born_herb.age == 0
        assert new_born_herb.weight == w_child


@pytest.mark.parametrize('carnivore', [Carnivore])
class TestCarnivores:
    def test_calculate_fitness(self, carnivore):
        """
        Tests the fitness calculation is zero, when weight is zero
        :param carnivore: THe class Carnivore
        :return:
        """
        species = carnivore()
        species.weight = 10
        species.age = 10
        species.calculate_fitness()
        assert species.fitness == pytest.approx(0.916714)

    def test_death_not_dead(self, carnivore, mocker):
        """
        Tests the death function is false when not dead
        :param carnivore: The class Carnivore
        :param mocker: Lets us sett the random value
        :return:
        """
        species = carnivore()
        species.weight = 10
        species.age = 10
        mocker.patch('random.random', return_value=0.1)  # death prob = 0.08%
        species.death()
        assert species.is_dead is False

    def test_death_dead(self, carnivore, mocker):
        """
        Tests the death function is true when dead
        :param carnivore: The class Carnivore
        :param mocker: Lets us sett the random value
        :return:
        """
        species = carnivore()
        species.weight = 10
        species.age = 10
        mocker.patch('random.random', return_value=0)
        species.death()
        assert species.is_dead is True

    def test_birth_prob_low_weight(self, carnivore, mocker):
        """
        Tests birth probability with low weight
        :param carnivore: The class Carnivore
        :param mocker: Lets us sett the random value
        :return:
        """
        species = carnivore()
        mocker.patch('random.random', return_value=0.78)  # set slightly lower than prob carn birth so birth happens
        mocker.patch('random.gauss', return_value=8)

        species.weight = 9
        species.calculate_fitness()
        new_born_carn = species.birth(100)  # large N value to show that probability is zero
        assert new_born_carn is None

    def test_birth(self, carnivore, mocker):
        """
        Test birth probability with normal weight
        :param carnivore: The class Carnivore
        :param mocker: Lets us sett the random value
        :return:
        """
        species = carnivore()
        w_child = 8
        mocker.patch('random.random', return_value=0.78)  # set slightly lower than prob carn birth so birth happens
        mocker.patch('random.gauss', return_value=8)

        species.weight = 25  # just bigger than one of the zero conditions for birth
        species.calculate_fitness()
        new_born_carn = species.birth(2)
        assert new_born_carn.age == 0
        assert new_born_carn.weight == w_child


class TestCarnivoreKill:
    @pytest.fixture(autouse=True)
    def create_herbivore(self):
        self.age_h = 5
        self.weight_h = 10
        self.herb = Herbivore(self.age_h, self.weight_h)

    @pytest.fixture(autouse=True)
    def create_carnivore(self):
        self.age_c = 5
        self.weight_c = 20
        self.carn = Carnivore(self.age_c, self.weight_c)

    def test_carnivore_kill_prob(self):
        """
        Tests the calculation of kill probability for predator
        """
        self.carn.fitness = 0.40
        self.herb.calculate_fitness()
        assert self.carn.carnivore_kill_prob(self.herb) == 0

        prob = (0.55 - self.herb.fitness)/self.carn.params['DeltaPhiMax']
        self.carn.fitness = 0.55
        self.carn.carnivore_kill_prob(self.herb)
        assert self.carn.carnivore_kill_prob(self.herb) == pytest.approx(prob)
