import streamlit as st
import pandas as pd

# Modal-style pop-up with custom CSS
st.markdown(
    """
    <style>
    .modal {
        display: block;
        position: fixed;
        top: 20%;
        left: 25%;
        width: 50%;
        height: 50%;
        background-color: white;
        border: 2px solid black;
        padding: 10px;
        z-index: 100;
    }
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 99;
    }
    </style>
    """, unsafe_allow_html=True)

# Display a simple button to trigger modal
if st.button("Show Data"):
    st.markdown('<div class="modal-overlay"></div>', unsafe_allow_html=True)
    st.markdown('<div class="modal"><h2>What we Found from Data</h2></div>', unsafe_allow_html=True)

    columns = ["ID", "Name", "Age"]
    data = [[1, "John", 28], [2, "Sarah", 35], [3, "Alex", 40]]
    df = pd.DataFrame(data, columns=columns)
    st.write(df)
