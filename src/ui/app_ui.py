from tkinter import Tk, Canvas, Button, Entry, Label, messagebox, StringVar, OptionMenu, Frame, Scrollbar
import numpy as np
from ahc_algorithm import agglomerative_clustering

class AppUI:
    def __init__(self, master):
        self.master = master
        master.title("Agglomerative Hierarchical Clustering Simulator")

        # Canvas for clustering visualization
        self.canvas = Canvas(master, width=600, height=400, bg='white')
        self.canvas.pack()

        # Frame chứa canvas và scrollbar cho dendrogram
        dendrogram_frame = Frame(master)
        dendrogram_frame.pack(fill="both", expand=True)

        # Canvas for dendrogram visualization
        self.dendrogram_canvas = Canvas(dendrogram_frame, width=600, height=200, bg='white')
        self.dendrogram_canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar dọc
        dendrogram_scrollbar = Scrollbar(dendrogram_frame, orient="vertical", command=self.dendrogram_canvas.yview)
        dendrogram_scrollbar.pack(side="right", fill="y")

        # Gán scrollbar vào canvas
        self.dendrogram_canvas.configure(yscrollcommand=dendrogram_scrollbar.set)
        self.dendrogram_canvas.bind('<Configure>', self.on_dendrogram_configure)

        # Input section
        Label(master, text="Enter data points (x,y):").pack()
        self.entry = Entry(master)
        self.entry.pack()

        Label(master, text="Select Linkage Method:").pack()
        self.linkage_method = StringVar(master, value="single")
        OptionMenu(master, self.linkage_method, "single", "complete", "average").pack()

        # Buttons
        self.start_button = Button(master, text="Start", command=self.start_clustering)
        self.start_button.pack()

        self.next_button = Button(master, text="Next", command=self.next_step, state="disabled")
        self.next_button.pack()

        # Data storage
        self.points = []
        self.steps = []
        self.dendrogram_steps = []
        self.current_step = -1

        self.draw_axes()

    def draw_axes(self):
        """Draw coordinate axes on the clustering canvas."""
        self.canvas.create_line(0, 200, 600, 200, arrow="last", fill="black")  # X-axis
        self.canvas.create_line(300, 0, 300, 400, arrow="last", fill="black")  # Y-axis
        self.canvas.create_text(590, 210, text="X", fill="black")
        self.canvas.create_text(310, 10, text="Y", fill="black")

    def parse_input(self, input_data):
        try:
            return [tuple(map(float, point.strip().split(','))) for point in input_data.split(';')]
        except ValueError:
            return []

    def start_clustering(self):
        input_data = self.entry.get()
        self.points = self.parse_input(input_data)

        if not self.points:
            messagebox.showerror("Input Error", "Please enter valid data points.")
            return

        # Reset everything
        self.steps.clear()
        self.dendrogram_steps.clear()
        self.current_step = -1
        self.canvas.delete("all")
        self.dendrogram_canvas.delete("all")
        self.draw_axes()

        # Run clustering and store steps
        def step_callback(clusters, dendrogram_step):
            self.steps.append([list(cluster) for cluster in clusters])
            self.dendrogram_steps.append(dendrogram_step)

        linkage = self.linkage_method.get()
        agglomerative_clustering(self.points, step_callback, linkage)

        # Initially, only show points
        self.update_visualization([[p] for p in self.points])
        self.dendrogram_canvas.create_text(300, 100, text="Dendrogram will appear step by step", fill="gray")

        self.next_button.config(state="normal")

    def update_visualization(self, clusters):
        self.canvas.delete("all")
        self.draw_axes()

        colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta']
        zoom = 2.5
        center_x, center_y = 300, 200
        point_size = 5

        for idx, cluster in enumerate(clusters):
            color = colors[idx % len(colors)]
            for (x, y) in cluster:
                screen_x = center_x + x * zoom
                screen_y = center_y - y * zoom
                self.canvas.create_oval(screen_x - point_size, screen_y - point_size,
                                        screen_x + point_size, screen_y + point_size, fill=color)

    def update_dendrogram(self, step_data):
        self.dendrogram_canvas.delete("all")

        # Draw boxes
        for idx, (x, y) in enumerate(step_data["boxes"]):
            self.dendrogram_canvas.create_rectangle(x - 20, y - 10, x + 20, y + 10, fill="white", outline="black")
            if self.current_step < len(self.steps) and idx < len(self.steps[self.current_step]):
                cluster = self.steps[self.current_step][idx]
                if len(cluster) == 1:
                    label = f"({cluster[0][0]:.1f}, {cluster[0][1]:.1f})"
                else:
                    label = f"{len(cluster)} pts"
                self.dendrogram_canvas.create_text(x, y + 20, text=label, font=("Arial", 8), fill="black")

        # Draw lines
        for (x1, y1, x2, y2) in step_data["lines"]:
            self.dendrogram_canvas.create_line(x1, y1, x2, y2, fill="blue")

        # Cập nhật lại vùng scroll
        self.dendrogram_canvas.configure(scrollregion=self.dendrogram_canvas.bbox("all"))

    def next_step(self):
        if self.current_step + 1 >= len(self.steps):
            messagebox.showinfo("Clustering Complete", "All steps have been completed.")
            self.next_button.config(state="disabled")
            return

        self.current_step += 1
        self.update_visualization(self.steps[self.current_step])
        self.update_dendrogram(self.dendrogram_steps[self.current_step])

    def on_dendrogram_configure(self, event):
        """Cập nhật vùng scroll tự động."""
        self.dendrogram_canvas.configure(scrollregion=self.dendrogram_canvas.bbox("all"))

if __name__ == "__main__":
    root = Tk()
    app = AppUI(root)
    root.mainloop()
