# Start from a core stack version
FROM jupyter/minimal-notebook:dc57157d6316
# Install from requirements.txt file
COPY requirements.txt /tmp/

RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions "$CONDA_DIR" && \
    fix-permissions "/home/$NB_USER"

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]