"""
This class creates and applies function that
make up for the behavior for the animals.
So whether the animal shall move or not and makes
sure they ages each year.

.. note:: All params for animals can be found under their class,
          as well as in the task file.
          All formulas can also be found in the task

"""

import random as rd
import math as m


class Animal:
    """Class for all functions the animals have in common"""
    def __init__(self, age, weight):
        """
        Initiates instance of animal

        :param age: the age of the animal
        :type age: int
        :param weight: the weight of the animal
        :type weight: float
        """
        if age is None:
            age = 0
        elif age < 0:
            raise ValueError('Age has to be a positive integr')
        self.age = age
        if weight is None:
            weight = 0
        elif weight < 0:
            raise ValueError('Weight has to be positive interg or zero')
        self.weight = weight
        self.fitness = None
        self.has_migrated = False
        self.is_dead = False

    def set_params(cls, params):
        """
        Takes an dictionary of parameters and replaces default params

        :param params: parameters for the animals
        :type params: dictionary with parameter as key and value as value
        """
        for parameter in params:
            if parameter in cls.params:
                if params[parameter] < 0:
                    raise ValueError(f'{parameter} has to be positive, cant be {params[parameter]}')
                if parameter == 'eta' and params[parameter] > 1:
                    raise ValueError(f'eta has to be smaller than 1 cant be {params[parameter]}')
                if parameter == 'DeltaPhiMax' and params[parameter] == 0:
                    raise ValueError(f'DeltaPhiMax must be nonzero positive, cannot be {params[parameter]}')
                else:
                    cls.params[parameter] = params[parameter]
            else:
                raise KeyError(f'{parameter} is not a accepted parameter')

    def calculate_fitness(self):
        r"""
        Calculates the fitness of the animal by the given formula

        .. math::
            \Phi = \begin{cases}
                    0 & w \leq 0 \\
                    q^+ (a,a_{\frac{1}{2}},\phi_{age}) \times q^-(w,w_{\frac{1}{2}},\phi_{weight})  & \text{ else}
                    \end{cases}

        where

        .. math::
            q^\pm(x,x_{\frac{1}{2}},\phi) = \frac{1}{(1+e^{\pm \phi(x-x_{\frac{1}{2}})})}

        Note that

        .. math::
            0\leq\Phi\leq1


        """
        if self.weight <= 0:
            self.fitness = 0
        else:
            q_plus = 1/(1 + m.exp(self.params['phi_age']*(self.age - self.params['a_half'])))
            q_minus = 1/(1 + m.exp(-self.params['phi_weight']*(self.weight - self.params['w_half'])))
            self.fitness = q_plus*q_minus

    def grow_one_year(self):
        """
        Makes the animal one year older
        """
        self.age += 1

    def weight_gained_from_eating(self, fodder):
        r"""
        Calculates the gain of weight by an animal eating

        :param fodder: food accessible to the animal
        :type fodder: float

        .. math::
                \beta\times F
        """
        self.weight += fodder * self.params['beta']

    def lose_weight(self):
        r"""
        Calculates the weight after the annual weight lost

        .. math::
                \eta\times w
        """
        self.weight -= self.weight*self.params['eta']
        if self.weight < 0:
            self.weight = 0

    def death(self):
        r"""
        Calculates if animal dies using formula below.

        :return: returns 1 if the animal dies and 0 if it lives

        Formula to calculate if they die or survive

        .. math::
                w(1-\Phi)

        They also die when weight is zero:

        .. math::
                w\leq0

        """
        p = rd.random()
        self.calculate_fitness()
        prob_death = self.params['omega'] * (1 - self.fitness)
        if self.weight == 0 or p < prob_death:
            self.is_dead = True

    def migrate(self):
        r"""
        Calculates if animal shall move or stay
        with this formula

        .. math::
                \mu\times\Phi
        """
        if not self.has_migrated:
            self.calculate_fitness()
            move_prob = self.params['mu'] * self.fitness
            p = rd.random()
            if p < move_prob:
                self.has_migrated = True
        else:
            self.has_migrated = False

    def birth(self, n, species='herb'):
        r"""
        Calculates the probability for birth of animals and returns a child if
        the probability strikes by random.random()

        :param n: is the number of animals in the cell
        :type n: integer
        :param species: selects what kind of animal to return, default is Herbivore
        :type species: string

        This is the equation witch calculate the probability:

        .. math::
                min(1,\gamma\times\Phi\times(N-1))

        The probability is also zero when:

        .. math::
                w<\zeta(w_{birth} + \sigma_{birth})

        Newborn are born with the weight:

        .. math::
                w \sim N(w_{birth}, \sigma_{birth})

        """
        self.calculate_fitness()
        w_child = rd.gauss(self.params['w_birth'], self.params['sigma_birth'])
        lost_weight = w_child*self.params['xi']
        zero_conditon = self.params['zeta']*(self.params['w_birth']+self.params['sigma_birth'])
        if self.weight < lost_weight:
            return None
        elif w_child <= 0:
            return None
        elif self.weight < zero_conditon:
            return None
        else:
            p = rd.random()
            p_birth = min(1, self.params['gamma']*self.fitness*(n-1))
            if p < p_birth:
                self.weight -= lost_weight
                if species == 'herb':
                    return Herbivore(0, w_child)
                elif species == 'carn':
                    return Carnivore(0, w_child)


class Herbivore(Animal):
    """
    Class containing animals of species herbivores
    The params dictionary contains all the "static" parameters of the species

    params = {
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
    'F': 10}
    """

    params = {
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

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)

    def __repr__(self):
        return f'Herbivore, (age:{self.age}, Weight:{self.weight}, Is_dead: {self.is_dead}, ' \
               f'Has_migrated: {self.has_migrated})'


class Carnivore(Animal):
    """
    Class containing animals of species carnivore
    The params dictionary contains all the "static" parameters of the species

    params = {
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
    'DeltaPhiMax': 10}
    """
    params = {
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

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)

    def __repr__(self):
        return f'Carnivore, (age:{self.age}, Weight:{self.weight}, Is_dead: {self.is_dead}, ' \
               f'Has_migrated: {self.has_migrated})'

    def carnivore_kill_prob(self, prey):
        r"""
        Calculates the probability that carnivore kills herbivore

        :param prey: the prey the animal hunts
        :type prey: Herbivore, object of animal class
        :return: probability of carnivore killing herbivore

        Calculate the kill prob with this formula:

        .. math::
                p = \begin{cases}
                    0 & \text{if } \Phi_{carn} \leq \Phi_{herb} \\
                    \frac{\Phi_{carn} - \Phi_{herb}}{\Delta\Phi_{max}} & \text{if } 0<\Phi_{carn} -
                    \Phi_{herb}<\Delta\Phi_{max}\\
                    1 & \text{otherwise}
                    \end{cases}
        """

        difference_fitness = self.fitness - prey.fitness
        if self.fitness < prey.fitness:
            prob = 0
        elif 0 < difference_fitness < self.params['DeltaPhiMax']:
            prob = difference_fitness/self.params['DeltaPhiMax']
        else:
            prob = 1

        return prob
