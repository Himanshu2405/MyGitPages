# Wise — Regional Product Analyst Interview Prep
## Presentation Outline: MXN → USD Currency Route Case Study

> ## HARD RULES — READ BEFORE EDITING THIS FILE
> 1. **Never edit the live Google Slides deck (`Wise_Case_Study`) or the `wise_funnel_events_regional` Google Sheet.** All changes to those two files are made by Himanshu only, not by Claude. This file is the only place new/changed slide content gets drafted and reviewed.
> 2. **Build additions/edits slide by slide, with explicit permission before each one.** Propose the content in chat first, wait for the go-ahead, and only then write it into this file. Do not get ahead of confirmed content — if only slide N is confirmed, this file should not contain drafted content past slide N.
> 3. **Points and subpoints, not long paragraphs**, wherever the content allows it — on-screen content, speaker notes, and back pocket items should all default to bulleted points rather than dense prose.
> 4. **Speaker notes and back pocket items must be full, complete sentences in easy, plain English** — written so they can be read aloud and rehearsed directly, not shorthand or compressed phrases. Bullet them, but each bullet should be a real sentence, not a fragment.

**Source files (read-only from here):**
- Live deck: `Wise_Case_Study` — Google Slides, https://docs.google.com/presentation/d/1DkZEpygLCafKcauK6SbksRR-gBMxW6ERtQFErcoYPnU/edit
- Data/SQL: `wise_funnel_events_regional` — Google Sheet, https://docs.google.com/spreadsheets/d/1G4lqBH2kdf3HyuM-3RhbWLlPCXmsCK0HuH4P1G6SNdk/edit
- Case study brief: `Wise - Regional Product Analyst - Case Study.pdf` — local copy at `/Users/himanshudubey/Documents/Projects/Personal/company/Wise/Wise - Regional Product Analyst - Case Study.pdf`

## Original Take-Home Prompt (from Wise)

> **Task:** At Wise, the Regional Expansion Tribe is responsible for ensuring we have localised product offerings in our existing markets and expanding into new markets, all while ensuring we maintain a very high bar for compliance. For this case study, we will be exploring an opportunity to launch a new currency route from MXN to USD allowing money to be sent from Mexican currency holders to USD bank accounts.
> 1. **Demand estimation.** First things first, let's start with understanding whether it's worth launching this route. Please propose relevant data / methodologies that could be used to estimate the demand for this route. Consider that you have access to all Wise Internal data.
> 2. **Evaluating the launch.** Let's assume the route has been launched and we have some initial data on its usage. Could you take a look at this data to generate insights?
>    - Does the performance seem on track?
>    - Are there any findings that would be valuable to share with the product team?

## Interview Focus Area Being Prepped Right Now

> **2. Technical Scoping & Demand Estimation** — As we scale our NorthAm expansion, our analysts must understand the "cost" of their logic.
> - **The Focus:** Quantifying demand for new routes or features.
> - **Critical Thinking:** How do you decide if a specific route is worth the investment? How do your queries and pipeline designs affect database performance at scale?

*(The interview also covers two other focus areas — Technical Fluency & Data Integrity, and Product Sense & Strategic Synthesis — but those get their own pass later. This file currently targets Area 2 only.)*

**Status (2026-08-16): Deck complete.** Final live deck is 16 slides. Every slide has both content and speaker notes finalized. Only Back pocket sections remain empty across the board, no other open items on the deck itself. **Slide 3 confirmed** (content and speaker notes both, includes the new "How I Approached This" framing block). **Slide 4 confirmed** (reverse-corridor signal added, redundant USD Balance Holders bullet resolved by nesting, speaker notes finalized). **Slide 5 confirmed** (High/Low Intent bucketing rule added, Customer Value/Profile reframed as a cross-tab method, speaker notes finalized). **Slide 6 confirmed** (conversion-rate sub-bullet added, Final output rewritten as two explicit, unit-labeled formulas tying Slide 5's High-Intent Users into expected adopters and volume, speaker notes finalized). **Slide 7 confirmed, new slide** (Revenue vs. Cost synthesis, not yet added to the live deck, that's the next action item for Himanshu). Slide 2's table of contents updated to list the new 4th sub-item.

**Slide budget constraint (set 2026-08-15, scoped to the demand-estimation section only):** no more than 2 new slides added, full demand-estimation section fits within Slides 3–7. Honored: exactly 1 new slide added there (Slide 7). This constraint didn't extend to the launch-evaluation section (Part 2), where a second new slide was added by explicit request, see Slide 13 below.

**Launch-evaluation section (Part 2, Slides 9–16) verified against the SQL and sheet data, 2026-08-15:** every claim checked out exactly against the `Overall`, `funnel by Region`, and `funnel by Experience` tabs. Slide 11 (Android root cause) checked out too, but only after tracing through a real labeling bug in the `funnel mix` tab, a table headered "Europe - Android - New" actually contains non-Android data (missing the word "non"), confirmed via the raw `SQL DATA` tab. The true Android+New+Europe numbers live in a different, correctly-computed block and do support the slide's "~3%" claim. Worth having as a ready story in `hard-followup-qa.md`, since it's a strong, concrete data-integrity example. Confirmed via the actual slide charts (not just the working sheet tabs) that this labeling bug never made it onto any slide, the deck itself is clean.

**Final deck reconciled against Himanshu's exported PDF, 2026-08-16:** the live deck is 16 slides, not 17. Two fixes made to match: (1) Slide 12 and 13 swapped, Cost of the Bug actually sits at 12 (right after Root Cause) and Funnel Performance by Region at 13, not the order originally planned. (2) The old appendix slide "The Android Problem Affects New Users Only" was removed from the live deck, deleted from this file too. Also caught and confirmed fixed: Slide 5 had regressed to "trailing 1 month" (should be 12), and Slide 13's footnote pointed at "slide 3" instead of Slide 11, both corrected by Himanshu in the live deck, 2026-08-16.

**Former known gap, now resolved:** the deck's demand-estimation section previously had no explicit "is this route worth the investment" framing, it stopped at *how much demand exists and how much will convert*. Slide 7 now closes that loop with Revenue vs. Cost and an explicit payback-based decision.

---

## Baseline — Existing Deck (Confirmed, transcribed as-is from the live Slides deck)

### Slide 1 — Title

**Content (on screen):**
- Strategic Expansion: The MXN-USD Currency Route
- Take Home Assignment
- Himanshu Dubey

**Speaker notes (~15 sec):**
- Thanks for having me. I'm going to walk through my take-home on launching a new MXN to USD currency route at Wise.
- This covers two parts: estimating demand before launch, and evaluating how the actual launch performed.

**Back pocket:** *(to be drafted)*

---

### Slide 2 — Table of Contents

**Content (on screen):**
1. Strategic Expansion: Launching MXN-USD Currency Route
2. Demand Estimation: Data and Methodologies
   - Identify demand
   - Evaluate demand quality
   - Estimate future adoption
   - Is it worth launching (revenue vs. cost)
3. Evaluating the launch
   - MXN to USD Route Launch

**Speaker notes (~20 sec):**
- Quick roadmap. First, strategic context and how I approached the problem.
- Second, demand estimation, identifying demand, evaluating its quality, estimating adoption, and weighing revenue against cost.
- Third, evaluating the actual launch, what happened once the route went live.

**Back pocket:** *(to be drafted)*

---

### Slide 3 — Strategic Expansion: Launching MXN-USD Currency Route — ✅ CONFIRMED

**Content (on screen):**

Wise mission:
- To build money without borders; making it move faster, more conveniently, and eventually for free

Strategic Expansion: MXN-USD:
- Launch of a new currency route from MXN-USD
- Facilitating money transfers from Mexican currency holders to USD currency holders

How I Approached This:
- The real question isn't just "how much demand exists," it's "is this route worth building"
- The four steps below answer this, in order

Demand Estimation Methodology:
- Identify demand signals
- Segment user intent
- Benchmark adoption potential using similar corridors
- Weigh revenue against cost

**Speaker notes (~40 sec, follows slide order top to bottom):**
- Wise's mission is money without borders, moving it faster, more conveniently, and eventually for free.
- This slide is about one specific piece of that mission: launching a new route so Mexican currency holders can send to USD.
- Before jumping into data, here's how I framed the problem. The real question isn't just how much demand exists, it's whether this route is worth building.
- That splits into four steps: identify demand signals, segment user intent, benchmark adoption using similar corridors, and weigh revenue against cost.
- The rest of this section walks through those four steps, in order.

**Back pocket:** *(to be drafted)*

---

### Slide 4 — Identify Demand Signals (Current User Behavior) — ✅ CONFIRMED

**Content (on screen):**

Identify whether existing Wise users with MXN balances demonstrate demand for an MXN to USD transfer route.

Product event logs — Primary Signal:
- MXN to USD Attempt Rate: % of users holding MXN balances who attempt MXN to USD transfers (Send = MXN, Receive = USD)
  - Track volume, trend, and repeat attempts per user
- USD Balance Holders: % of users holding MXN balances who also hold a USD balance
  - Reverse-Corridor Activity: % of MXN-balance holders with a completed USD to MXN transfer history
- USD-Related Product Engagement: % of MXN-balance users who viewed USD transfer info, calculator, or FAQ pages

Customer Feedback — Secondary Validation:
- Support Requests: MXN to USD related tickets ÷ total MXN related support tickets
  - Validate customer pain points and unmet needs
- Customer Surveys: % of MX survey respondents expressing interest in MXN to USD
  - Strong qualitative signal; low response volume, directional only, not for sizing demand

Assumptions:
1. Wise users globally can hold MXN balances, but MXN to USD transfers are currently unavailable.
2. Eligible Wise users with multi-currency accounts can hold USD balances.

**Speaker notes (~45 sec, follows slide order top to bottom):**
- Before we build anything: are people already trying to do this?
- Product event logs give us three signals. First, how many MXN balance holders attempt an MXN to USD transfer today, and how often they retry.
- Second, how many also hold USD balances, and within that, how many have already converted between USD and MXN elsewhere, that's completed behavior, not just intent.
- Third, how many are browsing USD transfer info or FAQs.
- Beyond product data, support tickets and surveys validate this from the customer's own voice, directionally, not for sizing demand.
- Together, this tells us real demand exists. Next: not everyone here converts equally, so we segment by intent.

**Back pocket:** *(to be drafted)*

---

### Slide 5 — Segment Demand Quality — ✅ CONFIRMED

**Content (on screen):**

Avoid overestimating demand by assuming all users holding MXN balances will adopt equally

Intent Strength (Based on Customer Behavior) — Analyze signals that differentiate high vs. low likelihood adopters:
- Multi-currency vs. Single-currency users
  - High intent: Multi-currency users who hold or has held a balance in 2+ currencies
  - Users already managing multiple currencies show stronger cross-border needs
- International transfer history vs. Limited transfer history
  - Cross-border history: ≥1 completed international transfer in trailing 12 months
- Repeat vs. One-time engagement
  - ≥2 distinct MXN to USD attempt events in trailing 90 days
- High Intent = meets all three signals above; Low Intent = everyone else

Customer Value/Profile — additional segmentation dimensions:
- Account Tenure
  - New vs. tenured users
- Account Type
  - Personal vs. Business accounts
- Historical Financial Activity
  - Transfer volume
  - Transfer frequency
  - Currency balance activity
- Cross-tab against Intent Strength above to find the strongest opportunity segment (e.g., high-intent Business vs. high-intent Personal), not just "high intent" as one bucket

**Speaker notes (~45 sec, follows slide order top to bottom):**
- Not everyone showing intent is equal, so who's actually likely to convert?
- We define high intent with three signals: holding two or more currencies, at least one international transfer in the past year, and two or more MXN to USD attempts in the past 90 days.
- Meeting all three means high intent, everyone else is low intent, a clean, defensible split.
- Beyond intent, we layer in customer value: tenure, account type, and historical transfer activity.
- The real value isn't listing these separately, it's cross-tabbing them against intent, so we find the single strongest segment, like high-intent business users, instead of treating high intent as one bucket.
- That gives us who to prioritize. Next: how many of them will actually adopt.

**Back pocket:** *(to be drafted)*

---

### Slide 6 — Estimate Future Adoption — ✅ CONFIRMED

**Content (on screen):**

Estimate how much of the identified demand will convert into actual MXN to USD usage after launch.

Similar Corridor Launch Analysis — a realistic benchmark for expected adoption based on actual Wise customer behavior instead of assuming all interested users will convert:
- Analyze comparable currency launches (e.g., BRL to USD, PHP to USD)
  - Based on similar customer behavior, transfer frequency, and volume patterns
  - Conversion rate: % of each corridor's pre-launch high-intent pool that actually converted after launch
- Post-adoption behavior (transfer frequency, average transfer size, retention)

Demand Estimation Approach:
- How much interest exists? (Demand signal)
- How strong is that interest? (High-intent segments)
- How much of that interest converts? (Comparable launch benchmarks)
- Final output:
  - Expected adopters, # = High-Intent Users volume × comparable corridor conversion rate
  - Expected transfer volume, $ = Expected Adopters (#) × post-adoption transfer size ($/transfer) × frequency (transfers/period), from comparable corridors

**Speaker notes (~45 sec, follows slide order top to bottom):**
- We estimate how much of the demand we identified will actually convert once we launch.
- We study comparable currency launches, BRL to USD and PHP to USD, since they share similar customer behavior, transfer frequency, and volume patterns.
- From each, we pull two numbers: the conversion rate, what share of the pre-launch high-intent pool actually converted, and post-adoption behavior, transfer frequency, size, and retention.
- Putting it together: expected adopters equals our high-intent user count from the last slide, multiplied by that conversion rate.
- Expected volume is those adopters multiplied by post-adoption size and frequency.
- That's a real forecast, grounded in what actually happened last time Wise launched a corridor like this.

**Back pocket:** *(to be drafted)*

---

### Slide 7 — Is It Worth Launching? Revenue vs. Cost — ✅ CONFIRMED

**Content (on screen):**

With adopters and transfer volume, we now calculate revenue and cost, both benchmarked from the same comparable corridors

Expected Revenue:
- Expected Revenue, $ = Expected Transfer Volume ($) × transfer fee rate
- Transfer fee rate = the % fee Wise charges per transfer on this corridor (benchmarked from comparable corridors)

Cost of Launching (benchmarked from the same comparable corridors, BRL to USD, PHP to USD):
- Operational cost: compliance & licensing for the new currency pair, payout rail/banking partner setup, support scaling
- Marketing cost: acquisition spend to acquire customers

Is It Worth It, Revenue vs. Cost:
- Payback/Breakeven: point where cumulative revenue crosses cumulative cost
- Compared against a target payback window

Decision:
- Worth launching if breakeven falls within the target window
- And the High Intent base is large enough to sustain volume post-ramp

**Speaker notes (~40 sec, follows slide order top to bottom):**
- With adopters and transfer volume from the last slide, we now calculate revenue and cost, both benchmarked from the same comparable corridors.
- Revenue: we apply a transfer fee rate, the percentage Wise charges per transfer on this corridor, to get expected revenue.
- Cost has two pieces: operational, compliance, licensing, and payout setup, and marketing, the spend to acquire customers, both pulled from the same corridors.
- Revenue versus cost gives us a payback point, compared against a target window.
- We call it worth launching if breakeven falls within that window, and the high intent base is large enough to sustain volume after the initial ramp.

**Back pocket:** *(to be drafted)*

**Note:** confirmed live in the Google Slides deck as of this screenshot, 2026-08-15.

---

### Slide 8 — Section Divider

**Content (on screen):**
- Launch Performance Evaluation: MXN to USD Route

**Speaker notes (~15 sec):**
- That's the demand case. Now let's look at what actually happened once we launched this route.

**Back pocket:** *(to be drafted)*

---

### Slide 9 — Adoption Is Strong, Conversion Is Drifting Down

**Title:** New route adoption is strong (~5.6K users/week created a transfer flow); but conversion is drifting down

**Content (on screen):**

Volume is growing:
- Weekly users creating a transfer grew from 1.1K to 5.6K in 8 weeks
- Funded and transferred users grew alongside it — this is real usage, not just attempts

But the conversion rate is falling:
- % of users who funded dropped from ~51% to ~41%
- The drop starts in the week of Jan 29 and then flattens — it's a step change, not a slow slide

Note: No `transfer_id` given, so the funnel is built at user level.

**Speaker notes (~45 sec, follows slide order top to bottom):**
- Starting with the headline: weekly users creating a transfer grew from 1.1 thousand to 5.6 thousand over 8 weeks, and funded and transferred users grew right alongside it, so this is real usage, not just people kicking the tires.
- But the conversion rate is falling. The share of users who funded dropped from about 51 percent to about 41 percent.
- That drop isn't gradual, it starts sharply in the week of January 29th and then flattens out, a step change, not a slow slide.
- One data note: there's no transfer ID in this dataset, so the funnel here is built at the user level, not the transfer level.

**Back pocket:** *(to be drafted)*

---

### Slide 10 — Non-Europe Normalizes, Europe Scales but Converts Weakly

**Title:** Non-Europe normalised after the launch spike; Europe scaled 3x but converts at 31%

**Content (on screen):**
- Volume tripled after Jan 22
- Step decline in conversion rates
- Launch spike settling to a stable baseline

Non-Europe: launch spike settling to a new normal
- Conversion steady at ~52%, nothing broke here

Europe: 3x growth, but weak and getting weaker
- Converts at ~31%; this is what pulled the blended rate down

**Speaker notes (~45 sec, follows slide order top to bottom):**
- So where is that conversion drop coming from? Splitting by region tells the story.
- Volume tripled after January 22nd, and that's exactly where we see the step decline in conversion.
- Non-Europe settled into a stable baseline after the launch spike, conversion steady at around 52 percent, nothing broke there.
- Europe is the opposite story, 3x growth in volume, but converting at only about 31 percent, and that's what pulled the overall blended rate down.

**Back pocket:** *(to be drafted)*

---

### Slide 11 — Root Cause: New Android Users in Europe Can't Fund

**Title:** Root cause: New Android users in Europe cannot fund the transfer

**Content (on screen):**

They fund at ~3% vs ~30% on iOS and web — a 10x gap that has existed since launch week.

Europe's new users grew 6x and the funnel scaled the failure with them:
- Created went from 0.3K to 1.8K users/week
- Funded grew in exact proportion — the rate never improved, it stayed stuck at ~17%

The whole problem sits in one cell:
- New EU users on Android fund at ~1.5–4%
- New EU users on iOS and web fund at ~28–33% — ~10x better

It's a blocker, not slow conversion:
- The rate has been near-zero since week one, it never worked
- It only became visible when this segment grew 6x

**Speaker notes (~50 sec, follows slide order top to bottom):**
- Digging into Europe specifically, the root cause is narrow and sharp: new Android users in Europe cannot fund the transfer.
- They fund at about 3 percent, compared to about 30 percent on iOS and web, a 10x gap that's existed since launch week.
- Europe's new users grew 6 times over, from 0.3 thousand to 1.8 thousand a week, and the funnel scaled that failure right along with them, the funded rate never improved, it stayed stuck at around 17 percent blended.
- The whole problem sits in one cell: new EU Android users fund at 1.5 to 4 percent, new EU iOS and web users fund at 28 to 33 percent.
- This is a blocker, not slow conversion. The rate has been near zero since week one, it never actually worked, it only became visible once this segment grew large enough to matter.

**Back pocket:** *(to be drafted)*

---

### Slide 12 — The Cost of the Bug: Missed Opportunity from Europe's New Android Users — ✅ CONFIRMED

**Content (on screen):**

- Actual performance was only about a tenth of what the same users would have produced on iOS or Web, roughly a 10x gap
- That gap holds consistently at both the funding stage and the completion stage
- Fixing this alone lifts Europe's overall funded rate from 33% to 39%

*Assuming Android had converted at the same rate as iOS and Web, same users, same period, only the platform differs.*

Chart 1 — Funded:
- Chart title: "Funded Transfers: What the Bug Cost Us"
- Y-axis: "Funded Transfers (#)"
- X-axis: "Funded of Created"
- Bars: Counterfactual Funded = 853, Missed (Android bug) = −773, Subtotal (Actual) = 80

Chart 2 — Completed Transfers:
- Chart title: "Completed Transfers: What the Bug Cost Us"
- Y-axis: "Completed Transfers (#)"
- X-axis: "Transferred of Created"
- Bars: Counterfactual Transferred = 650, Missed (Android bug) = −585, Subtotal (Actual) = 65

**Speaker notes (~50 sec, follows slide order top to bottom):**
- Actual performance was only about a tenth of what the same users would have produced on iOS or Web, roughly a 10x gap.
- That gap holds consistently at both the funding stage and the completion stage.
- Fixing this one issue alone would lift Europe's overall funded rate from 33% to 39%.
- Assuming Android had converted at the same rate as iOS and Web, same users, same period, only the platform differs, we'd have expected 853 funded and 650 completed transfers.
- We got 80 funded and 65 completed. That gap, about 585 missed completed transfers, is why fixing this isn't a nice to have, it's the single highest-leverage fix on this whole launch.

**Back pocket:** *(to be drafted)*

**Note:** confirmed live in the Google Slides deck, 2026-08-16. Now sits at Slide 12, right after Root Cause, not before Recommendations as originally planned, Himanshu placed it there when actually building it in Slides since it flows more naturally right off the root-cause finding. Funnel Performance Varies by Region (old Slide 12) moved to Slide 13 to make room.

---

### Slide 13 — Funnel Performance Varies by Region

**Title:** Funnel performance varies by region: "Other" funds best and completes worst; Europe the inverse

**Content (on screen):**

Existing customers only, to isolate corridor performance from new-user acquisition effects:
- "Other" funds best (72.9%) but completes worst (46.7%); Europe is the exact reverse (50.1% funding, 77.1% completion)
- "Other" is weakest end-to-end (34.1%) despite the strongest start vs. Europe (38.7%) and NorthAm (40.0%)

Note: Existing customers only — removes the new-user Android issue from Slide 11, so this chart isolates corridor performance. For new users, the completion pattern is nearly identical across all customers.

- We are collecting money we cannot deliver — post-funding failures cost refunds, reconciliation, and customer trust.
- Next: validate against compliance and payout-rejection data to confirm the cause.

**Speaker notes (~45 sec, follows slide order top to bottom):**
- Stepping away from Android specifically, and looking only at existing customers so the new-user Android issue doesn't distort the picture, funnel performance still varies sharply by region.
- "Other" funds best at 72.9 percent, but completes worst at 46.7 percent. Europe is the exact opposite, 50.1 percent funding but 77.1 percent completion.
- End to end, "Other" is actually the weakest region at 34.1 percent, despite having the strongest start, versus 38.7 percent for Europe and 40.0 percent for NorthAm.
- That means we're collecting money we can't deliver, post-funding failures cost us refunds, reconciliation work, and customer trust.
- Next step here is validating against compliance and payout-rejection data to confirm what's actually causing it.

**Back pocket:** *(to be drafted)*

---

### Slide 14 — Recommendations & Next Steps — ✅ CONFIRMED

**Content (on screen):**

Performance:
- Adoption is strong and growing; established non-EU markets have settled at a healthy baseline after the launch spike
- Recent growth is concentrated in new European users, who convert at roughly a third the rate of new users elsewhere
- The overall conversion decline is a mix effect, not a product regression, every segment's rate is flat
- Separately, in "Other" markets we are losing transfers after the customer has paid

Investigate:
- What launched in Europe in late January (campaign, market launch, etc.)
- Why new Android users in Europe cannot fund
- What is driving the post-funding failures in "Other"

Next steps:
- Audit Android funding flow for new EU accounts, check payment methods, KYC step, Android version support
- Work with Compliance on whether new EU users are being blocked, and where in the flow
- Break "Other" down to country level, it is not a uniform bucket; a few corridors may drive the whole gap
- Pull payout-rejection reason codes
- Benchmark against prior route launches (BRL to USD, PHP to USD) to establish whether these rates are normal

Conclusion:
- This isn't a broad product problem, it's one identifiable, fixable issue with an outsized and growing cost
- The Android audit is the single highest-leverage fix on this launch, prioritize it first

**Speaker notes (~55 sec, follows slide order top to bottom):**
- Stepping back, adoption is strong and growing, and outside Europe, performance settled into a healthy baseline after the initial launch spike.
- The overall conversion dip is a mix effect, not a broken product, every individual segment's rate held flat, it's just that a larger share of recent growth came from Europe's new Android users, who convert far below everyone else.
- Separately, in "Other" markets, we're losing transfers after the customer has already paid, that's a different problem worth its own investigation.
- Next steps split three ways: audit the Android funding flow directly, work with Compliance on whether new EU users are being blocked, and break "Other" down to country level since it's not a uniform bucket.
- Bottom line: this isn't a broad product problem, it's one identifiable, fixable issue with an outsized cost, and the Android audit is the single highest-leverage fix on this launch.

**Back pocket:** *(to be drafted)*

**Note:** confirmed live in the Google Slides deck, 2026-08-15. "MXN to EUR" was dropped from the benchmark bullet to match the Slide 6 decision. "Cost of Opportunity" stats were considered for this slide but left out, they're already fully covered on Slide 13, repeating them here would be redundant.

---

### Slide 15 — Section Divider

**Content (on screen):**
- Appendix

**Speaker notes (~10 sec):**
- That's the core analysis. A couple of supporting cuts follow in the appendix if useful.

---

### Slide 16 — Europe: New vs. Existing Customers

**Content (on screen):**
- New users drove all the growth and all the decline; existing customers stayed flat at ~50% funding

**Speaker notes (~25 sec):**
- One more supporting cut. Splitting Europe by new versus existing customers, new users drove all the growth and all the decline we saw.
- Existing customers stayed completely flat throughout, funding at around 50 percent the whole time, so this really is a new-user problem specifically, not something affecting the whole Europe customer base.

**Back pocket:** *(to be drafted)*

---

## Area 2 — Remaining Work

1. ~~**"Worth the investment" framing**~~ — ✅ Done, Slide 7 (Is It Worth Launching? Revenue vs. Cost), live in the Slides deck.
2. **Query & pipeline performance at scale** — how the SQL in `wise_funnel_events_regional` (or the approach behind it) is designed with database cost/performance in mind — partition pruning, scan volume, join strategy, incremental vs. full builds. Not yet represented anywhere in the deck. Not yet started.

---

**Log:**
- Baseline transcribed from the live `Wise_Case_Study` Google Slides deck (15 slides), 2026-08-15.
- Slide 4 finalized, 2026-08-15: added Reverse-Corridor Activity as a nested cut under USD Balance Holders (resolved overlap between the two rather than dropping either), tightened USD-Related Product Engagement into a measurable rate. Himanshu made the corresponding edits directly in the live Slides deck himself.
- Slide 4 speaker notes finalized, 2026-08-15: full ~45-second narration written to track the slide's bullet order top to bottom (first draft jumped to Reverse-Corridor Activity before Attempt Rate, out of order with the slide, corrected). Assumptions deliberately left out of the spoken narration since they're small on-screen text the audience reads directly. Back pocket still pending.
- Slide 4 denominators standardized, 2026-08-15: Attempt Rate and USD Balance Holders were scoped to two different populations ("active users holding MXN balances" vs. "multi-currency users holding MXN balances"), caught as an inconsistency. Fixed by dropping the redundant "multi-currency" qualifier (implied by "also hold a USD balance") and dropping "active" everywhere since it was never defined with a time window. All three primary signals now share one consistent base: "users holding MXN balances." Also dropped "active" from the Reverse-Corridor Activity sub-bullet ("active or completed" → "completed") for the same reason.
- Slide 5 finalized, 2026-08-15: since the deck was already submitted, changes were kept light (additions only, no restructure). Added one line operationalizing Intent Strength into a real bucketing rule ("High Intent = meets all three signals above; Low Intent = everyone else") instead of leaving three qualitative comparisons undefined. Added explicit thresholds under each signal (2+ currencies, ≥1 international transfer in trailing 12 months, ≥2 MXN to USD attempts in trailing 90 days). Reframed Customer Value/Profile from a flat list into a stated cross-tab method (Intent Strength × Account Type) to find the single strongest opportunity segment. A typo in the live slide ("trailing 1 months") was caught and fixed by Himanshu to "trailing 12 months." One minor grammar item flagged but left as-is pending confirmation: "users who hold or has held" has a subject-verb mismatch. Speaker notes finalized, ~45 sec, follows slide order top to bottom.
- Slide 6 finalized, 2026-08-15: closed the gap where the comparable-corridor benchmark never actually connected to Slide 5's High Intent population. Added a "Conversion rate" sub-bullet under the comparable-launches bullet (% of each corridor's pre-launch high-intent pool that converted post-launch). Rewrote "Final output" from a vague restatement into two explicit formulas: Expected Adopters = High-Intent Users × comparable-corridor conversion rate, and Expected Volume = Expected Adopters × post-adoption transfer size/frequency. Considered adding MXN to EUR as a third comparable corridor (it's already referenced on Slide 12, and would match on the sending currency rather than the receiving one), but decided against it to keep the change light, BRL to USD and PHP to USD only. Speaker notes finalized, ~45 sec, follows slide order top to bottom.
- Slide 6 formula corrected, 2026-08-15: caught two dimensional-analysis errors in the Expected Transfer Volume formula. First, "Adopters × Frequency" alone is a transfer count, not a dollar volume, average transfer size was missing as a multiplier. Second, once size was added back in, it was mistakenly labeled "transfer volume" on both sides of the equation (the aggregate output and the per-transaction input used the same word), fixed by renaming the input to "transfer size." Final formula: Expected transfer volume, $ = Expected Adopters (#) × post-adoption transfer size ($/transfer) × frequency (transfers/period). Units now explicit on every term.
- Slide 7 created, 2026-08-15: new slide, "Is It Worth Launching? Revenue vs. Cost," inserted after Slide 6 to close the loop on the take-home's opening question. Combines the "Cost of Launching" and "Is It Worth It" content drafted earlier in the session into a single slide, honoring the 1-new-slide budget. Revenue side: Expected Revenue = Expected Transfer Volume × transfer fee rate, with "transfer fee rate" specifically defined as Wise's per-transfer % fee on this corridor (not a company-wide margin) after catching that "take rate" was ambiguous. Cost side: operational (compliance/licensing, payout rails, support scaling) and marketing (acquisition spend to acquire customers, simplified down from an earlier "modeled adoption curve" reference that Himanshu flagged as an unexplained concept he couldn't confidently defend), both benchmarked from the same BRL to USD / PHP to USD corridors already used in Slide 6. Decision pulled out as its own labeled section, split into two clean bullets (payback within target window; High Intent base large enough to sustain post-ramp volume). All slides from the old Slide 7 divider onward renumbered up by one (7→8 ... 15→16), including one internal cross-reference on the old Slide 11 (now 12) that pointed to "Slide 10" (now 11). Slide 2's ToC and Slide 3's methodology overview updated to preview this 4th piece.
- Slide 7 confirmed live, 2026-08-15: Himanshu added the finalized slide to the live Google Slides deck himself and shared a screenshot matching the file exactly. Speaker notes updated to match the final on-screen order. The full demand-estimation arc (Slides 3–7) is now complete end to end: signal → intent → forecast → verdict.
- Launch-evaluation data verification, 2026-08-15: cross-checked the SQL query and every derived tab (`Overall`, `funnel by Region`, `funnel by Experience`, `funnel by platform`, `funnel mix`, `SQL DATA`) against Slides 9, 10, 11, 12, 13 (old numbering). All numbers confirmed accurate. Found one real labeling bug in `funnel mix`, a table headered "Europe - Android - New" is actually non-Android data (missing "non" in the header). Traced the true Android+New+Europe numbers via the raw `SQL DATA` rows and confirmed they do support the "~3%" claim on the Android slide. The slide itself is correct; the underlying sheet has a typo worth knowing about before presenting live.
- New Slide 13 built, 2026-08-15: "The Cost of the Bug: Missed Opportunity from Europe's New Android Users." Quantifies the Android bug's impact as a counterfactual, same New-Europe users, same 8 weeks, converting at the non-Android (iOS + Web) rate instead. Computed by hand from the raw `SQL DATA` tab, per-week: Funded, Actual 80 vs. Counterfactual 853 (≈772-773 missed depending on rounding stage). Transferred, Actual 65 vs. Counterfactual 650-655 (≈585-590 missed). Built as two reversed waterfall charts (Counterfactual → Android bug impact as a negative delta → Actual as the ending subtotal), so the "cost" bar renders in red via the chart's native Negative category rather than needing a manual color override. Inserted before the original Recommendations slide (now Slide 14), renumbering everything after it up by one. Live in the Slides deck, screenshot-matched.
- Slide 14 finalized, 2026-08-15: added a "Conclusion" section (2 bullets, priority call on the Android fix), placed last. A combined "Cost of Opportunity & Conclusion" section was drafted but the cost-of-opportunity stats were ultimately left off this slide since they're already fully covered on Slide 13, kept to just "Conclusion" to avoid repeating numbers. Also computed and discussed, but did not add to any slide: Europe's overall funded rate would rise from 33.3% to an estimated 38.9% if the Android bug were fixed (using the precise `Overall` tab region totals, 4,579/13,768 actual vs. (4,579−80+852)/13,768 counterfactual), still below Non-Europe's ~53%, so the bug explains part but not all of Europe's underperformance. Speaker notes finalized, ~55 sec.
- Slide 3 corrected and finalized, 2026-08-15: the original baseline transcription didn't match the live slide, it had an extra "Wise mission" bullet, an entire "Aligning with Mission" section, and "USD bank accounts" where the live slide actually says "USD currency holders." Corrected to match reality. Added a new "How I Approached This" block between the MXN-USD context and the methodology list, so the four-step methodology reads as reasoned structure (the take-home's real question is "is this worth building," which breaks into sizing demand and weighing it against cost) instead of an unexplained bullet list.
- Slide 3 methodology bullet reworded, 2026-08-15: "Weigh against launch cost to determine if it's worth it" broke the terse verb-first rhythm of the other three bullets and didn't match Slide 7's actual title. Shortened to "Weigh revenue against cost."
- Slide 3 speaker notes finalized, 2026-08-15: ~40 sec, follows slide order (mission → MXN-USD context → how I approached this → four-step preview). This completes Slide 3, content and speaker notes both locked.
- Final deck reconciliation, 2026-08-16: Himanshu shared the exported PDF, treated as the source of truth. Fixed two structural mismatches (Slide 12/13 order swapped to match the live deck; removed appendix slide "The Android Problem Affects New Users Only," no longer in the deck). Confirmed two live-deck regressions were already fixed by Himanshu before this pass: Slide 5's "trailing 1 month" back to "trailing 12 months," and Slide 13's footnote back to referencing Slide 11 instead of "slide 3." Also added a third bullet to Slide 12 that Himanshu had added live but not shared a screenshot of: "Fixing this alone lifts Europe's overall funded rate from 33% to 39%."
- Speaker notes completed for every remaining slide, 2026-08-16: Slides 1, 2, 8, 9, 10, 11, 13, 15, 16 all drafted in one pass at Himanshu's request ("this is final from my side, add speaker notes of all slides"). Every slide in the 16-slide deck now has speaker notes. Only thing left everywhere is Back pocket (anticipated pushback answers), still empty on every slide.
