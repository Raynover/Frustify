import os
import time
import subprocess
import platform
import importlib
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Circular Frustum Generator", layout="wide")

# --- Custom CSS for Layout Spacing, Disabling Step Buttons, & Disabling Header Links ---
st.markdown(
    """
    <style>
    /* Reduce top margins */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
    }
    /* Ensure form/action buttons expand to fill full container width */
    div.stButton > button {
        width: 100% !important;
    }
    /* Custom centered green alert box matched precisely to Streamlit button height */
    .custom-success-box {
        background-color: #1e4620;
        color: #e8f5e9;
        border: 1px solid #2e7d32;
        border-radius: 8px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 14px;
        box-sizing: border-box;
        margin-top: 0px;
    }
    /* Hide the plus and minus step buttons completely */
    div[data-testid="stNumberInput"] button {
        display: none !important;
    }
    /* Remove anchor links / clickable headers */
    .stMarkdown h2 a, .stMarkdown h3 a, 
    a.anchor-link, [data-testid="stHeaderActionElements"] {
        display: none !important;
        pointer-events: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title & Description (Centered) ---
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 15px;">
        <h2 style="margin-bottom: 2px;">Circular Frustum Generator</h2>
        <p style="font-size: 13px; color: #666; margin-top: 0px;">
            A tool that generates AutoCAD-ready scripts for unfolded circular wooden frustums designed for CNC cutting.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state for tracking completion
if "generation_done" not in st.session_state:
    st.session_state.generation_done = False

# Function to safely overwrite variable assignments in parameters.py
def update_parameters_file(R_val, r_val, h_val, discwidth_val):
    param_filepath = os.path.join(os.path.dirname(__file__), "parameters.py")
    
    with open(param_filepath, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("R =") or stripped.startswith("R="):
            new_lines.append(f"R = {R_val}\n")
        elif stripped.startswith("r =") or stripped.startswith("r="):
            new_lines.append(f"r = {r_val}\n")
        elif stripped.startswith("h =") or stripped.startswith("h="):
            new_lines.append(f"h = {h_val}\n")
        elif stripped.startswith("discwidth =") or stripped.startswith("discwidth="):
            new_lines.append(f"discwidth = {discwidth_val}\n")
        else:
            new_lines.append(line)
            
    with open(param_filepath, "w") as f:
        f.writelines(new_lines)

# Function to handle opening the system file manager
def open_output_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    else:  # Linux / Unix
        subprocess.Popen(["xdg-open", path])

# Function to generate the static 3D reference frustum figure
def create_fixed_3d_frustum():
    # Fixed visual reference dimensions: R=8, r=3.7, h=11.5
    R_ref = 8.0
    r_ref = 3.7
    h_ref = 11.5

    # Parametric surface generation for circular frustum
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, 1, 20)
    U, V = np.meshgrid(u, v)

    X = (R_ref + (r_ref - R_ref) * V) * np.cos(U)
    Y = (R_ref + (r_ref - R_ref) * V) * np.sin(U)
    Z = h_ref * V

    # Custom wood tone colorscale
    wood_colorscale = [
        [0.0, '#5c3a21'],  # Dark wood brown
        [0.5, '#8b5a2b'],  # Medium wood tone
        [1.0, '#c69c6d']   # Light wood tone
    ]

    fig = go.Figure()

    # Add translucent frustum mesh (opacity = 0.65) with hover contours disabled
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z, 
        colorscale=wood_colorscale, 
        opacity=0.65, 
        showscale=False,
        hoverinfo='skip',
        contours=dict(
            x=dict(highlight=False, show=False),
            y=dict(highlight=False, show=False),
            z=dict(highlight=False, show=False)
        )
    ))

    # Highlighted Dimension Lines & Centered Colored Labels
    # 1. Large (bottom) base radius (R)
    fig.add_trace(go.Scatter3d(
        x=[0, R_ref], y=[0, 0], z=[0, 0], 
        mode='lines',
        line=dict(color='red', width=5), 
        name="Bottom base radius (R)"
    ))
    fig.add_trace(go.Scatter3d(
        x=[R_ref / 2], y=[0], z=[0], 
        mode='text',
        text=["R"],
        textposition="top center",
        textfont=dict(color='red', size=16),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # 2. Small (top) base radius (r)
    fig.add_trace(go.Scatter3d(
        x=[0, r_ref], y=[0, 0], z=[h_ref, h_ref], 
        mode='lines',
        line=dict(color='orange', width=5), 
        name="Top base radius (r)"
    ))
    fig.add_trace(go.Scatter3d(
        x=[r_ref / 2], y=[0], z=[h_ref], 
        mode='text',
        text=["r"],
        textposition="top center",
        textfont=dict(color='orange', size=16),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # 3. Height (h)
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[0, h_ref], 
        mode='lines',
        line=dict(color='purple', width=5), 
        name="Height (h)"
    ))
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[h_ref / 2], 
        mode='text',
        text=["h"],
        textposition="middle right",
        textfont=dict(color='purple', size=16),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data',
            dragmode='turntable',
            camera=dict(
                eye=dict(x=1.1, y=1.1, z=1.8)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False
    )
    return fig

# --- Main Layout: Side-by-Side Setup ---
col_left, col_right = st.columns([1.1, 1], gap="medium", vertical_alignment="center")

# LEFT COLUMN: 3D Rotatable Reference Guide
with col_left:
    st.plotly_chart(
        create_fixed_3d_frustum(), 
        use_container_width=True,
        config={
            'displayModeBar': False,
            'scrollZoom': False
        }
    )

# RIGHT COLUMN: User Inputs & Action
with col_right:
    # Restored the surrounding bordered box around input parameters
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 15px;">
                <h3 style="margin-top: 0px; margin-bottom: 2px;">Input Parameters</h3>
                <p style="font-size: 13px; color: #666; margin-top: 0px;">
                    Input your frustum's dimensions (rotate 3D figure for reference).
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            R_input = st.number_input("R (in mm):", value=493.0, step=1.0, format="%.1f")
            r_input = st.number_input("r (in mm):", value=217.0, step=1.0, format="%.1f")
            
        with form_col2:
            h_input = st.number_input("h (in mm):", value=710.0, step=1.0, format="%.1f")
            discwidth_input = st.number_input("Disc width (in mm):", value=3.0, step=0.1, format="%.1f")
        
        # --- Live Input Validation Check ---
        is_valid = (
            (R_input is not None and 0 < R_input <= 1500) and
            (r_input is not None and 0 < r_input < R_input) and
            (h_input is not None and 0 < h_input < 2000) and
            (discwidth_input is not None and 0 < discwidth_input < 10)
        )

        # Grid section under the input boxes
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            st.markdown("<label style='visibility: hidden;'>\u200b</label>", unsafe_allow_html=True)
            submit_button = st.button(
                label="Run Calculation & Generate Files", 
                use_container_width=True,
                disabled=not is_valid
            )
            if submit_button:
                st.session_state.generation_done = False
            
        with action_col2:
            st.markdown("<label style='visibility: hidden;'>\u200b</label>", unsafe_allow_html=True)
            action_slot = st.empty()
            
            if st.session_state.generation_done:
                open_folder_submitted = action_slot.button(label="📁 Open Output Folder", use_container_width=True)
                if open_folder_submitted:
                    import parameters as prms
                    output_dir = getattr(prms, "OUTPUT_DIR", os.path.join(os.path.dirname(__file__), "output"))
                    os.makedirs(output_dir, exist_ok=True)
                    open_output_folder(output_dir)

# --- Execution Handling ---
if submit_button and is_valid:
    # Update parameters file
    update_parameters_file(R_input, r_input, h_input, discwidth_input)

    # Reload parameters module
    import parameters as prms
    importlib.reload(prms)

    # 1. Progress Bar strictly replacing the action slot
    progress_bar = action_slot.progress(0)
    progress_bar.progress(50)

    import main
    importlib.reload(main)
    if hasattr(main, 'main'):
        main.main()

    progress_bar.progress(100)
    time.sleep(0.75)

    # 2. Replace progress bar with centered green message box 
    action_slot.markdown(
        '<div class="custom-success-box">Output files are ready!</div>', 
        unsafe_allow_html=True
    )
    time.sleep(1.5)

    # 3. Mark generation as done and rerun to render the Open Output Folder button in the same slot
    st.session_state.generation_done = True
    st.rerun()
