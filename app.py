from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load Excel data at startup
data = pd.read_excel("JGP.xlsx")    

@app.route("/")
def index():
    # Serve the HTML page
    return render_template("index.html")

@app.route("/api/data")
def get_counties():
    try:
        # Extract unique counties
        counties = data["County"].dropna().unique().tolist()
        return jsonify(counties)  # Return the counties as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error in case of failure

@app.route("/api/search", methods=["POST"])
def search():
    try:
        # Extract filters from the POST request
        filters = request.json
        county = filters.get("county", "").lower()
        id_number = filters.get("idNumber", "").strip()
        phone_number = filters.get("phoneNumber", "").strip()
        full_name = filters.get("fullName", "").lower()

        # Apply filters to the data
        filtered_data = data
        if county:
            filtered_data = filtered_data[filtered_data["County"].str.lower() == county]
        if id_number:
            filtered_data = filtered_data[filtered_data["WHAT IS YOUR NATIONAL ID?"].astype(str).str.contains(id_number, na=False)]
        if phone_number:
            filtered_data = filtered_data[filtered_data["Phone Number"].astype(str).str.contains(phone_number, na=False)]
        if full_name:
            filtered_data = filtered_data[filtered_data["Full Name"].str.lower().str.contains(full_name, na=False)]

        # Ensure JSON serializability by replacing NaN with empty strings
        results = filtered_data.fillna("").to_dict(orient="records")
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return error in case of failure

if __name__ == "__main__":
    app.run(debug=True)
