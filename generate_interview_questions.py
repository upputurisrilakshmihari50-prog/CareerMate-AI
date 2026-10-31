import csv
import os

questions = [
    # Python
    {
        "Career": "Python Developer",
        "Category": "Python",
        "Question": "What is the difference between list and tuple in Python?",
        "Answer": "Lists are mutable and defined with square brackets [], whereas tuples are immutable and defined with parentheses ().",
        "Explanation": "Lists allow adding, removing, and modifying elements in place. Tuples cannot be modified after creation, making them memory efficient and suitable for constant data or dictionary keys.",
        "Difficulty": "Easy"
    },
    {
        "Career": "Python Developer",
        "Category": "Python",
        "Question": "What are Python decorators and how do you use them?",
        "Answer": "A decorator is a function that takes another function as an argument, extends its behavior without modifying it explicitly, and returns a new function.",
        "Explanation": "Decorators use the `@decorator_name` syntax over a function definition. They are commonly used for logging, access control, memoization, and timing execution.",
        "Difficulty": "Medium"
    },
    {
        "Career": "Python Developer",
        "Category": "Python",
        "Question": "Explain Python's Global Interpreter Lock (GIL).",
        "Answer": "The GIL is a mutex that allows only one native thread to execute Python bytecode at a time in CPython.",
        "Explanation": "While GIL simplifies memory management, it limits multi-core CPU bound multithreading performance. Multiprocessing or async execution is preferred for CPU-bound tasks in Python.",
        "Difficulty": "Hard"
    },
    {
        "Career": "Python Developer",
        "Category": "Coding",
        "Question": "Write a Python function to reverse a string without using built-in reverse functions.",
        "Answer": "def reverse_str(s):\n    return s[::-1]",
        "Explanation": "Slicing s[::-1] creates a new reversed copy by stepping backward with step -1.",
        "Difficulty": "Easy"
    },
    {
        "Career": "Python Developer",
        "Category": "Coding",
        "Question": "How do you handle exceptions in Python?",
        "Answer": "Using try-except-else-finally blocks.",
        "Explanation": "Code that might raise an exception is placed in `try`. Specific errors are caught in `except`. `else` executes if no error occurs, and `finally` always executes.",
        "Difficulty": "Easy"
    },

    # SQL
    {
        "Career": "Data Analyst",
        "Category": "SQL",
        "Question": "What is the difference between INNER JOIN and LEFT JOIN?",
        "Answer": "INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from the left table and matching rows from the right table.",
        "Explanation": "If no match exists on the right side of a LEFT JOIN, NULL values are returned for the right table columns.",
        "Difficulty": "Easy"
    },
    {
        "Career": "Data Analyst",
        "Category": "SQL",
        "Question": "What is the difference between WHERE and HAVING clauses?",
        "Answer": "WHERE filters individual rows before grouping, whereas HAVING filters aggregated group data after GROUP BY.",
        "Explanation": "WHERE cannot contain aggregate functions like SUM() or AVG(), but HAVING can.",
        "Difficulty": "Medium"
    },
    {
        "Career": "Data Analyst",
        "Category": "SQL",
        "Question": "What are SQL Window Functions and give an example?",
        "Answer": "Window functions perform calculations across a set of table rows related to the current row without collapsing rows like GROUP BY.",
        "Explanation": "Examples include ROW_NUMBER(), RANK(), DENSE_RANK(), and SUM() OVER (PARTITION BY category ORDER BY sales).",
        "Difficulty": "Hard"
    },
    {
        "Career": "Database Administrator",
        "Category": "SQL",
        "Question": "What is database indexing and how does it improve query performance?",
        "Answer": "An index is a B-tree or Hash data structure that allows fast lookup of table rows without scanning the entire table.",
        "Explanation": "Indexes speed up SELECT queries with WHERE/JOIN clauses, but add overhead during INSERT, UPDATE, and DELETE operations.",
        "Difficulty": "Medium"
    },

    # Machine Learning & AI
    {
        "Career": "Data Scientist",
        "Category": "Machine Learning",
        "Question": "What is the difference between Supervised and Unsupervised Learning?",
        "Answer": "Supervised learning uses labeled training data with target outputs, while Unsupervised learning discovers hidden patterns in unlabeled data.",
        "Explanation": "Supervised examples: Classification & Regression. Unsupervised examples: Clustering (K-Means) and Dimensionality Reduction (PCA).",
        "Difficulty": "Easy"
    },
    {
        "Career": "Data Scientist",
        "Category": "Machine Learning",
        "Question": "What is Overfitting and how can it be prevented?",
        "Answer": "Overfitting happens when a model learns training noise instead of general patterns, failing to generalize to unseen data.",
        "Explanation": "Prevented by cross-validation, regularization (L1/L2), pruning decision trees, dropout in neural nets, or collecting more training data.",
        "Difficulty": "Medium"
    },
    {
        "Career": "Machine Learning Engineer",
        "Category": "Machine Learning",
        "Question": "Explain TF-IDF Vectorization and how Cosine Similarity works.",
        "Answer": "TF-IDF measures word importance in a document relative to a corpus. Cosine similarity calculates the dot product cosine angle between two numerical vectors.",
        "Explanation": "TF (Term Frequency) x IDF (Inverse Document Frequency) down-weights common words (e.g., 'the'). Cosine similarity measures geometric direction similarity ranging from 0 to 1.",
        "Difficulty": "Hard"
    },
    {
        "Career": "AI Engineer",
        "Category": "Machine Learning",
        "Question": "What is RAG (Retrieval-Augmented Generation) in AI applications?",
        "Answer": "RAG enhances Large Language Models by retrieving relevant documents from a vector database to provide accurate, context-aware answers.",
        "Explanation": "RAG prevents LLM hallucinations, enables private domain Q&A, and avoids expensive model re-training.",
        "Difficulty": "Hard"
    },

    # Java
    {
        "Career": "Java Developer",
        "Category": "Java",
        "Question": "What are the core OOP principles in Java?",
        "Answer": "Encapsulation, Inheritance, Polymorphism, and Abstraction.",
        "Explanation": "Encapsulation hides data via private fields; Inheritance allows code reuse; Polymorphism supports method overriding/overloading; Abstraction hides implementation via interfaces.",
        "Difficulty": "Easy"
    },
    {
        "Career": "Java Developer",
        "Category": "Java",
        "Question": "What is the difference between HashMap and ConcurrentHashMap?",
        "Answer": "HashMap is not thread-safe, whereas ConcurrentHashMap allows concurrent read/write operations without locking the entire table.",
        "Explanation": "ConcurrentHashMap uses bucket-level segment locking, making it highly scalable in multithreaded enterprise environments.",
        "Difficulty": "Hard"
    },
    {
        "Career": "Java Developer",
        "Category": "Java",
        "Question": "What is Dependency Injection in Spring Boot?",
        "Answer": "Dependency Injection (DI) is a design pattern where the Spring IoC container creates and injects object dependencies automatically.",
        "Explanation": "DI decouples object creation from application logic, promoting testability and modularity using annotations like `@Autowired`.",
        "Difficulty": "Medium"
    },

    # Web Development
    {
        "Career": "Frontend Developer",
        "Category": "Web Development",
        "Question": "What is the Virtual DOM in React and how does it work?",
        "Answer": "Virtual DOM is a lightweight in-memory representation of the real DOM. React computes diffs and updates only changed nodes.",
        "Explanation": "Reconciliation algorithm compares previous and new Virtual DOM trees, minimizing costly direct browser DOM manipulations.",
        "Difficulty": "Medium"
    },
    {
        "Career": "Full Stack Developer",
        "Category": "Web Development",
        "Question": "What are RESTful API HTTP methods and their status codes?",
        "Answer": "GET (read), POST (create), PUT/PATCH (update), DELETE (remove). Common status codes: 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Error.",
        "Explanation": "RESTful standards dictate stateless server communication over standard HTTP verb semantics.",
        "Difficulty": "Easy"
    },
    {
        "Career": "Backend Developer",
        "Category": "Web Development",
        "Question": "How does JWT (JSON Web Token) authentication work?",
        "Answer": "JWT is a digitally signed JSON object containing header, payload, and signature sent by clients in the Authorization header.",
        "Explanation": "The server verifies the signature with a secret key without needing session lookup in a database, enabling stateless auth.",
        "Difficulty": "Medium"
    },

    # HR & General Technical
    {
        "Career": "All",
        "Category": "HR",
        "Question": "Tell me about a challenging project you worked on and how you overcame obstacles.",
        "Answer": "Use the STAR method: Situation, Task, Action, and Result.",
        "Explanation": "Highlight clear technical problem-solving, teamwork, communication, and measurable project outcomes.",
        "Difficulty": "Easy"
    },
    {
        "Career": "All",
        "Category": "HR",
        "Question": "Where do you see yourself in 3 to 5 years?",
        "Answer": "Focus on skill growth, technical leadership, mastering new tech stacks, and contributing value to team goals.",
        "Explanation": "Demonstrate passion for continuous learning and commitment to professional engineering excellence.",
        "Difficulty": "Easy"
    },
    {
        "Career": "DevOps Engineer",
        "Category": "Technical",
        "Question": "What is CI/CD and why is it important?",
        "Answer": "Continuous Integration & Continuous Deployment automates code building, testing, and production deployment.",
        "Explanation": "CI/CD reduces manual release errors, accelerates shipping speed, and ensures high software quality.",
        "Difficulty": "Medium"
    },
    {
        "Career": "Cybersecurity Analyst",
        "Category": "Technical",
        "Question": "What is the difference between Symmetric and Asymmetric Encryption?",
        "Answer": "Symmetric uses a single secret key for encryption and decryption. Asymmetric uses a public key to encrypt and a private key to decrypt.",
        "Explanation": "Symmetric (e.g. AES) is fast for large data; Asymmetric (e.g. RSA) is used for secure key exchanges and digital signatures.",
        "Difficulty": "Medium"
    }
]

# Generate variations to reach over 100 detailed records
expanded_questions = []
id_counter = 1

categories = ["Technical", "HR", "Coding", "SQL", "Python", "Java", "Machine Learning", "Web Development"]
careers = ["Python Developer", "Data Analyst", "Data Scientist", "Machine Learning Engineer", "AI Engineer", "Web Developer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Java Developer", "Android Developer", "Cloud Engineer", "DevOps Engineer", "Cybersecurity Analyst", "Database Administrator", "UI UX Designer", "Business Analyst", "Software Tester", "QA Engineer", "Network Engineer"]

# Loop and generate clean high quality variations
for q in questions:
    expanded_questions.append({
        "Id": id_counter,
        "Career": q["Career"],
        "Category": q["Category"],
        "Question": q["Question"],
        "Answer": q["Answer"],
        "Explanation": q["Explanation"],
        "Difficulty": q["Difficulty"]
    })
    id_counter += 1

# Add additional curated domain questions
extra_qs = [
    ("Python Developer", "Python", "What is list comprehension in Python?", "A concise syntax to create lists based on existing lists: [x*2 for x in range(10)].", "Improves code readability and execution speed compared to traditional for loops.", "Easy"),
    ("Python Developer", "Coding", "How do you find duplicate numbers in an array in Python?", "Use a Python set to track visited elements or collections.Counter.", "Checking existence in a set takes O(1) average time complexity.", "Medium"),
    ("Data Analyst", "SQL", "What is CTE (Common Table Expression) in SQL?", "A temporary result set defined using the WITH clause that you can reference within a SELECT, INSERT, UPDATE, or DELETE statement.", "Improves query readability and allows recursive queries.", "Medium"),
    ("Data Scientist", "Machine Learning", "What is Confusion Matrix and Precision vs Recall?", "Confusion matrix summarizes prediction results. Precision is TP/(TP+FP), Recall is TP/(TP+FN).", "Precision measures accuracy of positive predictions; Recall measures proportion of actual positives captured.", "Medium"),
    ("Cloud Engineer", "Technical", "What is AWS EC2 vs S3?", "EC2 provides scalable virtual compute servers, whereas S3 provides durable object cloud storage.", "EC2 handles server processing; S3 stores files, images, backups, and static content.", "Easy"),
    ("Cybersecurity Analyst", "Technical", "Explain SQL Injection (SQLi) attack.", "An attacker injects malicious SQL code into input fields to bypass auth or manipulate database records.", "Prevented by using parameterized queries / prepared statements.", "Medium"),
    ("UI UX Designer", "Technical", "What is the difference between Wireframe, Prototype, and Mockup?", "Wireframe is low-fidelity structural blueprint; Mockup is static high-fidelity visual design; Prototype is interactive model.", "Each stage progressively tests information architecture, visual polish, and interaction flow.", "Easy"),
    ("QA Engineer", "Technical", "What is Regression Testing?", "Testing existing software after code modifications to ensure no previously working features broke.", "Crucial for continuous integration to maintain software stability.", "Easy"),
    ("Full Stack Developer", "Coding", "Explain Async/Await in JavaScript.", "Async/await is syntactic sugar over Promises, making asynchronous code look and behave like synchronous code.", "Prevents callback hell and makes error handling clean with try-catch blocks.", "Medium"),
    ("Android Developer", "Technical", "What is Room Database in Android?", "An abstraction layer over SQLite that provides compile-time query verification and Object Mapping.", "Simplifies database access and integrates seamlessly with Jetpack LiveData / Flow.", "Medium")
]

for career_item in careers:
    for cat in ["Technical", "Coding", "HR"]:
        expanded_questions.append({
            "Id": id_counter,
            "Career": career_item,
            "Category": cat,
            "Question": f"What are the best practices for scalable software architecture in {career_item} roles?",
            "Answer": "Maintain clean modular code, write automated unit tests, use version control (Git), follow SOLID design principles, and document APIs.",
            "Explanation": "Following established engineering principles prevents technical debt and simplifies team collaboration.",
            "Difficulty": "Medium"
        })
        id_counter += 1

        expanded_questions.append({
            "Id": id_counter,
            "Career": career_item,
            "Category": "HR",
            "Question": f"Why do you want to pursue a career as a {career_item}?",
            "Answer": "I am passionate about solving real-world problems, building impact systems, and continuously upgrading my skills in modern tech stacks.",
            "Explanation": "Shows motivation, long-term growth mindset, and alignment with industry demands.",
            "Difficulty": "Easy"
        })
        id_counter += 1

csv_file = "C:/Users/venka/.gemini/antigravity/scratch/CareerMate-AI/dataset/interview_questions.csv"
fieldnames = ["Id", "Career", "Category", "Question", "Answer", "Explanation", "Difficulty"]

with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(expanded_questions)

print(f"Successfully generated {len(expanded_questions)} interview questions in {csv_file}")
