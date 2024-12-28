import tkinter as tk
from tkinter import ttk, messagebox
from social_network import SocialNetwork

class SocialNetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sosyal Ağ Analizi")
        self.social_net = SocialNetwork()
        
        # Ana frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Kullanıcı ekleme bölümü
        ttk.Label(self.main_frame, text="Yeni Kullanıcı:").grid(row=0, column=0, pady=5)
        self.user_entry = ttk.Entry(self.main_frame)
        self.user_entry.grid(row=0, column=1, pady=5)
        ttk.Button(self.main_frame, text="Kullanıcı Ekle", 
                  command=self.add_user).grid(row=0, column=2, pady=5)
        
        # Arkadaşlık ekleme bölümü
        ttk.Label(self.main_frame, text="Kullanıcı 1:").grid(row=1, column=0, pady=5)
        self.user1_entry = ttk.Entry(self.main_frame)
        self.user1_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.main_frame, text="Kullanıcı 2:").grid(row=2, column=0, pady=5)
        self.user2_entry = ttk.Entry(self.main_frame)
        self.user2_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(self.main_frame, text="Arkadaşlık Ekle", 
                  command=self.add_friendship).grid(row=2, column=2, pady=5)
        
        # Kullanıcı listesi
        ttk.Label(self.main_frame, text="Kullanıcılar:").grid(row=3, column=0, pady=5)
        self.user_listbox = tk.Listbox(self.main_frame, height=6)
        self.user_listbox.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Butonlar
        ttk.Button(self.main_frame, text="Ağı Görselleştir", 
                  command=self.visualize).grid(row=5, column=0, pady=5)
        ttk.Button(self.main_frame, text="Popüler Kullanıcılar", 
                  command=self.show_popular_users).grid(row=5, column=1, pady=5)
        
        # Örnek veri yükleme butonu
        ttk.Button(self.main_frame, text="Örnek Veri Yükle", 
                  command=self.load_sample_data).grid(row=5, column=2, pady=5)
    
    def add_user(self):
        username = self.user_entry.get().strip()
        if username:
            if self.social_net.add_user(username):
                self.update_user_list()
                self.user_entry.delete(0, tk.END)
                messagebox.showinfo("Başarılı", f"{username} ağa eklendi!")
            else:
                messagebox.showerror("Hata", "Bu kullanıcı zaten var!")
        else:
            messagebox.showerror("Hata", "Kullanıcı adı boş olamaz!")
    
    def add_friendship(self):
        user1 = self.user1_entry.get().strip()
        user2 = self.user2_entry.get().strip()
        if user1 and user2:
            if self.social_net.add_friendship(user1, user2):
                self.user1_entry.delete(0, tk.END)
                self.user2_entry.delete(0, tk.END)
                messagebox.showinfo("Başarılı", "Arkadaşlık bağı oluşturuldu!")
            else:
                messagebox.showerror("Hata", "Kullanıcılar bulunamadı!")
        else:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")
    
    def update_user_list(self):
        self.user_listbox.delete(0, tk.END)
        for user in self.social_net.network.nodes():
            self.user_listbox.insert(tk.END, user)
    
    def visualize(self):
        self.social_net.visualize_network()
    
    def show_popular_users(self):
        popular_users = self.social_net.get_popular_users(3)
        message = "En popüler kullanıcılar:\n\n"
        for user, count in popular_users:
            message += f"{user}: {count} arkadaş\n"
        messagebox.showinfo("Popüler Kullanıcılar", message)
    
    def load_sample_data(self):
        # Örnek kullanıcılar
        users = ["Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Zeynep"]
        for user in users:
            self.social_net.add_user(user)
        
        # Örnek arkadaşlıklar
        friendships = [
            ("Ahmet", "Mehmet"),
            ("Ahmet", "Ayşe"),
            ("Mehmet", "Ali"),
            ("Ayşe", "Fatma"),
            ("Fatma", "Zeynep"),
            ("Zeynep", "Ahmet"),
            ("Ali", "Ayşe")
        ]
        
        for user1, user2 in friendships:
            self.social_net.add_friendship(user1, user2)
        
        self.update_user_list()
        messagebox.showinfo("Başarılı", "Örnek veri yüklendi!")

def main():
    root = tk.Tk()
    app = SocialNetworkGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 