#!/bin/bash
set -euo pipefail

echo "🚀 Starting Surfer H - Holo Model Run"
echo "======================================"

# Load environment variables using Python helper
eval "$(uv run python3 load_env.py HAI_API_KEY HAI_MODEL_URL_NAVIGATION HAI_MODEL_NAME_NAVIGATION HAI_MODEL_URL_LOCALIZATION HAI_MODEL_NAME_LOCALIZATION)"
echo ""

# Start frontend server
echo "Starting frontend server..."
uv run streamlit run automation_forms_filling/app.py &
FRONTEND_PID=$!
echo "Frontend server started with PID $FRONTEND_PID"
sleep 5 # Wait for server to start

# Cleanup function to kill the frontend server
cleanup() {
    echo "Cleaning up..."
    kill $FRONTEND_PID
}
trap cleanup EXIT

# Task configuration
TASK='fill input[placeholder="Benutzername *"] with "admin"; fill input[placeholder="Passwort"] with "password123"; click "Anmelden"'
URL="file://$(pwd)/automation_forms_filling/login.html"

echo "🎯 Starting task: $TASK"
echo "🌐 Target URL: $URL"

echo "🤖 Model: $HAI_MODEL_NAME_NAVIGATION"
echo "🤖 Model: $HAI_MODEL_NAME_LOCALIZATION"
echo ""

# Sync dependencies
echo "📦 Syncing dependencies..."
uv sync

# Set up API keys for the run
export API_KEY_NAVIGATION="$HAI_API_KEY"
export API_KEY_LOCALIZATION="$HAI_API_KEY"

# Run the surfer-h-cli command
uv run surfer-h-cli \
    --task "$TASK" \
    --url "$URL" \
    --max_n_steps 30 \
    --base_url_localization "$HAI_MODEL_URL_LOCALIZATION" \
    --model_name_localization "$HAI_MODEL_NAME_LOCALIZATION" \
    --temperature_localization 0.7 \
    --base_url_navigation "$HAI_MODEL_URL_NAVIGATION" \
    --model_name_navigation "$HAI_MODEL_NAME_NAVIGATION" \
    --temperature_navigation 0.0