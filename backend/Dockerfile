FROM python:3.11-slim

# Create a non-root user (required by Hugging Face)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

# Run FastAPI on the port HF expects
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
