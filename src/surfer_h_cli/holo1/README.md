### Installing vLLM

1. Install vLLM using the instructions provided by vLLM  `https://docs.vllm.ai/en/latest/getting_started/installation/index.html`
(we use version 0.8.4 and cuda 12.8, which we installed with `pip install vllm==0.8.4 --extra-index-url https://download.pytorch.org/whl/cu128`)

2. `pip install "transformers<4.53.0" to get the correct version of transformers`

### Serving a Model

#### Serving a Single Model

This is how you serve Holo1-3B
```
vllm serve Hcompany/Holo1-3B --port 8081
```

In this case the server address and api-key will default to:
```
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8081/v1"
```

You can test it out with this example (adapted from the vLLM Quickstart guide)

```sh
curl http://localhost:8081/v1/chat/completions     -H "Content-Type: application/json"     -d '{
        "model": "Hcompany/Holo1-3B",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }'
```

The above request should return:

```json
{
    "id":"chatcmpl-7ee08d9882c44adbac1872c9073d81da",
    "object":"chat.completion",
    "created":1751378545,
    "model":"Hcompany/Holo1-3B",
    "choices":[
        {
            "index":0,
            "message":{
                "role":"assistant",
                "reasoning_content":null,
                "content":"The New York Yankees won the World Series in 2020.",
                "tool_calls":[]},
                "logprobs":null,
                "finish_reason":"stop",
                "stop_reason":null
                }
            ],
    "usage":{
        "prompt_tokens":31,
        "total_tokens":47,
        "completion_tokens":16,
        "prompt_tokens_details":null
    },
    "prompt_logprobs":null}
```

### Serving more than one model
This is only necessary if you want different components of your agent to use different models that you also happen to host local.
In this case you will need more than one GPU as the memory requirements per model is likely to exceed the memory of one GPU.
To achieve this, we limit the visible GPUs to the one we want to use.
We also need to give each models its own port using `--port`, in order for the requests to be routed correctly.

```sh
# this launches the first model
CUDA_VISIBLE_DEVICES=0 vllm serve Hcompany/Holo1-3B --port 8081
```

```sh
# this launches the second model
CUDA_VISIBLE_DEVICES=1 vllm serve Hcompany/Holo1-7B --port 8082
```

```sh
# query the first model
curl http://localhost:8081/v1/chat/completions     -H "Content-Type: application/json"     -d '{
        "model": "Hcompany/Holo1-3B",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }'

# query the second model model
curl http://localhost:8082/v1/chat/completions     -H "Content-Type: application/json"     -d '{
        "model": "Hcompany/Holo1-7B",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }'
```

There is, of course, more to it than the above, you can tweak things like tensor and pipeline-parallelism and do a lot
of other stuff to tweak the inference speed of your model(s) please refer to the vLLM documentation for more details!
