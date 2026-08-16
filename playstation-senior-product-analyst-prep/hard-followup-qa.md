# PlayStation — Hard Follow-Up Q&A Prep
## Anticipated Grilling on the SMS Causal Study + Experiment Presentation

> ## HARD RULES — READ BEFORE EDITING THIS FILE
> 1. **Points and subpoints, not long paragraphs**, wherever the content allows it — answers should default to bullets, not dense prose.
> 2. **Easy, plain English.** Explain any technical term the moment it's used, in one short clause.
> 3. **Questions are grouped by priority** — Must-Do, Skim, Least Priority — since there are 30+ of them and not all are equally likely or equally high-stakes.
> 4. **Every answer is checked against the actual deck data** in `presentation-outline.md`, and tagged so you know how solid it is:
>    - ✅ **From deck** — pulled directly from a back-pocket note already written for the presentation.
>    - 🧩 **Suggested** — a reasonable answer built from the deck's own logic, but not written down verbatim — check it matches what you actually did before treating it as fact.
>    - ✍️ **Your story needed** — a real personal/behavioral memory the deck doesn't contain. A structure is given; you fill in the real example.
> 5. Answers stay **balanced** — enough of the "why" that a non-technical interviewer follows along, without dumbing down the one technical term that matters.

---

## Tier 1 — Must-Do (prep these cold)

### 1. Why CEM (Coarsened Exact Matching) over propensity score matching?
✅ From deck
- CEM is "model-free" — it sorts people into groups by their actual traits, not by trusting a prediction model that could be wrong.
- Propensity matching uses a model to guess "how likely is this person to buy SMS," then matches on that guess — if the model's off, the whole match is off.
- With CEM, the fairness of the comparison comes from the bucketing itself, not from an assumption you have to hope holds.

### 2. Walk me through the placebo test.
✅ From deck
- Reran the whole analysis, but handed out a **fake** treatment — randomly told some non-buyers "pretend you bought SMS."
- If the method were just picking up noise or bias, this fake treatment should also show a big fake effect.
- It collapsed to near zero — proof the method detects something real, not just manufacturing results.

### 3. How do you rule out reverse causality — that already-growing customers were simply more likely to try SMS anyway?
🧩 Suggested — confirm this matches what you actually checked
- The matching step controls for this upfront: buyers and non-buyers already looked alike on size, spend, and engagement *before* the SMS purchase date.
- The covariate balance check (differences close to zero) is the direct evidence both groups were on the same trajectory going in.
- The strongest answer: the follow-on randomized experiment. Random assignment means nobody "chose" anything — so when the same halo pattern shows up there too, self-selection can't be the explanation.

### 4. Is the 79%/21% split (new conversions vs. upgrades) causal too, or just a breakdown of an already-causal number?
🧩 Suggested
- The causal claim sits on the lift itself (the $62 non-SMS revenue lift) — that's what matching and diff-in-diff (comparing the change over time between the two groups) support.
- The 79/21 split just shows *where* that already-proven lift came from — new customers converting to paid (79%) vs. existing customers upgrading (21%). It's not a second causal claim stacked on top, just a breakdown of one.
- Watch out: the overall revenue lift (SMS + non-SMS combined) also happens to round to ~79% — that's a completely separate, unrelated number that coincidentally matches. Don't mix the two up if asked to clarify which "79%" you mean.
- Simple line to have ready: "The lift itself is the causal number. This split just shows where it came from."

### 5. Why should timing from people who chose SMS themselves (55% within 1 day) predict a lift for people who were shown a screen, not choosing on their own?
🧩 Suggested — this is a real logic gap, have a tight answer ready
- The 55% stat wasn't proof by itself — it was a signal for *when* intent is highest, used to design where in the funnel to test.
- The actual proof is the real experiment result (+23% purchase rate) — the historical stat picked the bet, the experiment settled it.
- Ready line: "The data told us where to place the bet. The experiment told us if it paid off."

### 6. MDE (minimum detectable effect — the smallest lift you sized the test to catch) was 7%, you got 23%. Isn't that overshoot suspicious of a bug or a novelty effect?
✅ From deck
- The confidence interval sat entirely above zero *and* above the 7% MDE — not a borderline result, a solid one.
- A low starting base can make a modest absolute change look like a big percentage jump — not unusual on its own.
- Fair to flag novelty effect as a real open question — the honest answer is that a longer monitoring window after launch is how you'd check if the lift holds once the "new screen" wears off.

### 7. Walk through the $2.3M — how does a 14-day revenue lift project cleanly over 12 months?
✅ From deck (framing) + 🧩 Suggested (the worked mechanics below — a reconstruction consistent with the deck's description, not verbatim)
- **Simple version, lead with this:** "It was projected from the observed revenue lift per user, scaled across the population expected to go through onboarding, and rolled forward over 12 months. It's a projection, not a guarantee."
- **If pushed on the mechanics:**
  - Estimate how many new users will complete onboarding over a full year (start from the test's own population — the variant arm was half of it, since the split was 50/50 — then scale that ~28-day test-window population up to a 12-month figure).
  - Multiply that annual new-user count by the 14-day ARPU lift per user (variant ARPU minus control ARPU — already an incremental number, not total revenue, since it's a *difference* between the two arms).
  - No extra time-multiplier needed on top of that — the 14-day lift is a one-time thing per new user, since each person only goes through onboarding once. Multiplying it again by "how many 14-day periods fit in a year" would double-count.
- **Trap to avoid:** don't isolate "the users who converted because of the 23% purchase-rate lift" and multiply just them by the population-wide ARPU lift number — that mixes a subset count with an already-diluted population average and understates the result. The population-wide ARPU lift already has those incremental buyers priced into it; no need to isolate them separately.
- **If asked about decay over time:** honest answer is that wasn't separately modeled here, and would be worth revisiting with more data.

### 8. How did you personally win the placement argument when every team wanted that screen?
✅ From deck
- "We think SMS matters" doesn't win that fight — a defensible, causal number does.
- The causal study's rigor (matching + placebo test + triangulating multiple methods) is what turned this from an opinion into evidence leadership could act on.
- It wasn't just an analysis exercise — it was the actual evidence used to secure the experiment's placement.

### 9. What if the causal study had come back negative — was there a plan for that?
🧩 Suggested
- No specific fallback plan is documented — be honest about that if asked directly.
- Fair answer: a negative result would still have been valuable — it would have stopped SMS from getting resourced on a false premise, which is exactly what this method exists to catch.

### 10. Tell me about a disagreement with your manager or a senior stakeholder on this project.
✍️ Your story, drafted — confirm this matches how it actually went, adjust freely
- **Situation:**
  - Deciding which causal matching method to use for the SMS study — not a minor technical footnote, since the whole revenue-lift claim rested on it
  - I proposed CEM based on the pre-purchase attributes we had
  - My manager pushed back and suggested PSM instead
  - Their concern: matching exactly across several covariates could fragment the data into small, hard-to-fill buckets, and a propensity model would let us match more efficiently without needing an exact match on every trait
- **My position:**
  - Several of our covariates were categorical (plan type, free-trial status) — CEM handles that cleanly since it's just bucketing on actual values
  - We had a huge pool of non-buyers (500,000+) against just 13,500 buyers, so sparsity wasn't actually a real risk here
  - More importantly, this study was going to leadership to justify resourcing and roadmap decisions — and CEM's story is simple to defend: "we found each buyer's near-identical twin who didn't buy, and compared them"
  - A propensity model adds a step people have to trust blindly — if that model were even slightly off, the comparison could look balanced on paper while hiding a real difference underneath
- **Resolution:**
  - Not either/or — I ran CEM as the primary method since it fit our data and gave the more defensible story for leadership
  - But took the concern seriously rather than overriding it, and ran PSM (plus IPW and a doubly-robust estimator) in Python afterward as a triangulation check
  - All of them landed in the same direction as CEM — not just one method agreeing with itself, but four independent approaches agreeing
  - That pushback made the analysis stronger than going with my first instinct alone
- **Ready line:** "My manager pushed for PSM, I pushed for CEM — we landed on CEM as the primary method since it fit our data and was easier to defend to leadership, but I folded PSM in as a validation check, which is exactly what made the final result so solid."
- **Note:** this is the technical/methodology-flavored disagreement story. If the question leans more business/PM (e.g. "tell me about a prioritization fight"), use Q33 instead.

### 11. Did anyone challenge your methodology or conclusion directly?
✍️ Your story needed — the deck hints at *why* you built defenses for this, not the actual moment
- Likely candidates based on the deck: someone asking why CEM over a simpler comparison, or "how do you know this isn't just correlation?"
- Your strongest concrete evidence to point to: the triangulation step (several matching methods agreeing) and the placebo test.
- Fill in who actually asked, and what the real exchange looked like.

### 12. How did you convince a skeptical, non-technical stakeholder that "causal" meant something real?
🧩 Suggested — grounded in the deck's own framing
- Led with plain English first: "we found each buyer's near-identical twin who didn't buy, and compared them" — not the statistical name.
- Showed the balance check simply: the two groups looked the same on everything that mattered *before* SMS, so the difference *after* is more likely caused by SMS.
- Backed it with the placebo test in plain terms: "we ran the same method on a fake purchase, and it found nothing — so the method isn't just seeing things that aren't there."

### 13. Walk me through diff-in-diff mechanically — how did you actually get the lift number and its confidence interval?
✅ From deck (matches R production script + Q6 in `cem_causal_study.md`) — kept intentionally non-technical, this isn't a heavy tech round
- **Two steps, not one:**
  - First: look at how each customer's own revenue changed — before they bought SMS vs. after.
  - Second: compare that change to a similar group of customers who never bought SMS.
- **Why the comparison is fair:**
  - The non-SMS group wasn't just anyone — it was built to look just like the SMS buyers *before* the purchase (same size, spend, activity).
  - So any difference that shows up afterward is more likely caused by SMS, not just "these were already better customers."
- **How we got the actual number:**
  - Compared the average change for SMS buyers vs. the average change for that matched group.
  - That gap is the $62 lift.
- **How we knew it wasn't just random noise:**
  - Ran a standard statistical test comparing the two groups.
  - That gave a range — $57 to $66 — instead of just one number.
  - Since that whole range stays above zero, it means we can trust it's a real effect, not luck.
- **Ready one-liner:** "I looked at how each customer's revenue changed after buying SMS, compared it to a similar group who didn't buy SMS, and the difference held up as statistically significant."
- **Trap to avoid:** don't say "I ran diff-in-diff on the covariates." The covariates (account age, list size, AOV, etc.) were only used to build the fair comparison group — diff-in-diff itself compares revenue, between the matched groups.
- **Only if pushed technical:** also cross-checked with a weighted regression using cluster-robust standard errors (accounts for matched users not being fully independent of each other, since they share matching buckets) — same conclusion, more careful treatment of uncertainty. No need to volunteer this unless asked.

### 14. Why 90 days for the pre/post comparison window, and not something shorter or longer?
✅ From deck
- Long enough to see real behavioral change — paid conversions, plan upgrades, and email activity take time to show up, not something you'd catch in a week or two
- Short enough to still include buyers from later in the study window and have complete post-period data for all of them — a longer window would've meant dropping the most recent buyers since they wouldn't have enough time elapsed yet
- It's also a standard measurement window used elsewhere in Mailchimp analytics, so the result is comparable to other studies rather than using a one-off custom window
- **Ready line:** "90 days was long enough to see real behavior change like upgrades, but short enough that I didn't have to drop recent buyers for lack of post-period data."
- **If pushed further — why not 30 or 60 days instead:** shorter windows risk catching the initial spike around the purchase without giving slower-moving behaviors (like a plan upgrade decision) enough time to materialize — 90 days was the point where the team had confidence the picture was complete, not just an early read

---

## Tier 2 — Skim (know the shape of the answer, don't over-rehearse)

### 15. How many attributes did you match on, and what happens with more attributes?
✅ From deck + 🧩 suggested for the second half
- Keep it vague if asked exactly: "about a dozen pre-purchase signals," "tens of thousands of buyers matched against a much larger pool of non-buyers."
- More attributes = more precise buckets, but also smaller, harder-to-fill buckets — a known tradeoff, softened here by having a large non-buyer pool to draw from.

### 16. Did you test the "parallel trends" assumption behind diff-in-diff (the idea that both groups would've moved the same way without SMS)?
✅ From deck
- Yes — there's an actual chart for this: % of users on a paid Mailchimp plan, tracked daily for both groups. The two lines move together, almost flat and parallel, right up until just before the SMS purchase date — then they diverge.
- That visual is the direct evidence the two groups were on the same trajectory before SMS, which is exactly what the parallel-trends assumption requires.
- Backup evidence, from a different angle: the covariate balance check (differences near zero before purchase) shows the same thing.

### 17. What happened to precision when a bucket had only one non-buyer matched to many buyers?
🧩 Suggested
- Very few buyers were dropped entirely, thanks to the large non-buyer pool.
- Standard practice for thin buckets is to weight the available non-buyers rather than randomly discard extras — using all the data instead of throwing part of it away.

### 18. "Close to zero" — what threshold, and did any attribute fail to balance?
🧩 Suggested
- No exact number is written down — safe to describe it as "no meaningful gap left on any attribute we matched on."
- If pushed for a number: standard practice is under ~0.1 on a standardized difference scale — confirm this is really what you used before stating it as fact.

### 19. Walk me through the actual roadmap decision moment.
✅ From deck
- The experiment came first — fastest way to test the finding at scale.
- Onboarding changes and sales enablement followed once the experiment validated it further.
- This is the "hinge" of the talk — sound most confident here, it's proof the work changed real decisions, not just produced a slide.

### 20. Why 50/50 split instead of a smaller ramp, given this is the highest-engagement page?
🧩 Suggested
- 50/50 reaches a solid, trustworthy answer fastest — smaller ramps take longer to hit the same confidence.
- The real risk (interrupting the top page) was managed by watching the guardrail metric (product payoff rate) closely — mention the safety net, not just "we decided to."

### 21. SRM check (sample ratio mismatch — confirms group sizes match the expected split) — what if it had come back 51/49 instead of clean 50/50?
✅ From deck
- Small natural variation is expected and fine — SRM only flags a problem when the gap is statistically unlikely to happen by chance.
- If it had failed: standard response is to pause and investigate the rollout mechanism before trusting any result from the test.

### 22. Product payoff rate stayed flat — flat compared to what, and could that be masking a small negative?
✅ From deck
- The test ran the primary metric's full required duration, so the guardrail had more data than it needed — flat here is a real flat result, not an underpowered one.
- Different from the secondary funnel metrics, which were only shown directionally, not formally tested.

### 23. The two studies split revenue differently (79/21 vs. 69/31) — isn't that apples to oranges?
✅ From deck, synthesized
- These are two different cuts of a similar total lift — one splits new-conversions vs. upgrades, the other splits non-SMS vs. SMS revenue. Not meant to be the same number stated twice.
- What actually replicated across both: the core halo pattern — buying SMS lifts more than just SMS revenue.
- Be upfront if pushed: the exact split composition isn't identical, and that's expected since they're cutting the data differently.

### 24. Did the lower-engagement variant users catch up later, or stay dead weight?
✅ From deck
- A real, acknowledged cost — name it as such rather than downplay it.
- The documented next step is watching whether those users catch up over a longer window — this wasn't already answered at presentation time.

### 25. Was there a moment you were wrong and had to walk it back?
✍️ Your story needed
- Not in the deck — needs a real, specific memory.
- Structure: what you initially believed → what changed your mind → how you communicated the correction.

### 26. Who was your biggest skeptic, and what got them on board?
✍️ Your story needed
- The deck implies a skeptical audience (other teams wanting the same placement) but not a specific person or conversation.
- Fill in a real (anonymized) example and the specific evidence that changed their mind.

---

## Tier 3 — Least Priority (aware of, not rehearsed)

### 27. What's the biggest omitted variable you're worried about?
🧩 Suggested
- Anything correlated with "decided to try something new right now" that wasn't in your matching attributes — e.g. a seasonal spike or a marketing push on the customer's own side that made them both more experimental and more likely to grow anyway.
- Honest framing: matching reduces this risk but can't fully remove it — exactly why the later randomized experiment mattered so much.

### 28. Defend showing secondary metrics directionally instead of formally testing all of them.
✅ From deck
- Testing every metric independently risks false positives from running too many comparisons at once.
- Picking one primary metric to formally test, and showing the rest directionally, is a standard, defensible tradeoff — not a shortcut.

### 29. If the randomized experiment and the observational study had disagreed, which would you trust?
🧩 Suggested
- The experiment — random assignment removes selection bias by design, it doesn't lean on a matching assumption holding.
- Worth adding: a disagreement wouldn't automatically mean the study was "wrong" — could mean the two were measuring subtly different things, worth digging into rather than just picking a winner.

### 30. What's the confidence interval on the $2.3M?
🧩 Suggested
- Not spelled out as a specific range — safe line: "I'd want to check what I can share externally on the exact interval, but the underlying purchase-rate lift was statistically significant, with the interval sitting entirely above zero."

### 31. Which of the two projects was harder to get buy-in for?
✍️ Your story needed
- Reasonable guess from the deck: the causal study was likely the harder room to win, since it's a less familiar method without randomization; the experiment was an easier sell once the study existed.
- Replace with your real read on which was actually harder.

### 32. If you redid this, what's the one methodological change you'd make?
✅ From deck
- Would want a true randomized experiment on the exact causal-study question if feasible — which is effectively what the follow-on A/B test approximated.

### 33. If you could go back in time, what's one non-methodological thing you'd do differently?
✍️ Your story needed
- Think process, timing, or communication — not the analysis itself.

### 34. Was there tension between SMS and other product teams over how findings should be used?
✍️ Your story, drafted — this is the PM/leadership-flavored disagreement (vs. Q10's technical one); confirm and fill in the real resolution
- **Situation:**
  - Once the causal study proved SMS mattered, the natural next move was placing an SMS prompt right after onboarding — the data showed that's when purchase intent was highest
  - Problem: that onboarding screen is the single highest-engagement page in the whole product, and other product teams wanted that same real estate for their own initiatives
  - Not a stats disagreement — a resourcing/prioritization one
- **My position:**
  - Didn't try to win on opinion or seniority — brought the causal study's number to the table: a statistically significant non-SMS revenue lift per buyer, which the competing ask didn't have an equivalent figure for
  - Reframed it from "whose feature matters more" to "here's the quantified expected return of this specific placement" — turned a subjective fight into an evidence comparison
  - Stayed honest about the limits too — didn't have a number for what the other team's initiative was worth, so didn't overclaim, just pointed out SMS was the one with defensible evidence behind it right now
- **Resolution — this part needs your real answer:**
  - Did SMS get the full placement, a shared/partial one, or get sequenced after the other team's test?
  - Whatever it was, the throughline: leadership weighed the evidence, and having a causal number the other ask didn't have is what tipped the scale
- **Ready line (adjust once resolution is filled in):** "There was real tension over who got that onboarding placement, since it's the highest-engagement page in the product. I didn't try to win it on opinion — I brought a defensible, causal number to the table, which is what the other ask didn't have, and that's ultimately what carried the decision."

### 35. Did you ever have to say no to a stakeholder's request during this project?
✍️ Your story needed
- Needs a real example — e.g. pushing back on a request for an exact dollar figure, a shorter timeline, or a bigger initial rollout than the guardrails supported.

---

**Log:**
- Built from the two rounds of follow-up questions discussed in chat (technical/causal-study questions + general behavioral/conflict questions).
- Not yet linked into `presentation-outline.md` — kept as a standalone prep file per your instruction.
- Added Q13 (diff-in-diff mechanics: per-user diff vs. between-group diff, t-test as the source of the lift + confidence interval) from a follow-up chat on 2026-08-11.
- Added Q14 (why 90 days for the pre/post window) as Tier 1, from a follow-up chat on 2026-08-13.
