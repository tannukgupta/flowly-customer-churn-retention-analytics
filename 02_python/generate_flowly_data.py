"""
Flowly Customer Churn & Retention Analytics
--------------------------------------------
Purpose:
    Generate a reproducible, simulated SaaS customer dataset for a portfolio project.

Important:
    This is SIMULATED data. It is not extracted from a real company's customer records.

How to reproduce:
    python generate_flowly_data.py

The script uses a fixed random seed so the same code produces the same dataset.
"""

from __future__ import annotations

import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

# =========================
# Configuration
# =========================

SEED = 20260918
N_CUSTOMERS = 10_000

START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 6, 30)

OUTPUT_DIR = Path("flowly_churn_project")

rng = random.Random(SEED)


# =========================
# Helper functions
# =========================

def weighted_choice(items, weights):
    """Pick one category using business-style weighted probabilities."""
    return rng.choices(items, weights=weights, k=1)[0]


def clamp(value, minimum, maximum):
    """Keep a numeric value inside a defined range."""
    return max(minimum, min(maximum, value))


def sigmoid(x):
    """Convert a score into a probability between 0 and 1."""
    return 1 / (1 + math.exp(-x))


def month_start(d):
    return d.replace(day=1)


def days_between(start, end):
    return max(0, (end - start).days)


def write_csv(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


# =========================
# Business dimensions
# =========================

COUNTRIES = ["India", "United States", "United Kingdom", "Canada", "Australia", "Singapore"]
COUNTRY_WEIGHTS = [0.46, 0.20, 0.11, 0.08, 0.08, 0.07]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
AGE_WEIGHTS = [0.12, 0.35, 0.28, 0.17, 0.08]

COMPANY_SIZES = ["Individual", "Small", "Medium", "Large"]
COMPANY_SIZE_WEIGHTS = [0.44, 0.28, 0.18, 0.10]

ACQUISITION_CHANNELS = ["Organic", "Referral", "Google Ads", "Meta Ads", "Partner", "Email"]
ACQUISITION_WEIGHTS = [0.28, 0.18, 0.18, 0.16, 0.12, 0.08]

CUSTOMER_TYPES = ["Individual", "Business"]
CUSTOMER_TYPE_WEIGHTS = [0.58, 0.42]

PLANS = ["Free", "Basic", "Professional", "Business"]
PLAN_WEIGHTS = [0.16, 0.36, 0.34, 0.14]
PLAN_PRICE = {
    "Free": 0.0,
    "Basic": 19.0,
    "Professional": 49.0,
    "Business": 99.0,
}

BILLING_CYCLES = ["Monthly", "Annual"]
BILLING_WEIGHTS = [0.74, 0.26]

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "PayPal"]
PAYMENT_WEIGHTS = [0.29, 0.22, 0.23, 0.14, 0.12]

ISSUE_TYPES = ["Technical", "Billing", "Account", "Feature Request", "Performance", "Other"]
ISSUE_WEIGHTS = [0.25, 0.18, 0.14, 0.12, 0.17, 0.14]

MARKETING_CHANNELS = ["Email", "Google Ads", "Meta Ads", "Referral", "Partner", "In-App"]
MARKETING_WEIGHTS = [0.26, 0.19, 0.18, 0.15, 0.12, 0.10]

INTERACTION_TYPES = ["Open", "Click", "View", "Conversion"]
INTERACTION_WEIGHTS = [0.38, 0.29, 0.24, 0.09]

CHURN_REASONS = [
    "Low Usage",
    "Too Expensive",
    "Poor Experience",
    "Missing Features",
    "Competitor",
    "Support Issues",
    "Payment Failure",
    "Other",
]

VOLUNTARY_REASON_WEIGHTS = [0.20, 0.16, 0.17, 0.13, 0.12, 0.10, 0.00, 0.12]
INVOLUNTARY_REASON_WEIGHTS = [0.00, 0.00, 0.00, 0.00, 0.02, 0.03, 0.90, 0.05]


# =========================
# 1. Customers
# =========================

customers = []
profiles = {}

date_span = days_between(START_DATE, END_DATE) - 45

for number in range(1, N_CUSTOMERS + 1):
    customer_id = f"C{number:05d}"

    signup_date = START_DATE + timedelta(days=rng.randint(0, date_span))

    age_group = weighted_choice(AGE_GROUPS, AGE_WEIGHTS)
    country = weighted_choice(COUNTRIES, COUNTRY_WEIGHTS)
    company_size = weighted_choice(COMPANY_SIZES, COMPANY_SIZE_WEIGHTS)
    acquisition_channel = weighted_choice(
        ACQUISITION_CHANNELS, ACQUISITION_WEIGHTS
    )
    customer_type = weighted_choice(CUSTOMER_TYPES, CUSTOMER_TYPE_WEIGHTS)

    # Hidden behavioural parameters used only to create realistic relationships.
    price_sensitivity = rng.betavariate(2.2, 4.5)
    engagement_propensity = rng.betavariate(2.6, 2.8)
    support_proneness = rng.betavariate(1.7, 5.0)
    payment_risk = rng.betavariate(1.6, 7.0)

    customers.append([
        customer_id,
        signup_date.isoformat(),
        age_group,
        country,
        company_size,
        acquisition_channel,
        customer_type,
    ])

    profiles[customer_id] = {
        "signup_date": signup_date,
        "age_group": age_group,
        "country": country,
        "company_size": company_size,
        "acquisition_channel": acquisition_channel,
        "customer_type": customer_type,
        "price_sensitivity": price_sensitivity,
        "engagement_propensity": engagement_propensity,
        "support_proneness": support_proneness,
        "payment_risk": payment_risk,
    }


# =========================
# 2. Subscriptions + churn
# =========================

subscriptions = []

for number, customer in enumerate(customers, start=1):
    (
        customer_id,
        signup_date_text,
        age_group,
        country,
        company_size,
        acquisition_channel,
        customer_type,
    ) = customer

    profile = profiles[customer_id]

    plan = weighted_choice(PLANS, PLAN_WEIGHTS)

    # Business customers are less likely to be on the free plan.
    if customer_type == "Business" and plan == "Free":
        plan = weighted_choice(
            ["Basic", "Professional", "Business"],
            [0.28, 0.50, 0.22],
        )

    billing_cycle = weighted_choice(BILLING_CYCLES, BILLING_WEIGHTS)
    base_price = PLAN_PRICE[plan]

    # Annual customers receive a simulated discount.
    monthly_price = base_price
    if billing_cycle == "Annual" and base_price > 0:
        monthly_price = round(base_price * 0.85, 2)

    signup_date = profile["signup_date"]
    tenure_days = days_between(signup_date, END_DATE)
    tenure_months = max(1, tenure_days // 30)

    # -------------------------
    # Churn-generation logic
    # -------------------------
    # These coefficients are design assumptions for the simulated business.
    # They create analyzable patterns; they are NOT causal claims about real users.

    churn_score = (
        -2.15
        + 0.70 * profile["price_sensitivity"]
        + (0.55 if plan == "Free" else 0)
        + (0.40 if plan == "Basic" else 0)
        + (0.30 if billing_cycle == "Monthly" else 0)
        + (0.45 if tenure_months <= 6 else 0)
        - 0.65 * profile["engagement_propensity"]
        + 0.35 * profile["payment_risk"]
        + 0.18 * profile["support_proneness"]
        + (0.12 if acquisition_channel in ["Meta Ads", "Google Ads"] else 0)
    )

    churn_probability = clamp(sigmoid(churn_score), 0.03, 0.60)
    churned = rng.random() < churn_probability

    churn_date = None
    status = "Active"

    if churned:
        latest = min(
            END_DATE,
            signup_date + timedelta(days=max(30, min(420, tenure_days))),
        )
        earliest = signup_date + timedelta(days=21)

        if latest > earliest:
            churn_date = earliest + timedelta(
                days=rng.randint(0, days_between(earliest, latest))
            )
            status = "Cancelled"

    subscriptions.append([
        f"S{number:05d}",
        customer_id,
        plan,
        signup_date.isoformat(),
        churn_date.isoformat() if churn_date else "",
        billing_cycle,
        round(monthly_price, 2),
        status,
    ])

    profile["plan"] = plan
    profile["billing_cycle"] = billing_cycle
    profile["monthly_price"] = monthly_price
    profile["churned"] = churned
    profile["churn_date"] = churn_date


# =========================
# 3. Transactions
# =========================

transactions = []
transaction_number = 1

for customer_id, profile in profiles.items():
    price = profile["monthly_price"]
    signup_date = profile["signup_date"]
    stop_date = profile["churn_date"] or END_DATE

    if price == 0:
        # Some free users generate small add-on purchases.
        if rng.random() < 0.35:
            for _ in range(rng.randint(1, 3)):
                transaction_date = signup_date + timedelta(
                    days=rng.randint(0, days_between(signup_date, stop_date))
                )
                amount = round(
                    weighted_choice([5, 9, 12], [0.55, 0.30, 0.15]), 2
                )

                transactions.append([
                    f"T{transaction_number:07d}",
                    customer_id,
                    transaction_date.isoformat(),
                    amount,
                    weighted_choice(PAYMENT_METHODS, PAYMENT_WEIGHTS),
                    "Successful",
                ])
                transaction_number += 1

        continue

    current_date = month_start(signup_date)
    month_number = 0

    while current_date <= stop_date:
        if profile["billing_cycle"] == "Annual":
            if month_number % 12 == 0:
                amount = round(price * 12, 2)
                failed = rng.random() < (
                    0.03 + 0.12 * profile["payment_risk"]
                )
                transaction_status = "Failed" if failed else "Successful"

                transaction_date = current_date + timedelta(days=rng.randint(0, 5))

                transactions.append([
                    f"T{transaction_number:07d}",
                    customer_id,
                    transaction_date.isoformat(),
                    amount,
                    weighted_choice(PAYMENT_METHODS, PAYMENT_WEIGHTS),
                    transaction_status,
                ])
                transaction_number += 1
        else:
            amount = round(price, 2)
            failed = rng.random() < (
                0.025 + 0.11 * profile["payment_risk"]
            )
            transaction_status = "Failed" if failed else "Successful"

            transaction_date = current_date + timedelta(days=rng.randint(0, 5))

            transactions.append([
                f"T{transaction_number:07d}",
                customer_id,
                transaction_date.isoformat(),
                amount,
                weighted_choice(PAYMENT_METHODS, PAYMENT_WEIGHTS),
                transaction_status,
            ])
            transaction_number += 1

        month_number += 1

        # Move to the next month without requiring external libraries.
        current_date += timedelta(days=31)
        current_date = current_date.replace(day=1)


# =========================
# 4. Customer activity
# =========================

activities = []
activity_number = 1

for customer_id, profile in profiles.items():
    signup_date = profile["signup_date"]
    stop_date = profile["churn_date"] or END_DATE

    history_days = days_between(signup_date, stop_date)

    target_activity_days = int(
        history_days * (
            0.18 + 0.35 * profile["engagement_propensity"]
        )
    )
    target_activity_days = clamp(
        target_activity_days,
        4,
        min(history_days + 1, 160),
    )

    sampled_days = sorted({
        rng.randint(0, max(0, history_days))
        for _ in range(target_activity_days)
    })

    # Churned customers experience a simulated engagement decline.
    decline_multiplier = (
        rng.uniform(0.45, 0.80)
        if profile["churned"]
        else 1.0
    )

    for day_offset in sampled_days:
        activity_date = signup_date + timedelta(days=day_offset)

        recency_ratio = day_offset / max(1, history_days)
        multiplier = (
            decline_multiplier
            if profile["churned"] and recency_ratio > 0.65
            else 1.0
        )

        sessions = max(
            1,
            int(
                round(
                    rng.gauss(
                        2.5 + 5 * profile["engagement_propensity"],
                        1.8,
                    )
                )
            ),
        )
        sessions = int(clamp(sessions * multiplier, 1, 15))

        session_minutes = int(
            clamp(
                rng.gauss(
                    22 + 20 * profile["engagement_propensity"],
                    12,
                ),
                5,
                180,
            )
        )

        projects_created = int(
            clamp(
                rng.gauss(
                    0.4 + 1.5 * profile["engagement_propensity"],
                    0.8,
                ),
                0,
                10,
            )
        )

        files_uploaded = int(
            clamp(
                rng.gauss(
                    1.5 + 4.0 * profile["engagement_propensity"],
                    2,
                ),
                0,
                25,
            )
        )

        features_used = int(
            clamp(
                rng.gauss(
                    2.0 + 3.0 * profile["engagement_propensity"],
                    1.5,
                ),
                1,
                8,
            )
        )

        activities.append([
            f"A{activity_number:08d}",
            customer_id,
            activity_date.isoformat(),
            sessions,
            session_minutes,
            projects_created,
            files_uploaded,
            features_used,
            1,
        ])
        activity_number += 1


# =========================
# 5. Support tickets
# =========================

support_tickets = []
ticket_number = 1

for customer_id, profile in profiles.items():
    signup_date = profile["signup_date"]
    stop_date = profile["churn_date"] or END_DATE

    ticket_count = int(
        round(
            profile["support_proneness"] * 7
            + rng.random() * 2
        )
    )

    if profile["churned"]:
        ticket_count += rng.randint(0, 4)

    for _ in range(ticket_count):
        ticket_date = signup_date + timedelta(
            days=rng.randint(0, days_between(signup_date, stop_date))
        )

        issue_type = weighted_choice(ISSUE_TYPES, ISSUE_WEIGHTS)

        poor_ticket = (
            rng.random()
            < (0.28 + 0.35 * profile["support_proneness"])
        )

        satisfaction_score = int(
            clamp(
                round(
                    rng.gauss(
                        2.5 if poor_ticket else 4.1,
                        0.9,
                    )
                ),
                1,
                5,
            )
        )

        resolution_hours = int(
            clamp(
                rng.gauss(
                    16 if poor_ticket else 8,
                    7,
                ),
                1,
                72,
            )
        )

        resolved = (
            "No"
            if poor_ticket and rng.random() < 0.18
            else "Yes"
        )

        support_tickets.append([
            f"ST{ticket_number:07d}",
            customer_id,
            ticket_date.isoformat(),
            issue_type,
            resolution_hours,
            satisfaction_score,
            resolved,
        ])
        ticket_number += 1


# =========================
# 6. Marketing interactions
# =========================

marketing_interactions = []
interaction_number = 1

campaign_ids = [f"CAM{number:03d}" for number in range(1, 16)]

for customer_id, profile in profiles.items():
    interaction_count = rng.randint(1, 8)

    for _ in range(interaction_count):
        interaction_date = profile["signup_date"] - timedelta(
            days=rng.randint(0, 30)
        )

        if interaction_date < START_DATE:
            interaction_date = START_DATE

        channel = weighted_choice(
            MARKETING_CHANNELS,
            MARKETING_WEIGHTS,
        )

        interaction_type = weighted_choice(
            INTERACTION_TYPES,
            INTERACTION_WEIGHTS,
        )

        # More engaged customers are somewhat more likely to click/convert.
        if rng.random() < profile["engagement_propensity"] * 0.35:
            interaction_type = weighted_choice(
                ["Click", "Conversion", "Open"],
                [0.45, 0.20, 0.35],
            )

        marketing_interactions.append([
            f"MI{interaction_number:07d}",
            customer_id,
            rng.choice(campaign_ids),
            channel,
            interaction_date.isoformat(),
            interaction_type,
        ])
        interaction_number += 1


# =========================
# 7. Churn events
# =========================

churn_events = []
churn_number = 1

for customer_id, profile in profiles.items():
    if not profile["churned"]:
        continue

    involuntary = (
        profile["payment_risk"] > 0.74
        and rng.random() < 0.55
    )

    churn_type = "Involuntary" if involuntary else "Voluntary"

    if involuntary:
        churn_reason = weighted_choice(
            CHURN_REASONS,
            INVOLUNTARY_REASON_WEIGHTS,
        )
    else:
        churn_reason = weighted_choice(
            CHURN_REASONS,
            VOLUNTARY_REASON_WEIGHTS,
        )

    churn_events.append([
        f"CE{churn_number:06d}",
        customer_id,
        profile["churn_date"].isoformat(),
        churn_reason,
        churn_type,
    ])
    churn_number += 1


# =========================
# 8. Intentional raw-data issues
# =========================
# These issues are deliberately inserted to create a realistic cleaning stage.
# They should NOT be called "errors in the business"—they are training artifacts.

for row in rng.sample(customers, 18):
    row[3] = ""  # Missing country

for row in rng.sample(activities, 25):
    duplicate = row.copy()
    duplicate[0] = f"A{activity_number:08d}"
    activities.append(duplicate)
    activity_number += 1

for row in rng.sample(support_tickets, min(20, len(support_tickets))):
    row[5] = ""  # Missing satisfaction score


# =========================
# 9. Write files
# =========================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

write_csv(
    OUTPUT_DIR / "customers.csv",
    [
        "customer_id",
        "signup_date",
        "age_group",
        "country",
        "company_size",
        "acquisition_channel",
        "customer_type",
    ],
    customers,
)

write_csv(
    OUTPUT_DIR / "subscriptions.csv",
    [
        "subscription_id",
        "customer_id",
        "plan",
        "start_date",
        "end_date",
        "billing_cycle",
        "monthly_price",
        "status",
    ],
    subscriptions,
)

write_csv(
    OUTPUT_DIR / "transactions.csv",
    [
        "transaction_id",
        "customer_id",
        "transaction_date",
        "amount",
        "payment_method",
        "transaction_status",
    ],
    transactions,
)

write_csv(
    OUTPUT_DIR / "customer_activity.csv",
    [
        "activity_id",
        "customer_id",
        "activity_date",
        "sessions",
        "session_minutes",
        "projects_created",
        "files_uploaded",
        "features_used",
        "active_days",
    ],
    activities,
)

write_csv(
    OUTPUT_DIR / "support_tickets.csv",
    [
        "ticket_id",
        "customer_id",
        "ticket_date",
        "issue_type",
        "resolution_hours",
        "satisfaction_score",
        "resolved",
    ],
    support_tickets,
)

write_csv(
    OUTPUT_DIR / "marketing_interactions.csv",
    [
        "interaction_id",
        "customer_id",
        "campaign_id",
        "channel",
        "interaction_date",
        "interaction_type",
    ],
    marketing_interactions,
)

write_csv(
    OUTPUT_DIR / "churn_events.csv",
    [
        "churn_id",
        "customer_id",
        "churn_date",
        "churn_reason",
        "churn_type",
    ],
    churn_events,
)

# Expected outputs for a deterministic run.
manifest = {
    "project": "Flowly Customer Churn & Retention Analytics",
    "data_type": "Simulated business data",
    "seed": SEED,
    "customers": len(customers),
    "subscriptions": len(subscriptions),
    "transactions": len(transactions),
    "customer_activity": len(activities),
    "support_tickets": len(support_tickets),
    "marketing_interactions": len(marketing_interactions),
    "churn_events": len(churn_events),
    "churn_rate": round(len(churn_events) / len(customers), 4),
    "date_range": {
        "start": START_DATE.isoformat(),
        "end": END_DATE.isoformat(),
    },
}

with (OUTPUT_DIR / "generation_manifest.json").open("w", encoding="utf-8") as file:
    import json
    json.dump(manifest, file, indent=2)

print("Flowly dataset generated successfully.")
print(f"Output directory: {OUTPUT_DIR.resolve()}")
print(f"Random seed: {SEED}")
print()
for key in [
    "customers",
    "subscriptions",
    "transactions",
    "customer_activity",
    "support_tickets",
    "marketing_interactions",
    "churn_events",
]:
    print(f"{key:24s}: {manifest[key]:,}")

