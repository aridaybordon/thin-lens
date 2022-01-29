from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import time

import numpy as np

class Optics_simul:

    def __init__(self, s_ob) -> None:
        self.f_ob = -1              # Focal objeto
        self.f_im = -self.f_ob      # Focal imagen

        self.s_ob = s_ob
    
        self.y_ob      = 0.3
        self.compute_im_pos()

        self.fig, self.ax = self.create_figure()
        self.draw_axis(self.f_ob, self.f_im)
        self.create_slider()

        self.slider.on_changed(self.slider_updater)

        self.draw_text()
        self.create_labels()
        self.slider_updater(val=1)

        plt.show()
        plt.ion()

        self.fig.savefig('simul.png')

    def compute_im_pos(self):
        self.s_im = 1 / (1/self.s_ob + 1/self.f_im)
        self.y_im = self.s_im*self.y_ob / self.s_ob

    def slider_updater(self, val):
        current = self.s_ob

        self.s_ob += (val - current)
        self.compute_im_pos()

        self.refresh_plot()
        self.update_plot()

    def refresh_plot(self):
        self.remove_lines()
        self.reset_labels()
        self.draw_axis(self.f_ob, self.f_im)

    def update_plot(self):
        self.update_labels()
        self.update_object()
        self.update_image()
        self.draw_light_rays()   

        self.fig.canvas.draw() 

    def create_figure(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.subplots_adjust(bottom=.2, left=.1, right=.9)

        return fig, ax

    def create_labels(self):
        text1 = self.ax.text(2, 0.95, s='')
        text2 = self.ax.text(4, 0.95, s='')
        text3 = self.ax.text(2, 0.80, s='')
        text4 = self.ax.text(4, 0.80, s='')

        self.labels = [text1, text2, text3, text4]

    def update_labels(self):
        self.labels[0].set_text(f'$s = {self.s_ob:.2f}$')
        self.labels[1].set_text(f'$s\' = {self.s_im:.2f}$')
        self.labels[2].set_text(f'$y = {self.y_ob:.2f}$')
        self.labels[3].set_text(f'$y\' = {self.y_im:.2f}$')

    def draw_axis(self, *points):
        self.xmax       = 5
        
        self.ax.set_xlim(-self.xmax, self.xmax)
        self.ax.set_ylim(-1, 1)

        for point in points:
            self.ax.plot(point, 0, '.k')

        self.ax.axhline(y=0, color='k', linewidth=.7)
        self.ax.axvline(x=0, ymin=0.1, ymax=0.9, color='k', linewidth=.9)

        plt.axis('off')

    def draw_text(self):
        for point, text in [[self.f_im, 'F\''], [self.f_ob, 'F']]:
            self.ax.text(x=point+0.01, y=-0.12, s=text, ha='center')

    def update_object(self) -> None:
        self.ax.plot([self.s_ob, self.s_ob], [0, self.y_ob], 'k-')

    def update_image(self) -> None:
        self.ax.plot([self.s_im, self.s_im], [0, self.y_im], 'k-')
        self.ax.plot(self.s_im, self.y_im, '.r')

    def draw_light_rays(self):
        if self.s_ob < 0:
            # First line
            l = self.draw_line_from_two_points(self.s_ob, 0, [[self.s_ob, self.y_ob], [self.f_ob, 0]], '.-r')
            self.draw_line_from_two_points(0, self.xmax, [[0, l[0]]], '-r')
            self.draw_line_from_two_points(-self.xmax, 0, [[0, l[0]]], '--r')

            # Second line
            self.draw_line_from_two_points(self.s_ob, 0, [[self.s_ob, self.y_ob]], '.-r')
            self.draw_line_from_two_points(0, self.xmax, [[0, self.y_ob], [self.f_im, 0]], '-r')
            self.draw_line_from_two_points(-self.xmax, 0, [[0, self.y_ob], [self.f_im, 0]], '--r')

            # Third line
            self.draw_line_from_two_points(self.s_ob, 0, [[self.s_ob, self.y_ob], [0, 0]], '.-r')
            self.draw_line_from_two_points(0, self.xmax, [[self.s_ob, self.y_ob], [0, 0]], '-r')
            self.draw_line_from_two_points(-self.xmax, 0, [[self.s_ob, self.y_ob], [0, 0]], '--r')
        
        else:
            # First line
            l = self.draw_line_from_two_points(-self.xmax, 0, [[self.s_ob, self.y_ob], [self.f_ob, 0]], '.-r')
            self.draw_line_from_two_points(0, self.xmax, [[0, l[0]]], '-r')
            self.draw_line_from_two_points(-self.xmax, 0, [[0, l[0]]], '--r')

            # Second line
            self.draw_line_from_two_points(0, self.xmax, [[self.s_ob, self.y_ob]], '.-r')
            self.draw_line_from_two_points(0, self.xmax, [[0, self.y_ob], [self.f_im, 0]], '--r')
            self.draw_line_from_two_points(-self.xmax, 0, [[0, self.y_ob], [self.f_im, 0]], '-r')

            # Third line
            self.draw_line_from_two_points(-self.xmax, 0, [[self.s_ob, self.y_ob], [0, 0]], '.-r')
            self.draw_line_from_two_points(0, self.xmax, [[self.s_ob, self.y_ob], [0, 0]], '-r')

    def create_slider(self) -> None:
        axis = plt.axes([0.25, 0.1, 0.5, 0.03])
        axis.set_axis_on()
        axis.set_facecolor('black')

        self.slider = Slider(axis, 'Posición del\nobjeto', valmin=-self.xmax, valmax=self.xmax, valinit=self.s_ob)

    def draw_line_from_two_points(self, xmin, xmax, points, sty) -> float:
        if len(points) == 2:
            A, B    = [[point[0], 1] for point in points], [[point[1]] for point in points]

            a, b    = np.linalg.inv(A).dot(B)
            y       = lambda x: a*x+b
        
        elif len(points) == 1:
            y       = lambda x: points[0][1]

        elif len(points) > 2:
            raise ValueError('You have provided an incorrect amount of points to draw!')

        self.ax.plot([xmin, xmax], [y(xmin), y(xmax)], sty, linewidth=.6)

        return y(xmax)
    
    def reset_labels(self):
        for label in self.labels:
            label.set_text('')

    def remove_lines(self):
        n_lines = len(self.ax.lines)
        [self.ax.lines.pop(0) for i in range(n_lines)]


if __name__ == '__main__':
    image = Optics_simul(s_ob=-1.8)