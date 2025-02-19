# GitHub Setup Instructions

1. First, create a new repository on GitHub:
   - Go to https://github.com/new
   - Name your repository (e.g., "edusphere-landing")
   - Choose if you want it to be public or private
   - Don't initialize with README (we already have one)

2. Initialize git in your project folder:
```bash
git init
```

3. Add your files and make your first commit:
```bash
git add .
git commit -m "Initial commit"
```

4. Add your GitHub repository as remote and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

Note: Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual GitHub username and repository name.

Important: Make sure you have Git installed and are logged in with your GitHub credentials.
