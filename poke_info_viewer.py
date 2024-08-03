from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from poke_api import get_pokemon_info  # Correct import

# Create the main window
root = Tk()
root.title("Pokemon Information")

# Create the frames
user_input_frame = ttk.Frame(root, padding="10")
user_input_frame.grid(row=0, column=0, sticky=(W, E))

info_frame = ttk.LabelFrame(root, text="Info", padding="10")
info_frame.grid(row=1, column=0, sticky=(W, E))

stats_frame = ttk.LabelFrame(root, text="Stats", padding="10")
stats_frame.grid(row=2, column=0, sticky=(W, E))

# User input frame
pokemon_name_label = ttk.Label(user_input_frame, text="Pokémon Name:")
pokemon_name_label.grid(row=0, column=0, padx=5, pady=5)

pokemon_name_entry = ttk.Entry(user_input_frame, width=20)
pokemon_name_entry.grid(row=0, column=1, padx=5, pady=5)

get_info_button = ttk.Button(user_input_frame, text="Get Info", command=lambda: get_pokemon_info_callback(pokemon_name_entry.get()))
get_info_button.grid(row=0, column=2, padx=5, pady=5)

def get_pokemon_info_callback(pokemon_name):
    if not pokemon_name:
        messagebox.showerror("Error", "Please enter a Pokémon name.")
        return
    
    pokemon_data = get_pokemon_info(pokemon_name)
    
    if pokemon_data:
        display_pokemon_info(pokemon_data)
    else:
        messagebox.showerror("Error", f"Unable to fetch information for {pokemon_name} from the PokeAPI.")

def display_pokemon_info(pokemon_data):
    # Clear previous information
    for widget in info_frame.winfo_children():
        widget.destroy()
    for widget in stats_frame.winfo_children():
        widget.destroy()

    # Display Pokémon types 
    types = [t['type']['name'].capitalize() for t in pokemon_data['types']]
    types_label = ttk.Label(info_frame, text="Types: " + ", ".join(types))
    types_label.grid(row=0, column=0, padx=5, pady=5)

    # Display stats 
    stats = ['special-attack', 'special-defense', 'speed']
    row = 0
    for stat in stats:
        stat_label = ttk.Label(stats_frame, text=stat.replace('-', ' ').capitalize())
        stat_label.grid(row=row, column=0, padx=5, pady=5)
        
        stat_value = next(s['base_stat'] for s in pokemon_data['stats'] if s['stat']['name'] == stat)
        stat_bar = ttk.Progressbar(stats_frame, length=200, maximum=200)
        stat_bar['value'] = stat_value
        stat_bar.grid(row=row, column=1, padx=5, pady=5)
        
        row += 1

root.mainloop()
