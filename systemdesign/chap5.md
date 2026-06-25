# Handling Missing Values 

3 Types of Missing Values:

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



