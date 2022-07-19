import tkinter as tk
from tkinter import ttk, END
import json
import requests

# currency list
api_key = 'b6be16e9b424f098861980388c1036f0bd605c99'
url_list = "https://api.getgeoapi.com/v2/currency/list?api_key={}&format=json".format(api_key)
response = requests.get(url_list)
data = json.loads(response.text)
del data["status"]


class dictionary(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


currency_list = dictionary()
currency_list2 = list()

for x, y in data.items():
    for key in y:
        currency_list.key = key
        currency_list.value = y[key]
        currency_list.add(currency_list.key, currency_list.value)
        currency_list2.append(currency_list.key + ":" + currency_list.value)

# two lists for printing curriencies in combobox
print(currency_list)
print(currency_list2)

# Define window
root = tk.Tk()
root.title('Currency Conversion')
# root.iconbitmap('ruler.ico')
root.resizable(0, 0)

# Define fonts and colors
field_font = ('Cambria', 10)
bg_color = "gray"
button_color = "#f5cf87"
root.config(bg=bg_color)


# Define functions
def convert():
    # Clear the output field
    output_field.delete(0, END)
    # Get all user information
    from_currency1 = input_combobox.get()
    from_currency = from_currency1[0:3]
    to_currency1 = output_combobox.get()
    to_currency = to_currency1[0:3]
    currency_amount = float(input_field.get())

    if from_currency in currency_list.keys():
        if to_currency in currency_list.keys():

            url_convert = "https://api.getgeoapi.com/v2/currency/convert?api_key={}&from={}&to={}&amount={}&format=json".format(
                api_key, from_currency, to_currency, currency_amount)
            print(url_convert)
            response2 = requests.get(url_convert)
            data2 = json.loads(response2.text)
            rates = (data2.get("rates"))
            rates2 = (rates.get(to_currency))
            rates3 = (rates2.get("rate_for_amount"))
            print(rates3)

            # Update output field with answer
            output_field.insert(0, str(rates3))
        else:
            output_combobox.set("That is not a currency!")
    else:
        input_combobox.set("That is not a currency!")


# Define layout
# Create the input and output entry fields
input_field = tk.Entry(root, width=20, font=field_font, borderwidth=3)
output_field = tk.Entry(root, width=20, font=field_font, borderwidth=3)
equal_label = tk.Label(root, text="=", font=field_font, bg=bg_color)

input_field.grid(row=0, column=0, padx=10, pady=10)
equal_label.grid(row=0, column=1, padx=10, pady=10)
output_field.grid(row=0, column=2, padx=10, pady=10)

input_field.insert(0, 'Enter your quantity')

# Create combobox for currencies
input_combobox = ttk.Combobox(root, value=sorted(list(currency_list2)), font=field_font, justify='center')

output_combobox = ttk.Combobox(root, value=sorted(list(currency_list2)), font=field_font, justify='center')

to_label = tk.Label(root, text="to", font=field_font, bg=bg_color)

input_combobox.grid(row=1, column=0, padx=10, pady=10)
to_label.grid(row=1, column=1, padx=10, pady=10)
output_combobox.grid(row=1, column=2, padx=10, pady=10)

input_combobox.set('initial currency')
output_combobox.set('final currency')

# Create a conversion button
convert_button = tk.Button(root, text='Convert', font=field_font, bg=button_color, command=convert)

convert_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, ipadx=50)

# Run the root window's main loop
root.mainloop()