import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

df_reviews = pd.read_csv('./livros_amazon/customer reviews.csv')
df_top100_books = pd.read_csv('./livros_amazon/Top-100 Trending Books.csv')

def get_stars(rating):
    full_stars = int(rating)  
    half_star = rating - full_stars >= 0.5  
    stars = "⭐" * full_stars  
    if half_star:
        stars += "✩" 
    return stars

st.sidebar.title("Book Reviews")

books = df_top100_books['book title'].unique()
book = st.sidebar.selectbox('Books', books)

df_book = df_top100_books[df_top100_books['book title'] == book]
df_reviews_f = df_reviews[df_reviews['book name'] == book]

book_title = df_book['book title'].iloc[0]
book_genre = df_book['genre'].iloc[0]
book_price = f"${df_book['book price'].iloc[0]}"
book_rating = df_book['rating'].iloc[0]
book_year = df_book['year of publication'].iloc[0]

st.title(book_title)
st.subheader(book_genre)
col1, col2, col3 = st.columns(3)
col1.metric('Price', book_price)
col2.metric('Rating', book_rating)
col3.metric('Year', book_year)

st.divider()

df_books_sem_review = df_top100_books[~df_top100_books["book title"].isin(df_reviews["book name"])]

if book in df_books_sem_review["book title"].values:
    st.warning("❌ This book has no review yet.")
else:
    for row in df_reviews_f.values:
        rating = float(row[4])  
        stars = get_stars(rating)  

        st.subheader(f"{stars} ({rating})")
        st.write(f"**{row[2]}**")  
        st.write(f"{row[5]}")


