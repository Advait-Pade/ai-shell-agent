FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y software-properties-common curl \
    libxcb1 \
    libx11-6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

# RUN mkdir vllm-test
WORKDIR /app/vllm-test

RUN uv venv --python 3.11
RUN uv pip install \
    --python .venv/bin/python \
    vllm \
    bitsandbytes \
    --torch-backend=auto

CMD ["/app/vllm-test/.venv/bin/python"]
# CMD ["/app/vllm-test/.venv/bin/python", "-m", "vllm.entrypoints.openai.api_server", "--host", "0.0.0.0","--port", "8000","--model", "mistralai/Mistral-7B-Instruct-v0.3","--tensor-parallel-size", "1","--max-model-len", "8192","--quantization", "bitsandbytes","--gpu-memory-utilization", "0.85","--max-num-seqs", "8","--max-num-batched-tokens", "2048","--enable-auto-tool-choice","--tool-call-parser", "mistral"]
