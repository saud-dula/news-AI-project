# BLOCK 1: Import only Python standard-library tools.
import csv
import json
import math
import random
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "training_data.csv"
MODEL_FILE = BASE / "model" / "model.json"
METRICS_FILE = BASE / "model" / "metrics.json"
RANDOM_SEED = 42

# BLOCK 2: Split text into lowercase word tokens.
def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())

# BLOCK 3: Read the exact CSV dataset supplied with this project.
def load_rows():
    with DATA_FILE.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    return [(row["text"], row["label"].upper()) for row in rows]

# BLOCK 4: Train a Multinomial Naive Bayes text classifier.
def train(rows):
    classes = {"REAL": {"documents": 0, "total_words": 0, "words": Counter()},
               "FAKE": {"documents": 0, "total_words": 0, "words": Counter()}}
    vocabulary = set()
    for text, label in rows:
        words = tokenize(text)
        classes[label]["documents"] += 1
        classes[label]["words"].update(words)
        classes[label]["total_words"] += len(words)
        vocabulary.update(words)
    return {"algorithm": "Multinomial Naive Bayes", "classes": classes,
            "vocabulary": sorted(vocabulary), "document_count": len(rows)}

# BLOCK 5: Predict one article using log probabilities and Laplace smoothing.
def predict(model, text):
    words = tokenize(text)
    vocabulary_size = len(model["vocabulary"])
    scores = {}
    for label in ("REAL", "FAKE"):
        info = model["classes"][label]
        score = math.log(info["documents"] / model["document_count"])
        denominator = info["total_words"] + vocabulary_size
        for word in words:
            score += math.log((info["words"].get(word, 0) + 1) / denominator)
        scores[label] = score
    return max(scores, key=scores.get)

# BLOCK 6: Use a fixed 80/20 stratified train-test split.
def split_rows(rows):
    random.seed(RANDOM_SEED)
    real = [row for row in rows if row[1] == "REAL"]
    fake = [row for row in rows if row[1] == "FAKE"]
    random.shuffle(real); random.shuffle(fake)
    real_cut = int(len(real) * 0.8); fake_cut = int(len(fake) * 0.8)
    return real[:real_cut] + fake[:fake_cut], real[real_cut:] + fake[fake_cut:]

# BLOCK 7: Calculate accuracy, precision, recall, F1, and confusion matrix.
def evaluate(model, test_rows):
    matrix = {"REAL": {"REAL": 0, "FAKE": 0}, "FAKE": {"REAL": 0, "FAKE": 0}}
    for text, actual in test_rows:
        matrix[actual][predict(model, text)] += 1
    correct = matrix["REAL"]["REAL"] + matrix["FAKE"]["FAKE"]
    total = len(test_rows)
    per_class = {}
    for label, other in (("REAL", "FAKE"), ("FAKE", "REAL")):
        tp = matrix[label][label]
        fp = matrix[other][label]
        fn = matrix[label][other]
        precision = tp / (tp + fp) if tp + fp else 0
        recall = tp / (tp + fn) if tp + fn else 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
        per_class[label] = {"precision": precision, "recall": recall, "f1": f1}
    return {"accuracy": correct / total, "test_samples": total,
            "confusion_matrix": matrix, "per_class": per_class}

# BLOCK 8: Evaluate honestly, then retrain the delivered model on all rows.
rows = load_rows()
train_rows, test_rows = split_rows(rows)
evaluation_model = train(train_rows)
metrics = evaluate(evaluation_model, test_rows)
final_model = train(rows)

# Convert Counter objects into normal JSON dictionaries.
for label in ("REAL", "FAKE"):
    final_model["classes"][label]["words"] = dict(final_model["classes"][label]["words"])

MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
MODEL_FILE.write_text(json.dumps(final_model, indent=2), encoding="utf-8")
metrics.update({"algorithm": final_model["algorithm"], "total_dataset_samples": len(rows),
                "training_samples_for_evaluation": len(train_rows), "random_seed": RANDOM_SEED,
                "dataset_type": "Synthetic educational dataset generated from varied templates",
                "warning": "This benchmark does not guarantee the same accuracy on real-world news."})
METRICS_FILE.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(f"Training complete: {len(rows)} samples")
print(f"Holdout accuracy: {metrics['accuracy'] * 100:.2f}%")
print("Model:", MODEL_FILE)
print("Metrics:", METRICS_FILE)
