import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os

class ZipExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zip File Extractor")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # zip file path
        self.zip_path = tk.StringVar()
        # Output directory path
        self.output_dir = tk.StringVar()
        #Password field
        self.password = tk.StringVar()

        # UI Elements
        tk.Label(root,text="Zip File Extractor", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root,text="Select Zip File:").pack(anchor="w", padx=20, pady=5)
        tk.Entry(root,textvariable=self.zip_path,width=50,).pack(padx=20)
        tk.Button(root,text="Browse",command=self.browse_zip).pack(pady=5)
        tk.Label(root,text="Select Output Folder:").pack(anchor="w", padx=20, pady=5)
        tk.Entry(root,textvariable=self.output_dir, width=50).pack(padx=20)
        tk.Button(root,text="Browse",command=self.browse_output).pack(pady=5)
        tk.Label(root,text="Password (if any):").pack(anchor="w",padx=20, pady=5)
        tk.Entry(root,textvariable=self.password, width=30,show="*").pack(padx=20)
        tk.Button(root,text="Extract",command=self.extract_zip,bg="green",fg="white",width=15).pack(pady=15)
        
        self.result_box = tk.Listbox(root, width=65, height=10)
        self.result_box.pack(padx=20, pady=10)

    def browse_zip(self):
        file_path = filedialog.askopenfilename(filetypes=[("Zip Files","*.zip")])
        if file_path:
            self.zip_path.set(file_path)

    def browse_output(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_dir.set(folder_path)
    
    def extract_zip(self):
        zip_file = self.zip_path.get()
        output_dir = self.output_dir.get()
        pwd = self.password.get()

        if not zip_file or not output_dir:
            messagebox.showerror("Error", "Please select both zip file and output folder")
            return
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                if pwd:
                    zip_ref.extractall(output_dir, pwd=bytes(pwd, 'utf-8'))
                else:
                    zip_ref.extractall(output_dir)
                messagebox.showinfo("Success", "Extraction completed successfully!")

                # Show extract files in listbox
                self.result_box.delete(0, tk.END)
                for file in zip_ref.namelist():
                    self.result_box.insert(tk.END,f" {file}")
        
        except RuntimeError:
            messagebox.showerror("Error", "Incorrect Password!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Zip file not found!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ZipExtractorApp(root)
    root.mainloop()