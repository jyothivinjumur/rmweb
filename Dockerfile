# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Install SVM-light and download data files
RUN set -ex; \
	\
	apt-get update; \
	apt-get install -y --no-install-recommends wget; \
	rm -rf /var/lib/apt/lists/*; \
	\
	mkdir -p /fs/clip-ediscovery/jyothi/Research && \
	\
	wget -O svm_light_linux64.tar.gz "http://download.joachims.org/svm_light/current/svm_light_linux64.tar.gz" && \
	\
	tar -xzf svm_light_linux64.tar.gz -C /fs/clip-ediscovery/jyothi/Research/; \
	\
	mkdir /app/data;\
	\
	wget -O /app/data/ECAT-ds-op-label.tuple.dictionary.199328.p https://storage.googleapis.com/umd-may-jk/data-files/datafiles/ECAT-ds-op-label.tuple.dictionary.199328.p && \
	wget -O /app/data/GPOL-ds-op-label.tuple.dictionary.199328.p https://storage.googleapis.com/umd-may-jk/data-files/datafiles/GPOL-ds-op-label.tuple.dictionary.199328.p && \
	wget -O /app/data/rcv1_ECAT.txt https://storage.googleapis.com/umd-may-jk/data-files/datafiles/rcv1_ECAT.txt && \
	wget -O /app/data/rcv1_GPOL.txt https://storage.googleapis.com/umd-may-jk/data-files/datafiles/rcv1_GPOL.txt && \
	apt-get purge -y --auto-remove wget; 


# Copy the current directory contents into the container at /app
ADD . /app

# Create a log dir
RUN mkdir -p /app/logs

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80


# # Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
# CMD ["bash"]

