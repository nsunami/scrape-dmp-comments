from dmpcomments import get_all_plans, get_comments_for_plan
import config

# Get all plans from the table
all_plans_df = get_all_plans(cookies=config.cookies, headers=config.headers)

# Only get plans using the EUR v4.5 template (takes ~5 minutes)
v45_plans = all_plans_df[
    all_plans_df["Template Sort by templates"] == "Data Management Plan v4.5"
]
v45_plans["comments"] = v45_plans["plan_id"].map(
    lambda plan_id: get_comments_for_plan(plan_id, config.cookies, config.headers)
)

# Save data
## Pickle
v45_plans.to_pickle("v45_plans.pkl")
## JSON
v45_plans.to_json("v45_plans.json", indent=2)
