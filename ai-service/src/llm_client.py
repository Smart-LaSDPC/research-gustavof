import json
from langchain_openai import ChatOpenAI
from ratelimit import limits, sleep_and_retry

# System prompt instructs the LLM on its role and task expectations
SYSTEM_PROMPT = """You are a load balancing expert analyzing NGINX ingress metrics.
Your task is to:
1. Analyze provided NGINX ingress metrics
2. Evaluate if the current load balancing algorithm is optimal
3. Recommend whether to change the algorithm
4. Support your recommendation with clear, metric-based reasoning

Provide concise, technical recommendations focusing on load balancing efficiency."""


# Analysis prompt provides the data structure and expected analysis parameters
ANALYSIS_PROMPT_TEMPLATE = """
Analyze the following NGINX ingress metrics data:

Metrics Summary (JSON format):
{metrics_summary}

Please provide:
1. A brief overview of the current load distribution patterns
2. Analysis of performance trends across multiple time windows:
   - Short-term: 5m, 1h, 3h
   - Medium-term: 6h, 12h, 1d
   - Long-term: 3d, 7d
3. Specific recommendation on load balancing algorithm changes
4. Justification based on observed metrics patterns

Focus on key indicators such as request distribution, response times, and error rates if available.
"""

@sleep_and_retry
@limits(calls=5, period=60)  # 5 calls per minute
def get_llm_analysis(existing_summary, api_key):
    # Format the analysis prompt with the metrics summary
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        metrics_summary=json.dumps(existing_summary, indent=2)
    )
    
    # LLM is the model used to generate the analysis
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=api_key,
    )

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", prompt),
    ]
    output = llm.invoke(messages)

    return output.content
