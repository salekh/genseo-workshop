#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Stopping application..."
    # Kill all child processes of this script
    pkill -P $$
    exit
}

trap cleanup SIGINT SIGTERM

echo "Starting Backend..."
cd backend
# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "Using uv to run backend..."
    # Run uvicorn with uv, ensuring dependencies are available
    uv run uvicorn main:app --reload --port 8000 &
else
    echo "uv not found, trying python directly..."
    uvicorn main:app --reload --port 8000 &
fi
BACKEND_PID=$!
cd ..

echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Application started."
echo "Backend running on PID $BACKEND_PID (http://localhost:8000)"
echo "Frontend running on PID $FRONTEND_PID (http://localhost:3000)"
echo "Press Ctrl+C to stop both."

wait
