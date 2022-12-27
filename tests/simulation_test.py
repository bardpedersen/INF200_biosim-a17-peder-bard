from biosim.simulation import BioSim
from biosim.landscapes import Lowland, Highland
from biosim.animals import Herbivore, Carnivore
import pytest
import textwrap3


class TestSimulation:
    """
    Adds more test to the simulation file, the test file test_biosim_interface
    doesn't test all functions
    """
    @pytest.fixture(autouse=True)
    def sett_up_simulation(self):
        island_map = """\
           WWW
           WLW
           WWW"""
        island_map = textwrap3.dedent(island_map)
        self.seed = 123
        self.pop = [{'loc': (2, 2),
                     'pop': [{'species': 'Herbivore',
                              'age': 5,
                              'weight': 20}
                             for _ in range(20)]}]
        self.biosim = BioSim(island_map, self.pop, self.seed)

    def test_population_start(self):
        """
        Test that the simulation start with zero population
        :return:
        """
        assert self.biosim.num_animals == 0

    def test_add_population(self):
        """
        Test that you can add population
        :return:
        """
        self.biosim.add_population(self.pop)

    def test_year_zero(self):
        """
        Test that the simulation start at year zero
        :return:
        """
        assert self.biosim.year == 0

    def test_year(self):
        """
        Test that the years increase as it should
        :return:
        """
        number_years = 2
        self.biosim.simulate(number_years)
        assert self.biosim.year == number_years

    def test_num_animals_per_species(self):
        """
        Test that the function returns a dictionary
        :return:
        """
        assert isinstance(self.biosim.num_animals_per_species, dict)

    def test_set_animal_parameters(self):
        """
        Test that animal parameters are changeable
        :return:
        """
        herb = {'mu': 100}
        carn = {'beta': 0.9}
        self.biosim.set_animal_parameters('Herbivore', herb)
        self.biosim.set_animal_parameters('Carnivore', carn)
        assert Herbivore.params['mu'] == 100
        assert Carnivore.params['beta'] == 0.9
        """
        Reset params
        """
        herb = {'mu': 0.25}
        carn = {'beta': 0.75}
        self.biosim.set_animal_parameters('Herbivore', herb)
        self.biosim.set_animal_parameters('Carnivore', carn)

    def test_set_landscape_parameters(self):
        """
        Test that landscape parameters are changeable
        :return:
        """
        lowland = {'f_max': 100}
        highland = {'f_max': 150}
        self.biosim.set_landscape_parameters('L', lowland)
        self.biosim.set_landscape_parameters('H', highland)
        assert Lowland.params['f_max'] == 100
        assert Highland.params['f_max'] == 150
        """
        Reset params
        """
        lowland = {'f_max': 800}
        highland = {'f_max': 300}
        self.biosim.set_landscape_parameters('L', lowland)
        self.biosim.set_landscape_parameters('H', highland)
