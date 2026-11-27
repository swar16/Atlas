import time
from app.llm.client import model

start = time.perf_counter()

try:
    print("Sending request to NVIDIA...", flush=True)

    response = model.invoke("Say hello.")

    print("Response:", response.content)

except Exception as e:
    print("Error:", type(e).__name__, str(e))

finally:
    print(f"Elapsed: {time.perf_counter() - start:.2f}s")