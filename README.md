## Streamlit Dashboard with Google collab
#### Instalasi streamlit di Google Colab
!pip install streamlit


#### Masukkan code untuk aplikasi streamlit
%%writefile dashboard.py

import streamlit as st

#### Dapatkan IP
!wget -q -O - ipv4.icanhazip.com


#### Jalankan aplikasi streamlit
!streamlit run dashboard.py & npx localtunnel --port 8501


Silakan isi field Endpoint IP dengan External URL lalu Submit
