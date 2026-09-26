# Problem Set

A Streamlit webpage for timed quant interview practice. Each attempt draws ten
different problem types from eleven templates, with fresh numbers, four choices,
60 seconds per question, answer feedback, and a solution review.

The templates are **adapted from the published problems in Jane Street's
[Probability & Markets guide](https://www.janestreet.com/static/pdfs/trading-interview.pdf)**.
Jane Street describes the guide as preparation for its quantitative trading and
research interviews. The randomized versions here are practice adaptations;
they are not verified accounts of live interview questions. Each app question
links to the corresponding page of the guide.

| Problem type | Guide page |
| --- | ---: |
| Two distinct dice: probability of a sum | 2 |
| Two card draws with or without replacement | 4 |
| Odd product of die rolls | 4 |
| Expected value of a weighted die | 5 |
| Expected die value given a minimum roll | 7 |
| Number of heads conditional on at least one tail | 7 |
| Prime die result, conditional probability | 8 |
| Expected profit on a die contract | 9 |
| Expected maximum of dice | 10 |
| Optimal choice to reroll once | 10 |
| Waiting for consecutive heads | 11 |

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

The two-dice problem treats the dice as distinct (for example, red and blue):
(red 1, blue 6) and (red 6, blue 1) are two outcomes among 36. The pair order
matters when counting equally likely elementary outcomes, even though both
pairs have the same sum.

At the end, you can download your attempt as CSV. Results remain in the current
browser session unless downloaded; cross-session history can be added later.

To put the app online later, deploy this repository on Streamlit Community Cloud
with `problem_set/app.py` as its entrypoint.
