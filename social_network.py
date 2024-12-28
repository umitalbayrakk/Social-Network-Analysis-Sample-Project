import networkx as nx
import matplotlib.pyplot as plt
import community
from datetime import datetime

class SocialNetwork:
    def __init__(self):
        self.network = nx.Graph()
        
    def add_user(self, username, color="#1f77b4", **attributes):
        """Ağa yeni bir kullanıcı ekler"""
        if username not in self.network.nodes():
            attributes['color'] = color
            attributes['join_date'] = datetime.now()
            self.network.add_node(username, **attributes)
            return True
        return False
    
    def add_friendship(self, user1, user2, weight=1, **attributes):
        """İki kullanıcı arasında arkadaşlık bağı oluşturur"""
        if user1 in self.network.nodes() and user2 in self.network.nodes():
            attributes['weight'] = weight
            attributes['created_at'] = datetime.now()
            self.network.add_edge(user1, user2, **attributes)
            return True
        return False
    
    def get_friends(self, username):
        """Bir kullanıcının arkadaşlarını listeler"""
        if username in self.network.nodes():
            return list(self.network.neighbors(username))
        return []
    
    def get_popular_users(self, n=5):
        """En çok arkadaşı olan n kullanıcıyı döndürür"""
        degrees = dict(self.network.degree())
        return sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_network_stats(self):
        """Ağ istatistiklerini hesaplar"""
        stats = {
            'density': nx.density(self.network),
            'clustering': nx.average_clustering(self.network),
            'avg_path_length': 0
        }
        
        if len(self.network.nodes()) > 1:
            try:
                stats['avg_path_length'] = nx.average_shortest_path_length(self.network)
            except nx.NetworkXError:
                stats['avg_path_length'] = float('inf')
                
        return stats
    
    def detect_communities(self):
        """Toplulukları tespit eder"""
        partition = community.best_partition(self.network)
        communities = {}
        for node, community_id in partition.items():
            if community_id not in communities:
                communities[community_id] = []
            communities[community_id].append(node)
        return list(communities.values())
    
    def get_user_connections(self, username):
        """Bir kullanıcının tüm bağlantılarını detaylı olarak getirir"""
        if username not in self.network.nodes():
            return []
            
        connections = []
        for neighbor in self.network.neighbors(username):
            edge_data = self.network[username][neighbor]
            connections.append({
                'with': neighbor,
                'type': edge_data.get('relationship_type', 'Arkadaş'),
                'weight': edge_data.get('weight', 1),
                'date': edge_data.get('date', 'Belirtilmemiş'),
                'notes': edge_data.get('notes', '')
            })
        return connections
    
    def visualize_network(self):
        """Sosyal ağı görselleştirir"""
        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(self.network)
        nx.draw(self.network, pos, with_labels=True, node_color='lightblue', 
                node_size=1500, font_size=10, font_weight='bold')
        plt.title("Sosyal Ağ Görselleştirmesi")
        plt.show() 