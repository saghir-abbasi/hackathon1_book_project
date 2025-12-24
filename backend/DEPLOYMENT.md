# Backend Deployment Guide

## Vercel Deployment

To deploy the backend to Vercel, follow these steps:

1. Install the Vercel CLI:
```bash
npm install -g vercel
```

2. Login to your Vercel account:
```bash
vercel login
```

3. Navigate to the backend directory and deploy:
```bash
cd backend
vercel
```

## Environment Variables

For the deployed backend to work properly with the frontend, you need to set the following environment variables in your Vercel project settings:

### Required Environment Variables:

- `QDRANT_HOST`: Your Qdrant cloud instance URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_COLLECTION_NAME`: Your Qdrant collection name (default: book_embeddings)
- `DATABASE_URL`: Your PostgreSQL database connection string
- `EMBEDDING_MODEL_PROVIDER`: Either "gemini", "openai", or "claude"
- `GEMINI_API_KEY`: Your Google Gemini API key (if using Gemini)
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)
- `CLAUDE_API_KEY`: Your Anthropic API key (if using Claude)

### CORS Configuration:

- `CORS_ORIGINS`: Comma-separated list of allowed origins for your frontend
  - Example: `http://localhost:3000,https://your-username.github.io,https://your-frontend.vercel.app`

## Setting Environment Variables in Vercel Dashboard

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add all the required environment variables listed above

## Frontend Origin Configuration

Make sure to include all origins where your frontend will be hosted:

- Development: `http://localhost:3000` (or your Docusaurus dev server port)
- GitHub Pages: `https://your-username.github.io`
- Vercel deployment: `https://your-frontend-project.vercel.app`
- Any other deployment domains

## Testing the Deployment

After deployment, you can test the API at:
- Health check: `https://your-project.vercel.app/health`
- API endpoints: `https://your-project.vercel.app/api/...`

## Troubleshooting

If the frontend cannot connect to the backend after deployment:
1. Verify that the CORS_ORIGINS environment variable includes your frontend's origin
2. Check the browser console for CORS error messages
3. Ensure all required environment variables are properly set in Vercel
4. Verify that your Qdrant and database connections are working