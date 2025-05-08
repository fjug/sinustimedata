import numpy as np
from tifffile import imwrite
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

np.random.seed(1)

gen_image_size = (256, 256)
len_diagonal = int(np.sqrt(gen_image_size[0]**2 + gen_image_size[1]**2))

draw_full_sinusoids = False
num_movies = 100

for movie in range(num_movies):

    num_sinosoids = 100
    num_frames = 100

    range_frequencies = (0.05, 0.5)
    range_amplitudes = (5, 15)

    frequencies = np.random.uniform(range_frequencies[0], range_frequencies[1], num_sinosoids)
    amplitudes = np.random.uniform(range_amplitudes[0], range_amplitudes[1], num_sinosoids)
    phase_shifts = np.random.uniform(0, 2 * np.pi, num_sinosoids)
    directions = np.random.uniform(0, 2 * np.pi, num_sinosoids)
    offsets_x = np.random.uniform(0, gen_image_size[0], num_sinosoids)
    offsets_y = np.random.uniform(0, gen_image_size[1], num_sinosoids)

    def draw_circle(image, center, radius: float):
        """Draw a circle on the image."""
        intrad = int(np.ceil(radius))
        for x in range(center[0] - intrad, center[0] + intrad + 1):
            for y in range(center[1] - intrad, center[1] + intrad + 1):
                if (x - center[0])**2 + (y - center[1])**2 <= radius**2:
                    if 0 <= x < image.shape[0] and 0 <= y < image.shape[1]:
                        image[x, y] = 1

    frames = np.zeros((num_frames, gen_image_size[0], gen_image_size[1]), dtype=np.int16)
    for t in range(num_frames):
        frame = np.zeros(gen_image_size, dtype=np.int16)
        for i in range(num_sinosoids):
            frequency = frequencies[i]
            amplitude = amplitudes[i]
            phase_shift = phase_shifts[i] + t * frequency
            
            offset_x = offsets_x[i]
            offset_y = offsets_y[i]
            direction = directions[i]

            if (draw_full_sinusoids):

                # Draw the sinusoid
                for dist in np.linspace(-len_diagonal, len_diagonal, len_diagonal*10):
                    # Calculate the coordinates of the pixel
                    x = int(np.round(offset_x + dist * np.cos(direction)))
                    y = int(np.round(offset_y + dist * np.sin(direction)))

                    orthogonal_distance = int(np.round(amplitude * np.sin(frequency * dist + phase_shift)))
                    orthogonal_direction = direction + np.pi / 2
                    # draw a point at distance orthogonal_distance from (x,y) in the direction of orthogonal_direction
                    x_sin = int(np.round(x + orthogonal_distance * np.cos(orthogonal_direction)))
                    y_sin = int(np.round(y + orthogonal_distance * np.sin(orthogonal_direction)))
                    if 0 <= x_sin < gen_image_size[0] and 0 <= y_sin < gen_image_size[1]:
                        # frame[x_sin, y_sin] = 1
                        draw_circle(frame, (x_sin, y_sin), 1.5)

            else: 
                # Draw a circle waving sinusoidally at the offset location
                # Calculate the coordinates of the pixel
                x = int(np.round(offset_x + np.cos(direction)))
                y = int(np.round(offset_y + np.sin(direction)))

                orthogonal_distance = int(np.round(amplitude * np.sin(frequency * phase_shift)))
                orthogonal_direction = direction + np.pi / 2
                # draw a point at distance orthogonal_distance from (x,y) in the direction of orthogonal_direction
                x_sin = int(np.round(x + orthogonal_distance * np.cos(orthogonal_direction)))
                y_sin = int(np.round(y + orthogonal_distance * np.sin(orthogonal_direction)))
                if 0 <= x_sin < gen_image_size[0] and 0 <= y_sin < gen_image_size[1]:
                    # frame[x_sin, y_sin] = 1
                    draw_circle(frame, (x_sin, y_sin), 2.5)

        if t%10 == 0:
            print(':', end='', flush=True)
        else:
            print('-', end='', flush=True)
        frames[t] = frame  
    print(' - ',movie)  

    imwrite(f'movie_{movie:03d}.tif', frames[:,np.newaxis,...], imagej=True)

    # fig, ax = plt.subplots()
    # m = ax.imshow(frames[0], cmap='gray')
    # plt.show()

    # def animate(i : int):
    #     m.set_array(frames[i])