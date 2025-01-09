# Streamlit Installation and Usage Guide for Ubuntu

## Installation

### Prerequisites
```bash
# Update package list
sudo apt update

# Install Python and pip if not already installed
sudo apt install python3 python3-pip

# Install required system dependencies
sudo apt install python3-dev build-essential
```

### Install Streamlit
```bash
# Install streamlit using pip
pip install streamlit

# Verify installation
streamlit --version
```

## Running Streamlit Applications

### Basic Commands
```bash
# Run a streamlit app
streamlit run app.py

# Run with specific port and host (for deployment)
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Clear cache
streamlit cache clear

# Get help
streamlit --help
```

## Streamlit Syntax Guide

### Basic Page Layout
```python
# Page configuration
st.set_page_config(
    page_title="My App",
    page_icon="🚀",
    layout="wide"
)

# Title and headers
st.title("Main Title")
st.header("Header")
st.subheader("Sub Header")

# Text elements
st.text("Simple text")
st.markdown("**Bold** and *italic* text")
st.write("Automatic formatting")
```

### Input Widgets
```python
# Text input
name = st.text_input("Enter your name")
password = st.text_input("Password", type="password")

# Numeric input
age = st.number_input("Age", min_value=0, max_value=120)
price = st.slider("Price", 0.0, 100.0, 25.0)

# Selection
option = st.selectbox("Choose an option", ["A", "B", "C"])
options = st.multiselect("Multiple choices", ["1", "2", "3"])

# Date and time
date = st.date_input("Select date")
time = st.time_input("Select time")
```

### Display Elements
```python
# Data display
st.dataframe(df)  # Display pandas DataFrame
st.table(data)    # Static table display
st.json(data)     # Display JSON data

# Media
st.image("image.jpg", caption="Image caption")
st.audio("audio.mp3")
st.video("video.mp4")

# Progress and status
st.progress(75)
st.spinner("Loading...")
st.success("Done!")
st.error("Error message")
st.warning("Warning message")
st.info("Info message")
```

### Layout Organization
```python
# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Column 1")
with col2:
    st.write("Column 2")

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Content for tab 1")

# Expander
with st.expander("Click to expand"):
    st.write("Hidden content")

# Sidebar
with st.sidebar:
    st.write("Sidebar content")
```

### Forms and Buttons
```python
# Form
with st.form("my_form"):
    name = st.text_input("Name")
    submit = st.form_submit_button("Submit")
    if submit:
        st.write(f"Hello {name}!")

# Buttons
if st.button("Click me"):
    st.write("Button clicked!")

# Download button
data = generate_data()
st.download_button("Download", data, "file.csv")
```

### State Management
```python
# Session state
if 'count' not in st.session_state:
    st.session_state.count = 0

# Increment counter
if st.button('Increment'):
    st.session_state.count += 1

st.write('Count:', st.session_state.count)
```

### Cache and Performance
```python
# Cache function results
@st.cache_data
def expensive_computation(param):
    # This will only be run once for each param value
    return heavy_computation(param)

# Cache resource objects
@st.cache_resource
def init_database():
    return Database()
```

## Best Practices

1. **Performance Tips**
   - Use `st.cache_data` for expensive computations
   - Load large datasets using `st.cache_resource`
   - Avoid unnecessary recomputation in callbacks

2. **UI/UX Guidelines**
   - Group related inputs in forms
   - Use appropriate widgets for data types
   - Provide clear feedback for user actions
   - Include progress indicators for long operations

3. **Development Workflow**
   - Use `st.experimental_rerun()` for page updates
   - Enable debug mode during development
   - Organize code into modules for larger applications
   - Handle exceptions gracefully with try-except blocks

4. **Deployment Considerations**
   - Set appropriate server configurations
   - Use environment variables for secrets
   - Configure proper authentication if needed
   - Monitor application performance
