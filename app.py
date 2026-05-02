from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random

app = Flask(__name__)

# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df = df.dropna()

    # 🟢 Simulate real-time data (new row every refresh)
    new_row = {
        "show_id": f"s_new_{random.randint(100,999)}",
        "type": random.choice(["Movie", "TV Show"]),
        "title": "Live Content",
        "director": "Random Director",
        "cast": "Random Actor",
        "country": random.choice(["USA", "India", "UK"]),
        "date_added": "Jan 2024",
        "release_year": random.randint(2015, 2023),
        "rating": random.choice(["PG", "PG-13", "R"]),
        "duration": "120 min"
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df


def create_graphs(df):
    # Bar Chart
    plt.figure()
    df["type"].value_counts().plot(kind='bar')
    plt.title("Movies vs TV Shows")
    plt.savefig("static/bar.png")
    plt.close()

    # Scatter Plot
    plt.figure()
    plt.scatter(df["release_year"], df.index)
    plt.title("Release Year Distribution")
    plt.savefig("static/scatter.png")
    plt.close()

    # Heatmap
    plt.figure()
    numeric_df = df.select_dtypes(include=['int64'])
    sns.heatmap(numeric_df.corr(), annot=True)
    plt.title("Heatmap")
    plt.savefig("static/heatmap.png")
    plt.close()


@app.route("/")
def home():
    df = load_data()  # reload + update data
    create_graphs(df)

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