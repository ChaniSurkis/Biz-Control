FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy NetFree CA
COPY certs/Netfree.crt /usr/local/share/ca-certificates/Netfree.crt

# Register CA into Linux trust store
RUN update-ca-certificates

# ----- FIX FOR PYTHON / CERTIFI -----
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org certifi
RUN python3 - << 'EOF'
import certifi, shutil
print("Replacing certifi CA...")
shutil.copyfile("/etc/ssl/certs/ca-certificates.crt", certifi.where())
print("Certifi CA replaced successfully.")
EOF
# ------------------------------------

# Copy project requirements first
COPY requirements.txt .

# Install project dependencies including PostgreSQL driver and email validator
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt


RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org alembic

# Copy app source code
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Run the app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
