from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Flask app (templates folder auto-detected)
app = Flask(__name__)

# Load dataset
df = pd.read_csv("netflix_titles.csv")
df = df.dropna()

# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# Function to create graphs
def create_graphs():
    # Bar Chart
    plt.figure()
    df["type"].value_counts().plot(kind='bar')
    plt.title("Movies vs TV Shows")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.savefig("static/bar.png")
    plt.close()

    # Scatter Plot
    plt.figure()
    plt.scatter(df["release_year"], df.index)
    plt.title("Release Year Distribution")
    plt.xlabel("Release Year")
    plt.ylabel("Index")
    plt.savefig("static/scatter.png")
    plt.close()

    # Heatmap
    plt.figure()
    numeric_df = df.select_dtypes(include=['int64'])
    sns.heatmap(numeric_df.corr(), annot=True)
    plt.title("Correlation Heatmap")
    plt.savefig("static/heatmap.png")
    plt.close()

# Generate graphs
create_graphs()

@app.route("/")
def home():
    avg_year = df["release_year"].mean()
    total = len(df)
    movies = df[df["type"] == "Movie"].shape[0]
    shows = df[df["type"] == "TV Show"].shape[0]

    return render_template("index.html",
                           avg_year=round(avg_year, 2),
                           total=total,
                           movies=movies,
                           shows=shows)

if __name__ == "__main__":
    app.run(debug=True)