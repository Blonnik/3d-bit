from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from moviepy.editor import VideoClip

def create_rotating_gif(image_path, output_path, size=(200, 200), duration=2, fps=30):
    """
    Tworzy GIF z realistycznym obrotem obrazu względem osi Y (efekt 3D z przeźroczystym tłem).

    :param image_path: Ścieżka do obrazu wejściowego (PNG, JPG itp.)
    :param output_path: Ścieżka do zapisu wygenerowanego GIF-a
    :param size: Rozmiar obrazu (szerokość, wysokość)
    :param duration: Czas trwania animacji w sekundach
    :param fps: Liczba klatek na sekundę
    """
    try:
        # Otwórz obraz
        image = Image.open(image_path).convert("RGBA")

        # Zmień rozmiar obrazu
        image = image.resize(size, Image.Resampling.LANCZOS)

        # Wymiary obrazu
        width, height = image.size

        def make_frame(t):
            """
            Funkcja generująca pojedynczą klatkę w danym czasie t.
            """
            angle = (t / duration) * 360  # Oblicz kąt na podstawie czasu
            rad_angle = np.radians(angle)

            # Wylicz współczynnik "perspektywy" dla osi Y
            scale = abs(np.cos(rad_angle))

            # Przeskaluj szerokość obrazu w zależności od kąta
            new_width = max(1, int(width * scale))
            scaled_image = image.resize((new_width, height), Image.Resampling.LANCZOS)

            # Odwróć obraz, gdy jest obrócony o > 90 i < 270 stopni (tył obrazu)
            if 90 < angle % 360 < 270:
                scaled_image = scaled_image.transpose(Image.FLIP_LEFT_RIGHT)

            # Stwórz przezroczyste tło
            background = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            offset = ((width - new_width) // 2, 0)  # Wyśrodkowanie na osi X
            background.paste(scaled_image, offset, scaled_image)

            return np.array(background)

        # Utwórz animację za pomocą MoviePy
        animation = VideoClip(make_frame, duration=duration)
        animation.write_gif(output_path, fps=fps, program="ffmpeg")

        print(f"GIF zapisano jako: {output_path}")
        messagebox.showinfo("Sukces", f"GIF zapisano jako: {output_path}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Obrazy", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        if output_path:
            create_rotating_gif(file_path, output_path)

if __name__ == "__main__":
    # Tworzenie GUI
    root = tk.Tk()
    root.title("Tworzenie GIF-a z obrotem obrazu")

    # Etykieta tytułu
    label = tk.Label(root, text="Wybierz obraz do utworzenia GIF-a", font=("Arial", 14))
    label.pack(pady=20)

    # Przycisk do wyboru pliku
    select_button = tk.Button(root, text="Wybierz plik", command=select_file, font=("Arial", 12))
    select_button.pack(pady=10)

    # Uruchomienie aplikacji
    root.mainloop()
