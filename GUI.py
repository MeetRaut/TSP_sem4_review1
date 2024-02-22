import tkinter as tk
from tkinter import ttk
import turtle
import BnB
import NN
import math
import distance  # Importing distance.py module

class TSPSolverApp:
    def __init__(self, master):
        self.master = master
        master.title("TSP Solver")
        self.distance_matrix = None  # Initialize distance_matrix attribute

        self.radio_var = tk.IntVar()

        input_panel = tk.Frame(master)
        input_panel.grid(row=0, column=0, columnspan=2)

        cities_label = tk.Label(input_panel, text="Number of Cities:")
        cities_label.grid(row=0, column=0)

        self.cities_entry = tk.Entry(input_panel)
        self.cities_entry.grid(row=0, column=1)

        self.branch_and_bound_radio = tk.Radiobutton(input_panel, text="Branch and Bound", variable=self.radio_var, value=1)
        self.nearest_neighbor_radio = tk.Radiobutton(input_panel, text="Nearest Neighbor", variable=self.radio_var, value=2)
        self.solve_button = tk.Button(input_panel, text="Solve TSP", command=self.solve_tsp)

        self.branch_and_bound_radio.grid(row=1, column=0)
        self.nearest_neighbor_radio.grid(row=1, column=1)
        self.solve_button.grid(row=2, column=0, columnspan=2)

    def solve_tsp(self):
        import distance  # Importing the distance module here
        num_cities_str = self.cities_entry.get()
        try:
            num_cities = int(num_cities_str)
        except ValueError:
            print("Please enter a valid integer for the number of cities.")
            return

        # Ensure num_cities is at least 2
        if num_cities < 2:
            print("Number of cities must be at least 2.")
            return

        self.distance_matrix = distance.generate_distance_matrix(num_cities)  # Generate distance matrix based on number of cities
        if self.distance_matrix:
            
            choice = self.radio_var.get()
            if choice == 1:
                solver = BnB.BranchAndBound(self.distance_matrix)
                path, optimal_distance = solver.tsp_branch_and_bound()
                algorithm_name = "Branch and Bound"
            else:
                solver = NN.NearestNeighbor(self.distance_matrix)
                path, optimal_distance = solver.tsp_nearest_neighbor()
                algorithm_name = "Nearest Neighbor"
            

            
            # Determine time complexity based on the algorithm used
            if choice == 1:
                time_complexity = "O((n-1)!)"
            else:
                time_complexity = "O(n^2)"

            self.show_turtle_graphics(path, optimal_distance, algorithm_name, time_complexity)

        else:
            print("Failed to generate distance matrix for the selected number of cities.")


    def show_turtle_graphics(self, path, distance, algorithm_name, time_complexity):
        if self.distance_matrix is None:
            print("Distance matrix not found.")
            return
        window = turtle.Screen()
        window.title("TSP Solution")

        turtle.delay(200)

        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()

        num_cities = len(self.distance_matrix)
        radius = 200
        angle = 360 / num_cities

        city_coordinates = []

        # Draw nodes in a circular pattern and connect them
        for i in range(num_cities):
            x = radius * math.cos(math.radians(i * angle - 90))
            y = radius * math.sin(math.radians(i * angle - 90))
            t.penup()
            t.goto(x, y)
            t.pendown()
            t.circle(10)
            city_coordinates.append((x, y))

        # Write numbers inside circles
        t.penup()
        for i, (x, y) in enumerate(city_coordinates):
            t.goto(x + 2, y + 5)  # Adjust y position to move the number inside the circle
            t.write(f"{i+1}", align="center", font=("Arial", 10, "bold"))

        # Draw optimal path
        t.penup()
        t.goto(city_coordinates[path[0]][0], city_coordinates[path[0]][1])
        t.pendown()
        for city_index in path[1:]:
            t.goto(city_coordinates[city_index][0], city_coordinates[city_index][1])
        t.goto(city_coordinates[path[0]][0], city_coordinates[path[0]][1])

        
        # State optimal distance
        t.penup()
        t.goto(0, -radius - 40)
        t.pendown()
        t.write(f"Optimal Distance: {distance}", align="center", font=("Arial", 12, "normal"))

        # State optimal path
        t.penup()
        t.goto(0, -radius - 70)
        t.pendown()
        return_path = path + [path[0]]
        t.write(f"Optimal Path: {' -> '.join(map(lambda x: str(x + 1), return_path))}", align="center", font=("Arial", 12, "normal"))

        # Display time complexity        
        t.penup()
        t.goto(0, -radius - 100)
        t.pendown()
        t.write(f"Time Complexity ({algorithm_name}): {time_complexity}", align="center", font=("Arial", 12, "normal"))

        window.mainloop()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TSPSolverApp(root)
    root.mainloop()
