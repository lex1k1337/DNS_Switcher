import tkinter as tk
from tkinter import messagebox
import os
import re


class DnsPreset:
    def __init__(self, name, primary_dns, secondary_dns):
        self.name = name
        self.primary_dns = primary_dns
        self.secondary_dns = secondary_dns


def create_preset():
    name = name_entry.get()
    primary_dns = primary_dns_entry.get()
    secondary_dns = secondary_dns_entry.get()

    presets.append(DnsPreset(name, primary_dns, secondary_dns))
    save_presets_to_file(presets, filename)
    messagebox.showinfo("Success", f"Preset '{name}' successfully created!")


def save_presets_to_file(presets, filename):
    with open(filename, "w") as file:
        for preset in presets:
            file.write(f"{preset.name},{preset.primary_dns},{preset.secondary_dns}\n")


def load_presets_from_file(filename):
    presets = []
    try:
        with open(filename, "r") as file:
            for line in file:
                name, primary_dns, secondary_dns = line.strip().split(",")
                presets.append(DnsPreset(name, primary_dns, secondary_dns))
    except FileNotFoundError:
        pass
    return presets


def set_dns_manually(primary_dns, secondary_dns):
    os.system(f"netsh interface ipv4 set dns name=Ethernet source=static address={primary_dns} register=primary")
    if secondary_dns:
        os.system(f"netsh interface ipv4 add dns name=Ethernet address={secondary_dns} index=2")


def set_dns_to_automatic():
    os.system("netsh interface ipv4 set dns name=Ethernet source=dhcp")


def get_current_dns():
    result = os.popen("netsh interface ipv4 show dns name=Ethernet").read()
    dns_servers = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", result)
    return dns_servers


def apply_automatic_dns():
    set_dns_to_automatic()
    messagebox.showinfo("Success", "DNS set to automatic.")


def apply_preset_dns(preset_index):
    if 0 <= preset_index < len(presets):
        set_dns_manually(presets[preset_index].primary_dns, presets[preset_index].secondary_dns)
        messagebox.showinfo("Success", f"DNS set according to preset '{presets[preset_index].name}'.")
    else:
        messagebox.showerror("Error", "Invalid preset number.")


def show_presets():
    preset_list = "\n".join([preset.name for preset in presets])
    messagebox.showinfo("Presets", f"Available presets:\n{preset_list}")


def main():
    global name_entry, primary_dns_entry, secondary_dns_entry, presets, filename

    filename = "dns_presets.txt"
    presets = load_presets_from_file(filename)

    window = tk.Tk()
    window.title("DNS Presets")

    tk.Label(window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Primary DNS:").grid(row=1, column=0)
    primary_dns_entry = tk.Entry(window)
    primary_dns_entry.grid(row=1, column=1)

    tk.Label(window, text="Secondary DNS:").grid(row=2, column=0)
    secondary_dns_entry = tk.Entry(window)
    secondary_dns_entry.grid(row=2, column=1)

    create_button = tk.Button(window, text="Create Preset", command=create_preset)
    create_button.grid(row=3, column=0, columnspan=2)

    current_dns_button = tk.Button(window, text="Show Current DNS", command=lambda: messagebox.showinfo("Current DNS",
                                                                                                        f"Current DNS servers: {', '.join(get_current_dns())}"))
    current_dns_button.grid(row=4, column=0, columnspan=2)

    automatic_dns_button = tk.Button(window, text="Apply Automatic DNS", command=apply_automatic_dns)
    automatic_dns_button.grid(row=5, column=0, columnspan=2)

    preset_dns_button = tk.Button(window, text="Apply Preset DNS",
                                  command=lambda: apply_preset_dns(int(preset_entry.get()) - 1))
    preset_dns_button.grid(row=6, column=0, columnspan=2)

    tk.Label(window, text="Preset Number:").grid(row=7, column=0)
    preset_entry = tk.Entry(window)
    preset_entry.grid(row=7, column=1)

    show_presets_button = tk.Button(window, text="Show Presets", command=show_presets)
    show_presets_button.grid(row=8, column=0, columnspan=2)

    window.mainloop()
    #qwerty


if __name__ == "__main__":
    main()
