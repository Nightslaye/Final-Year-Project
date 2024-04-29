import tkinter as tk
from tkinter import ttk

import customtkinter
from PIL import ImageTk, Image
import foliumtest

def submit():
    ideal_borough = borough_entry.get()
    comparative_borough = prev_borough_entry.get()

    # You can add your logic or print the values for demonstration
    print("Ideal Borough:", ideal_borough)
    print("Comparative Borough:", comparative_borough)

# Create the main window
window = tk.Tk()
window.title("Real Estate GUI")

# Load the background image
background_image = Image.open("background.png")
background_image_tk = ImageTk.PhotoImage(background_image)

# Set the window size to match the image dimensions
window.geometry(f"{background_image.width}x{background_image.height}")

# Create a Canvas with the background image
canvas = tk.Canvas(window, width=background_image.width, height=background_image.height)
canvas.create_image(0, 0, anchor=tk.NW, image=background_image_tk)
canvas.place(x=0, y=0)  # Place the canvas in the window

# Introduction Label
intro_text = (
    "\n\n                                                 Welcome to the London Mortgage Calculator!\n"
    "\nThis tool provides information in regards to getting a mortgage in your ideal borough whilst comparing with a secondary borough \nIt will tell you a number of metrics such as: 1.) Average Price 2.) Recommended Deposit 3.) Estimated monthly repayments and more!\n\nPlease your ideal borough and a borough you would like to compare with below:\n\n"
    "These are the available Boroughs:\n \n"
    "1. Barking and Dagenham         12. Lewisham                23. Barnet\n"
    "2. Bexley                       13. Redbridge               24. Wandsworth\n"
    "3. Newham                       14. Waltham Forest          25. Haringey\n"
    "4. Croydon                      15. Harrow                  26. Hackney\n"
    "5. Havering                     16. Bromley                 27. Islington\n"
    "6. Sutton                       17. Ealing                  28. Richmond upon Thames\n"
    "7. Greenwich                    18. Kingston upon Thames    29. Hammersmith and Fulham\n"
    "8. Enfield                      19. Southwark               30. Camden\n"
    "9. Hillingdon                   20. Lambeth                 31. City of London\n"
    "10. Tower Hamlets               21. Brent                   32. City of Westminster\n"
    "11. Hounslow                    22. Merton                  33. Kensington and Chelsea\n \n"
)


intro_label = tk.Label(window, text=intro_text, bg='black', fg='white', font=('Courier', 10), justify='left', padx=20, pady=20)
intro_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# Load the background image for the text
text_background_image = Image.open("text_background.png")

# Get the size of the text
text_width, text_height = text_background_image.width, text_background_image.height

# Create a label to measure the size of the text
temp_label = tk.Label(window, text=intro_text, font=('Courier', 12), fg='white', justify='left', padx=20, pady=0)
temp_label.update_idletasks()  # Update the label to get accurate size
text_width, text_height = temp_label.winfo_reqwidth(), temp_label.winfo_reqheight()
temp_label.destroy()  # Destroy the temporary label

# Resize the background image to fit the text tightly
text_background_image_resized = text_background_image.resize((text_width, text_height))

# Convert the resized image to a Tkinter-compatible format
text_background_image_tk = ImageTk.PhotoImage(text_background_image_resized)

# Create a label for the text with the background image
text_label = tk.Label(window, image=text_background_image_tk, compound=tk.CENTER, text=intro_text, font=('Courier', 12), fg='white', justify='left', padx=0, pady=0, bg= 'black')
text_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
text_label.image = text_background_image_tk  # Keep a reference to avoid garbage collection

# Hide the intro_label as it's no longer needed
intro_label.destroy()

# Create labels
borough_label = ttk.Label(window, text="Ideal Borough:", font=('Arial', 13))
prev_county_label = ttk.Label(window, text="Comparative Borough:", font=('Arial', 13))

# Create entry boxes
borough_entry = ttk.Entry(window, width=30, font=('Arial', 13))
prev_borough_entry = ttk.Entry(window, width=30, font=('Arial', 13))

entries = []
entries.append(borough_entry)
entries.append(prev_borough_entry)



# Create submit button with a fully green background and black text
submit_button = ttk.Button(window, text="Submit",
                           command=lambda: foliumtest.highlight_boroughs(entries), style='Green.TButton')
customtkinter.set_appearance_mode("Dark")
style = ttk.Style()

style.configure('Green.TButton', background='#4CAF50', font=('Arial', 12), foreground='#000000')  # Green button with black text

# Place the widgets in the window using place layout
borough_label.place(relx=0.45, rely=0.75, anchor=tk.CENTER)
borough_entry.place(relx=0.6, rely=0.75, anchor=tk.CENTER)
prev_county_label.place(relx=0.43, rely=0.80, anchor=tk.CENTER)
prev_borough_entry.place(relx=0.6, rely=0.80, anchor=tk.CENTER)
submit_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

# Start the Tkinter event loop
window.mainloop()
