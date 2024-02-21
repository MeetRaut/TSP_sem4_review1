import tkinter as tk
import turtle
import BnB
import NN
import math

class TSPSolverApp:
    def __init__(self, master):
        self.master = master
        master.title("TSP Solver")

        self.distance_matrix = [
            [0, 2, 100, 123, 87],
            [100, 0, 2, 18, 7],
            [2, 100, 0, 6, 7],
            [12, 0, 0, 0, 5],
            [45, 0, 0, 2, 0]
        ]

        self.radio_var = tk.IntVar()

        self.branch_and_bound_radio = tk.Radiobutton(master, text="Branch and Bound", variable=self.radio_var, value=1)
        self.nearest_neighbor_radio = tk.Radiobutton(master, text="Nearest Neighbor", variable=self.radio_var, value=2)
        self.solve_button = tk.Button(master, text="Solve TSP", command=self.solve_tsp)

        self.branch_and_bound_radio.grid(row=0, column=0)
        self.nearest_neighbor_radio.grid(row=0, column=1)
        self.solve_button.grid(row=1, column=0, columnspan=2)

    def solve_tsp(self):
        choice = self.radio_var.get()
        if choice == 1:
            solver = BnB.BranchAndBound(self.distance_matrix)
            path, distance = solver.tsp_branch_and_bound()
        else:
            solver = NN.NearestNeighbor(self.distance_matrix)
            path, distance = solver.tsp_nearest_neighbor()

        self.show_turtle_graphics(path, distance)

    def show_turtle_graphics(self, path, distance):
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
        t.write(f"Optimal Distance: {distance}", align="center", font=("Arial", 16, "normal"))

        # State optimal path
        t.penup()
        t.goto(0, -radius - 80)
        t.pendown()
        t.write(f"Optimal Path: {' -> '.join(map(lambda x: str(x + 1), path))}", align="center", font=("Arial", 12, "normal"))

        window.mainloop()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TSPSolverApp(root)
    root.mainloop()
