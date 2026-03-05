from flask import Flask, render_template, request, url_for
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

model = pickle.load(open("placement_model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    features = [float(x) for x in request.form.values()]
    final_features = [np.array(features)]
    prediction = model.predict(final_features)

    result = "Placed ✅" if prediction[0] == 1 else "Not Placed ❌"

    return render_template("result.html", prediction_text=result)

@app.route("/dashboard")
def dashboard():

    df = pd.read_csv("placement_dataset.csv")

    # 1️⃣ Placement Distribution Pie Chart
    plt.figure()
    df["Placed"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Placement Distribution")
    plt.ylabel("")
    plt.savefig("static/pie.png")
    plt.close()

    # 2️⃣ Average CGPA by Placement
    plt.figure()
    df.groupby("Placed")["CGPA"].mean().plot(kind="bar")
    plt.title("Average CGPA by Placement")
    plt.savefig("static/bar.png")
    plt.close()

    # 3️⃣ Feature Importance
    importance = model.coef_[0]
    features = df.drop("Placed", axis=1).columns

    plt.figure()
    plt.barh(features, importance)
    plt.title("Feature Importance")
    plt.savefig("static/importance.png")
    plt.close()

    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
