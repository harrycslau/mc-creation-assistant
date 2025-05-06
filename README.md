# Multiple-Choice Questions Creation Assistant
A lightweight teacher tool to streamline the multiple-choice question creation process.

[DEMO](https://www.goodstudy.fi/tools/phymc/)

## My Lessons Learned in This Project

- **Using LLM APIs**: Gained experience integrating Large Language Model (LLM) APIs with FastAPI to create interactive web applications that utilize AI-powered responses.

- **LLM API Request Handling**: Learned how to manage LLM API requests efficiently, including setting up and saving API keys securely and ensuring that requests are routed properly to the correct services.

- **Helicone for LLM Monitoring**: Explored how to use Helicone as a monitoring and analytics tool to track LLM API performance, manage API usage, and optimize the handling of AI-based services.

- **Reverse Proxy Setup**: Learned how to set up a reverse proxy using Nginx to route specific URL paths (e.g., `/api/`) to a backend service like FastAPI.

- **Handling SSL with FastAPI**: Understood the importance of using Nginx to handle SSL and HTTPS for FastAPI, as FastAPI does not come with built-in SSL support.


## Note on Setting up FastAPI with Nginx Proxy

By default, FastAPI listens on port `8000`, but it does not have SSL enabled. To securely expose your FastAPI service, you can set up an Nginx proxy to direct traffic from `/api/` to `127.0.0.1:8000`.

In this example, we are using **HestiaCP** with the **Nginx** web server.

### Important: Avoid Directly Editing the Nginx Configuration

Instead of directly modifying the Nginx configuration files located at:

- `/etc/nginx/conf.d/domains/mydomain.com.conf`
- `/etc/nginx/conf.d/domains/mydomain.com.ssl.conf`

These files will be **rebuilt automatically** by HestiaCP, so any manual changes will be lost.

### Step 1: Create a Custom Nginx Template

To make persistent changes, you should create a custom Nginx template. This can be done by copying and editing the existing default templates.

1. Navigate to the templates directory:

   ```bash
   cd /usr/local/hestia/data/templates/web/nginx
   ```

2. Copy the default templates to new custom templates:

   ```bash
   sudo cp default.tpl default_api.tpl
   sudo cp default.stpl default_api.stpl
   ```

### Step 2: Edit the Custom Template

Edit the `default_api.stpl` file (for SSL-enabled traffic). This file will handle HTTPS traffic. You only need to edit this if you have HTTP auto-forwarding to HTTPS.

```bash
sudo nano /usr/local/hestia/data/templates/web/nginx/default_api.stpl
```

Inside the `server` block, add the following lines to set up the reverse proxy for FastAPI:

```nginx
# Proxy /api/ requests to FastAPI
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Save the changes to the template file.

### Step 3: Apply the Custom Template in HestiaCP

1. Log in to **HestiaCP**.
2. Navigate to the **Web** section.
3. Find your domain and click **Edit**.
4. Click **Advanced Settings**.
5. Under **Proxy Template**, select the new `default_api` template that you just created.
6. Save the changes.

<img width="641" alt="image" src="https://github.com/user-attachments/assets/148cf784-28b1-4362-800b-46ffb1746d4e">

Your domain is now set up to forward API requests from `mydomain.com/api/` to your FastAPI app running on `127.0.0.1:8000`.
