import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

class GasSimulation:
    def __init__(self):
        # Constants
        self.R = 0.0821  # Gas constant in L⋅atm/(mol⋅K)
        
        # Initial conditions
        self.pressure = 1.0     # atm
        self.volume = 1.0       # L
        self.temperature = 300  # K
    
        self.moles = 1.0        # mol
        
        # Setup the figure and animation
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.setup_plot()

    def setup_plot(self):
        # Create main plot
        self.ax.set_xlim(0, 2)
        self.ax.set_ylim(0, 2)
        self.ax.set_xlabel('Volume (L)')
        self.ax.set_ylabel('Pressure (atm)')
        self.ax.grid(True)
        
        # Create particles
        self.num_particles = 100
        self.particles, = self.ax.plot([], [], 'bo', ms=2, alpha=0.5)
        
        # Add container rectangle
        self.container = plt.Rectangle((0.5, 0.5), self.volume, self.volume, 
                                       fill=False, color='black')
        self.ax.add_patch(self.container)
        
        # Add sliders
        self.setup_sliders()
        
        # Add reset button
        self.setup_reset_button()
        
        # Initialize particle positions
        self.x = np.random.uniform(0.5, 0.5 + self.volume, self.num_particles)
        self.y = np.random.uniform(0.5, 0.5 + self.volume, self.num_particles)

    def setup_sliders(self):
        # Temperature slider
        ax_temp = plt.axes([0.1, 0.02, 0.3, 0.02])
        self.temp_slider = Slider(ax_temp, 'Temperature (K)', 
                                  100, 500, valinit=self.temperature)
        self.temp_slider.on_changed(self.update_temperature)
        
        # Volume slider
        ax_vol = plt.axes([0.1, 0.06, 0.3, 0.02])
        self.vol_slider = Slider(ax_vol, 'Volume (L)', 
                                 0.1, 2.0, valinit=self.volume)
        self.vol_slider.on_changed(self.update_volume)
        
        # Moles slider
        ax_moles = plt.axes([0.6, 0.02, 0.3, 0.02])
        self.moles_slider = Slider(ax_moles, 'Moles', 
                                   0.1, 2.0, valinit=self.moles)
        self.moles_slider.on_changed(self.update_moles)

    def setup_reset_button(self):
        ax_reset = plt.axes([0.8, 0.06, 0.1, 0.02])
        self.reset_button = Button(ax_reset, 'Reset')
        self.reset_button.on_clicked(self.reset)

    def update_temperature(self, val):
        self.temperature = val
        self.update_pressure()

    def update_volume(self, val):
        self.volume = val
        self.update_pressure()
        self.container.set_width(val)
        self.container.set_height(val)  # Update height for square shape

    def update_moles(self, val):
        self.moles = val
        self.update_pressure()

    def update_pressure(self):
        # Calculate new pressure using ideal gas law
        self.pressure = (self.moles * self.R * self.temperature) / self.volume
        self.ax.set_title(f'Pressure = {self.pressure:.2f} atm')

    def reset(self, event):
        # Reset all values to initial conditions
        self.temperature = 300
        self.volume = 1.0
        self.moles = 1.0
        self.temp_slider.reset()
        self.vol_slider.reset()
        self.moles_slider.reset()
        self.update_pressure()
        self.container.set_width(self.volume)
        self.container.set_height(self.volume)

    def animate(self, frame):
        # Update particle positions based on current conditions
        speed_factor = np.sqrt(self.temperature / 300)

        self.x += np.random.normal(0, 0.02 * speed_factor, self.num_particles)
        self.y += np.random.normal(0, 0.02 * speed_factor, self.num_particles)

        # Keep particles within container
        self.x = np.clip(self.x, 0.5, 0.5 + self.volume)
        self.y = np.clip(self.y, 0.5, 0.5 + self.volume)

        self.particles.set_data(self.x, self.y)
        return self.particles,

    def run(self):
        # Create animation
        anim = animation.FuncAnimation(self.fig, self.animate, 
                                       frames=200, interval=50, blit=False)
        plt.show()

# Create and run simulation
if __name__ == "__main__":
    simulation = GasSimulation()
    simulation.run()
