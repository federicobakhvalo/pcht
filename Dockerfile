FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY ./req.txt /app/req.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code
COPY . /app/

# Set the entry point for the bot
#CMD ["sh", "-c",  "python bot.py"]
#CMD ["sh", "-c", "python MySqlConnection.py && python bot.py"]