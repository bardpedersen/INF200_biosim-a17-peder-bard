#! /usr/bin/env python

"""
Full island simulation with herbivores and carnivores.
"""

__author__ = 'Peder Ørmen Bukaasen, Bård Tollef Pedersen'

import textwrap
from biosim.simulation import BioSim

if __name__ == '__main__':

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWLWLLLWWW
               WWWWWWWWWWWWWWWWWWWWWWWWWWWWWLWLLLLLLLWW
               WWWWWWWWWWWWWWWWWWWWWWWWWWWWWLLLLLLLLLLW
               WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWLLLLLLLLWW
               WWWWWWWWWWWWWWWWWWWWWWWWWWWWLWWLLHLWWLLW
               WWWWWWWWWWWWWWWWWWWWWWWWWWWWLLLHHHLWWLWW
               WWWWWWWWWWWWWWWWWWWWWWWWWWLLLLLHHHLWWWWW
               WWWWWWWWWWWWWWWWWWWWWWWWLLWLLLWLLLLWWWWW
               WWWWWWWWWWWWWWWWWWWWWWWWLLLLLLWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWWLWWLLWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWWWLLLWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWWWHHWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWWLHLWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWWLHLWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWLHLWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWLLWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWLLWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWLLLWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWLLWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWLLHLLWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWLHLWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWLLHLWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWLLLHLLWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWLLLHHLLWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWLLLLHHLLWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWLLLLHHHLLWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWLLLLHHHLLLWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWLLLLHHHHLLLLWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWLLLHHHHHLLLWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWLLLHHHHHLLWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWLLHHHHLLLLWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWLLLLHHLLLLWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWLLLHLLLLWWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWLLLLLDDWLWWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWLLLLDWWWWWWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWLLDWWWWWWWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"""
               
    geogr = textwrap.dedent(geogr)
    ini_herbs = [{'loc': (35, 15),
                  'pop': [{'species': 'Herbivore',
                           'age': 3,
                           'weight': 20}
                          for _ in range(200)]}]
    ini_carns = [{'loc': (34, 15),
                  'pop': [{'species': 'Carnivore',
                           'age': 3,
                           'weight': 15}
                          for _ in range(50)]}]

    sim = BioSim(geogr, ini_herbs + ini_carns, seed=1,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 cmax_animals={'Herbivore': 200, 'Carnivore': 100},
                 img_dir='../results',
                 img_base='norway',
                 vis_years=1)
    sim.simulate(100)
    sim.make_movie()

    input('Press ENTER')
