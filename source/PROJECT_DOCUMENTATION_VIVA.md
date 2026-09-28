# NewsCheck AI — Complete Project and Viva Documentation

## 1. Project summary

**Project name:** NewsCheck AI  
**Project type:** Offline beginner-level fake-news text classifier  
**Frontend:** HTML, CSS, and JavaScript  
**AI algorithm:** Multinomial Naive Bayes  
**Training language:** Python 3  
**Dataset:** 1,000 synthetic English news-style samples  
**Output:** `REAL NEWS` or `FAKE NEWS`, with model confidence and vocabulary coverage

NewsCheck AI reads the words in a news article and compares their learned patterns with examples labeled `REAL` and `FAKE`. It does not search the internet and does not verify an event against live sources. It is a text-pattern classifier and an educational demonstration.

---

## 2. Problem statement

Fake or misleading information can spread quickly online. A beginner may not know how to check every claim. This project demonstrates how a machine-learning text classifier can examine writing patterns and provide an initial warning.

The model is not a replacement for professional fact-checking. A final decision should also consider the original source, date, supporting evidence, and reports from other reliable publishers.

---

## 3. Project objectives

1. Accept news text from the user.
2. Convert the text into words that a model can process.
3. Compare the words with learned REAL and FAKE patterns.
4. Display `REAL NEWS` or `FAKE NEWS`.
5. Show an understandable confidence indicator.
6. Work offline without uploading the user's text.
7. Keep the code simple enough for a beginner to explain.
8. Include the exact training data, model, and evaluation report.

---

## 4. Folder structure

```text
NewsCheck_AI_v3/
│
├── NewsCheck_AI.html          # Complete standalone website and embedded model
├── START_HERE.bat             # Windows launcher
├── README_FIRST.txt           # Short opening and usage instructions
├── PROJECT_DOCUMENTATION_VIVA.md
│
├── generate_dataset.py        # Generates the synthetic dataset
├── train_model.py             # Trains and evaluates the AI model
├── build_app.py               # Embeds model.json into the final HTML file
│
├── data/
│   └── training_data.csv      # Exact 1,000-row training dataset
│
└── model/
    ├── model.json             # Trained word counts, vocabulary, and model settings
    └── metrics.json           # Accuracy, precision, recall, F1, and confusion matrix
```

---

## 5. How the complete system works

The project has two different phases.

### Phase A: Development and training

```text
generate_dataset.py
        ↓
data/training_data.csv
        ↓
train_model.py
        ↓
model/model.json + model/metrics.json
        ↓
build_app.py
        ↓
NewsCheck_AI.html
```

### Phase B: User prediction

```text
User opens NewsCheck_AI.html
        ↓
User pastes news text
        ↓
JavaScript tokenizes the text
        ↓
Embedded Naive Bayes model calculates REAL and FAKE scores
        ↓
The larger score becomes the prediction
        ↓
The page displays REAL NEWS or FAKE NEWS
```

The final user does not need Python because the trained model has already been embedded inside `NewsCheck_AI.html`.

---

# PART A — AI MODEL

## 6. Which AI model is used?

The project uses **Multinomial Naive Bayes**.

It is a supervised machine-learning classification algorithm. “Supervised” means the model learns from examples that already have correct labels. In this project, every training row is labeled either `REAL` or `FAKE`.

Multinomial Naive Bayes is suitable for a beginner project because:

- it works well with word counts;
- it is fast;
- it requires little computer memory;
- its calculations are easier to explain than a neural network;
- the trained model can be stored as simple JSON data.

## 7. Simple explanation of Naive Bayes

Imagine two boxes:

- a REAL box containing words learned from real-style examples;
- a FAKE box containing words learned from fake-style examples.

If words such as `official`, `published`, `report`, and `verified` frequently appear in the REAL box, they increase the REAL score.

If words such as `shocking`, `secret`, `miracle`, `overnight`, and `share immediately` frequently appear in the FAKE box, they increase the FAKE score.

The model calculates both scores and returns the class with the higher probability.

## 8. What does “naive” mean?

The algorithm makes a simplifying assumption that each word contributes independently to the result. Real language is more complicated, so this assumption is not completely true. However, it often works well enough for basic text-classification demonstrations.

## 9. Why logarithms are used

The probability of a complete article is produced by multiplying many small word probabilities. That number can become too small for a computer to represent accurately. The code therefore adds logarithms of probabilities instead of directly multiplying tiny numbers.

## 10. What is Laplace smoothing?

A new article may contain a word that never appeared in one class. Without protection, its probability would become zero and destroy the full score.

Laplace smoothing adds `1` to every word count:

```text
smoothed word probability = (word count + 1) / (total words + vocabulary size)
```

This allows the model to handle previously unseen words.

---

## 11. Where exactly is the AI model stored?

The trained development model is stored in:

```text
model/model.json
```

It contains:

- algorithm name;
- total document count;
- full vocabulary;
- number of REAL documents;
- number of FAKE documents;
- total word counts for both classes;
- count of every learned word in each class.

The final application also contains the same model inside:

```text
NewsCheck_AI.html
```

Search for this line inside the HTML file:

```javascript
const model = { ... };
```

`build_app.py` copies the data from `model/model.json` into that JavaScript variable. This is why the final HTML works offline and does not need a separate model file.

---

## 12. Was the model pre-trained?

Yes. The delivered `NewsCheck_AI.html` already contains the trained model. The user can open it and immediately make predictions.

It is important to use the correct meaning:

- It is **pre-trained for this project** on the supplied 1,000-row dataset.
- It is **not** a large pre-trained language model such as BERT or ChatGPT.
- It does not understand facts or browse the internet.
- It learns statistical word patterns.

---

## 13. Dataset details

The exact dataset is:

```text
data/training_data.csv
```

CSV means Comma-Separated Values. It can be opened in Excel, Google Sheets, LibreOffice Calc, or a text editor.

It has two columns:

```csv
text,label
"The health department published a report...",REAL
"Shocking secret cure...",FAKE
```

Dataset size:

- 1,000 total samples;
- 500 REAL samples;
- 500 FAKE samples;
- English language;
- synthetic educational content generated from varied phrase templates.

### Why the dataset is called synthetic

The articles were created by code from controlled phrase groups. They were not collected from live news websites. This makes the dataset safe and easy to distribute, but less realistic than a professional dataset.

---

## 14. How and where was the model trained?

The model was trained using:

```text
train_model.py
```

Training was performed in a Python environment. The script reads `data/training_data.csv`, counts words in REAL and FAKE examples, evaluates the model, and saves the trained result in `model/model.json`.

The training computer or location is not required after training. The learned model is saved in the project and embedded into the HTML application.

### Why training did not need exactly 25 minutes

Multinomial Naive Bayes is not an epoch-based deep neural network. It learns the required counts in one complete pass through the dataset. Once every row has been processed, leaving it running for more minutes does not improve the model. Therefore, training was completed to convergence and then evaluated instead of being artificially delayed.

---

## 15. Training and evaluation process

A fixed random seed of `42` was used so the split can be reproduced.

The labeled data was divided using an 80/20 stratified split:

- 800 samples for training during evaluation;
- 200 samples for holdout testing;
- 100 REAL test samples;
- 100 FAKE test samples.

“Stratified” means both classes keep the same balanced proportion.

After evaluation, the final delivered model was trained again on all 1,000 rows so it could learn from the complete supplied dataset.

---

## 16. Evaluation results

The report is stored in:

```text
model/metrics.json
```

Recorded holdout result:

- Accuracy: 100%
- REAL precision: 100%
- REAL recall: 100%
- REAL F1-score: 100%
- FAKE precision: 100%
- FAKE recall: 100%
- FAKE F1-score: 100%

Confusion matrix:

| Actual class | Predicted REAL | Predicted FAKE |
|---|---:|---:|
| REAL | 100 | 0 |
| FAKE | 0 | 100 |

### Honest limitation of this result

The score is unusually high because training and test data were generated from the same controlled template system. This creates very clear patterns. It does **not** prove 100% accuracy on real internet news and does not guarantee real-world 90% accuracy.

A professional evaluation should use articles from different publishers, topics, writing styles, dates, and sources that were not used while creating the training data.

---

## 17. Meaning of evaluation terms

### Accuracy

The percentage of all test predictions that were correct.

```text
Accuracy = correct predictions / all predictions
```

### Precision

When the model predicts a class, precision measures how often that prediction is correct.

### Recall

Recall measures how many items of a class the model successfully found.

### F1-score

F1 combines precision and recall into one balanced score.

### Confusion matrix

A table showing correct and incorrect predictions for each class.

---

# PART B — FILE-BY-FILE AND BLOCK-BY-BLOCK EXPLANATION

## 18. `generate_dataset.py`

### BLOCK 1 — Basic setup

Imports `csv`, `random`, and `Path`. It sets a fixed random seed and decides where the CSV file will be saved.

### BLOCK 2 — Phrase pools

Stores lists of subjects, actions, sources, times, details, fake claims, pressure phrases, and neutral sentences.

Examples:

- real-style source: “on its official website”;
- fake-style pressure: “Forward this to twenty friends now.”

### BLOCK 3 — Generate unique samples

The function combines random phrases into complete text. A Python `set` prevents duplicate rows. It creates exactly 500 REAL and 500 FAKE samples.

### BLOCK 4 — Save CSV

Creates `data/training_data.csv` with the columns `text` and `label`.

---

## 19. `train_model.py`

### BLOCK 1 — Imports and file paths

Imports standard-library tools. No external machine-learning package is required. It defines the locations of the CSV, model JSON, and metrics JSON files.

### BLOCK 2 — Tokenization

The `tokenize()` function:

1. changes text to lowercase;
2. finds English letters and numbers;
3. returns a list of words.

Example:

```text
"Official Report Released!" → ["official", "report", "released"]
```

### BLOCK 3 — Load data

Opens the CSV file and reads each row as `(text, label)`.

### BLOCK 4 — Train model

For each labeled article, the script:

1. tokenizes the article;
2. increases the document count for its class;
3. counts each word;
4. updates the total number of words;
5. adds the word to the vocabulary.

### BLOCK 5 — Predict one article

Calculates REAL and FAKE log scores using class probability, word probability, and Laplace smoothing. It returns the class with the larger score.

### BLOCK 6 — Split the data

Separates REAL and FAKE examples, shuffles them using seed `42`, and creates the 80/20 split.

### BLOCK 7 — Evaluate the model

Builds the confusion matrix and calculates accuracy, precision, recall, and F1-score.

### BLOCK 8 — Save the final outputs

First evaluates a model using only the training portion. Then trains the final model on all rows. It saves:

- `model/model.json`;
- `model/metrics.json`.

---

## 20. `build_app.py`

### Main block — Build the standalone application

This script reads:

- `model/model.json`;
- `model/metrics.json`.

It then creates the final HTML template and replaces the placeholder `__MODEL_JSON__` with the actual trained model.

Final output:

```text
NewsCheck_AI.html
```

This technique connects the model and website permanently in one file.

---

## 21. `NewsCheck_AI.html`

### BLOCK 1 — HTML document setup

Defines UTF-8 text, responsive mobile behavior, page description, and browser title. It also states that the app is standalone.

### BLOCK 2 — Shared colors and dimensions

CSS variables store common colors such as blue, green, red, text, border, and background colors. Changing a variable updates many parts of the design.

### BLOCK 3 — Navigation and status

Styles the top bar, project logo, and “Pre-trained model ready” indicator.

### BLOCK 4 — Hero and model information

Styles the large heading and the model-information card. The card displays the algorithm, dataset size, offline status, and readiness.

### BLOCK 5 — News input card

Styles the text area, character counter, Clear button, and Analyze news button. Focus styling helps keyboard and accessibility users.

### BLOCK 6 — Prediction result

Creates different visual states:

- green for REAL NEWS;
- red for FAKE NEWS;
- amber for an input error.

It also styles the confidence bar and explanation.

### BLOCK 7 — Samples and safety guidance

Styles sample buttons, verification cards, and the benchmark warning. Responsive CSS changes multi-column sections into one column on small screens.

### BLOCK 8 — Visible interface

Contains the actual page content that the user sees: navigation, heading, model information, text box, results, samples, verification advice, and warning.

### BLOCK 9 — Embedded trained model

The JavaScript variable `model` contains the trained data copied from `model/model.json`.

This is the most important answer to the viva question: **the AI model used by the final website is stored in the JavaScript `model` variable inside `NewsCheck_AI.html`.**

### BLOCK 10 — Tokenization in the browser

Converts user input to lowercase English word tokens using a regular expression.

### BLOCK 11 — Browser prediction

Calculates REAL and FAKE scores using the same Naive Bayes formula used in Python. It converts the two scores into a relative confidence value and counts recognized vocabulary words.

### BLOCK 12 — Connect controls

Uses JavaScript DOM selectors to connect the input field, counter, buttons, result label, icon, confidence, and explanation. It also makes the two sample buttons work.

### BLOCK 13 — Validate and display

Rejects input shorter than 40 characters. For valid input, it calls `predict()`, selects the result style, limits the displayed confidence to 97%, and shows vocabulary coverage plus a verification warning.

---

## 22. `START_HERE.bat`

### BLOCK 1 — Open the correct folder

`cd /d "%~dp0"` moves Command Prompt to the folder containing the launcher.

### BLOCK 2 — Open the application

The Windows `start` command opens `NewsCheck_AI.html` in the default browser.

### BLOCK 3 — Error guidance

If Windows cannot open it, the launcher tells the user to right-click the HTML file and choose Chrome or Edge.

---

## 23. `model/model.json`

This is not normal program code. It is serialized model data. JSON makes it easy for both Python and JavaScript to read the same trained model.

Important keys:

- `algorithm` — model name;
- `classes` — REAL and FAKE statistics;
- `documents` — documents learned in each class;
- `total_words` — total tokens per class;
- `words` — frequency of every learned word;
- `vocabulary` — all unique learned words;
- `document_count` — total training documents.

---

## 24. `model/metrics.json`

Stores the evaluation report in machine-readable JSON format. It records accuracy, test sample count, confusion matrix, precision, recall, F1, dataset type, and the real-world warning.

---

# PART C — RUNNING THE PROJECT

## 25. Can it run locally on another laptop?

Yes. The easiest version works on Windows, macOS, or Linux as long as a modern browser is installed.

### Method 1 — No Python required

1. Copy `NewsCheck_AI.html` to the other laptop.
2. Double-click the file.
3. If it does not open, right-click it.
4. Select **Open with**.
5. Select Chrome, Edge, Firefox, or Safari.

The app is offline because the HTML contains the CSS, JavaScript, and model.

### Method 2 — Windows launcher

1. Copy the complete folder.
2. Double-click `START_HERE.bat`.

### Method 3 — Simple local web server

If Python is installed, open Command Prompt in the project folder and run:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/NewsCheck_AI.html
```

### Method 4 — Retrain the model

Python 3 is required:

```bash
python train_model.py
python build_app.py
```

Then reopen `NewsCheck_AI.html`.

---

# PART D — GITHUB PAGES DEPLOYMENT FOR A COMPLETE BEGINNER

## 26. What GitHub and GitHub Pages do

GitHub stores project files in an online folder called a repository. GitHub Pages can publish static HTML, CSS, and JavaScript files as a public website.

This project is suitable for GitHub Pages because prediction runs directly in the browser. No Python server is needed after deployment.

## 27. Before uploading

GitHub Pages normally looks for a home file named:

```text
index.html
```

Make a copy of `NewsCheck_AI.html` and rename the copy to `index.html`. A GitHub-ready package is supplied separately with this documentation.

## 28. Create a GitHub account

1. Open `https://github.com/`.
2. Click **Sign up**.
3. Enter your email address.
4. Create a password and username.
5. Complete verification.
6. Verify the message sent to your email.
7. Keep the account recovery information safe.

## 29. Create a repository

1. Sign in to GitHub.
2. Click the **+** icon near the top-right corner.
3. Select **New repository**.
4. Repository name: `newscheck-ai`.
5. Description: `Beginner offline AI fake news detection project`.
6. Select **Public** if you want to use the simplest free GitHub Pages setup.
7. Optionally check **Add a README file**.
8. Click **Create repository**.

## 30. Upload without Git commands

1. Open the new repository.
2. Click **Add file**.
3. Select **Upload files**.
4. Drag `index.html` into the upload area.
5. You may also upload `training_data.csv`, `train_model.py`, `model.json`, `metrics.json`, and the documentation for project evidence.
6. In the commit message box, write `Upload NewsCheck AI project`.
7. Click **Commit changes**.

Only `index.html` is required for the live website because the trained model is embedded inside it.

## 31. Turn on GitHub Pages

1. Open the repository.
2. Select **Settings**.
3. In the left sidebar, select **Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select the `main` branch.
6. Select the `/ (root)` folder.
7. Click **Save**.
8. Wait a few minutes.
9. Refresh the Pages settings screen.
10. GitHub will display the public website address.

The URL normally looks similar to:

```text
https://YOUR-USERNAME.github.io/newscheck-ai/
```

## 32. Updating the live website

1. Edit or rebuild `NewsCheck_AI.html`.
2. Rename or copy it as `index.html`.
3. Open the GitHub repository.
4. Open the existing `index.html`.
5. Use the edit/upload option to replace it.
6. Commit the change.
7. Wait for GitHub Pages to rebuild.

## 33. Common GitHub Pages problems

### The site shows 404

- Confirm the file is exactly `index.html`.
- Confirm Pages uses the `main` branch and `/ (root)`.
- Wait several minutes after enabling Pages.

### The repository is visible but the site is not

Uploading files and enabling Pages are separate actions. Complete the Pages settings steps.

### The model does not load

Use the supplied standalone `index.html`. The model is embedded, so no external path should be needed.

### Changes do not appear

Wait for deployment, then refresh with `Ctrl + F5`.

---

# PART E — LIMITATIONS AND FUTURE IMPROVEMENTS

## 34. Current limitations

1. The dataset is synthetic.
2. The model mainly learns vocabulary and not deep meaning.
3. It does not browse or verify facts.
4. It cannot inspect images or video.
5. It can be influenced by writing style.
6. Confidence is a model score, not proof that an event is true.
7. The final trained vocabulary is English-focused.

## 35. Future improvements

1. Train on a trusted real-news dataset.
2. Remove duplicates and publisher-specific shortcuts.
3. Test on sources not used in training.
4. Add separate Hindi and multilingual models.
5. Use TF-IDF with Logistic Regression as a stronger classical baseline.
6. Compare with transformer models such as BERT.
7. Add URL/source verification.
8. Add explainable highlighted words.
9. Add model-version and dataset-version tracking.
10. Deploy a secure backend if a larger model is used.

---

# PART F — VIVA QUESTIONS AND SHORT ANSWERS

## 36. Important viva questions

### Q1. What is the purpose of your project?
It demonstrates how machine learning can classify news text as REAL-style or FAKE-style using learned word patterns.

### Q2. Which algorithm did you use?
Multinomial Naive Bayes.

### Q3. Why did you select Naive Bayes?
It is fast, lightweight, suitable for text word counts, easy to explain, and works offline.

### Q4. Is the model pre-trained?
Yes, for this project. It was trained on the supplied 1,000-row dataset and embedded into the final HTML. It is not a large general-purpose pre-trained model.

### Q5. Where is the model stored?
The development model is in `model/model.json`. The deployed model is embedded in the JavaScript `model` variable inside `NewsCheck_AI.html`.

### Q6. Where is the dataset?
In `data/training_data.csv`.

### Q7. How many training examples are there?
1,000 total: 500 REAL and 500 FAKE.

### Q8. How did you test the model?
Using a fixed stratified 80/20 split: 800 training samples and 200 holdout test samples.

### Q9. Why is the test accuracy 100%?
The dataset is synthetic and template-generated, so its patterns are very easy to separate. The score is not a real-world guarantee.

### Q10. What is tokenization?
It is the process of converting text into individual lowercase words.

### Q11. What is Laplace smoothing?
It adds one to word counts so unseen words do not make a class probability zero.

### Q12. Does the project need internet?
No. The model runs inside the browser.

### Q13. Does the project send user text to a server?
No. Prediction happens locally in JavaScript.

### Q14. Why is Python included if the website uses JavaScript?
Python generates the dataset, trains and evaluates the model, and builds the final HTML. JavaScript performs predictions for the end user.

### Q15. Can GitHub Pages run Python?
Not as a normal backend. This project does not need it because the deployed prediction code is JavaScript and the model is embedded in `index.html`.

### Q16. Is confidence equal to truth probability?
No. It shows how strongly the model prefers one learned class. It is not proof that the news is true or false.

### Q17. How would you improve real-world accuracy?
Use a large verified dataset, remove duplicates, test on unseen publishers and dates, compare several models, and use professional fact-check sources.

### Q18. What is the frontend?
HTML provides structure, CSS provides design, and JavaScript handles interaction and prediction.

### Q19. What is JSON used for?
JSON stores the trained vocabulary, word counts, model settings, and evaluation metrics in a format readable by Python and JavaScript.

### Q20. What is the biggest ethical point?
The output must be presented as a warning or hint, not as unquestionable truth.

---

## 37. One-minute viva introduction

“NewsCheck AI is an offline educational fake-news text-classification project. I used a supervised Multinomial Naive Bayes algorithm trained on 1,000 labeled English samples, with 500 REAL and 500 FAKE examples. Python was used to generate the dataset, train the model, and evaluate it using an 80/20 stratified split. The trained word counts and vocabulary were saved in JSON and then embedded inside one standalone HTML file. In the final application, JavaScript tokenizes the user’s news text, calculates REAL and FAKE log-probability scores with Laplace smoothing, and displays the larger result. The app works offline and does not upload user text. Its 100% holdout score is limited to the synthetic template-generated dataset and is not a guarantee on real-world news.”

---

## 38. Thirty-second demonstration plan

1. Open `NewsCheck_AI.html`.
2. Point to “Pre-trained model ready.”
3. Show the model-information card.
4. Select the real-style sample and run it.
5. Select the fake-style sample and run it.
6. Explain that the result is based on learned language patterns.
7. Show `training_data.csv`, `model.json`, and `metrics.json` as project evidence.
8. Finish by stating the real-world limitation.
