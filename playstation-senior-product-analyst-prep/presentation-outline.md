# PlayStation — Senior Product Analyst Presentation
## Causal Study to Experimentation: How SMS Became a Growth Lever for Mailchimp

> ## HARD RULES — READ BEFORE EDITING THIS FILE
> 1. Build this deck **slide by slide, with explicit permission before each addition or change.**
>    Before drafting or updating any slide: propose the content in chat first, wait for the user's go-ahead, and only then write it into this file.
>    Do not get ahead of confirmed slides — if only slide N is confirmed, the file should not contain drafted content past slide N.
> 2. **Points and subpoints, not long paragraphs**, wherever the content allows it — on-screen content, speaker notes, and back pocket items should all default to bulleted points rather than dense prose.
> 3. **Speaker notes and back pocket items must be full, complete sentences in easy, plain English** — written so they can be read aloud and rehearsed directly, not shorthand or compressed phrases. Bullet them, but each bullet should be a real sentence, not a fragment.

**Source project:** [SMS CEM Causal Project](../../Personal/SMS%20CEM%20Causal%20Project/cem_causal_study.md) — full underlying project (write-up, notebooks, production code, executive PDF/PPT) at `/Users/himanshudubey/Documents/Projects/Personal/SMS CEM Causal Project`

## Original Interview Prompt (from PlayStation)

> We'd love to hear about a past analytics project where your work drove measurable business impact. Please prepare a 10-15 minute presentation covering the following:
>
> * What is the problem you are trying to solve?
> * How was your analytics approach?
> * What are your biggest challenges and how did you overcome them?
> * What was the impact of the project?

**Format:** 10–15 min presentation, "past analytics project with measurable business impact"
**Structure:** Problem → Analytics Approach → Biggest Challenges → Impact, told as one connected story across two linked projects (a causal study, then the A/B test it led to)

> **Note on numbers:** Keep figures relative (percentages, ranges) rather than exact dollar amounts, per-user economics, or precise cohort sizes throughout this deck. If pushed for a specific figure, it's fine to say "I'd want to check what I can share externally on the exact number, but directionally..." and stay in percentages.

**Status:** Building slide by slide. Confirmed so far: Title, Slide 1, Slide 2, Slide 3, Slide 4, Slide 5, Slide 6, Slide 7.

---

## Title Slide

**Title:** Causal Study to Experimentation:
How SMS Became a Growth Lever for Mailchimp

**Speaker notes:**
- I'm going to walk you through two connected projects at Mailchimp.
- First, I proved that a new product channel was actually creating value for the business.
- Then I used that proof to help design and launch an experiment.
- I picked these two together because they show the full loop, from finding an insight to making a business decision.
- That loop is a big part of what this kind of role looks like day to day.

**Back pocket:**
- If I'm asked to introduce myself first, I should keep it to one sentence and get straight to the project, not spend presentation time on a full bio.
- I should be careful from this very first slide onward not to share exact dollar figures, exact cohort sizes, or internal tool and table names.

---

## Slide — Table of Contents

**Title:** Agenda

**Content (on screen):**
1. The Business Problem
2. Proving Causality — The Causal Study
3. Business Impact of the Study
4. The Experiment — Driving SMS Adoption
5. Results & The Halo Effect Confirmed
6. Q&A

**Speaker notes (~20 sec):**
- Quick roadmap before diving in.
- I'll cover the business problem, the causal study that proved SMS mattered, its business impact, the experiment that followed, and the results, including how the two methods confirmed each other.
- Then I'll open it up for questions.

---

## Slide 1 — Context & The Problem (Part 1)

**Title:** The Business Problem

**Content (on screen):**
- Mailchimp: multichannel marketing platform for small and medium businesses
- Historically email-first; launched SMS in 2024 as a new channel alongside email campaigns
- Two years in, SMS was still in growth stage. To grow further, it needed:
  - To unlock more resources
  - And to position SMS in Mailchimp's business strategy
- But proving that required answering one question first:
  - does SMS actually make the business better,
  - or are already-successful customers just self-selecting into it?
- Historical data showed a pattern that hinted at an answer, but wasn't proof on its own: customers who adopted SMS also tended to have
  - larger contact lists
  - sent more email campaigns
  - activated more automations
  - higher-tier plans
  - higher overall revenue

**Speaker notes:**
- Mailchimp is a multichannel marketing platform for small and medium businesses.
- Historically, it was an email-first product.
- In 2024, we launched SMS as a new channel, so businesses could send SMS campaigns alongside their email campaigns.
- It was still early days, SMS was in growth stage.
- Two years in, the SMS team needed more resources and a clearer place in Mailchimp's overall business strategy.
- But proving that required answering one question first.
- Was SMS actually growing the business, or were already-successful customers just choosing to try it on their own?
- Looking at historical data, we noticed a pattern. Customers who had adopted SMS also tended to have larger contact lists, send more email campaigns, activate more automations, sit on higher tier plans, and generate more overall revenue.
- But that was just a hint, not proof, correlation alone couldn't answer the question.
- That question is exactly what this project set out to answer.

**Back pocket:**
- Without proof, SMS would be competing for resources just on a feeling that it was working, and that loses against teams who bring harder numbers.
- If I'm asked to define "growth stage" more precisely, I should keep it general, just a new channel that was still ramping up and not yet a proven pillar of the business.
- **Transition to next slide:** "So how do you prove something is causing growth, when you can't just randomly assign customers to buy it?"

---

## Slide 2 — Proving It Without an Experiment

**Title:** Hypothesis: SMS adoption causes real incremental value for Mailchimp, not just a correlation with already-successful customers who happened to try it.

**Content (on screen):**

Idea:
- Find lookalike SMS non-adopters and compare them with SMS adopters

Challenges:
- Customers who bought SMS were already bigger spenders before they tried it
- A direct comparison would be unfair, and misleading
- Couldn't run an A/B test: can't randomly assign who buys credits

Solution:
- Find a technique that makes this a fair comparison
- Matched SMS buyers to lookalike non-buyers on pre-purchase behavior
- Coarsened Exact Matching (CEM)
  - Sorts customers into buckets based on shared pre-purchase attributes,
  - Then pairs each SMS buyer with a non-buyer from that exact same bucket

Metric: Overall Mailchimp and Non-SMS revenue in the 90 days before and after purchase
- Set a reference date for each customer (SMS purchase date, or an equivalent random date for non-buyers)
- Pre-period = 90 days before HVA; Post-period = 90 days after HVA

**Speaker notes:**
- Here's the question I was trying to answer: was SMS actually creating new value for the business, or were we just watching customers who were already doing well happen to try it?
- That was the hypothesis I set out to test.
- The idea was simple: find customers who looked just like SMS buyers, but never bought SMS, and compare the two groups.
- But that comparison had a problem. Customers who bought SMS were already bigger spenders before they ever touched it.
- If we just compared the two groups directly, we would be giving SMS credit for revenue that was already going to happen anyway.
- We also couldn't fix this with a normal experiment, because you can't randomly assign customers to buy credits.
- So we needed a technique that could make this comparison fair.
- We used Coarsened Exact Matching, or CEM. It sorts customers into buckets based on shared pre-purchase attributes, then pairs each SMS buyer with a non-buyer from that exact same bucket.
- For the metric, we tracked both overall Mailchimp revenue and non-SMS revenue specifically, not just SMS revenue itself.
- To measure that fairly, I set a reference date for each customer, their SMS purchase date for buyers, or an equivalent random date for non-buyers, and compared the 90 days before that date to the 90 days after.
- If SMS only lifted SMS spend, that would be expected and not very interesting on its own.
- The real question was whether SMS also lifted everything else, like email plans, upgrades, and overall platform usage.

**Back pocket:**
- If I'm asked why I chose CEM over propensity score matching, I should say CEM is model free, so the balance between groups is guaranteed by how the matching itself is built, not assumed from a model that could be wrong.
- I should keep the exact number of matching attributes and cohort sizes vague if asked, something like "about a dozen pre-purchase signals" and "tens of thousands of buyers matched against a much larger pool of non-buyers."
- If asked how I validated the match was fair, I should say the differences between the two groups dropped close to zero after matching, across every attribute used.
- If asked why 90 days specifically, I should say it was long enough to see real behavior change like upgrades and plan changes, but short enough to keep the analysis clean.
- If asked what HVA stands for, I should say High Value Action, a reference date used to anchor the pre and post comparison window for each customer.
- **Transition to next slide:** "So what did that comparison actually show?"

---

## Slide 3 — The Causal Study: Results

**Title:** The Halo Effect: Buying SMS Doesn't Just Add SMS Revenue — It Makes Customers More Valuable to Mailchimp Across the Board

**Content (on screen):**

Findings:
- SMS buyers saw a ~79% lift in total revenue in the 90 days after purchase, compared to matched non-buyers
- Even after removing SMS spend entirely, buyers still spent ~28% more on the rest of Mailchimp

Where the Extra Revenue Came From:
- ~79% from new free to paid conversions: free trial, free package, and inbound users converting to a paid plan
- ~21% from existing paid users upgrading to a higher plan or tier

Signs They Went Deeper Into Mailchimp:
- Sent 28% more email campaigns than matched non-buyers; grew their contact lists to reach more customers
- Activated 3.4x more automations
- Connected their stores to Mailchimp
- 90-day retention was 4 percentage points higher

Validation:
- The two matched groups looked nearly identical on every pre-purchase attribute (differences close to zero), confirming the comparison was fair

**Speaker notes:**
- The goal was to prove that SMS creates a halo effect, that buying SMS doesn't just add SMS revenue, it makes customers more valuable to Mailchimp across the board.
- The results confirmed it at every level.
- SMS buyers saw close to an 80 percent lift in total revenue compared to their matched non-buyer counterparts.
- Even after removing SMS spend entirely, buyers still spent about 28 percent more on the rest of Mailchimp.
- When I looked at where that came from, most of it was new paid conversions, users moving from a free trial or free plan into a paid one. The rest came from existing paid users upgrading to a higher tier.
- And it wasn't just about spend. These customers were using Mailchimp more broadly, growing their contact lists, sending more email, turning on more automations, connecting their online stores.
- They sent 28 percent more email, turned on more than three times as many automations, and had four points higher retention at the 90 day mark.
- And before trusting any of this, I confirmed the two matched groups looked nearly identical on every pre-purchase attribute, which is what made this comparison fair in the first place.
- That's the halo effect. SMS wasn't competing with the rest of the platform for revenue, it was pulling customers deeper into it.

**Back pocket:**
- These percentages are safe to say out loud as-is, no need to soften or round them further if asked to repeat.
- I should still avoid exact dollar figures or exact user counts if asked to go more specific than this.
- If asked how I know this is causal and not a fluke, I should say I stress-tested it further, and point to the challenges slide rather than over-explaining here.
- **Transition to next slide:** "That answered whether SMS mattered. It didn't answer how to get more people to adopt it."

---

## Slide 4 — Business Impact of the Causal Study

**Title:** The Study Didn't Just Prove the hypothesis, it Changed the Roadmap

**Content (on screen):**

SMS became growth lever of Mailchimp

SMS Cross-Sell Experiment
- Used the findings to target users who completed onboarding with in-app prompts to adopt SMS
- Became a direct follow-on experiment

Rethinking Onboarding
- Instead of treating Email and SMS as separate products, Mailchimp started targeting omnichannel adoption, Email + SMS together from day one

Sales and Support Enablement
- Sales and customer-facing teams were trained and given incentives to cross-sell SMS

**Speaker notes:**
- The study gave leadership the proof they needed.
- SMS wasn't just a product being built, it was a real growth lever for the whole Mailchimp business.
- That directly led to three things.
- First, an SMS cross-sell experiment, we used the findings to target users right after onboarding with in-app prompts to adopt SMS, and that became a direct follow-on project, which I'll walk through next.
- Second, it changed how the company thought about onboarding itself. Instead of treating Email and SMS as separate products, Mailchimp started targeting people for omnichannel adoption, Email and SMS together from day one.
- Third, sales and customer-facing teams were trained and given real incentives to cross-sell SMS, built directly on this finding.

**Back pocket:**
- If asked how these three things were prioritized or sequenced, I should say the experiment came first since it was the fastest way to test the finding at scale, and the onboarding and sales changes followed once the experiment validated it further.
- This slide is the hinge of the whole presentation, it's where I should sound most confident, since it's proof the work didn't just produce a slide, it changed real decisions.
- **Transition to next slide:** "The first of those three things, the cross-sell experiment, is worth walking through in full."

---

## Slide 5 — The Next Question: Driving Adoption

**Title:** The next question: How do we get more users to adopt SMS? SMS Cross-Sell Experiment

**Content (on screen):**

What the Data Showed:
- Engagement with new products drops sharply after the first 2 weeks of account activation, intent is highest right at the start
- 55% of all SMS engagement happen within 1 day of the Mailchimp plan purchase
- Target users the moment they complete onboarding

Hypothesis:
If new paid users see an SMS registration screen at the end of onboarding, SMS purchase rate will increase, because 55% of SMS application starts already happen within 1 day of the Mailchimp plan purchase

Experiment Design (50/50 split):
- Control: standard onboarding, no SMS mention, users discover SMS on their own via the left nav or in-product prompts
- Variant: SMS takeover screen at the end of onboarding, shown to all eligible users, with a direct CTA into SMS registration
- User-level randomization, assigned when a user completed onboarding
- Ran for 28 days, sized to detect the desired minimum detectable effect (MDE)
- Verified randomization was clean with a SRM check, the observed split matched the expected 50/50 with no imbalance

**Speaker notes:**
- The next question was how to get more users to adopt SMS on the Mailchimp platform.
- Historical data pointed us in a clear direction.
- Engagement with any new product drops off sharply after the first two weeks of account activation, the window to reach someone is short, and intent to try something new is highest right at the beginning.
- We also saw that 55 percent of all SMS engagement happens within 1 day of the Mailchimp plan purchase.
- It was evident from the data that we needed to target users the moment they complete onboarding.
- So the hypothesis for this test was, if new paid users see an SMS registration screen at the end of onboarding, then SMS purchase rate will increase, because 55 percent of SMS application starts already happen within 1 day of the Mailchimp plan purchase.
- Control users completed the standard onboarding flow with no mention of SMS anywhere, they had to discover it on their own through the left nav or other in-product prompts.
- The variant added an SMS takeover screen at the end of onboarding, shown to all eligible users, with a direct call to action into SMS registration.
- Randomization happened at the user level, assigned the moment someone completed onboarding.
- The test ran for 28 days, and was sized to detect the effect size we cared about.
- I also checked that the randomization itself was clean using a sample ratio mismatch check, and the observed split matched the expected 50/50 with no imbalance.

**Back pocket:**
- If asked what a SRM check is, I should say it's a statistical check that confirms the number of users in each group matches what you'd expect from a clean random split, catching any hidden bias in how the test was rolled out.
- I should hold back the "every team wants that screen" detail for the Challenges slide, not use it here.
- If asked why 55 percent specifically mattered, I should say it told us intent was concentrated in a narrow window, which is why timing, not just visibility, was the core hypothesis.
- **Transition to next slide:** "Here's what came back."

---

## Slide 6 — Results

**Title:** Results: The Data Supports Rolling Out the Variant

**Content (on screen):**

| Tier | Metrics | Lift |
|---|---|---|
| Primary | SMS Purchase Rate | 🟢 +23% (stat sig) |
| Secondary (Funnel Engagement) | SMS Application Start Rate | 🟢 |
| Secondary (Funnel Engagement) | SMS Application Complete Rate | 🟢 |
| Secondary (Product Engagement) | SMS send rate | 🟡 Flat to slightly positive |
| Secondary (Product Engagement) | SMS create rate | 🟡 Flat to slightly positive |
| Secondary (Product Engagement) | SMS contact addition rate | 🟡 Flat to slightly positive |
| Secondary (Revenue) | SMS 14D ARPU | 🟢 |
| Secondary (Revenue) | MC 14D ARPU | 🟢 +11% |
| Guardrail | Product payoff rate | 🟡 Flat |

Note:
- Only the primary metric was formally powered and significance-tested; secondary metrics are shown directionally
- Test ran for the primary metric's runtime, guardrails were more than adequately powered

Takeaway:
The SMS Cross-sell experiment confirmed the hypothesis: placing an SMS takeover screen right after onboarding worked, it:
- Significantly improved SMS Purchase rate
- Significantly improved MC 14D Revenue
- Without disrupting our core product experience

**Speaker notes:**
- Here's what came back after the test ran its full course.
- The primary metric, SMS purchase rate, was up 23 percent on a relative basis, and this result was statistically significant.
- Funnel engagement moved in the same direction, both SMS application start rate and completion rate improved.
- Product engagement metrics, sends, creates, and contact additions, were flat to slightly positive.
- On revenue, SMS 14-day ARPU improved, and Mailchimp 14-day ARPU was up 11 percent.
- The guardrail, product payoff rate, stayed flat, meaning the new screen didn't hurt the core product experience.
- I want to be upfront about one thing. Only the primary metric was formally powered and significance-tested, the secondary metrics are shown directionally, not independently tested.
- The test ran for the primary metric's full required runtime, which meant the guardrail metric was more than adequately powered, so a flat result there is a real flat result, not just an underpowered one.
- Putting it together, the experiment confirmed the hypothesis. Placing an SMS takeover screen right after onboarding significantly improved SMS purchase rate and Mailchimp revenue, without disrupting the core product experience.

**Back pocket:**
- If asked for the confidence interval or MDE detail on the primary metric, I should say the interval sat entirely above zero and above the 7 percent MDE we powered for, so this was both statistically and practically significant, not just barely detectable.
- If asked why secondary metrics don't have significance markers, I should say testing every metric independently risks false positives from multiple comparisons, so I chose to show them directionally and reserve formal significance testing for the primary metric.
- If asked whether guardrails were adequately powered, I should say yes, the test ran for the primary metric's longer required duration, so the guardrail metric had more data than it needed to detect a real problem if one existed.
- If asked about "probability to beat control" language, I should be ready to clarify whether the test used a frequentist p-value/confidence-interval approach or a Bayesian posterior probability, and keep my terminology consistent with whichever it actually was.
- **Transition to next slide:** the halo effect / ARPU decomposition and the tradeoff deep-dive.

---

## Slide 7 — The Halo Effect, Confirmed

**Title:** The causal study proved causality; the RCT confirmed it.

**Content (on screen):**

Where the revenue lift came from:
- ~69% from non-SMS Mailchimp revenue (plan upgrades, monthly plan spend)
- ~31% from SMS revenue itself
- Same halo pattern as the earlier causal study — but now proven under true randomization, ruling out selection bias

The expected tradeoff in secondary metrics:
- Control users found SMS organically, so they were already SMS-ready and intentional
- Variant users were reached out to proactively, pulling in some who weren't yet SMS-ready

Business Impact:
- $2.3M projected revenue impact over the next 12 months

The Bigger Picture:
- The first study answered: Does SMS create incremental value?
- The experiment answered: Can we create more SMS adoption?
- And together, they answered: Can we turn that incremental value into scalable business growth?

**Speaker notes:**
- When I looked at where the ARPU lift actually came from, the pattern was striking.
- About 69 percent of the lift came from non-SMS Mailchimp revenue, things like plan upgrades and monthly plan spend, and the remaining 31 percent came from SMS revenue itself.
- That's the same halo pattern the earlier causal study found. But this time it came from a true randomized experiment, so selection bias is ruled out by design.
- Seeing the same pattern show up under randomization is what gave the team real confidence, not just in this experiment, but retroactively in the earlier causal study too.
- There was an expected tradeoff in the secondary metrics, and it makes sense once you think about who was in each group.
- Control users found SMS organically, so they were already SMS-ready and intentional.
- Variant users were reached out to proactively, which pulled in some people who weren't yet SMS-ready.
- Putting a number on the overall business impact, this drove a projected $2.3 million in revenue over the next 12 months.
- Zooming out, here's the bigger picture.
- The first study answered whether SMS creates incremental value.
- The experiment answered whether we could create more SMS adoption.
- And together, they answered whether we could turn that incremental value into scalable business growth.

**Back pocket:**
- If asked how the $2.3 million was calculated, I should say it was projected from the observed revenue lift per user, scaled across the eligible population, and rolled forward over 12 months.
- If asked whether the tradeoff concerns me, I should say it's a real cost worth tracking, and the natural next step is watching whether those lower-engagement users catch up over a longer window.
- If asked how confident I am the halo effect is real and not a coincidence, I should point out it replicated under two different methods, an observational causal study and a randomized experiment, which is about as strong a confirmation as you can get without a third independent test.
- This closing line is the one to land with real conviction, it's the thesis of the entire presentation, not just a recap.
- **Transition to next slide:** pivot into Challenges, the biggest-challenges section of the talk.

---

## Challenges (verbal answer — no dedicated slide)

**Decision:** No dedicated Challenges slide, the deck is already the right length for a 15-20 minute talk. Use this as a ready-to-speak answer if the interviewer asks directly ("what were your biggest challenges?"), since the original prompt explicitly lists this as one of the four things to cover.

1. **Proving causation without being able to run an experiment.**
   - Couldn't randomize who buys SMS credits, so the causal study had to earn trust a different way.
   - I ran a placebo test, I reran the whole pipeline with a fake, randomly assigned treatment, and the effect collapsed to near zero, which confirmed the real result wasn't just a matching artifact.
   - I also triangulated the result across a few independent matching and estimation methods, and they all agreed in direction, before I took the finding to leadership.

2. **Winning the onboarding placement, not just proving the finding.**
   - The screen right after onboarding is the highest-engagement page in the product, and every other team wanted that same placement.
   - "We think SMS matters" doesn't win that argument on its own, a defensible causal number does.
   - The causal study's rigor is what made the case winnable, it wasn't just an analytical exercise, it was the evidence needed to secure the experiment's placement in the first place.

---

## Appendix

**Process note:** Core deck (Title → ToC → Problem → Approach → Impact → Close) gets finished first. Appendix slides get built after, once the core flow is fully locked. This section is a running log of what we've decided belongs in the appendix as we go, each entry a 1-liner until we actually draft it.

**Planned appendix slides (3, revisit count/order once content is final):**
1. What Is CEM — *drafted below*
2. How the causal study was built — *drafted below*
3. Experiment: additional technical detail (randomization, sizing, primary metric significance, frequentist vs. Bayesian note) — not drafted yet

---

### Appendix Slide 1 — Coarsened Exact Matching

**Title:** Coarsened Exact Matching

**Content (on screen):**

A matching technique used to build a fair comparison group when you can't run a randomized experiment

Core idea:
- Sort customers into buckets based on shared pre-purchase characteristics
- Then pair each treated customer with a non-treated customer from the exact same bucket

Advantage:
- A large pool of non-buyers meant CEM found a high-quality match for nearly every buyer
- Very few were dropped, the direct payoff of having far more controls than treated units

**Diagram:** A bucket-matching visual sits beside the text — three account-age buckets (`<1 year`, `1-3 years`, `>3 years`), each showing an adopter (coral dot) paired with a matched non-adopter (gray dot, connected by a teal line) and one unused non-adopter nearby. The last bucket has no non-adopters at all, so the adopter has no match and is shown faded with a "no match → dropped" label. Legend at top: adopter / non-adopter / matched pair. Built and rendered for screenshotting, dark-theme version already placed into the real slide.

**Speaker notes:**
- Here's a quick primer on the method behind the causal study, Coarsened Exact Matching, or CEM.
- It's a matching technique used to build a fair comparison group when you can't run a randomized experiment.
- The core idea is to sort customers into buckets based on shared pre-purchase characteristics, then pair each treated customer with a non-treated customer from that exact same bucket.
- One real advantage in our case, we had a large pool of non-buyers to match against, so CEM found a high-quality match for nearly every buyer.
- Very few were dropped, which is the direct payoff of having far more controls than treated units.

**Back pocket:**
- If asked why the diagram shows one match per adopter when a bucket has multiple non-adopters, I should clarify that's a simplification for teaching the bucketing concept — in practice, CEM keeps all non-adopters in a matched bucket and weights them (via the later weighted regression step) rather than randomly discarding extras. Weighting is more statistically efficient than random selection, since it uses all available data instead of throwing part of it away arbitrarily.
- If asked for a simple analogy, I should say it's like finding a twin for every treated customer, someone who looked identical on everything that mattered before the treatment happened, so any difference afterward is more likely caused by the treatment itself.
- **Decision:** no CEM-specific "more attributes → more sparse buckets" limitation added anywhere in the deck. The existing observational/residual-confounding limitation already planned for Appendix Slide 2 is sufficient.

---

### Appendix Slide 2 — How the Causal Study Was Built

**Title:** How the Causal Study Was Built

**Content (on screen):**

Who We Studied:
- Mailchimp customers on a paid plan, comparing SMS buyers to matched non-buyers

How We Anchored the Comparison in Time:
- Set a reference date for each customer (SMS purchase date, or an equivalent date for non-buyers)
- Compared the 90 days before that date to the 90 days after

How We Measured the Impact:
- Diff-in-diff: change in revenue for SMS buyers, minus the same change for matched non-buyers
- Isolates what changed because of SMS, not just each group's own trend

Covariate Balance Check:
- Differences between the two matched groups stayed close to zero across every pre-purchase attribute, confirming the comparison was fair
- *(Love plot chart goes here — the sample one already built shows this exact concept)*

Validation Checks:
- Placebo test: reran the pipeline with a fake, randomly assigned treatment, the effect collapsed to near zero
- Triangulated the result across a few independent matching and estimation methods, all agreed in direction

Limitations:
- Observational, not a randomized experiment, residual confounding from unobserved variables is always possible
- The later A/B test provided independent corroboration of the same halo pattern under true randomization, the strongest mitigation short of re-running this exact study as an RCT

**Speaker notes:**
- Here's a bit more on how the study was actually built.
- I studied Mailchimp customers on a paid plan, comparing SMS buyers to a matched group of non-buyers.
- To anchor the comparison in time, I set a reference date for each customer, their SMS purchase date for buyers, or an equivalent date for non-buyers, and compared the 90 days before that date to the 90 days after.
- To measure the impact, I used a diff-in-diff approach, the change in revenue for SMS buyers, minus the same change for matched non-buyers, which isolates what changed because of SMS, not just each group's own underlying trend.
- Before trusting any of it, I checked covariate balance. The differences between the two matched groups stayed close to zero across every pre-purchase attribute, which confirmed the comparison was genuinely fair. This is what a love plot shows, before matching the two groups looked different, after matching they lined up closely.
- I also ran two validation checks. A placebo test, where I reran the whole pipeline with a fake, randomly assigned treatment, and the effect collapsed to near zero. And I triangulated the result across a few independent matching and estimation methods, which all agreed in direction.
- The honest limitation is that this is observational, not a randomized experiment, so residual confounding from unobserved variables is always possible. That's actually why the later A/B test mattered so much, it provided independent corroboration of the same halo pattern under true randomization, which is about as strong a mitigation as you can get short of re-running this exact study as an RCT.

**Back pocket:**
- If asked why 90 days specifically, I should say it was long enough to see real behavioral change like upgrades and plan changes, but short enough to keep the analysis clean and include recent buyers.
- If asked what SUTVA is and whether it holds, I should say it's the assumption that one customer's treatment doesn't affect another customer's outcome, and it's reasonable to assume it holds here since customers make independent purchase decisions.
- If asked what I'd do differently, I should say I'd want a true randomized experiment on this exact question if it were feasible, which is exactly what the follow-on A/B test approximated.

---

**Log:**
- **Causal study technical deep-dive** — covariate balance check, placebo test, and triangulation. *Drafted, now placed on Appendix Slide 2.*
- **Sample love plot** — built and shown for reference (7 illustrative features, before/after matching SMD dumbbell chart, blue two-shade convention). *Placed on Appendix Slide 2, under the Covariate Balance Check bullet.*

---

## Raw Story Notes (reference only — not yet turned into a slide)

Kept here so it isn't lost before we get to the right slide for it. This is the user's own framing, in their words, for the "problem, part 2" and "challenges" beats:

- Mailchimp had a huge customer base on the email plan
- When SMS launched, the belief was that email plan customers would adopt SMS on their own
- After 2 years, that assumption hadn't fully played out
  - To grow the business, we needed to bring in new customers too, not just convert existing email customers
- The best place to reach new customers was right after they complete onboarding
- But every other product team also wants placement on that screen
  - The screen right after onboarding is the page with the highest engagement in the product
- That's why proving SMS increases overall user spend, not just SMS spend, was necessary to position SMS in Mailchimp's strategy

**Where this likely belongs once we get there:**
- The "email customers didn't organically adopt SMS" + "onboarding is the best moment to reach new customers" piece → **Problem, Part 2** (bridge slide between the causal study and the experiment)
- The "every team wants that screen, it's the highest-engagement page" piece → **Challenges** (this is what made the causal study's proof necessary — you needed a defensible number to win that placement)
