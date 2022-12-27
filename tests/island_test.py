from biosim.island_map import Map
import pytest
import textwrap3


class TestIslandMap:
    """
    Test that the island is working properly
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

    @pytest.fixture(autouse=True)
    def create_map(self):
        islandmap = """\
        WWWWW
        WLLHW
        WLHHW
        WDDDW
        WWWWW"""
        islandmap = textwrap3.dedent(islandmap)
        self.map = Map(islandmap)

    @pytest.fixture(autouse=True)
    def animals(self):
        self.animals_nr = 20
        self.animals_weight = 20
        self.animals_age = 5
        self.loc = (3, 3)
        self.herb_list = [{'loc': self.loc, 'pop':
                          [{'species': 'Herbivore', 'age': self.animals_age,
                           'weight': self.animals_weight}
                           for _ in range(self.animals_nr)]}]
        self.carn_list = [{'loc': self.loc, 'pop':
                          [{'species': 'Carnivore', 'age': self.animals_age,
                           'weight': self.animals_weight}
                           for _ in range(self.animals_nr)]}]

    @pytest.fixture(autouse=True)
    def creates_map_and_adds_animals(self):
        self.map.creating_map()
        self.map.island_add_population(self.herb_list)
        self.map.island_add_population(self.carn_list)
        self.map.island_total_herbivores_and_carnivores()
        self.map.island_total_sum_of_animals()

    def test_validate_map_not_surrounded_by_water(self):
        islandmap = """\
                WL
                WW"""
        islandmap = textwrap3.dedent(islandmap)
        map_test = Map(islandmap)
        with pytest.raises(Exception):
            map_test.creating_map()

    def test_validate_map_not_right_letter(self):
        islandmap = """\
                WWW
                WKW
                WWW"""
        islandmap = textwrap3.dedent(islandmap)
        map_test = Map(islandmap)
        with pytest.raises(Exception):
            map_test.creating_map()

    def test_validate_map_not_right_shape(self):
        islandmap = """\
                W
                WW"""
        islandmap = textwrap3.dedent(islandmap)
        map_test = Map(islandmap)
        with pytest.raises(Exception):
            map_test.creating_map()

    def test_creating_map(self):
        self.map.creating_map()
        assert isinstance(self.map.map_dict, dict)

    def test_island_add_population(self):
        """
        Test that adding animals work
        :return:
        """
        assert self.map.island_total_carnivores == self.animals_nr
        assert self.map.island_total_herbivores == self.animals_nr
        assert self.map.island_total_animals == self.animals_nr * 2

    def test_island_migration_prob_max(self, mocker):
        """
        Test that animals migrate when the prob is max
        :param mocker: Lets us choose random value
        :return:
        """
        mocker.patch('random.random', return_value=0)  # Sett the prob to make sure they migrate
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.migrate()

        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.has_migrated is True

    def test_island_migration_prob_min(self, mocker):
        """
        Test that animals dont migrate when the prob is zero
        :param mocker: Lets us choose random value
        :return:
        """
        mocker.patch('random.random', return_value=10)  # Sett the prob to make sure they don't migrate
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.migrate()

        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.has_migrated is False

    def test_migration_move_right(self, mocker):
        """
        If the random value is less than 0.25 the animal will move right
        :param mocker: Lets us choose random value
        :return:
        """
        mocker.patch('random.random', return_value=0.0)
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.has_migrated = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.has_migrated = True

        for loc in self.map.map_dict.keys():
            self.map.island_migration_carn(loc)
            self.map.island_migration_herb(loc)
            self.map.map_dict[loc].cell_migration_remove()

        for loc in self.map.map_dict:
            self.map.map_dict[loc].cell_sum_of_animals()

        self.new_loc = (3, 4)  # This will be to the right for self.loc / (3,3)
        for loc in self.map.map_dict:
            if loc == self.new_loc:
                assert self.map.map_dict[loc].population_sum_herb == self.animals_nr
                assert self.map.map_dict[loc].population_sum_carn == self.animals_nr
            else:
                assert self.map.map_dict[loc].population_sum_herb == 0
                assert self.map.map_dict[loc].population_sum_carn == 0

    def test_migration_move_left(self, mocker):
        """
        If the random value is more than 0.25 and less than 0.5
        the animal will move left
        :param mocker:Lets us choose random value
        :return:
        """
        mocker.patch('random.random', return_value=0.35)  # This makes the animals move left
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.has_migrated = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.has_migrated = True

        for loc in self.map.map_dict.keys():
            self.map.island_migration_carn(loc)
            self.map.island_migration_herb(loc)
            self.map.map_dict[loc].cell_migration_remove()

        for loc in self.map.map_dict:
            self.map.map_dict[loc].cell_sum_of_animals()

        self.new_loc = (3, 2)  # This will be to the left for self.loc / (3,3)
        for loc in self.map.map_dict:
            if loc == self.new_loc:
                assert self.map.map_dict[loc].population_sum_herb == self.animals_nr
                assert self.map.map_dict[loc].population_sum_carn == self.animals_nr
            else:
                assert self.map.map_dict[loc].population_sum_herb == 0
                assert self.map.map_dict[loc].population_sum_carn == 0

    def test_migration_move_up(self, mocker):
        """
        If the random value is more than 0.5 and less than 0.75
        the animals move up
        :param mocker: Lets us choose random value
        :return:
        """
        mocker.patch('random.random', return_value=0.65)  # This makes the animals move left
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.has_migrated = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.has_migrated = True

        for loc in self.map.map_dict.keys():
            self.map.island_migration_carn(loc)
            self.map.island_migration_herb(loc)
            self.map.map_dict[loc].cell_migration_remove()

        for loc in self.map.map_dict:
            self.map.map_dict[loc].cell_sum_of_animals()

        self.new_loc = (2, 3)  # This will be up for self.loc / (3,3)
        for loc in self.map.map_dict:
            if loc == self.new_loc:
                assert self.map.map_dict[loc].population_sum_herb == self.animals_nr
                assert self.map.map_dict[loc].population_sum_carn == self.animals_nr
            else:
                assert self.map.map_dict[loc].population_sum_herb == 0
                assert self.map.map_dict[loc].population_sum_carn == 0

    def test_migration_move_down(self, mocker):
        """
        If the random value is more than 0.75
        the animals move down
        :param mocker: Lets us choose random value
        :return:
        """
        mocker.patch('random.random', return_value=0.9)  # This makes the animals move up
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.has_migrated = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.has_migrated = True

        for loc in self.map.map_dict.keys():
            self.map.island_migration_carn(loc)
            self.map.island_migration_herb(loc)
            self.map.map_dict[loc].cell_migration_remove()

        for loc in self.map.map_dict:
            self.map.map_dict[loc].cell_sum_of_animals()

        self.new_loc = (4, 3)  # This will be down for self.loc / (3,3)
        for loc in self.map.map_dict:
            if loc == self.new_loc:
                assert self.map.map_dict[loc].population_sum_herb == self.animals_nr
                assert self.map.map_dict[loc].population_sum_carn == self.animals_nr
            else:
                assert self.map.map_dict[loc].population_sum_herb == 0
                assert self.map.map_dict[loc].population_sum_carn == 0

    def test_island_weight_loss(self):
        """
        Test that animals lose weight every year
        :return:
        """
        self.map.island_weight_loss()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.weight == self.animals_weight - (self.animals_weight * self.params_herb['eta'])

    def test_island_aging(self):
        """
        Test that animals age every year
        :return:
        """
        _nr_years = 4
        for _ in range(_nr_years):
            self.map.island_aging()
        self.map.island_total_sum_of_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.age == self.animals_age + _nr_years

    def test_island_feeding_herb(self):
        """
        Test that herbivores gain weight from eating
        :return:
        """
        self.map.island_feeding()
        self.map.island_total_sum_of_animals()
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                assert animal.weight == self.animals_weight + self.params_herb['F'] * self.params_herb['beta']

    def test_island_feeding_carn(self, mocker):
        """
        Test that carnivores kills herbivores and the dead
        animals are removed
        :param mocker: Lets us choose random value
        :return:
        """
        mocker.patch('random.random', return_value=0)  # Makes the kill prob happen
        total_nr_herb_before = self.map.island_total_herbivores
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.weight = 1  # Makes the herbivore fitness low,
                animal.age = 50    # so the carnivores can easily kill

        self.map.island_feeding()
        self.map.island_total_sum_of_animals()
        total_nr_herb_after = self.map.island_total_herbivores
        assert total_nr_herb_before == self.animals_nr
        assert total_nr_herb_after == 0

    def test_island_death(self):
        """
        Test that dead animals are removed from the island
        :return:
        """
        animals_before_death = self.map.island_total_animals

        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.is_dead = True
            for animal in self.map.map_dict[loc].population_carn:
                animal.is_dead = True

        self.map.island_death()
        self.map.island_total_sum_of_animals()
        animals_after_death = self.map.island_total_animals
        assert animals_before_death == self.animals_nr*2
        assert animals_after_death is None

    def test_island_procreation(self, mocker):
        """
        Test that animals can get children
        :param mocker: Lets us choose random value
        :return:
        """
        mocker.patch('random.random', return_value=0)
        animals_before_procreation = self.map.island_total_animals
        for loc in self.map.map_dict:
            for animal in self.map.map_dict[loc].population_herb:
                animal.weight = 50
            for animal in self.map.map_dict[loc].population_carn:
                animal.weight = 50
        self.map.island_procreation()
        self.map.island_total_sum_of_animals()
        animals_after_procreation = self.map.island_total_animals
        assert animals_before_procreation == self.animals_nr * 2
        assert animals_after_procreation == self.animals_nr * 2 + (self.animals_nr * 2 - 2)

    def test_one_year(self):
        """
        Test that all functions are callable, as well as the one_year function
        :return:
        """
        assert callable(self.map.island_feeding)
        assert callable(self.map.island_procreation)
        assert callable(self.map.island_migration)
        assert callable(self.map.island_aging)
        assert callable(self.map.island_weight_loss)
        assert callable(self.map.island_death)
        assert callable(self.map.island_total_herbivores_and_carnivores)
        assert callable(self.map.island_total_sum_of_animals)

        assert callable(self.map.island_update_one_year)
