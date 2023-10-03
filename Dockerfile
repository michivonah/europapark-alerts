FROM python:3.11

# Create directory
RUN mkdir app
WORKDIR /app/

# Copy files
COPY main.py .
COPY requirements.txt .

# Set enviromental variables
ENV DISCORD_WEBHOOK "https://discord.com/api/webhooks/XXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYY"
ENV SUBS "383533, 323530, 353030"

# Install needed packages
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pip install --no-cache-dir -r requirements.txt

# Start app
CMD ["python3","main.py"]