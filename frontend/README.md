# GenSEO Frontend (Next.js)

The **GenSEO Frontend** is a modern React application built with Next.js and Tailwind CSS. It provides an interactive interface for the SEO Agent.

## ✨ Features

-   **Mission Control**: Configure mission parameters (Topic, Content Type, Target Group, etc.).
-   **Real-time Feedback**: Connects to the backend via Server-Sent Events (SSE) to stream agent progress.
-   **Live Terminal**: Displays detailed logs of the agent's actions (e.g., "Found 10 competitors").
-   **Execution Graph**: Visualizes the current step in the SEO pipeline.
-   **Markdown Editor**: Displays the final generated content in an editable format.

## 🚀 Getting Started

### Prerequisites
-   Node.js 18+
-   npm

### Installation

```bash
cd frontend
npm install
```

### Running Development Server

```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## 🔧 Configuration

The frontend expects the backend to be running at `http://localhost:8000`.
To change this, update the `EventSource` URL in `app/page.tsx`.

## 📦 Key Libraries

-   `next`: React framework.
-   `tailwindcss`: Styling.
-   `lucide-react`: Icons.
-   `@uiw/react-md-editor`: Markdown editor.
