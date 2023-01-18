from tkinter import *
from tkinter import ttk


class FeetToMeters:
    def __init__(self, root):

        root.title("Feet to Meters")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.feet = StringVar()
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        self.meters = StringVar()

        ttk.Label(mainframe, textvariable=self.meters).grid(
            column=2, row=2, sticky=(W, E)
        )
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(
            column=3, row=3, sticky=W
        )

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)

    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
        except ValueError:
            pass


if __name__ == "__main__":
    root = Tk()
    FeetToMeters(root)
    root.mainloop()


# def calculate(*args):
#     try:
#         value = float(feet.get())
#         meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
#     except ValueError:
#         pass


# root = tk.Tk()
# root.title("Feet to Meters")

# frame = ttk.Frame(root, padding="3 3 12 12")
# frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# feet = tk.StringVar()
# feet_entry = ttk.Entry(frame, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

# meters = tk.StringVar()
# ttk.Label(frame, textvariable=meters).grid(column=2, row=2, sticky=(tk.W, tk.E))

# ttk.Button(frame, text="Calculate", command=calculate)

# ttk.Label(frame, text="feet").grid(column=3, row=1, sticky=tk.W)
# ttk.Label(frame, text="is equivalent to").grid(column=1, row=2, sticky=tk.E)
# ttk.Label(frame, text="meters").grid(column=3, row=2, sticky=tk.W)

# for child in frame.winfo_children():
#     child.grid_configure(padx=5, pady=5)

# feet_entry.focus()
# root.bind("<Return>", calculate)

# root.mainloop()

# # canvas = tk.Canvas(frame)
# # canvas.create_rectangle(5, 5, 10, 10)
# # canvas.pack()
# # ttk.Button(root, text="Hello World").grid()
