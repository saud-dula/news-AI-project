# BLOCK 1: This script creates the exact educational dataset used for training.
import csv
import random
from pathlib import Path

random.seed(42)
OUT = Path(__file__).parent / "data" / "training_data.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

# BLOCK 2: Phrase pools create varied, labeled news-style sentences.
real_subjects = ["the health department", "the election commission", "the city council", "the university", "the central bank", "the railway authority", "the district court", "the weather office", "the research team", "the police department", "the education ministry", "the public hospital", "the stock exchange", "the football club", "the transport agency"]
real_actions = ["published a detailed report", "released verified results", "announced the updated schedule", "confirmed the decision", "issued a public advisory", "shared the official figures", "approved the annual plan", "opened public applications", "scheduled the next hearing", "reported the quarterly numbers", "published the study methods", "updated the safety guidance"]
real_sources = ["on its official website", "in a signed public notice", "according to meeting minutes", "in a regulatory filing", "through a verified statement", "in a peer reviewed journal", "with a downloadable data table", "during a scheduled press briefing", "in the public case record", "through the official information portal"]
real_times = ["on Monday", "after Tuesday's meeting", "for the coming week", "before markets opened", "following a scheduled review", "for the next academic term", "after an independent audit", "during the monthly update"]
real_details = ["The document includes dates and contact information.", "The figures can be checked in the linked public record.", "Officials asked readers to follow the published instructions.", "The full methodology and limitations are listed in the report.", "Local offices were told to provide the same information.", "The statement names the responsible department and spokesperson."]

fake_openers = ["Shocking secret", "A viral message claims", "Anonymous experts reveal", "Share immediately because", "They do not want you to know that", "A deleted post proves", "Breaking hidden truth", "One miracle trick shows"]
fake_claims = ["one fruit cures every disease overnight", "all mobile phones will explode at midnight", "the internet will permanently close tomorrow", "a hidden planet will hit Earth this weekend", "every citizen will receive a free luxury car", "a secret code makes people invisible", "hot water removes every virus in five minutes", "one coin will become a million times more valuable", "schools are secretly controlled by aliens", "a leaf causes instant weight loss without exercise", "breathing outdoors will be banned tomorrow", "a celebrity has died without any family statement"]
fake_pressure = ["Forward this to twenty friends now.", "Act before every news channel deletes it.", "Click the unknown link and enter your bank details.", "Doctors and hospitals are hiding the truth.", "No evidence is needed because the message is guaranteed.", "Buy now before banks stop the offer.", "The unnamed source says it is one hundred percent true.", "Do not check other websites because they are part of the cover-up."]
fake_sources = ["No document or named source is provided.", "The claim comes from an undated voice note.", "The post gives no link to evidence.", "The account publishing it is anonymous.", "The image has no date, location, or original source.", "The message misuses an old photograph as proof."]

neutral_topics = ["The update concerns local services.", "Readers discussed the claim online.", "The story became popular during the evening.", "Several people asked for more information.", "The subject attracted public attention.", "The message mentions health and public safety."]

# BLOCK 3: Generate 500 unique REAL and 500 unique FAKE samples.
def create_unique(label, count):
    rows = set()
    while len(rows) < count:
        if label == "REAL":
            text = f"{random.choice(real_subjects).title()} {random.choice(real_actions)} {random.choice(real_times)} {random.choice(real_sources)}. {random.choice(real_details)} {random.choice(neutral_topics)}"
        else:
            text = f"{random.choice(fake_openers)} {random.choice(fake_claims)}. {random.choice(fake_pressure)} {random.choice(fake_sources)} {random.choice(neutral_topics)}"
        rows.add(text)
    return [(text, label) for text in sorted(rows)]

rows = create_unique("REAL", 500) + create_unique("FAKE", 500)
random.shuffle(rows)

# BLOCK 4: Save the training data as a normal CSV file.
with OUT.open("w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "label"])
    writer.writerows(rows)
print(f"Created {len(rows)} rows at {OUT}")
