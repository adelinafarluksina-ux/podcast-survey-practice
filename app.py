"""
Учебная практика: Одностраничный сайт-опросник на Streamlit + Firebase
Тема: Использование подкастов
"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ==========================================
# 🎨 КАСТОМНЫЕ СТИЛИ (РОЗОВЫЙ ДИЗАЙН)
# ==========================================
def local_css():
    st.markdown("""
    <style>
    /* Розовый градиентный фон */
    .stApp {
        background: linear-gradient(135deg, #fff0f6 0%, #ffe3ec 50%, #ffcce0 100%);
        background-attachment: fixed;
    }
    
    /* Шапка сайта */
    .header-container {
        background: linear-gradient(135deg, #ff8fab 0%, #fb6f92 100%); 
        padding: 35px; 
        border-radius: 20px; 
        margin-bottom: 25px; 
        box-shadow: 0 8px 25px rgba(251, 111, 146, 0.3);
        text-align: left;
    }
    
    .header-title {
        color: white; 
        margin: 0 0 15px 0; 
        font-size: 2.3em; 
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', sans-serif;
    }
    
    .header-desc {
        color: rgba(255,255,255,0.95); 
        margin: 0; 
        font-size: 1.1em; 
        line-height: 1.6;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Настройка стиля вкладок */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: bold;
        color: #fb6f92;
    }
    
    /* Стилизация карточки формы */
    div[data-testid="stForm"] {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(251, 111, 146, 0.15);
        border: 1px solid #ffe3ec;
    }

    /* Кнопки */
    .stButton>button {
        background: linear-gradient(135deg, #ff8fab, #d63384);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(214, 51, 132, 0.4);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# 🔥 ИНИЦИАЛИЗАЦИЯ FIREBASE
# ==========================================
def init_firebase():
    """Инициализация подключения к Firebase Firestore."""
    if not firebase_admin._apps:
        key_path = "serviceAccountKey.json"
        if not os.path.exists(key_path):
            st.error("❌ Ошибка: Файл serviceAccountKey.json не найден!")
            st.stop()
        
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

db = init_firebase()

# ==========================================
# 🎀 ШАПКА САЙТА (РОЗОВЫЙ ВАРИАНТ 3)
# ==========================================
st.markdown("""
<div class='header-container'>
    <h1 class='header-title'>🎧 Использование подкастов</h1>
    <p class='header-desc'>Исследование для учебной практики. Помогите понять, как подкасты влияют на наше мышление, учебу и повседневные привычки. 
        Опрос анонимный, займёт около 3 минут.
    </p>
</div>
""", unsafe_allow_html=True)

# Разделяем проект на красивую постраничную навигацию через вкладки (Tabs)
tab1, tab2 = st.tabs(["📋 Пройти анкетирование", "📊 Аналитический интерактивный дашборд"])

# ==========================================
# 📝 ВКЛАДКА 1: ФОРМА ОПРОСА
# ==========================================
with tab1:
    with st.form("podcast_survey_form"):
        
        # БЛОК 1: О респонденте
        st.markdown("### 👤 Блок 1: О вас")
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input(
                "1. Ваш возраст", 
                min_value=14, max_value=80, value=20, step=1,
                help="Укажите ваш возраст"
            )
            gender = st.radio(
                "2. Ваш пол", 
                ["Мужской", "Женский", "Предпочитаю не указывать"]
            )
        
        with col2:
            # Обновленный вопрос на основе нашего обсуждения
            education = st.selectbox(
                "3. Ваш род занятий / социальный статус", 
                ["Школьник", "Студент", "Работающий", "Другое"]
            )
        
        st.markdown("---")
        
        # БЛОК 2: Привычки слушания
        st.markdown("### 🎵 Блок 2: Ваши привычки слушания")
        col3, col4 = st.columns(2)
        
        with col3:
            frequency = st.selectbox(
                "4. Как часто вы слушаете подкасты?", 
                ["Каждый день", "Несколько раз в неделю", "Раз в неделю", "Пару раз в месяц", "Очень редко", "Вообще не слушаю"]
            )
            listening_time = st.radio(
                "5. Сколько времени вы обычно тратите на один подкаст?",
                ["Меньше 15 минут", "15-30 минут", "30-60 минут", "Больше часа", "Слушаю фоном целый день"]
            )
        
        with col4:
            listening_place = st.multiselect(
                "6. Где вы обычно слушаете подкасты?",
                ["В транспорте", "На прогулке или спорте", "Дома (уборка, готовка)", "Во время учёбы или работы", "Перед сном", "В другом месте"]
            )
        
        st.markdown("---")
        
        # БЛОК 3: Платформы
        st.markdown("### 📱 Блок 3: Платформы")
        platforms = st.multiselect(
            "7. Какие платформы вы используете для прослушивания подкастов?",
            ["Яндекс Музыка", "VK Подкасты", "Spotify", "Apple Podcasts", "YouTube", "Castbox", "Google Подкасты", "Другое"]
        )
        
        st.markdown("---")
        
        # БЛОК 4: Темы
        st.markdown("### 🎯 Блок 4: Темы")
        topics = st.multiselect(
            "8. Какие темы подкастов вас интересуют?",
            ["Образование и наука", "Технологии и IT", "Интервью и биографии", "True Crime / Криминал", 
             "Бизнес и финансы", "Психология и саморазвитие", "Юмор и развлечения", "Кино и сериалы", 
             "Книги и литература", "Гейминг", "Другое"]
        )
        
        st.markdown("---")
        
        # БЛОК 5: Влияние на знания
        st.markdown("### 📚 Блок 5: Влияние на обучение")
        impact = st.slider(
            "9. Насколько подкасты помогают вам узнавать новое и учиться? (1 - совсем не помогают, 10 - очень сильно)",
            min_value=1, max_value=10, value=5
        )
        
        col5, col6 = st.columns(2)
        
        with col5:
            notes = st.radio(
                "10. Делаете ли вы заметки во время или после прослушивания?",
                ["Да, всегда конспектирую", "Иногда выписываю главное", "Просто слушаю и запоминаю", "Нет, слушаю для удовольствия"]
            )
            application = st.radio(
                "11. Применяете ли вы знания из подкастов на практике?",
                ["Да, часто применяю", "Иногда использую", "Редко применяю", "Нет, просто слушаю"]
            )
        
        with col6:
            education_tool = st.radio(
                "12. Считаете ли вы подкасты полноценным образовательным инструментом?",
                ["Да, наравне с книгами и курсами", "Частично, как дополнение", "Нет, это просто развлечение", "Затрудняюсь ответить"]
            )
        
        submitted = st.form_submit_button("🎉 Отправить ответы", use_container_width=True)

    # Логика обработки клика по кнопке отправки
    if submitted:
        if not platforms or not topics or not listening_place:
            st.warning("⚠️ Пожалуйста, заполните все вопросы с множественным выбором (Места, Платформы и Темы)!")
        else:
            response_data = {
                "age": int(age),
                "gender": gender,
                "education": education,
                "frequency": frequency,
                "listening_time": listening_time,
                "listening_place": listening_place,
                "platforms": platforms,
                "topics": topics,
                "impact_score": int(impact),
                "notes_habit": notes,
                "application": application,
                "education_tool": education_tool,
                "timestamp": datetime.utcnow()
            }
            
            try:
                db.collection("podcast_responses").add(response_data)
                st.success("✅ Спасибо! Ваши ответы успешно сохранены в базе данных!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Ошибка при сохранении: {e}")

# ==========================================
# 📊 ВКЛАДКА 2: ИНТЕРАКТИВНЫЙ ДАШБОРД
# ==========================================
with tab2:
    st.subheader("📊 Аналитический интерактивный дашборд (Режим преподавателя)")
    
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        if st.button("🔄 Обновить графики"):
            st.rerun()
            
    try:
        # Загружаем данные напрямую из коллекции Firestore
        docs = db.collection("podcast_responses").stream()
        raw_data = [doc.to_dict() for doc in docs]
        
        if raw_data:
            df = pd.DataFrame(raw_data)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            
            # ==========================================
            # 📥 ЭКСПОРТ ДАННЫХ В CSV/EXCEL
            # ==========================================
            csv_data = df.to_csv(index=False).encode('utf-8')
            with col_nav2:
                st.download_button(
                    label="📥 Экспортировать данные в Excel/CSV",
                    data=csv_data,
                    file_name=f"podcast_survey_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
            # Метрики общей статистики верхнего уровня
            st.markdown("##### 📌 Ключевые показатели:")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Всего респондентов", len(df))
            with m2:
                st.metric("Средний балл полезности", round(df["impact_score"].mean(), 1))
            with m3:
                st.metric("Средний возраст слушателя", round(df["age"].mean(), 1))
                
            st.markdown("---")
            
            # --- СЕКЦИЯ СТИЛЬНЫХ ВИЗУАЛИЗАЦИЙ ---
            c_row1_1, c_row1_2 = st.columns(2)
            
            with c_row1_1:
                st.markdown("**📊 Оценки образовательной эффективности подкастов (Шкала 1-10):**")
                fig_impact = px.histogram(df, x="impact_score", nbins=10, 
                                          labels={'impact_score': 'Баллы полезности', 'count': 'Количество ответов'}, 
                                          color_discrete_sequence=['#D63384'])
                fig_impact.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_impact, use_container_width=True)
                
            with c_row1_2:
                st.markdown("**🎓 Считают ли подкасты полноценным инструментом обучения:**")
                fig_edu = px.pie(df, names="education_tool", color_discrete_sequence=px.colors.sequential.RdPu)
                fig_edu.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_edu, use_container_width=True)
                
            st.markdown("---")
            c_row2_1, c_row2_2 = st.columns(2)
            
            with c_row2_1:
                st.markdown("**📱 Рейтинг популярности стриминговых платформ:**")
                if "platforms" in df.columns:
                    df_platforms = df.explode('platforms')
                    platform_counts = df_platforms['platforms'].value_counts().reset_index()
                    platform_counts.columns = ['Платформа', 'Количество голосов']
                    fig_plat = px.bar(platform_counts, x='Количество голосов', y='Платформа', 
                                      orientation='h', color_discrete_sequence=['#FF69B4'])
                    fig_plat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_plat, use_container_width=True)
                
            with c_row2_2:
                st.markdown("**💡 Рейтинг самых востребованных тематик подкастов:**")
                if "topics" in df.columns:
                    df_topics = df.explode('topics')
                    topic_counts = df_topics['topics'].value_counts().reset_index()
                    topic_counts.columns = ['Тематика', 'Количество голосов']
                    fig_top = px.bar(topic_counts, x='Количество голосов', y='Тематика', 
                                     orientation='h', color_discrete_sequence=['#B02A6F'])
                    fig_top.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_top, use_container_width=True)

            # Перекрестный сложный график для демонстрации преподавателю
            st.markdown("---")
            st.markdown("**🔍 Связь между социальным статусом и оценкой полезности подкастов:**")
            fig_box = px.box(df, x="education", y="impact_score",
                             labels={'education': 'Социальный статус / Род занятий', 'impact_score': 'Оценка влияния (1-10)'},
                             color="education", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_box.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_box, use_container_width=True)

            # Таблица сырых данных
            st.markdown("---")
            st.markdown("**📋 Просмотр массива ответов из Firestore Database (Последние 10 сессий):**")
            st.dataframe(df.tail(10), use_container_width=True)
            
        else:
            st.info("🎈 Облачная база данных пуста. Перейдите на первую вкладку, пройдите опрос, и графики тут же построятся!")
    except Exception as e:
        st.error(f"❌ Ошибка генерации аналитических отчетов: {e}")

# ==========================================
# 🎀 ПОДВАЛ
# ==========================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #d63384; padding: 20px;'>
    <p> Спасибо за участие в исследовании!💖</p>
</div>
""", unsafe_allow_html=True)