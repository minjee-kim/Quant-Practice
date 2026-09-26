# Problem Set

A Streamlit webpage for timed quant interview practice. Each attempt has ten
multiple-choice questions (two each from five templates), fresh numbers,
60 seconds per question, answer feedback, and a solution review.

## Run it in VS Code

1. Open the `Quant-Practice` folder in VS Code.
2. Open **Terminal → New Terminal**. If the prompt says `>>>`, type `exit()`
   first to leave Python and return to the terminal.
3. From the repository root, run:

   ```bash
   python3 -m pip install -r requirements.txt
   python3 -m streamlit run problem_set/app.py
   ```

Your browser opens the local webpage, usually `http://localhost:8501`.
Leave that terminal running while you practice. Press **Ctrl+C** there to stop.
Select a choice and press **Enter** or click **Submit answer**.

## Edit the question bank

Open [`questions.py`](questions.py). Each generator chooses random numbers,
calculates the exact answer, and returns a prompt, four choices, and a worked
solution. To add a type, write another function accepting `rng` and add it to
`GENERATORS`. `engine.py` controls the timer and score; `app.py` draws the page.

At the end, you can download your attempt as CSV. Results remain in the current
browser session unless downloaded; cross-session history can be added later.

To put the app online later, deploy this repository on Streamlit Community Cloud
with `problem_set/app.py` as its entrypoint.
