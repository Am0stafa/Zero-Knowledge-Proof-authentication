FROM python:3.9-slim
WORKDIR /app
COPY . .
# packages to open a gui python app
RUN pip install -r requirements.txt && apt-get update && apt-get install -y libx11-6 libxext6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev tk-dev && rm -rf /var/lib/apt/lists/*
# stream the display
CMD ["python", "ui.py"]