import tkinter as tk
from tkinter import ttk


# ============================================================
# Measurement Metadata
# ============================================================

class MetadataFrame(ttk.LabelFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            text="Measurement Metadata",
            padding=10
        )

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):

        self.parent_dir_var = tk.StringVar()
        self.hybrid_name_var = tk.StringVar()
        self.tag_var = tk.StringVar()

        self.parent_dir_entry = ttk.Entry(
            self,
            textvariable=self.parent_dir_var,
            width=40
        )

        self.hybrid_name_entry = ttk.Entry(
            self,
            textvariable=self.hybrid_name_var,
            width=40
        )

        self.tag_entry = ttk.Entry(
            self,
            textvariable=self.tag_var,
            width=40
        )

    def create_layout(self):

        ttk.Label(
            self,
            text="Parent Directory Name:"
        ).grid(
            row=0,
            column=0,
            sticky="e",
            padx=5,
            pady=5
        )

        self.parent_dir_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        ttk.Label(
            self,
            text="Hybrid Name:"
        ).grid(
            row=1,
            column=0,
            sticky="e",
            padx=5,
            pady=5
        )

        self.hybrid_name_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        ttk.Label(
            self,
            text="Tag:"
        ).grid(
            row=2,
            column=0,
            sticky="e",
            padx=5,
            pady=5
        )

        self.tag_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=5,
            pady=5
        )

        self.columnconfigure(1, weight=1)

    def get_metadata(self):

        return {
            "parent_directory": self.parent_dir_var.get(),
            "hybrid_name": self.hybrid_name_var.get(),
            "tag": self.tag_var.get()
        }
