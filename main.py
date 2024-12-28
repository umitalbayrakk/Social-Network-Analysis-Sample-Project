from social_network import SocialNetwork

def main():
    # Sosyal ağ örneği oluştur
    social_net = SocialNetwork()
    
    # Örnek kullanıcılar ekle
    users = ["Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Zeynep"]
    for user in users:
        social_net.add_user(user)
    
    # Örnek arkadaşlık ilişkileri ekle
    friendships = [
        ("Ahmet", "Mehmet"),
        ("Ahmet", "Ayşe"),
        ("Mehmet", "Ali"),
        ("Ayşe", "Fatma"),
        ("Fatma", "Zeynep"),
        ("Zeynep", "Ahmet"),
        ("Ali", "Ayşe")
    ]
    
    for friendship in friendships:
        social_net.add_friendship(friendship[0], friendship[1])
    
    # Analizler
    print("\nPopüler Kullanıcılar:")
    popular_users = social_net.get_popular_users(3)
    for user, friend_count in popular_users:
        print(f"{user}: {friend_count} arkadaş")
    
    print("\nAhmet'in arkadaşları:")
    print(social_net.get_friends("Ahmet"))
    
    # Ağı görselleştir
    social_net.visualize_network()

if __name__ == "__main__":
    main() 