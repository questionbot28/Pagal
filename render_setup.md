# Render Deployment Setup Guide

## Environment Variables
Set these environment variables in your Render dashboard:

1. `DATABASE_URL`: Your PostgreSQL database URL (Render will provide this if you create a PostgreSQL database)
2. `SESSION_SECRET`: A secure random string for session encryption (generate using a secure method)
3. `DISCORD_CLIENT_ID`: Your Discord application client ID
4. `DISCORD_CLIENT_SECRET`: Your Discord application client secret
5. `DISCORD_REDIRECT_URI`: Set this to `https://your-render-app-name.onrender.com/callback`

## Steps for Deployment

1. **Create a new Web Service**
   - Connect your GitHub repository
   - Select the Python runtime environment
   - Build Command: `poetry install`
   - Start Command: `gunicorn main:app`

2. **Setup Database**
   - Create a new PostgreSQL database in Render
   - The `DATABASE_URL` will be automatically added to your environment variables

3. **Update Discord OAuth**
   - Go to Discord Developer Portal
   - Update your OAuth2 redirect URI to match your Render domain
   - Add `https://your-render-app-name.onrender.com/callback` to the allowed redirect URIs

4. **Verify Deployment**
   - Once deployed, your app will be available at `https://your-render-app-name.onrender.com`
   - Test the Discord login functionality
   - Check if the database connections are working

## Important Notes

- Make sure all the required packages are in your requirements.txt (already configured)
- The application uses gunicorn for production deployment (specified in Procfile)
- PostgreSQL database will be automatically provisioned if you create it in Render
- Always test the application locally before deploying

## Troubleshooting

If you encounter any issues:
1. Check the Render logs for any error messages
2. Verify all environment variables are set correctly
3. Ensure your Discord OAuth2 credentials and redirect URIs are properly configured
4. Check the database connection string format