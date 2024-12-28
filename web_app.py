import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from social_network import SocialNetwork
import random
from datetime import datetime
import pandas as pd

# Sayfa yapılandırması
st.set_page_config(
    page_title="Sosyal Ağ Analizi",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .user-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum durumunu başlat
if 'social_net' not in st.session_state:
    st.session_state.social_net = SocialNetwork()
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []

def log_activity(action, details):
    """Aktivite kaydı tutar"""
    st.session_state.activity_log.append({
        'timestamp': datetime.now(),
        'action': action,
        'details': details
    })

# Ana başlık
st.title("🌐 Sosyal Ağ Analizi")

# Yan menü
with st.sidebar:
    st.header("📊 Kontrol Paneli")
    
    # Kullanıcı ekleme
    with st.expander("👤 Yeni Kullanıcı Ekle", expanded=True):
        new_user = st.text_input("Kullanıcı Adı")
        user_color = st.color_picker("Profil Rengi", "#1f77b4")
        user_info = st.text_area("Kullanıcı Hakkında", placeholder="Kullanıcı bilgilerini girin...")
        user_age = st.number_input("Yaş", min_value=13, max_value=100, value=25)
        user_location = st.text_input("Konum")
        
        if st.button("➕ Kullanıcı Ekle"):
            if new_user:
                if st.session_state.social_net.add_user(
                    new_user, 
                    color=user_color,
                    info=user_info,
                    age=user_age,
                    location=user_location
                ):
                    log_activity("Kullanıcı Eklendi", new_user)
                    st.success(f"✅ {new_user} ağa eklendi!")
                else:
                    st.error("❌ Bu kullanıcı zaten var!")
            else:
                st.error("❌ Kullanıcı adı boş olamaz!")

    # Arkadaşlık ekleme
    with st.expander("🤝 Arkadaşlık Bağı Ekle", expanded=True):
        users = list(st.session_state.social_net.network.nodes())
        user1 = st.selectbox("1. Kullanıcı", [""] + users)
        user2 = st.selectbox("2. Kullanıcı", [""] + [u for u in users if u != user1])
        
        col1, col2 = st.columns(2)
        with col1:
            connection_strength = st.slider("Bağ Gücü", 1, 10, 5)
        with col2:
            connection_type = st.selectbox("Bağ Tipi", 
                ["Arkadaş", "Yakın Arkadaş", "Aile", "İş", "Okul", "Hobi"])
        
        connection_date = st.date_input("Bağlantı Tarihi")
        connection_notes = st.text_area("Notlar", placeholder="Bağlantı hakkında notlar...")
        
        if st.button("🔗 Bağlantı Oluştur"):
            if user1 and user2:
                if st.session_state.social_net.add_friendship(
                    user1, user2, 
                    weight=connection_strength,
                    relationship_type=connection_type,
                    date=connection_date,
                    notes=connection_notes
                ):
                    log_activity("Bağlantı Eklendi", f"{user1} - {user2}")
                    st.success(f"✅ {connection_type} bağı oluşturuldu!")
                else:
                    st.error("❌ Kullanıcılar bulunamadı!")
            else:
                st.error("❌ İki kullanıcı da seçilmelidir!")

    # Analiz araçları
    with st.expander("🔍 Analiz Araçları", expanded=True):
        if st.button("🔄 Ağ İstatistiklerini Güncelle"):
            stats = st.session_state.social_net.get_network_stats()
            st.write("📊 Ağ Yoğunluğu:", f"{stats['density']:.2f}")
            st.write("🔄 Ortalama Kümelenme:", f"{stats['clustering']:.2f}")
            st.write("📏 Ortalama Yol Uzunluğu:", f"{stats['avg_path_length']:.2f}")
            
        if st.button("🎯 Toplulukları Tespit Et"):
            communities = st.session_state.social_net.detect_communities()
            for i, community in enumerate(communities, 1):
                st.write(f"Topluluk {i}:", ", ".join(community))

# Ana içerik
col1, col2 = st.columns([2, 1])

with col1:
    # Ağ görselleştirme
    st.header("🕸️ Ağ Görselleştirmesi")
    
    # Görselleştirme ayarları
    viz_col1, viz_col2 = st.columns(2)
    with viz_col1:
        node_size = st.slider("Düğüm Boyutu", 1000, 3000, 2000)
        edge_scale = st.slider("Bağlantı Kalınlığı", 0.1, 2.0, 0.5)
    with viz_col2:
        layout_type = st.selectbox("Yerleşim Tipi", 
            ["Spring", "Circular", "Random", "Shell"])
        show_labels = st.checkbox("Etiketleri Göster", True)

    if st.session_state.social_net.network.nodes():
        fig, ax = plt.subplots(figsize=(15, 10))
        
        # Yerleşim tipine göre pozisyonları hesapla
        if layout_type == "Spring":
            pos = nx.spring_layout(st.session_state.social_net.network, k=1, iterations=50)
        elif layout_type == "Circular":
            pos = nx.circular_layout(st.session_state.social_net.network)
        elif layout_type == "Random":
            pos = nx.random_layout(st.session_state.social_net.network)
        else:
            pos = nx.shell_layout(st.session_state.social_net.network)
        
        # Düğümleri çiz
        node_colors = [st.session_state.social_net.network.nodes[node].get('color', '#1f77b4') 
                      for node in st.session_state.social_net.network.nodes()]
        
        nx.draw_networkx_nodes(st.session_state.social_net.network, pos,
                              node_color=node_colors,
                              node_size=node_size)
        
        # Etiketleri çiz
        if show_labels:
            nx.draw_networkx_labels(st.session_state.social_net.network, pos,
                                  font_size=10, font_weight='bold',
                                  font_color='white')
        
        # Kenarları çiz
        edges = st.session_state.social_net.network.edges()
        edge_colors = []
        edge_widths = []
        
        for (u, v) in edges:
            edge_data = st.session_state.social_net.network[u][v]
            rel_type = edge_data.get('relationship_type', 'Arkadaş')
            weight = edge_data.get('weight', 1)
            
            color_map = {
                'Arkadaş': '#1f77b4',
                'Yakın Arkadaş': '#2ecc71',
                'Aile': '#e74c3c',
                'İş': '#f1c40f',
                'Okul': '#9b59b6',
                'Hobi': '#3498db'
            }
            edge_colors.append(color_map.get(rel_type, '#1f77b4'))
            edge_widths.append(weight * edge_scale)
        
        nx.draw_networkx_edges(st.session_state.social_net.network, pos,
                              edge_color=edge_colors,
                              width=edge_widths)
        
        # Bağ tiplerini göster
        legend_elements = [plt.Line2D([0], [0], color=color, label=rel_type, linewidth=2)
                          for rel_type, color in color_map.items()]
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
        
        plt.axis('off')
        st.pyplot(fig)

with col2:
    # Kullanıcı detayları
    st.header("👥 Kullanıcı Detayları")
    users = list(st.session_state.social_net.network.nodes(data=True))
    if users:
        for user, data in users:
            with st.expander(f"👤 {user}", expanded=False):
                st.markdown(f"""
                    **Konum:** {data.get('location', 'Belirtilmemiş')}  
                    **Yaş:** {data.get('age', 'Belirtilmemiş')}  
                    **Bağlantı Sayısı:** {st.session_state.social_net.network.degree(user)}  
                    
                    **Hakkında:**  
                    {data.get('info', 'Bilgi girilmemiş')}
                """)
                
                # Kullanıcının bağlantıları
                st.subheader("🔗 Bağlantıları")
                connections = st.session_state.social_net.get_user_connections(user)
                for connection in connections:
                    st.write(f"- {connection['with']}: {connection['type']} (Güç: {connection['weight']})")

    # Aktivite günlüğü
    st.header("📝 Aktivite Günlüğü")
    if st.session_state.activity_log:
        df = pd.DataFrame(st.session_state.activity_log)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.dataframe(df.sort_values('timestamp', ascending=False))
    else:
        st.info("Henüz aktivite kaydı yok.")

# Ağ istatistikleri
st.header("📊 Ağ İstatistikleri")
stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.metric("Toplam Kullanıcı", len(st.session_state.social_net.network.nodes()))
with stats_col2:
    st.metric("Toplam Bağlantı", len(st.session_state.social_net.network.edges()))
with stats_col3:
    density = nx.density(st.session_state.social_net.network)
    st.metric("Ağ Yoğunluğu", f"{density:.2f}")
with stats_col4:
    if len(st.session_state.social_net.network.nodes()) > 0:
        clustering = nx.average_clustering(st.session_state.social_net.network)
        st.metric("Kümelenme Katsayısı", f"{clustering:.2f}") 