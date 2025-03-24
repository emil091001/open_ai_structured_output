
import json
from config import *
from metrics2 import Metrics


metrics = Metrics()

metrics.calculate("data/output", "data/target")
metrics.save("data/metrics.json")

# metrics.load('data/metrics.json')

print(json.dumps(metrics.table_averages(), indent=4))
