FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip

RUN echo "===== requirements.txt =====" && \
    cat requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "===== Installed multipart =====" && \
    pip show python-multipart

# Install AWS CLI (if your project actually needs it)
RUN pip install --no-cache-dir awscli

EXPOSE 5000

CMD ["python", "app.py"]