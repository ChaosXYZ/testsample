import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from datetime import datetime
import random

# Sample data generator
def generate_sample_data():
    """
    Generates a list of skill objects with the specified structure.
    Each object contains information about a skill, its subclass, class, last updated date,
    possible values, stage, and value.
    """
    data = [
        {
            "skill": "Flame",
            "subclass": "Pyromancer",
            "class": "Mage",
            "last_updated": random_date(),
            "Possible Values": "Fire1, Burn2, GreenFire, Fireburn",
            "Stage": "Released",
            "Value": "100"
        },
        {
            "skill": "Inferno",
            "subclass": "Pyromancer",
            "class": "Mage",
            "last_updated": random_date(),
            "Possible Values": "Blaze, Heatwave, Scorch",
            "Stage": "Beta",
            "Value": "200"
        },
        {
            "skill": "Frostbite",
            "subclass": "Cryomancer",
            "class": "Mage",
            "last_updated": random_date(),
            "Possible Values": "Ice1, Chill2, Snowfall",
            "Stage": "Released",
            "Value": "150"
        },
        {
            "skill": "Rage",
            "subclass": "Berserker",
            "class": "Warrior",
            "last_updated": random_date(),
            "Possible Values": "Fury, Wrath, Anger",
            "Stage": "Alpha",
            "Value": "300"
        },
        # Add more skill objects as needed
    ]
    return data

def random_date():
    """
    Generates a random date string in the format YYYY-MM-DD.
    """
    year = random.randint(2020, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # To avoid complications with February
    return datetime(year, month, day).strftime("%Y-%m-%d")

def process_data(data):
    """
    Processes the list of skill objects to extract hierarchical data.
    
    Returns:
        classes (list): Sorted list of unique classes.
        subclasses_dict (dict): Mapping of classes to their respective subclasses.
        skills_dict (dict): Mapping of subclasses to their respective skills.
    """
    classes = sorted(set(item['class'] for item in data))
    subclasses_dict = {cls: sorted(set(item['subclass'] for item in data if item['class'] == cls)) for cls in classes}
    skills_dict = {}
    for cls in classes:
        for subcls in subclasses_dict[cls]:
            skills = sorted(set(item['skill'] for item in data if item['class'] == cls and item['subclass'] == subcls))
            skills_dict[subcls] = skills
    return classes, subclasses_dict, skills_dict

class SampleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sample App")
        self.root.geometry("1500x750")  # Reduced window size
        sv_ttk.set_theme("light")  # Set to light theme

        # Initialize data structures
        self.data = []
        self.classes = []
        self.subclasses_dict = {}
        self.skills_dict = {}

        self.create_widgets()

    def create_widgets(self):
        # Main container frame
        self.container = ttk.Frame(self.root, padding=20)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(self.container, text="Sample App", font=("Helvetica", 24, "bold"))
        title.pack(pady=(0, 20))

        # Login Frame
        login_frame = ttk.Frame(self.container)
        login_frame.pack(fill=tk.X, pady=(0, 20))

        # Username
        username_label = ttk.Label(login_frame, text="Username:", font=("Helvetica", 14))  # Increased font size
        username_label.pack(side=tk.LEFT, padx=(0, 10))
        self.username_entry = ttk.Entry(login_frame, width=20, font=("Helvetica", 14))  # Increased font size
        self.username_entry.pack(side=tk.LEFT, padx=(0, 20))

        # Password
        password_label = ttk.Label(login_frame, text="Password:", font=("Helvetica", 14))  # Increased font size
        password_label.pack(side=tk.LEFT, padx=(0, 10))
        self.password_entry = ttk.Entry(login_frame, show="*", width=20, font=("Helvetica", 14))  # Increased font size
        self.password_entry.pack(side=tk.LEFT, padx=(0, 20))

        # Game Selection Combobox
        game_label = ttk.Label(login_frame, text="Select Game:", font=("Helvetica", 14))  # Increased font size
        game_label.pack(side=tk.LEFT, padx=(0, 10))
        self.game_combobox = ttk.Combobox(
            login_frame,
            values=["GAME2", "GAME3", "FIRSTGAME"],
            state="readonly",
            width=15,
            font=("Helvetica", 14)  # Increased font size
        )
        self.game_combobox.current(0)  # Set default selection
        self.game_combobox.pack(side=tk.LEFT, padx=(0, 20))

        # Login Button
        login_button = ttk.Button(login_frame, text="Login", command=self.login, width=10)
        login_button.pack(side=tk.LEFT, padx=(0, 10))

        # Refresh Button
        refresh_button = ttk.Button(login_frame, text="Refresh", command=self.refresh_data, width=10)
        refresh_button.pack(side=tk.LEFT, padx=(0, 10))

        # Separator
        separator = ttk.Separator(self.container, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        # Columns Frame
        columns_frame = ttk.Frame(self.container)
        columns_frame.pack(fill=tk.BOTH, expand=True)

        # Classes Column
        classes_frame = ttk.Frame(columns_frame)
        classes_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        classes_label = ttk.Label(classes_frame, text="Classes", font=("Helvetica", 16, "bold"))  # Increased font size
        classes_label.pack(pady=(0, 10))

        self.classes_listbox = tk.Listbox(classes_frame, exportselection=False, font=("Helvetica", 14))  # Increased font size
        self.classes_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 5))

        classes_scrollbar = ttk.Scrollbar(classes_frame, orient=tk.VERTICAL, command=self.classes_listbox.yview)
        classes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.classes_listbox.config(yscrollcommand=classes_scrollbar.set)
        self.classes_listbox.bind('<<ListboxSelect>>', self.on_class_select)

        # Subclasses Column
        subclasses_frame = ttk.Frame(columns_frame)
        subclasses_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        subclasses_label = ttk.Label(subclasses_frame, text="Subclasses", font=("Helvetica", 16, "bold"))  # Increased font size
        subclasses_label.pack(pady=(0, 10))

        self.subclasses_listbox = tk.Listbox(subclasses_frame, exportselection=False, font=("Helvetica", 14))  # Increased font size
        self.subclasses_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 5))

        subclasses_scrollbar = ttk.Scrollbar(subclasses_frame, orient=tk.VERTICAL, command=self.subclasses_listbox.yview)
        subclasses_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.subclasses_listbox.config(yscrollcommand=subclasses_scrollbar.set)
        self.subclasses_listbox.bind('<<ListboxSelect>>', self.on_subclass_select)

        # Skills Column
        skills_frame = ttk.Frame(columns_frame)
        skills_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0))

        skills_label = ttk.Label(skills_frame, text="Skills", font=("Helvetica", 16, "bold"))  # Increased font size
        skills_label.pack(pady=(0, 10))

        self.skills_listbox = tk.Listbox(skills_frame, exportselection=False, font=("Helvetica", 14))  # Increased font size
        self.skills_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 5))

        skills_scrollbar = ttk.Scrollbar(skills_frame, orient=tk.VERTICAL, command=self.skills_listbox.yview)
        skills_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.skills_listbox.config(yscrollcommand=skills_scrollbar.set)
        self.skills_listbox.bind('<<ListboxSelect>>', self.on_skill_select)

        # Initially disable columns until login
        self.enable_columns(False)

    def enable_columns(self, enable=True):
        """
        Enables or disables the Classes, Subclasses, and Skills listboxes.
        """
        state = tk.NORMAL if enable else tk.DISABLED
        self.classes_listbox.config(state=state)
        self.subclasses_listbox.config(state=state)
        self.skills_listbox.config(state=state)

    def login(self):
        """
        Handles the login process.
        - Validates that username and password are entered.
        - Prints username and selected game choice to the console.
        - Loads data and enables the columns if validation passes.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        game_choice = self.game_combobox.get()

        # Placeholder for actual authentication
        if username and password:
            self.load_data()
            self.enable_columns(True)
            print(f"Username: {username}, Game Choice: {game_choice}")
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        else:
            messagebox.showwarning("Login Failed", "Please enter both username and password.")

    def refresh_data(self):
        """
        Refreshes the data by regenerating the sample data and updating the Classes listbox.
        """
        if not self.data:
            messagebox.showwarning("Refresh Failed", "Please login first to refresh data.")
            return
        # In actual implementation, re-fetch data from API
        # For this sample, regenerate sample data
        self.data = generate_sample_data()
        self.process_and_update_data()
        messagebox.showinfo("Refresh", "Data has been refreshed.")

    def load_data(self):
        """
        Loads the sample data and processes it.
        """
        self.data = generate_sample_data()
        self.process_and_update_data()

    def process_and_update_data(self):
        """
        Processes the raw data and updates the Classes listbox.
        """
        self.classes, self.subclasses_dict, self.skills_dict = process_data(self.data)
        self.update_classes()

    def update_classes(self):
        """
        Populates the Classes listbox with the processed class data.
        """
        self.classes_listbox.config(state=tk.NORMAL)
        self.classes_listbox.delete(0, tk.END)
        for cls in self.classes:
            self.classes_listbox.insert(tk.END, cls)
        # Clear subclasses and skills
        self.subclasses_listbox.delete(0, tk.END)
        self.skills_listbox.delete(0, tk.END)

    def on_class_select(self, event):
        """
        Handles the event when a class is selected.
        Updates the Subclasses listbox based on the selected class.
        """
        selection = self.classes_listbox.curselection()
        if selection:
            index = selection[0]
            selected_class = self.classes_listbox.get(index)
            # Highlight selection
            self.highlight_selection(self.classes_listbox, index)
            # Update subclasses
            subclasses = self.subclasses_dict.get(selected_class, [])
            self.subclasses_listbox.config(state=tk.NORMAL)
            self.subclasses_listbox.delete(0, tk.END)
            for subcls in subclasses:
                self.subclasses_listbox.insert(tk.END, subcls)
            # Clear skills
            self.skills_listbox.delete(0, tk.END)

    def on_subclass_select(self, event):
        """
        Handles the event when a subclass is selected.
        Updates the Skills listbox based on the selected subclass.
        """
        class_selection = self.classes_listbox.curselection()
        subclass_selection = self.subclasses_listbox.curselection()
        if class_selection and subclass_selection:
            class_index = class_selection[0]
            subclass_index = subclass_selection[0]
            selected_class = self.classes_listbox.get(class_index)
            selected_subclass = self.subclasses_listbox.get(subclass_index)
            # Highlight selection
            self.highlight_selection(self.subclasses_listbox, subclass_index)
            # Update skills
            skills = self.skills_dict.get(selected_subclass, [])
            self.skills_listbox.config(state=tk.NORMAL)
            self.skills_listbox.delete(0, tk.END)
            for skill in skills:
                self.skills_listbox.insert(tk.END, skill)

    def on_skill_select(self, event):
        """
        Handles the event when a skill is selected.
        Opens a popup displaying detailed information about the selected skill.
        """
        selection = self.skills_listbox.curselection()
        if selection:
            index = selection[0]
            selected_skill = self.skills_listbox.get(index)
            # Highlight selection
            self.highlight_selection(self.skills_listbox, index)
            # Find the skill data
            class_index = self.classes_listbox.curselection()
            subclass_index = self.subclasses_listbox.curselection()
            if class_index and subclass_index:
                selected_class = self.classes_listbox.get(class_index[0])
                selected_subclass = self.subclasses_listbox.get(subclass_index[0])
                for item in self.data:
                    if (item['class'] == selected_class and 
                        item['subclass'] == selected_subclass and 
                        item['skill'] == selected_skill):
                        self.show_skill_popup(item)
                        break

    def highlight_selection(self, listbox, index):
        """
        Highlights the selected item in a Listbox.
        """
        # Clear all selections
        listbox.selection_clear(0, tk.END)
        # Select the current index
        listbox.selection_set(index)
        # Ensure the selection is visible
        listbox.see(index)

    def show_skill_popup(self, skill_data):
        """
        Displays a popup window with detailed information about the selected skill.
        """
        popup = tk.Toplevel(self.root)
        popup.title(skill_data['skill'])
        popup.geometry("450x400")
        popup.resizable(False, False)
        sv_ttk.set_theme("light")  # Ensure popup uses the light theme

        # Skill Details Frame
        details_frame = ttk.Frame(popup, padding=20)
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Skill Information
        info_labels = [
            f"Skill: {skill_data['skill']}",
            f"Subclass: {skill_data['subclass']}",
            f"Class: {skill_data['class']}",
            f"Last Updated: {skill_data['last_updated']}",
            f"Stage: {skill_data['Stage']}",
            f"Value: {skill_data['Value']}"
        ]

        for info in info_labels:
            label = ttk.Label(details_frame, text=info, font=("Helvetica", 14))  # Increased font size
            label.pack(anchor=tk.W, pady=2)

        # Possible Values Label
        possible_label = ttk.Label(details_frame, text="Possible Values:", font=("Helvetica", 14, "bold"))  # Increased font size
        possible_label.pack(anchor=tk.W, pady=(10, 5))

        # Possible Values Listbox with Scrollbar
        values_frame = ttk.Frame(details_frame)
        values_frame.pack(fill=tk.BOTH, expand=True)

        values_listbox = tk.Listbox(values_frame, font=("Helvetica", 14))  # Increased font size
        values_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(values_frame, orient=tk.VERTICAL, command=values_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        values_listbox.config(yscrollcommand=scrollbar.set)

        possible_values = [val.strip() for val in skill_data['Possible Values'].split(",")]
        for val in possible_values:
            values_listbox.insert(tk.END, val)

        # Close Button
        close_button = ttk.Button(details_frame, text="Close", command=popup.destroy, width=10)
        close_button.pack(pady=(20, 0))

def main():
    root = tk.Tk()
    app = SampleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
