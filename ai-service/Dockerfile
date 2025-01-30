# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV OPENAI_API_KEY=sk-proj-s246J7yBjSnfvFDjS5sbT3BlbkFJy5ml8zJ7CBGZGidVmWu8
ENV OPENAI_MODEL_NAME=gpt-4o-mini

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies with upgraded pip
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .
COPY tabs/ ./tabs/
COPY src/ ./src/

# Expose the port Streamlit runs on
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Command to run the application
CMD ["streamlit", "run", "main.py"]