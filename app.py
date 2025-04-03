from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import re

app = Flask(__name__)

# Function to clean and normalize text data
def preprocess_text(text):
    # Convert to lowercase and remove special characters
    return re.sub(r'[^a-z\s]', '', text.lower())

# Load and prepare the datasets
file_paths = [
    r"C:\c code\news_detector[2]\news_detector\news detector\comprehensive_news_data.csv",
    r"C:\c code\news_detector[2]\news_detector\news detector\fake_news_dataset.csv",
    r"C:\c code\news_detector[2]\news_detector\news detector\news_data.csv"
]

dataframes = []

for file_path in file_paths:
    df = pd.read_csv(file_path)
    # Check column names and print them for debugging
    print(f"Columns in {file_path}: {df.columns.tolist()}")

    # Ensure both 'title' and 'text' columns exist
    if 'title' in df.columns and 'text' in df.columns and 'label' in df.columns:
        # Concatenate title and text into a single content column
        df['content'] = df['title'].fillna('') + ' ' + df['text'].fillna('')  # Handle missing values
        df['content'] = df['content'].apply(preprocess_text)  # Preprocess text
        dataframes.append(df[['content', 'label']])  # Store relevant columns
    else:
        print(f"Warning: Required columns ('title', 'text', 'label') not found in {file_path}")

# Merge all dataframes
if dataframes:
    df_combined = pd.concat(dataframes, ignore_index=True)
    # Filter out rows where content is empty
    df_combined = df_combined[df_combined['content'].str.strip() != '']
    print(f"Number of rows in combined dataframe after filtering: {len(df_combined)}")
else:
    print("Error: No valid dataframes to combine.")
    exit(1)  # Exit if there are no valid dataframes

# Check if df_combined has any rows left
if df_combined.empty:
    print("Error: Combined dataframe is empty after filtering.")
    exit(1)  # Exit if the dataframe is empty

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df_combined['content'], 
    df_combined['label'], 
    test_size=0.33, 
    random_state=53
)

# Vectorization and training
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = tfidf_vectorizer.fit_transform(X_train)

clf = MultinomialNB()
clf.fit(tfidf_train, y_train)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['news_article']
    # Preprocess the input text before prediction
    text = preprocess_text(text)
    text_vector = tfidf_vectorizer.transform([text])

    # Check if vectorized input has any recognized features
    if text_vector.nnz == 0:
        prediction = "fake news"  # No matching features
    else:
        # Predict using the trained model
        prediction = clf.predict(text_vector)[0]
    
    return render_template('index.html', prediction=prediction, article=text)

if __name__ == '__main__':
    app.run(debug=True)
