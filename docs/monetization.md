# Monetization (draft)

Living document for revenue hypotheses. Update as product and markets clarify.

## Principles

- **Trust first:** history content competes on perceived accuracy and tone; aggressive ads can undermine the brand.
- **Cost awareness:** editorial or semi-automated ingestion has ongoing labor or tooling cost; image rights may dominate margin if not using public-domain or licensed bundles.

## Ad strategy (draft)

**Chosen format: rewarded video ads** — the user opts in to watch an ad in exchange for something the app can gate lightly (e.g. bonus daily pack, one extra “deep” story, or unlock of a feature for 24h). This project **will use rewarded ads**, capped at **one opportunity per user per day** to protect calm UX, trust, and time-on-app quality.

| Concept | Indicative range (illustrative, not a guarantee) |
|--------|--------------------------------------------------|
| **Revenue per completed view** (net-like, varies by network/geo/season) | **¥5 – ¥20** per completed view |
| **CPM equivalent (back-of-envelope)** | **~¥700 – ¥3,000+** (roughly **$5 – $20+** depending on USD/JPY) |

**Why rewarded ads (for this product)**

- **Higher completion and quality:** the user **chooses** to watch, which typically yields strong completion and fewer accidental impressions than interstitials.
- **Fits a “one per day” cap:** a single, explicit moment per day is easier to reason about than many small banners; pair with a clear in-app value exchange so it feels fair, not greedy.

**Revenue in plain terms**

- Ad networks pay per **valid completed view** (or per thousand such impressions, hence CPM). Your **expected daily ad revenue** is approximately:

  `daily ad revenue ≈ (DAU) × (share of users who start the ad) × (completion rate) × (revenue per completed view) × (1 – platform & network take rate)`

- Example (numbers are **illustration only**): 10,000 DAU, 20% of users open the daily rewarded placement, 90% complete it, and the net effective payout averages **¥12** per completed view. Then: `10,000 × 0.2 × 0.9 × 12 ≈ ¥21,600/day` before tax, before payment thresholds, and before any ad-fill failures.

- **Price vs “CPM”:** “¥5 – ¥20 per view” is a **per-completion** unit; CPM in the table is a **rough conversion** to the industry’s “per 1,000 impressions” language so you can compare to network dashboards. Realized CPM moves with fill rate, eCPM, viewability, geography, and platform cut.

**Risks to monitor**

- Over-gating content erodes the same trust the product depends on; keep the reward **small but meaningful** and **transparent**.
- **Family / brand safety:** use network controls and blocklists; rewarded still needs policy on categories (gambling, etc.) for store compliance.
- **Frequency:** more than one per day is usually not worth the extra revenue if D7 or session length drops.

## Options under consideration

| Model | Upside | Risk |
|-------|--------|------|
| **Free + ads** | Low friction distribution | Ad networks and UX friction; family-unfriendly ads if not curated |
| **Free + tasteful ads + paid remove** | Offsets cost while a subscription proves value | Must ship a premium worth paying for (offline, no ads, deeper archives) |
| **Subscription** | Predictable revenue; aligns with “calm” product | Need clear premium value (offline, themes, deeper archives, no ads) |
| **One-time unlock** | Simple mental model | Harder to fund continuous content updates |
| **B2B / education** | Higher contract value | Longer sales cycle; different product surface |

## Open questions

- Primary geography: Japan-only launch vs global “on this day” with localized packs?
- Whether **image-heavy** experiences require a paid tier to cover licensing.
- Whether **ChatGPT-assisted ingestion** stays internal only (recommended) vs any user-facing “AI explain” feature (separate cost and compliance path).

## Next steps

Align MVP with **rewarded once daily + a clear in-app value exchange**, then define **two metrics**: D7 retention and revenue per monthly active user (or revenue per DAU with completion funnel). Link experiments back to [product-strategy.md](product-strategy.md).
