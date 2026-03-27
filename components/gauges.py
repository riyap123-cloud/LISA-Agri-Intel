import plotly.graph_objects as go
import streamlit as st

def create_gauge(value, title, min_val=0, max_val=100):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "#2E7D32"},
            'steps': [
                {'range': [0, 30], 'color': "#FFCDD2"},
                {'range': [30, 70], 'color': "#FFF9C4"},
                {'range': [70, 100], 'color': "#C8E6C9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)