# main.py
import tkinter as tk
import turtle
import BnB
import NN

class TSPSolverApp:
    def __init__(self, master):
        self.master = master
        master.title("TSP Solver")

        self.distance_matrix = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
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

        turtle.delay(500)

        t = turtle.Turtle()
        t.speed(0)

        # Draw nodes
        for i in range(len(self.distance_matrix)):
            t.penup()
            t.goto(i * 100 - 200, 100)
            t.pendown()
            t.circle(5)
            t.penup()
            t.goto(i * 100 - 200, 90)
            t.write(f"{i}")

        # Draw optimal path
        t.penup()
        t.goto(path[0] * 100 - 200, 100)
        t.pendown()
        for city in path[1:]:
            t.goto(city * 100 - 200, 100)
        t.goto(path[0] * 100 - 200, 100)

        # State optimal distance
        t.penup()
        t.goto(0, -200)
        t.pendown()
        t.write(f"Optimal Distance: {distance}", align="center", font=("Arial", 16, "normal"))

        window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPSolverApp(root)
    root.mainloop()
