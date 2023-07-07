# Building App

# Step 1: import libraries
import streamlit as st
import numpy as np

# Step 2: load weights
model = np.load('weights.npz')
X_mean = model['X_mean']
X_std = model['X_std']
theta = model['theta']
@st.cache_resource

# Step 3: define predict function
def predict(carat, cut, color, clarity, depth, table, x, y, z, x_mean, x_std, theta):
    # mapping for cut 
    cut_mapping = {'Fair': 0, 'Good': 1, 'Ideal': 2, 'Very Good': 3, 'Premium':4}
    
    # mapping for color
    color_mapping = {'D': 0, 'E': 1, 'F': 2, 'G': 3, 'H': 4 , 'I': 5, 'J': 6}
    
    # mapping for clarity
    clarity_mapping = {'I1': 0, 'IF':1, 'SI1': 2, 'SI2': 3, 'VS1':4, 'VS2':5, 'VS2':6, 'VVS1':7, 'VVS2': 8}

    # convert variables to numerical values
    cut = cut_mapping.get(cut, 0) # If cut is a valid key in cut_mapping, the method returns the corresponding integer code. 
                                  # If cut is not a valid key in cut_mapping, the method returns a default value of 0.
    color = color_mapping.get(color, 0)
    clarity = clarity_mapping.get(clarity, 0)
    input = np.array([[carat, cut, color, clarity, depth, table, x, y, z]], dtype='float')
    
    # normalize input
    input = (input-X_mean)/X_std
    
    b = np.array([[1.0]])
    input = np.concatenate((b, input), axis=1)
    prediction = np.dot(input, theta)
    return prediction

# Step 4: design interface
st.title('💎 DIAMOND PRICE PREDICTION 💎')

st.header("Please enter the diamond's characteristic parameters")
carat = st.number_input('Carat Weight:', min_value=0.1, max_value=10.0, value=1)
cut = st.selectbox('Cut Rating:', ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'])
color = st.selectbox('Color Rating:', ['D', 'E', 'F', 'G', 'H', 'I', 'J'])
clarity = st.selectbox('Clarity Rating:', ['I1', 'IF', 'SI1', 'SI2', 'VS1', 'VS2', 'VVS1', 'VVS2'])
depth = st.number_input('The Percentage of Depth:', min_value=0.1, max_value=100.0, value=1)
table = st.number_input('The Table Width:', min_value=0.1, max_value=100.0, value=1.0)
x = st.number_input('Diamond Length (X) in mm:', min_value=0.1, max_value=100, value=1.0)
y = st.number_input('Diamond Width (Y) in mm:', min_value=0.1, max_value=100, value=1.0) 
z = st.number_input('Diamond Height (Z) in mm:', min_value=0.1, max_value=100, value=1.0)

if st.button('Predict'):
    out = predict(carat, cut, color, clarity, depth, table, x, y, z, x_mean, x_std, theta)
    st.success(f'The Predicted Price of Diamond is:, ${out[0,0]:.2f} USD')
