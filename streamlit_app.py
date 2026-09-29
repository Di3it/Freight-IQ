import importlib

try:
    st = importlib.import_module("streamlit")
except ModuleNotFoundError as exc:
    if exc.name != "streamlit":
        raise
    raise SystemExit(
        "Streamlit is not installed. Install it with: python -m pip install streamlit"
    ) from exc

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
