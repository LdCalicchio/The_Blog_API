# Roadmap Project - Blog API

This is a RESTful API for a blog application, built using Flask. It is designed to handle CRUD operations for blog posts.
You can find the original project idea here: https://roadmap.sh/projects/blogging-platform-api

## Features

- Create, Read, Update, and Delete blog posts.
- REST API endpoints.

## Setup Instructions

1. **Clone the repository**

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**
   ```bash
   flask run
   ```

5. **Post structure**
   ```json
   {
     "title": "Example of blog post",
     "content": "This is the content of the blog post.",
     "category": "Any",
     "tags": ["Example", "Post"]
   }
   ```