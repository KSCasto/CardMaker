FROM python:3.8-slim 
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Install dependencies
COPY src/requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY ./src .

# Use Gunicorn to serve the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
