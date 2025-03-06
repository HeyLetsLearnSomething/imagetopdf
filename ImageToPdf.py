import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from fpdf import FPDF
from PIL import Image

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("500x400")
        self.root.configure(bg="#2E2E2E")
        
        self.image_paths = []
        self.output_pdf_path = ""
        
        # Frame for Image Selection
        image_frame = tk.Frame(root, bg="#2E2E2E")
        image_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(image_frame, text="Import Image(s) or Folder", fg="white", bg="#2E2E2E", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.image_buttons_frame = tk.Frame(image_frame, bg="#2E2E2E")
        self.image_buttons_frame.pack(pady=5)
        
        tk.Button(self.image_buttons_frame, text="Select Images", command=self.select_images, bg="#444", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(self.image_buttons_frame, text="Select Folder", command=self.select_folder, bg="#444", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        
        self.image_location_label = tk.Label(image_frame, text="No images selected", fg="white", bg="#2E2E2E", font=("Arial", 10))
        self.image_location_label.pack(pady=5)
        
        # Frame for PDF Save Location
        pdf_frame = tk.Frame(root, bg="#2E2E2E")
        pdf_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(pdf_frame, text="Export Location", fg="white", bg="#2E2E2E", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.pdf_location_label = tk.Label(pdf_frame, text="No save location selected", fg="white", bg="#2E2E2E", font=("Arial", 10))
        self.pdf_location_label.pack(pady=5)
        
        tk.Button(pdf_frame, text="Choose Save Location", command=self.select_output_location, bg="#444", fg="white", font=("Arial", 10), width=20).pack(pady=5)
        
        # Convert Button
        tk.Button(root, text="Convert to PDF", command=self.convert_to_pdf, bg="#007BFF", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=20)
    
    def select_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff")])
        if files:
            self.image_paths = list(files)
            self.image_location_label.config(text=f"{len(self.image_paths)} images selected")
            messagebox.showinfo("Success", f"{len(self.image_paths)} images selected!")
    
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.image_paths = [os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"))]
            self.image_location_label.config(text=f"{len(self.image_paths)} images found in folder")
            messagebox.showinfo("Success", f"{len(self.image_paths)} images found!")
    
    def select_output_location(self):
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file:
            self.output_pdf_path = file
            self.pdf_location_label.config(text=f"Save to: {os.path.basename(file)}")
            messagebox.showinfo("Success", "Output location selected!")
    
    def convert_to_pdf(self):
        if not self.image_paths:
            messagebox.showerror("Error", "No images selected!")
            return
        if not self.output_pdf_path:
            messagebox.showerror("Error", "No output location selected!")
            return
        
        pdf = FPDF()
        for image_path in self.image_paths:
            with Image.open(image_path) as img:
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                    img.save(image_path)
                width, height = img.size
                if width > height:
                    img = img.transpose(Image.ROTATE_270)
                    img.save(image_path)
            pdf.add_page()
            pdf.image(image_path, 0, 0, 210, 297)
        
        pdf.output(self.output_pdf_path, "F")
        messagebox.showinfo("Success", "PDF successfully created!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()