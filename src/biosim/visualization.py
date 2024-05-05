"""
Visualization class for biosim.
This class has all the functions needed
to get graphs and picture from the date
that simulation makes. This class
creates an easy way of reading data.


Inspired by Hans Ekkehard Plesser Graphics ile from randvis prodject
Link: https://gitlab.com/nmbu.no/emner/inf200/h2021/inf200-course-materials/-/blob/main/january_block/examples/randvis_project/src/randvis/graphics.py
"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

_DEFAULT_DIR = os.path.join('../results')
_DEFAULT_NAME = 'sim'
_DEFAULT_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'

_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'


class Visualization:
    """ Visualizes the results from biosim"""
    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
        """
        :param img_dir: directory for image files to be stored
        :param img_name: start of image name
        :param img_fmt: format of image

        self._img_ctr: updates picture nr

        self._fig: Figure containing all the subplots

        self._map_ax: The subplot for map

        self._herb_ax: The place of subplot containing number of herbivore per cell

        self._herb_plot: The subplot containing number of herbivore per cell

        self._carn_ax: The place subplot containing number of carnivores per cell

        self_carn_plot: The subplot containing number of herbivore per cell

        self._pop_ax: The subplot containing number of animals

        self._herb_line: The line in population graph represented by number of herbivores

        self_carn_line: The line in population graph represented by number of carnivores

        self._fitness_ax: The subplot containing fitness

        self._weight_ax: The subplot containing weight

        self._age_ax: The subplot containing age
        """

        if img_name is None:
            img_name = _DEFAULT_NAME
        if img_dir is not None:

            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_FORMAT
        self._img_ctr = 0
        self._fig = None
        self._map_ax = None
        self._herb_ax = None
        self._herb_plot = None
        self._carn_ax = None
        self._carn_plot = None
        self._pop_ax = None
        self._herb_line = None
        self._carn_line = None
        self._fitness_ax = None
        self._weight_ax = None
        self._age_ax = None

    def _color_map(self, island_map):
        """
        Makes a colour map of the string map
        """
        colour = {'W': (0.0, 0.0, 1.0),
                  'L': (0.0, 0.6, 0.0),
                  'H': (0.5, 1.0, 0.5),
                  'D': (1.0, 1.0, 0.5)}

        colour_map = [[colour[column] for column in row]
                      for row in island_map.string_map.splitlines()]
        self._img_ax = plt.imshow(colour_map)

    def setup(self, island_map, final_year, y_max=500):
        """
        Prepares for plotting
        has to be called before :meth: 'update_plot'

        :param island_map: map object containing all info about island
        :param final_year: the final year of the simulation
        :param y_max: is the maximum of animals given from file
        """
        # create new plot window
        if self._fig is None:
            self._fig = plt.figure(figsize=(10, 8))

        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(3, 2, 1)
        self._color_map(island_map)

        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(3, 2, 3)
            self._herb_plot = None

        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(3, 2, 4)
            self._carn_plot = None

        if self._age_ax is None:
            self._age_ax = self._fig.add_subplot(3, 3, 7)

        if self._weight_ax is None:
            self._weight_ax = self._fig.add_subplot(3, 3, 8)

        if self._fitness_ax is None:
            self._fitness_ax = self._fig.add_subplot(3, 3, 9)

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(3, 2, 2)
            self._pop_ax.title.set_text('Population of island')
            self._pop_ax.set(xlabel='Years', ylabel='Num of animals')

        if y_max is not None:
            self._pop_ax.set_ylim(0, y_max)
        else:
            self._pop_ax.set_ylim(0)

        self._pop_ax.set_xlim(0, final_year+1)

        if self._herb_line is None:
            pop_plot = self._pop_ax.plot(np.arange(0, final_year+1), np.full(final_year+1, np.nan))
            self._herb_line = pop_plot[0]
        else:
            x_data, y_data = self._herb_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_line.set_data(np.hstack((x_data, x_new)), np.hstack((y_data, y_new)))

        if self._carn_line is None:
            pop_plot = self._pop_ax.plot(np.arange(0, final_year + 1), np.full(final_year + 1, np.nan))
            self._carn_line = pop_plot[0]
            self._pop_ax.legend(['herb', 'carn'])

        else:
            x_data, y_data = self._carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((x_data, x_new)), np.hstack((y_data, y_new)))

        self._fig.subplots_adjust(hspace=0.40)

    def update(self, year, island_map, cmax, hist_specs, y_max=None):
        """
        Updates plot with current year

        :param y_max: the range y-value is sett to in the graph
        :param year: is the year the simulation currently is in
        :param island_map: is the island map object to be plotted
        :param cmax: is a dictionary containing colorbar maxes for herbivore and carnivore heat map
        :param hist_specs: is a dictionary containing specifications for histograms of age weight and fitness
        """
        if cmax is None:
            cmax = {'Herbivore': 200,
                    'Carnivore': 50}

        self._fig.suptitle(f'Simulation, Year: {year}', fontsize=16)
        self._update_herb_map(island_map, cmax)
        self._update_carn_map(island_map, cmax)
        self._update_pop_graph(year, island_map, y_max)
        self._update_age_weight_fitness(island_map, hist_specs)
        self._fig.canvas.flush_events()
        plt.pause(1e-6)

    def _update_herb_map(self, island_map, cmax):
        """
        Plots the population of herbivores on the map by color

        :param island_map: is the island_map object containing info about the simulation
        :param cmax: is a dictionary containing colorbar maxes for herbivore and carnivore heat map
        """
        nested_list = list(map(list, island_map.string_map.splitlines()))
        x = 1
        for i in range(len(nested_list)):
            y = 1
            for j in range(len(nested_list[0])):
                if island_map.map_dict[(x, y)].population_sum_herb is None:
                    nested_list[i][j] = 0
                else:
                    nested_list[i][j] = island_map.map_dict[(x, y)].population_sum_herb
                y += 1
            x += 1

        matrix = np.array(nested_list)

        if self._herb_plot is None:
            self._herb_plot = self._herb_ax.imshow(matrix, interpolation='nearest', vmin=0, vmax=cmax['Herbivore'])
            plt.colorbar(self._herb_plot, ax=self._herb_ax)
            self._herb_ax.set_title('Herbivore heat map')
        else:
            self._herb_plot.set_data(matrix)

    def _update_carn_map(self, island_map, cmax):
        """
        Plots the population of carnivores on the map by color

        :param island_map: is the island_map object containing info about the simulation
        :param cmax: dictionary containing default values for colorbar max
        """
        nested_list = list(map(list, island_map.string_map.splitlines()))
        x = 1
        for i in range(len(nested_list)):
            y = 1
            for j in range(len(nested_list[0])):
                if island_map.map_dict[(x, y)].population_sum_carn is None:
                    nested_list[i][j] = 0
                else:
                    nested_list[i][j] = island_map.map_dict[(x, y)].population_sum_carn
                y += 1
            x += 1

        matrix = np.array(nested_list)
        if self._carn_plot is None:
            self._carn_plot = self._carn_ax.imshow(matrix, interpolation='nearest', vmin=0, vmax=cmax['Carnivore'])
            plt.colorbar(self._carn_plot, ax=self._carn_ax)
            self._carn_ax.set_title('Carnivore Heat map')
        else:
            self._carn_plot.set_data(matrix)

    def _update_age_weight_fitness(self, island_map, hist_specs=None):
        """
        Updates the histograms of age, weight and fitness,

        :param island_map: island_map object containing all info about island
        :param hist_specs:
        """
        if hist_specs is None:
            hist_specs = {
                'weight': {'max': 20, 'delta': 2},
                'age': {'max': 40, 'delta': 2},
                'fitness': {'max': 1, 'delta': 0.05}
            }

        herb, carn = island_map.island_age_weight_fitness()
        self._age_ax.cla()
        self._age_ax.set_title('Age')
        self._age_ax.hist(herb['age'], histtype='step',
                          bins=np.arange(0, hist_specs['age']['max'], hist_specs['age']['delta']))
        self._age_ax.hist(carn['age'], histtype='step',
                          bins=np.arange(0, hist_specs['age']['max'], hist_specs['age']['delta']))
        self._age_ax.legend(['herb', 'carn'])

        self._weight_ax.cla()
        self._weight_ax.set_title('Weight')
        self._weight_ax.hist(herb['weight'], histtype='step',
                             bins=np.arange(0, hist_specs['weight']['max'], hist_specs['weight']['delta']))
        self._weight_ax.hist(carn['weight'], histtype='step',
                             bins=np.arange(0, hist_specs['weight']['max'], hist_specs['weight']['delta']))

        self._weight_ax.legend(['Herb', 'Carn'])

        self._fitness_ax.cla()
        self._fitness_ax.set_title('Fitness')
        self._fitness_ax.hist(herb['fitness'], histtype='step',
                              bins=np.arange(0, hist_specs['fitness']['max'], hist_specs['fitness']['delta']))
        self._fitness_ax.hist(carn['fitness'], histtype='step',
                              bins=np.arange(0, hist_specs['fitness']['max'], hist_specs['fitness']['delta']))

        self._fitness_ax.legend(['Herb', 'Carn'])

    def _update_pop_graph(self, year, island_map, y_max):
        """
        Plotting the animals in the animal number graph by years

        :param year: what year it is in used for x axis in this case
        :param island_map: island_map object containing all info about island
        """
        y_data_herb = self._herb_line.get_ydata()
        y_data_herb[year] = island_map.island_total_herbivores
        self._herb_line.set_ydata(y_data_herb)

        y_data_carn = self._carn_line.get_ydata()
        y_data_carn[year] = island_map.island_total_carnivores
        self._carn_line.set_ydata(y_data_carn)
        plt.pause(1e-6)

        if y_max is None:
            self._pop_ax.set_ylim(0, max(y_data_herb)+500)

    def save_plots(self):
        """
        Saves plot to file if filename given
        """
        if self._img_base is None:
            return

        self._fig.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base, num=self._img_ctr, type=self._img_fmt))
        self._img_ctr += 1

    def make_movie(self, movie_fmt=None):
        """
        Creates MP4 movie from visualization images saved.

        Requires ffmpeg for MP4 and magick for GIF
        The movie is stored as img_base + movie_fmt
        """
        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)
