# Problem Set

A Streamlit webpage for timed quant interview practice. Each attempt draws ten
different problem types from thirteen templates, with fresh numbers, four choices,
60 seconds per question, answer feedback, and a solution review. Fractions,
conditional probabilities, and expected values render as math in the app.

Eleven templates adapt published problems in Jane Street's
[Probability & Markets guide](https://www.janestreet.com/static/pdfs/trading-interview.pdf).
Two adapt examples on Susquehanna's
[Game Theory + Decision Science page](https://sig.com/who-we-are/game-theory-decision-science/).
Every set includes both Susquehanna examples and eight Jane Street types. These
randomized questions are practice adaptations, **not verified accounts of live
interview questions**. Each app question links to its published source.
If a browser still has a round from the older question bank, the app resets that
round with a notice because its questions lack source information.

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

Susquehanna's published decision science examples inspire the **pain and rain**
conditional-rate comparison and **next coin flip after a heads streak** questions.
Their page is educational material, not an interview question list.

## Official guides from other firms

These firm-authored pages describe interviews and preparation. They do not
claim that the timed quiz contains those firms' actual interview questions.

| Firm | Official resource | What to prepare |
| --- | --- | --- |
| Citadel | [Quantitative Research Interview Process](https://www.citadel.com/careers/career-perspectives/our-quantitative-research-interview-process/) and [Quantitative Research FAQs](https://www.citadel.com/careers/career-perspectives/candidate-faqs-quantitative-research/) | Programming, research reasoning, algorithms, statistics, data analysis, and explaining trade-offs. |
| Two Sigma | [Interviewing for Quantitative Research & Modeling](https://www.twosigma.com/interviewing-for-quantitative-research-modeling/) | Data analysis, open-ended problem solving, coding, statistics, and its linked mock interview video. |
| Optiver | [Quant Research internship story](https://www.optiver.com/join-us/stories/from-computer-science-to-quant-research-lucys-internship-story/) | An intern describes a data-based, open-ended interview project and recommendations. |
| IMC | [How to prepare for an interview](https://www.imc.com/ap/articles/how-to-prepare-for-an-interview-at-imc) | Technical problem solving with a trader or engineer and explaining your work. |

The 60-second multiple-choice format covers quick concepts. For research-role
interviews, use the guides above to practice coding and longer data problems too.

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
