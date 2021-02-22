FROM rayproject/ray:nightly-py36

RUN pip install feast
RUN sudo apt update && sudo apt install -y curl

COPY serve_app.py .
