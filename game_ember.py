import streamlit as st
from collections import deque

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Water Jug Problem", page_icon="💧", layout="centered")

# --- INISIALISASI STATE GAME (SESSION STATE) ---
if 'current_state' not in st.session_state:
    st.session_state.current_state = [0, 0, 0]
if 'moves_count' not in st.session_state:
    st.session_state.moves_count = 0
if 'selected_jug' not in st.session_state:
    st.session_state.selected_jug = None
if 'show_hint' not in st.session_state:
    st.session_state.show_hint = False

capacities = (8, 5, 3)
goal_state = (4, 4, 0)

# --- FUNGSI AKSI LOGIKA ---
def reset_game():
    st.session_state.current_state = [0, 0, 0]
    st.session_state.moves_count = 0
    st.session_state.selected_jug = None
    st.session_state.show_hint = False

def fill_jug(idx):
    if st.session_state.current_state[idx] < capacities[idx]:
        st.session_state.current_state[idx] = capacities[idx]
        st.session_state.moves_count += 1
    st.session_state.selected_jug = None

def dump_jug(idx):
    if st.session_state.current_state[idx] > 0:
        st.session_state.current_state[idx] = 0
        st.session_state.moves_count += 1
    st.session_state.selected_jug = None

def pour_jug(src, dst):
    pour_amount = min(st.session_state.current_state[src], capacities[dst] - st.session_state.current_state[dst])
    if pour_amount > 0:
        st.session_state.current_state[src] -= pour_amount
        st.session_state.current_state[dst] += pour_amount
        st.session_state.moves_count += 1
    st.session_state.selected_jug = None

# --- HEADER INTERFACE ---
st.title("💧 Water Jug Problem")
st.markdown("### Target: **A = 4L B = 4L C = 0L**")

# Skor & Tombol Reset Atas
col_sc, col_rs = st.columns([3, 1])
with col_sc:
    st.metric(label="Langkah Anda", value=st.session_state.moves_count)
with col_rs:
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    if st.button(" Ulangi Game", use_container_width=True):
        reset_game()
        st.rerun()

st.divider()

# Cek Status Menang
game_won = tuple(st.session_state.current_state) == goal_state

# --- GRID EMBER (MENGGUNAKAN SIMULASI TEKS GEOMETRIS YANG AMAN) ---
names = ['A', 'B', 'C']
cols = st.columns(3)

for idx, col in enumerate(cols):
    with col:
        # Menentukan tanda panah penunjuk jika ember sedang dipilih
        status_pilih = "👉 [DIPILIH] 👈" if st.session_state.selected_jug == idx else ""
        st.markdown(f"<p style='text-align:center; color:#00f2fe; font-weight:bold;'>{status_pilih}</p>", unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='text-align: center; color: #c8d2f5;'>Ember {names[idx]} ({capacities[idx]}L)</h3>", unsafe_allow_html=True)
        
        # Menggambar isi ember trapesium menggunakan teks balok karakter yang stabil di semua browser
        current_water = st.session_state.current_state[idx]
        max_water = capacities[idx]
        
        bucket_art = ""
        # Gambar baris demi baris dari atas ke bawah
        for level in range(max_water, 0, -1):
            if level <= current_water:
                # Bagian yang terisi air (Warna biru jernih)
                bucket_art += "<span style='color:#3498db; font-size:24px;'>████████</span><br>"
            else:
                # Bagian ember yang kosong (Abu-abu gelap)
                bucket_art += "<span style='color:#3e445e; font-size:24px;'>░░░░░░░░</span><br>"
        
        # Tatakan bawah ember agar terlihat mengerucut
        bucket_art += "<span style='color:#c8d2f5; font-size:20px;'>\______/</span>"
        
        # Tampilkan ke layar
        st.markdown(f"<div style='text-align: center; line-height: 0.9; letter-spacing: 2px;'>{bucket_art}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: #ffffff;'>{current_water} / {max_water} L</h2>", unsafe_allow_html=True)
        
        # Tombol Interaksi per Ember
        if not game_won:
            if st.button(f"👆 Pilih / Tuang {names[idx]}", key=f"btn_{idx}", use_container_width=True):
                if st.session_state.selected_jug == idx:
                    st.session_state.selected_jug = None
                elif st.session_state.selected_jug is not None:
                    pour_jug(st.session_state.selected_jug, idx)
                    st.rerun()
                else:
                    st.session_state.selected_jug = idx
                    st.rerun()

st.markdown("<p style='text-align: center; color: #6c757d; font-size: 14px;'>💡 <b>Cara Menuang:</b> Klik tombol 'Pilih/Tuang' pada ember asal, lalu klik tombol 'Pilih/Tuang' pada ember tujuan.</p>", unsafe_allow_html=True)
st.divider()

# --- PANEL KONTROL GLOBAL (FILL & DUMP) ---
if not game_won:
    col_f, col_d, col_h = st.columns(3)
    
    with col_f:
        if st.button("🟢 ISI PENUH", use_container_width=True, disabled=st.session_state.selected_jug is None):
            fill_jug(st.session_state.selected_jug)
            st.rerun()
            
    with col_d:
        if st.button("🟠 BUANG AIR", use_container_width=True, disabled=st.session_state.selected_jug is None):
            dump_jug(st.session_state.selected_jug)
            st.rerun()
            
    with col_h:
        if st.button("🟡 PETUNJUK ", use_container_width=True):
            st.session_state.show_hint = not st.session_state.show_hint
            st.rerun()

# Tampilan Contekan Langkah Rute Tercepat (BFS)
if st.session_state.show_hint and not game_won:
    st.info("**CARA BERMAIN :**\n\n"
            "- Ember hanya bisa diisi penuh atau dibuang sampai habis\n"
            "- Ember hanya bisa dituang sampai habis atau sampai penuh\n\n\n"

        "**Goodluck**")
    #("**Urutan Solusi Optimal (Ember A, B, C):**\n\n"
            #"[0,0,0] → [8,0,0] → [3,5,0] → [3,2,3] → [6,2,0] → [6,0,2] → [1,5,2] → [1,4,3] → **[4,4,0]** 🏆 (8 Langkah)")

# --- NOTIFIKASI KEMENANGAN ---
if game_won:
    st.balloons()
    st.success("🎉 **KEMENANGAN! ANDA BERHASIL!** 🎉")
    st.markdown(f"""
    * **Total Langkah Anda:** {st.session_state.moves_count} langkah.
    * **Rekor Optimal Komputer:** 8 langkah.
    """)
    if st.session_state.moves_count == 8:
        st.balloons()
        st.info("🏆 **SKOR SEMPURNA!** Strategi Anda se-efisien kecerdasan buatan (AI)!")
    else:
        st.warning("Bagus! Coba tekan 'Ulangi Game' untuk mencoba memecahkannya dengan rute yang lebih pendek!")