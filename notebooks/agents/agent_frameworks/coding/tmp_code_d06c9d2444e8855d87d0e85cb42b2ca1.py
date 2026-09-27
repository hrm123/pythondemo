import numpy as np
import matplotlib.pyplot as plt

# 1. Define the parameters (Start, End, Number of points)
start_angle = -2 * np.pi
end_angle = 2 * np.pi
num_points = 400  # Higher number means a smoother curve

# 2. Generate the x-axis data (angles from -2π to 2π)
x = np.linspace(start_angle, end_angle, num_points)

# 3. Calculate the y-axis data (y = sin(x))
y = np.sin(x)

# 4. Create the plot figure
plt.figure(figsize=(12, 6)) # Optionally set the size of the plot
plt.plot(x, y, label='sin(x)', color='blue', linewidth=2)

# 5. Add labels, title, and grid for clarity
plt.title('Sine Wave Plot from -2π to 2π')
plt.xlabel('Angle (Radians)')
plt.ylabel('Amplitude')
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(0, color='black', linewidth=0.5) # Add a horizontal line at y=0
plt.legend()

# 6. Save the plot as requested
output_filename = 'sine_wave.png'
plt.savefig(output_filename)
print(f"\n✅ Success: The sine wave plot has been saved as '{output_filename}'")

# 7. Display the plot (useful if running in an interactive environment)
plt.show()