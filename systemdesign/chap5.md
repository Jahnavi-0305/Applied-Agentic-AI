# Handling Missing Values 

3 Types of Missing Values

MNAR (Missing Not At Random) = missing BECAUSE of the value itself → e.g., high earners hide income

MAR (Missing At Random) = missing because of ANOTHER variable → e.g., gender A skips age field

MCAR (Missing Completely At Random) = no pattern, just forgot → rarest type

2 Ways to Handle:

Deletion:

Column deletion = remove the whole column if >50% values missing

Row deletion = remove the sample if MCAR and <0.1% of data

❌ Risk = lose important info, create bias (removing gender A rows = model can't predict gender A)

Imputation (fill the gap):

Fill with default (empty string, "unknown")

Fill with mean / median / mode

❌ Risk = never fill with a possible real value (e.g., filling missing "number of children" with 0 — model can't tell zero kids vs missing data)

❌ Risk = can cause data leakage if done wrong

The Golden Rule:

"There is no perfect way. Deletion = lose info + bias. Imputation = inject bias + noise. Always investigate WHY values are missing before deciding."

# Encoding Categorical Features 

The Problem:

Categories in production are NOT static — new vendors, new users, new brands appear constantly

Model crashes or ignores them if it never saw them during training

3 Solutions (worst → best):

Approach	Problem
Assign each category a number	Crashes on new categories
"Unknown" bucket for rare ones	Model never learned "unknown" = useless recommendations
Hashing trick ✅	Fixed hash space handles ANY new category automatically
Hashing Trick — How it works:

Hash function converts ANY category name → index number (0 to 262,144)

New categories get hashed automatically — model never crashes

⚠️ Collision risk = two categories get same index — but research shows even 50% collision = less than 0.5% performance loss

Fix = choose large enough hash space

# Feature Crossing 

What: Combine 2+ features → create 1 new feature to capture nonlinear relationships

Example: marital_status × num_children → new feature marital_x_children

When to use:

Linear models (logistic regression, linear regression) — can't learn nonlinear on their own

Tree-based models — feature crossing helps them too

Neural networks — less critical but speeds up learning

⚠️ Risks:

Feature space explodes — 100 values × 100 values = 10,000 combinations

More features = higher overfitting risk

Need a LOT of data to cover all combinations

# Data Leakage

What: Future or test data accidentally leaks into training → model looks great in evaluation, fails in production

5 Common Causes:

Cause	Simple Explanation	Fix
Cause	Simple Explanation	Fix
Random split on time-series data	Future prices leak into training	Split by TIME not randomly
Scaling before splitting	Test set mean/variance leaks into training	Split FIRST, then scale using train stats only
Filling missing values before splitting	Test set mean leaks into training	Split FIRST, fill using train stats only
Duplicate data	Same sample in both train and test	Remove duplicates BEFORE splitting
Correlated samples split apart	Two scans of same patient in train + test	Understand data generation before splitting
Golden Rule:

"Split your data FIRST. Do everything else (scaling, filling missing values, feature engineering) AFTER. Never let your model see test data statistics during training."

# Business Metrics > ML Metrics

Companies don't care about accuracy — they care about revenue, cost saved, fraud prevented

Always tie your ML work to a business number

Example: Netflix measures "did the user watch the recommendation?" not "was the model accurate?"

ML is one component, not the whole system

Real systems = ML + logic rules + human review + other processes

If something fails, you can't always blame the ML model

ML returns take time — they compound over years, not overnight


# Reliability, Scalability, Maintainability, Adaptability
Reliability

System works correctly even when hardware fails, software bugs happen, or humans make mistakes

ML systems fail silently — no crash, no error, just wrong predictions nobody notices

This is why monitoring matters — you need to catch silent failures yourself

Scalability

System grows in 3 ways: model complexity, traffic volume, number of models

Scaling = not just adding more machines (resource scaling) but also managing more models (artifact management)

Use autoscaling — automatically add/remove machines based on load

100 models need automated monitoring and retraining — you can't do it manually

Maintainability

Different people work on ML systems — engineers, DevOps, domain experts

Code, data, and models must all be versioned and documented

Anyone should be able to reproduce a model even if the original author left

Adaptability

Data changes over time — your system must be able to update without going down

Build systems that can improve themselves without service interruption

# Iterative Process
The ML process is a loop, not a straight line

You don't just collect data → train → deploy → done

Real flow: scope → data → train → evaluate → fix → retrain → deploy → monitor → repeat forever

After deployment, the loop continues — models go stale, business goals change, data drifts

The 4 main stages (remember these)

Project Scoping — define the goal, metrics, constraints, who's involved

Data Engineering — collect, clean, label, store data

ML Model Development — train, evaluate, fix errors, retrain

Deployment — ship to production, monitor, update

Why models go stale

Data from 2 months ago ≠ data from today

Business goals change — optimizing impressions vs click-through rate = completely different model

Always plan for retraining from day one

# Objective function

What is an objective function? (simple)

It's just the question: "what is the model trying to get better at?"

Usually it's minimizing mistakes — the model makes a prediction, compares it to the right answer, and tries to do better next time

Common ones: cross-entropy (for classification), RMSE (for numbers)

Decoupling objectives (the important concept)

Real systems usually have more than one goal and those goals can conflict

Example: YouTube wants engagement AND wants to avoid showing harmful content — these two goals fight each other

Solution: train separate models for each goal, then combine their scores at the end

This is cleaner than forcing one model to do everything

The one rule to remember

When two objectives conflict, separate them into two models, combine results later. Don't force one model to do both.

# Batch vs Online vs Streaming 
Three modes of prediction

Batch prediction

Model runs on a schedule (hourly, daily)

Saves results in a DB / table, app reads later

Example: Netflix precomputes recommendations every few hours

Online prediction

Model runs when the user asks

Request comes in → model predicts → response goes back immediately

Example: Google Translate, chatbots, live invoice decision

Streaming prediction

Online prediction that also uses live streaming data

Combines precomputed features (batch) + live features (stream)

Example: DoorDash delivery ETA using restaurant history + current order load

Key points to remember

Batch = precomputed, good for heavy, slow-changing stuff

Online = on-demand, good for interactive features

Streaming = online + live streaming data, good for real-time estimates

Real systems usually use both batch and online together


# From Batch to Online Prediction 
Why batch prediction exists

Online prediction (predict when the request comes) can be too slow or too expensive for heavy models.

Batch prediction precomputes results on a schedule (hourly/daily) and stores them in a DB or cache.

When a user needs a result, the system just reads it instead of recomputing it — much faster.

Pros of batch prediction

Good for lots of predictions at once (millions of users, products, items).

Great when results don’t need to be perfectly up-to-the-second.

Can use distributed/batch tools (Spark, etc.) to process huge volumes efficiently.

Cons of batch prediction

Not responsive to rapid user changes (e.g., user suddenly starts liking comedy, but recommendations won’t update until next batch).

You must know in advance which queries to generate predictions for (works for users/items you already know; doesn’t work for totally new text, queries, etc.).

Why companies move from batch → online

As hardware and optimization techniques improve, online prediction gets cheaper and faster.

Online prediction can respond to user behavior immediately.

Modern systems build near real-time pipelines: incoming data → streaming features → model → live prediction.

Key idea

Batch prediction is a workaround when online prediction is too slow or expensive. As systems improve, teams try to replace batch with online or streaming prediction wherever possible.



