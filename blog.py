import streamlit as st
import pandas as pd

def load_posts():
    try:
        posts = pd.read_csv('posts.csv')
    except FileNotFoundError:
        posts = pd.DataFrame(columns=["Title", "Content"])
    return posts

def save_post(title, content):
    posts = load_posts()
    new_post = pd.DataFrame([[title, content]], columns=["Title", "Content"])
    updated_posts = pd.concat([posts, new_post], ignore_index=True)
    updated_posts.to_csv('posts.csv', index=False)

def blog():
    st.header("Resource Blog")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password = st.text_input("Admin Password", type="password")
        if st.button("Login"):
            if password == "636363Qa!!":  # Replace with your own admin password
                st.session_state.admin_logged_in = True
                st.success("Logged in as admin")
            else:
                st.error("Incorrect password")

    if st.session_state.admin_logged_in:
        st.subheader("Add New Post")
        title = st.text_input("Title")
        content = st.text_area("Content")
        if st.button("Add Post"):
            if title and content:
                save_post(title, content)
                st.success("Post added successfully")
            else:
                st.error("Title and content cannot be empty")

    st.subheader("All Posts")
    posts = load_posts()
    for _, post in posts.iterrows():
        st.write(f"### {post['Title']}")
        st.write(post['Content'])
        st.markdown("---")
