# 1. Official python image
FROM python:3.10-slim

# 2. Set the working dir inside the container
WORKDIR /app

# 3. Copy the dependency file
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Command to run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]