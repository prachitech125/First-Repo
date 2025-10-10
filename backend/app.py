import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from services.recommendation import recommend_routes
from services.points import PointsStore

load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    points_store = PointsStore()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/routes/recommend")
    def routes_recommend():
        data = request.get_json(silent=True) or {}
        source = data.get("source")
        destination = data.get("destination")
        if not source or not destination:
            return jsonify({"error": "source and destination are required"}), 400
        result = recommend_routes(source, destination)
        return jsonify(result)

    @app.post("/routes/choose")
    def routes_choose():
        data = request.get_json(silent=True) or {}
        user_id = data.get("userId", "guest")
        route = data.get("route")
        if not route:
            return jsonify({"error": "route is required"}), 400
        eco_points = int(route.get("ecoPoints", 0))
        points_store.add_points(user_id, eco_points)
        return jsonify({"ok": True, "userId": user_id, "totalPoints": points_store.get_points(user_id)})

    @app.get("/leaderboard")
    def leaderboard():
        return jsonify(points_store.get_leaderboard())

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)
