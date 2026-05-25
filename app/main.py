import streamlit as st
import base64
import pandas as pd
import joblib
import calendar
import numpy as np
import plotly.express as px

st.set_page_config(page_title="SALMAR", page_icon="✈️", layout="wide")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_page_bg(bin_file):
    try:
        bin_str = get_base64_of_bin_file(bin_file)
        page_bg_img = '''
        <style>
        .stApp {
            background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                            url("data:image/jpeg;base64,%s");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .hero-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 120px !important;
        font-weight: 900 !important;
        color: #1a1a1a !important;
        text-align: center;
        margin-top: 80px;        
        letter-spacing: -4px;
        line-height: 1;
        text-shadow: 2px 2px 25px rgba(255, 255, 255, 0.9), 
                    0px 0px 40px rgba(255, 255, 255, 0.7);
    }

        .hero-subtitle {
            font-size: 20px !important;
            color: #1a1a1a !important;
            text-align: center;
            margin-bottom: 30px;
            font-weight: 700;
            letter-spacing: 1.5px;
            background-color: rgba(255, 255, 255, 0.6);
            display: block;
            width: fit-content;
            margin-left: auto;
            margin-right: auto;
            padding: 6px 20px;
            border-radius: 30px;
            backdrop-filter: blur(5px);
        }

        .salmar-logo {
            position: fixed;
            top: 160px;
            left: 170px;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 38px;
            font-weight: 900;
            color: #0ea68c;
            letter-spacing: -1px;
            z-index: 9999;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 80px;
            justify-content: center;
            background-color: rgba(255,255,255,1);
            padding: 20px 100px;
            border-radius: 100px;
            backdrop-filter: none;
            border: 1px solid rgba(200,200,200,0.6);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #1a1a1a !important;
            font-weight: 800 !important;
            font-size: 24px !important;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            color: #0ea68c !important;
            transform: scale(1.1);
        }

        .info-box {
            background: rgba(255, 255, 255, 0.92);
            color: #1a1a1a;
            padding: 25px;
            border-radius: 20px;
            height: 220px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            border-left: 10px solid #11caa0;
            text-align: left;
            margin-bottom: 20px;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 40px 20px;
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            text-align: center;
            color: #1a1a1a;
            margin-top: 10px;
            font-weight: 600;
        }
        
        .metric-label { 
            font-size: 13px; 
            color: #0ea68c; 
            font-weight: 800; 
            text-transform: uppercase; 
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        div[data-baseweb="select"] > div {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border-radius: 15px !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #11caa0, #0ea68c) !important;
            color: white !important;
            border-radius: 50px !important;
            padding: 15px 40px !important;
            font-weight: 800 !important;
            border: none !important;
        }

        div[data-testid="stTabsContent"]:not(:first-child) {
            background: white;
        }
        </style>
        ''' % bin_str
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except:
        st.warning("⚠️ Asegúrate de que el archivo 'foto_avion.jpg' esté en la misma carpeta.")

@st.cache_resource
def cargar_recursos():
    mod_b = joblib.load('modelos/predictor_carrier.pkl')
    mod_m = joblib.load('modelos/clasificador_gravedad.pkl')
    return mod_b, mod_m

@st.cache_data
def cargar_datos():
    df = pd.read_feather('data/vuelos_2024_sample.feather')
    df['Month_Name'] = df['month'].apply(lambda x: calendar.month_name[int(x)])
    if 'is_delayed' not in df.columns:
        df['is_delayed'] = (df['arr_delay'] > 0).astype(int)
    if 'cancelled' not in df.columns:
        df['cancelled'] = 0
    return df

def riesgo_ruta(origen, destino):
    ruta = vuelos[
        (vuelos['origin'] == origen) &
        (vuelos['dest'] == destino) &
        (vuelos['cancelled'] == 0)
    ].dropna(subset=['arr_delay'])

    if len(ruta) == 0:
        return None

    delay_final = ruta['arr_delay'].mean()

    if delay_final < 5:
        nivel, emoji, consejo = 'BAJO', '🟢', 'Buen momento para volar, retrasos mínimos esperados ¡Genial!'
    elif delay_final < 20:
        nivel, emoji, consejo = 'MEDIO', '🟡', 'Riesgo moderado, considera salir con margen'
    else:
        nivel, emoji, consejo = 'ALTO', '🔴', 'Alta probabilidad de retraso significativo, ten precaución'

    return {'delay': round(delay_final, 1), 'nivel': nivel, 'emoji': emoji, 'consejo': consejo}


def mejor_momento(origen, destino):
    ruta = vuelos[
        (vuelos['origin'] == origen) &
        (vuelos['dest'] == destino) &
        (vuelos['cancelled'] == 0)
    ].dropna(subset=['arr_delay'])

    if len(ruta) == 0:
        return None

    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    por_mes = ruta.groupby('month')['arr_delay'].mean()
    por_dia = ruta.groupby('day_of_week')['arr_delay'].mean()

    ruta2 = ruta.copy()
    ruta2['hora_salida'] = ruta2['crs_dep_time'] // 100
    por_hora = ruta2.groupby('hora_salida')['arr_delay'].mean()

    return {
        'mejor_mes': calendar.month_name[por_mes.idxmin()],
        'peor_mes': calendar.month_name[por_mes.idxmax()],
        'min_mejor_mes': round(por_mes.min(), 1),
        'min_peor_mes': round(por_mes.max(), 1),
        'mejor_dia': dias[por_dia.idxmin() - 1],
        'peor_dia': dias[por_dia.idxmax() - 1],
        'min_mejor_dia': round(por_dia.min(), 1),
        'min_peor_dia': round(por_dia.max(), 1),
        'mejor_hora': f"{por_hora.idxmin():02d}:00",
        'peor_hora': f"{por_hora.idxmax():02d}:00",
        'min_mejor_hora': round(por_hora.min(), 1),
        'min_peor_hora': round(por_hora.max(), 1),
    }


def informe_aerolinea(aerolinea):
    df_ae = vuelos[vuelos['aerolinea'] == aerolinea]
    if len(df_ae) == 0:
        return None
    por_mes = df_ae.groupby('month')['is_delayed'].mean() * 100
    por_mes = por_mes.reindex(range(1, 13), fill_value=0)
    valores = list(por_mes.values)
    meses = [calendar.month_name[i] for i in range(1, 13)]
    return {
        'total_vuelos': len(df_ae),
        'pct_medio_anual': round(df_ae['is_delayed'].mean() * 100, 1),
        'retraso_medio': round(df_ae['arr_delay'].mean(), 1),
        'mejor_mes': meses[valores.index(min(valores))],
        'peor_mes': meses[valores.index(max(valores))],
        'pct_mejor_mes': round(min(valores), 1),
        'pct_peor_mes': round(max(valores), 1),
        'variabilidad': round(np.std(valores), 1),
        'tendencia': 'mejora ↓' if valores[-1] < valores[0] else 'empeora ↑',
        'q1': round(np.mean(valores[0:3]), 1),
        'q2': round(np.mean(valores[3:6]), 1),
        'q3': round(np.mean(valores[6:9]), 1),
        'q4': round(np.mean(valores[9:12]), 1),
        'por_mes': dict(zip(meses, [round(v,1) for v in valores]))
    }


try:
    vuelos = cargar_datos()
    predictor_bin, clasificador_det = cargar_recursos()
    set_page_bg('app/foto_avion.jpg')
except Exception as e:
    st.error(f"Error cargando archivos: {e}")
    st.stop()

    
tab1, tab2, tab3, tab4 = st.tabs([" INICIO", " PREDICCIÓN IA", " RUTAS", " AEROLÍNEAS"])

with tab1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p class="hero-title">SALMAR</p>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; margin-bottom:30px;"><span style="font-size:20px; font-weight:700; letter-spacing:1.5px; color:#1a1a1a; background-color:rgba(255,255,255,0.6); padding:6px 20px; border-radius:30px;">APLICACIÓN INTERACTIVA PARA INFORMACIÓN RELATIVA A VUELOS DE ESTADOS UNIDOS</span></div>', unsafe_allow_html=True)    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('''
            <div class="info-box">
                <h4 style="color:#0ea68c; margin-top:0; font-size:1.5rem;">¿Qué es SALMAR?</h4>
                <p style="font-size: 1.05rem; line-height: 1.5;">
                    Nuestra plataforma utiliza algoritmos de <b>Inteligencia Artificial</b> avanzados para analizar 
                    el tráfico aéreo de Estados Unidos. Proporcionamos herramientas precisas para predecir retrasos 
                    y explorar rutas, optimizando la planificación de tus viajes mediante el uso de Big Data.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    with col_info2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('''
            <div class="info-box">
                <h4 style="color:#0ea68c; margin-top:0; font-size:1.5rem;">Importancia de la Información</h4>
                <p style="font-size: 1.05rem; line-height: 1.5;">
                    En la actualidad, conocer la puntualidad de un vuelo es <b>fundamental</b>. Permite a los usuarios 
                    gestionar mejor su tiempo, reducir el estrés en conexiones críticas y asegurar el cumplimiento 
                    de sus compromisos profesionales y personales en un mundo en constante movimiento.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-label">Módulo IA</div><h3>Predicción</h3><p>Clasifica la probabilidad de retraso mediante modelos predictivos.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-label">Histórico</div><h3>Rutas</h3><p>Analiza el comportamiento y eficiencia de rutas directas en 2024.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-label">Corporativo</div><h3>Aerolíneas</h3><p>Auditoría de cumplimiento y puntualidad por compañía aérea.</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 style='color:#1a1a1a; text-align:center;'> Simulador Predictivo</h2>", unsafe_allow_html=True)
    
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        orig = st.selectbox("✈️ Origen", options=sorted(vuelos['origin'].unique()), key="origen_p")
    with col_in2:
        dest = st.selectbox("🛬 Destino", options=sorted(vuelos[vuelos['origin'] == orig]['dest'].unique()), key="dest_p")
    with col_in3:
        aero = st.selectbox("🏢 Aerolínea", options=sorted(vuelos[(vuelos['origin'] == orig) & (vuelos['dest'] == dest)]['aerolinea'].unique()), key="aero_p")

    col_in4, col_in5, col_in6 = st.columns(3)
    with col_in4:
        mes = st.selectbox("📅 Mes", options=list(range(1, 13)), 
                           format_func=lambda x: calendar.month_name[x], key="mes_p")
    with col_in5:
        dia_mes = st.selectbox("📅 Día del mes", options=list(range(1, 32)), key="diames_p")
    with col_in6:
        dia_semana = st.selectbox("📆 Día de la semana", 
                                  options=list(range(1, 8)),
                                  format_func=lambda x: ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"][x-1],
                                  key="diasem_p")

    if st.button("EJECUTAR PREDICCIÓN"):
        df_p = pd.DataFrame({
            'aerolinea': [aero],
            'origin':    [orig],
            'dest':      [dest],
            'month':     [mes],
            'day_of_month': [dia_mes],
            'day_of_week':  [dia_semana],
        })
        p_b = predictor_bin.predict(df_p)[0]
        p_d = clasificador_det.predict(df_p)[0]

        res_a, res_b = st.columns(2)
        with res_a:
            st.markdown(f'<div class="metric-card" style="background:rgba(255,255,255,0.95);"><div class="metric-label">Predicción</div><div class="metric-value">{"Alta probabilidad de retraso por motivos de la aerolínea" if p_b == 1 else "Baja probabilidad de retraso por motivos de la aerolínea"}</div></div>', unsafe_allow_html=True)
        with res_b:
            st.markdown(f'<div class="metric-card" style="background:rgba(255,255,255,0.95); border-top: 5px solid #11caa0;"><div class="metric-label">Gravedad</div><div class="metric-value">{p_d}</div></div>', unsafe_allow_html=True)
with tab3:
    st.markdown("<h2 style='color:#1a1a1a; text-align:center;'>📍 Explorador de Trayectos</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#555; font-size:16px;'>Consulta el retraso medio real de esta ruta basado en vuelos históricos de 2024.</p>", unsafe_allow_html=True)

    h1, h2 = st.columns(2)
    o_h = h1.selectbox("✈️ Salida", sorted(vuelos['origin'].unique()), key="o3")
    d_h = h2.selectbox("🛬 Llegada", sorted(vuelos[vuelos['origin'] == o_h]['dest'].unique()), key="d3")

    if st.button("📊 VER INFORME HISTÓRICO", use_container_width=True):
        if o_h == d_h:
            st.warning("⚠️ Selecciona un destino diferente al origen.")
        else:
            res_m = mejor_momento(o_h, d_h)
            res_r = riesgo_ruta(o_h, d_h)

            if res_m and res_r:
                st.divider()
                st.markdown(f'''
                    <div style="text-align:center; background:rgba(255,255,255,0.85); 
                                backdrop-filter:blur(8px); padding:15px 30px; 
                                border-radius:20px; margin:10px auto; 
                                box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                        <h3 style="margin:0; color:#1a1a1a;">📍 Informe de Ruta: {o_h} → {d_h}</h3>
                    </div>
                ''', unsafe_allow_html=True)

                color_riesgo = {"BAJO": "#11caa0", "MEDIO": "#f5a623", "ALTO": "#e74c3c"}[res_r['nivel']]
                st.markdown(f'''
                    <div style="background:white; border-left: 8px solid {color_riesgo}; padding:20px; 
                                border-radius:15px; margin:15px 0; box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                        <h3 style="color:{color_riesgo}; margin:0;">{res_r['emoji']} Riesgo Histórico: {res_r['nivel']} (media de retraso: {res_r['delay']} min)</h3>
                        <p style="margin:8px 0 0 0; color:#555;">💡 {res_r['consejo']}</p>
                    </div>
                ''', unsafe_allow_html=True)

                st.divider()

                # Mejor y peor momento — ahora en minutos de retraso
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f'''
                        <div style="background:white; padding:20px; border-radius:15px; box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                            <p style="font-weight:800; font-size:16px; color:#0ea68c;">📅 MESES</p>
                            <p style="background:#d4edda; padding:8px 12px; border-radius:8px;">✅ Mejor: <b>{res_m['mejor_mes']}</b> ({res_m['min_mejor_mes']} min)</p>
                            <p style="background:#f8d7da; padding:8px 12px; border-radius:8px;">❌ Peor: <b>{res_m['peor_mes']}</b> ({res_m['min_peor_mes']} min)</p>
                        </div>
                    ''', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'''
                        <div style="background:white; padding:20px; border-radius:15px; box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                            <p style="font-weight:800; font-size:16px; color:#0ea68c;">📆 DÍAS</p>
                            <p style="background:#d4edda; padding:8px 12px; border-radius:8px;">✅ Mejor: <b>{res_m['mejor_dia']}</b> ({res_m['min_mejor_dia']} min)</p>
                            <p style="background:#f8d7da; padding:8px 12px; border-radius:8px;">❌ Peor: <b>{res_m['peor_dia']}</b> ({res_m['min_peor_dia']} min)</p>
                        </div>
                    ''', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'''
                        <div style="background:white; padding:20px; border-radius:15px; box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                            <p style="font-weight:800; font-size:16px; color:#0ea68c;">⏰ HORARIOS</p>
                            <p style="background:#d4edda; padding:8px 12px; border-radius:8px;">✅ Mejor: <b>{res_m['mejor_hora']}</b> ({res_m['min_mejor_hora']} min)</p>
                            <p style="background:#f8d7da; padding:8px 12px; border-radius:8px;">❌ Peor: <b>{res_m['peor_hora']}</b> ({res_m['min_peor_hora']} min)</p>
                        </div>
                    ''', unsafe_allow_html=True)
            else:
                st.error(f"🚫 No existen datos históricos suficientes para la ruta **{o_h} → {d_h}**.")

with tab4:
    st.markdown("<h2 style='color:#1a1a1a; text-align:center;'> Auditoría de Aerolíneas</h2>", unsafe_allow_html=True)
    ae = st.selectbox("Compañía", options=sorted(vuelos['aerolinea'].unique()))
    
    inf = informe_aerolinea(ae)
    
    if inf:
        k1, k2, k3, k4 = st.columns(4)
        tarjetas = [
            ("✈️ Vuelos", str(inf['total_vuelos']), "#11caa0"),
            ("⏱️ Retraso Medio", f"{inf['retraso_medio']}m", "#0ea68c"),
            ("📊 % Retrasos Anual", f"{inf['pct_medio_anual']}%", "#11caa0"),
            ("📈 Tendencia", inf['tendencia'], "#0ea68c"),
        ]
        for col, (label, valor, color) in zip([k1,k2,k3,k4], tarjetas):
            with col:
                st.markdown(f'''
                    <div style="background:white; padding:25px 15px; border-radius:20px;
                                text-align:center; box-shadow:0 6px 20px rgba(0,0,0,0.12);
                                border-top: 5px solid {color}; margin-bottom:15px;">
                        <p style="color:#0ea68c; font-size:12px; font-weight:800;
                                   text-transform:uppercase; letter-spacing:2px; margin-bottom:8px;">{label}</p>
                        <p style="font-size:26px; font-weight:900; color:#1a1a1a; margin:0;">{valor}</p>
                    </div>
                ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f'''
                <div style="background:white; padding:25px; border-radius:20px;
                            box-shadow:0 6px 20px rgba(0,0,0,0.12); margin-bottom:15px;">
                    <p style="color:#0ea68c; font-weight:800; font-size:16px; margin-bottom:15px;">📅 Mejor y Peor Mes</p>
                    <p style="background:#d4edda; padding:10px 15px; border-radius:10px; margin-bottom:8px;">
                        ✅ Mejor: <b>{inf['mejor_mes']}</b> — {inf['pct_mejor_mes']}% retrasos
                    </p>
                    <p style="background:#f8d7da; padding:10px 15px; border-radius:10px;">
                        ❌ Peor: <b>{inf['peor_mes']}</b> — {inf['pct_peor_mes']}% retrasos
                    </p>
                    <p style="color:#888; font-size:13px; margin-top:10px;">
                        Variabilidad (σ): {inf['variabilidad']} — {"Alta irregularidad" if inf['variabilidad'] > 10 else "Comportamiento estable"}
                    </p>
                </div>
            ''', unsafe_allow_html=True)

        with col_b:
            st.markdown(f'''
                <div style="background:white; padding:25px; border-radius:20px;
                            box-shadow:0 6px 20px rgba(0,0,0,0.12); margin-bottom:15px;">
                    <p style="color:#0ea68c; font-weight:800; font-size:16px; margin-bottom:15px;">📆 Retrasos por Trimestre</p>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                        <div style="background:#f0faf8; padding:12px; border-radius:10px; text-align:center;">
                            <p style="color:#888; font-size:12px; margin:0;">Q1 Ene-Mar</p>
                            <p style="font-size:22px; font-weight:900; color:#1a1a1a; margin:0;">{inf['q1']}%</p>
                        </div>
                        <div style="background:#f0faf8; padding:12px; border-radius:10px; text-align:center;">
                            <p style="color:#888; font-size:12px; margin:0;">Q2 Abr-Jun</p>
                            <p style="font-size:22px; font-weight:900; color:#1a1a1a; margin:0;">{inf['q2']}%</p>
                        </div>
                        <div style="background:#f0faf8; padding:12px; border-radius:10px; text-align:center;">
                            <p style="color:#888; font-size:12px; margin:0;">Q3 Jul-Sep</p>
                            <p style="font-size:22px; font-weight:900; color:#1a1a1a; margin:0;">{inf['q3']}%</p>
                        </div>
                        <div style="background:#f0faf8; padding:12px; border-radius:10px; text-align:center;">
                            <p style="color:#888; font-size:12px; margin:0;">Q4 Oct-Dic</p>
                            <p style="font-size:22px; font-weight:900; color:#1a1a1a; margin:0;">{inf['q4']}%</p>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown("<p style='color:#0ea68c; font-weight:800; font-size:16px;'>📊 Detalle mensual de retrasos</p>", unsafe_allow_html=True)
        fig = px.bar(
            x=list(inf['por_mes'].keys()),
            y=list(inf['por_mes'].values()),
            labels={'x': 'Mes', 'y': '% Retrasos'},
            color=list(inf['por_mes'].values()),
            color_continuous_scale=['#11caa0', '#f5a623', '#e74c3c'],
        )
        fig.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            showlegend=False, coloraxis_showscale=False,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
