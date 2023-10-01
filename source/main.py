from physics import timestep
from utils import *

np.random.seed(69)

name = '2D_CA_model_1'

constants = {
    'initial_density': 0.15,
    'initial_velocity': 0.3,
    'max_velocity': 1.0,
    'acceleration': 0.2,
    'safety_distance': 7,
    'max_distance': 300,
    'pattern': 'random',
    'max_time': 500.0,
    'time_step': 1.0,
    'dimensions': 2,
}

def simulate(constants, save_plot=False):
    # we simulate traffic jams according to the equations from the 1D CA paper
    # create a road with a density of ro_0, with cars going at speed v_0
    # cars' positions are integers at the beginning
    cars = init_road(constants)

    if save_plot:
        init_plot(constants)

    full_speed_fraction = 0.0
    stopped_fraction = 0.0
    total_distance_covered = 0.0
    time = 0.0

    while time <= constants['max_time']:
        full_speed, stopped, distance = timestep(cars, constants)

        if save_plot:
            add_positions_to_plot(cars, time)

        time += constants['time_step']

        full_speed_fraction += full_speed
        stopped_fraction += stopped
        total_distance_covered += distance

    # calculate the fractions of time spent at full speed and stopped
    full_speed_fraction /= len(cars) * time
    stopped_fraction /= len(cars) * time
    # calculate the fraction of the total possible distance covered
    total_distance_covered = total_distance_covered / (len(cars) * constants['max_time'] * constants['max_velocity'])
    # save the plot
    if save_plot:
        save_results(name, constants)
        plt.show()

    return full_speed_fraction, stopped_fraction, total_distance_covered

# plot impact of acceleration on metrics
plot = plt.plot([], [])
variable = 'max_velocity'
plt.xlabel(variable)
plt.ylabel('Metrics')

arr1, arr2, arr3 = [], [], []

values = np.linspace(0.01, 2.0)
for value in values:
    constants[variable] = value
    full_speed_fraction, stopped_fraction, total_distance_covered = simulate(constants)

    arr1.append(full_speed_fraction)
    arr2.append(stopped_fraction)
    arr3.append(total_distance_covered)

plt.plot(values, arr1, 'b')
plt.plot(values, arr2, 'r')
plt.plot(values, arr3, 'g')

plt.legend(['Full speed fraction', 'Stopped fraction', 'Total distance covered'])
plt.show()