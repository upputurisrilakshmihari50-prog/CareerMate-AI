
import re

from recommendation import (
    get_career_recommendations,
    get_internship_recommendations,
    analyze_skill_gap,
    generate_learning_roadmap,
)
from database import save_chat_message


def process_chat_message(
    user_message,
    user_id=1,
    user_skills="Python, SQL",
):
    msg = user_message.lower().strip()
    skills = [s.strip() for s in user_skills.split(",") if s.strip()]

    save_chat_message(user_id, "user", user_message)

    def respond(reply):
        save_chat_message(user_id, "assistant", reply)
        return reply

    # 1. Greetings: match complete words
    if re.search(r"\b(hi|hello|hey|greetings)\b", msg) or msg in {
        "good morning", "good afternoon", "good evening"
    }:
        return respond(
            "Hello! 👋 Welcome to CareerMate AI.\n\n"
            "I can help with Python, Java, SQL, career options, "
            "internships, skill gap analysis, learning roadmaps, "
            "resumes, and interview preparation.\n\n"
            "What would you like to learn today?"
        )

    if any(x in msg for x in ["who are you", "what can you do"]):
        return respond(
            "I'm CareerMate AI, your career guidance assistant. "
            "I help students explore technical careers, identify "
            "skills to learn, prepare for interviews, and plan roadmaps."
        )

    # 2. Technical topic explanations
    topics = {
        "python": (
            "Python is a high-level programming language known for "
            "its readable syntax. It is used in automation, web "
            "development, data analysis, and machine learning."
        ),
        "java": (
            "Java is an object-oriented programming language. "
            "It is used in backend development, enterprise software, "
            "and many Android-related applications."
        ),
        "sql": (
            "SQL stands for Structured Query Language. It is used "
            "to create, read, update, and delete data in relational "
            "databases."
        ),
        "dbms": (
            "A DBMS (Database Management System) is software used "
            "to store, organize, retrieve, and manage data. "
            "Examples include MySQL, PostgreSQL, and Oracle Database."
        ),
        "oops": (
            "OOP stands for Object-Oriented Programming. Its four "
            "common principles are encapsulation, inheritance, "
            "polymorphism, and abstraction."
        ),
        "html": (
            "HTML stands for HyperText Markup Language. It defines "
            "the structure of web pages using elements such as "
            "headings, paragraphs, links, and forms."
        ),
        "css": (
            "CSS stands for Cascading Style Sheets. It controls the "
            "appearance of web pages, including colors, layouts, "
            "spacing, and fonts."
        ),
    }

    topic_patterns = {
        "python": r"\bpython\b",
        "java": r"\bjava\b",
        "sql": r"\bsql\b",
        "dbms": r"\bdbms\b|database management system",
        "oops": r"\boops\b|object[- ]oriented programming",
        "html": r"\bhtml\b",
        "css": r"\bcss\b",
    }

    # Answer definitions/explanations, not career recommendations.
    explanation_words = (
        "what is", "what are", "explain", "define",
        "meaning of", "tell me about"
    )

    if any(word in msg for word in explanation_words):
        for topic, pattern in topic_patterns.items():
            if re.search(pattern, msg):
                return respond(topics[topic])

    # 3. Learning roadmap
    roadmap_words = (
        "roadmap", "learning path", "how to become",
        "steps to become", "guide me to become"
    )

    if any(word in msg for word in roadmap_words):
        roles = [
            "machine learning engineer", "data scientist",
            "data analyst", "python developer", "java developer",
            "full stack developer", "web developer",
            "android developer", "cloud engineer",
            "devops engineer", "cybersecurity analyst",
        ]

        target = next(
            (role.title() for role in roles if role in msg),
            None,
        )

        if not target:
            return respond(
                "Which career roadmap do you need? For example, "
                "Python Developer, Data Analyst, Java Developer, "
                "or Full Stack Developer."
            )

        roadmap = generate_learning_roadmap(target)
        reply = f"### 🗺️ Roadmap: {roadmap['Career']}\n\n"

        for step in roadmap["Steps"]:
            reply += (
                f"**Step {step['Step_Number']}: {step['Title']}** "
                f"({step['Duration']})\n\n"
                f"{step['Description']}\n\n"
            )

        return respond(reply)

    # 4. Skill gap analysis
    if any(word in msg for word in [
        "skill gap", "skills needed", "skills should i learn",
        "skills to learn", "required skills",
    ]):
        roles = [
            "data scientist", "data analyst", "python developer",
            "java developer", "machine learning engineer",
            "web developer", "cloud engineer",
            "cybersecurity analyst",
        ]

        target = next(
            (role.title() for role in roles if role in msg),
            "Data Analyst",
        )

        gap = analyze_skill_gap(target, skills)

        reply = (
            f"### 🎯 Skill Gap Analysis: {gap['Target_Career']}\n\n"
            f"**Readiness:** {gap['Readiness_Percentage']}%\n\n"
            f"**Skills you have:** "
            f"{', '.join(gap['Matching_Skills']) or 'None matched yet'}\n\n"
            f"**Skills to learn:** "
            f"{', '.join(gap['Missing_Skills']) or 'Core skills covered'}\n\n"
            f"**Tools to learn:** {', '.join(gap['Tools_To_Learn'])}"
        )
        return respond(reply)

    # 5. Internship recommendations
    if "internship" in msg or "internships" in msg:
        roles = [
            "python", "java", "data analyst", "data scientist",
            "web developer", "full stack", "android", "devops", "cloud",
        ]

        preference = next(
            (role.title() for role in roles if role in msg),
            "All",
        )

        internships = get_internship_recommendations(
            career_target=preference
        )

        if not internships:
            return respond(
                "I couldn't find a matching internship profile "
                "in the current dataset. Try Python, Java, Data Analyst, "
                "or Web Developer."
            )

        reply = f"### 💼 Internship Suggestions: {preference}\n\n"

        for i, item in enumerate(internships[:4], 1):
            reply += (
                f"**{i}. {item['Internship_Title']}**\n\n"
                f"Industry: {item['Industry']}\n\n"
                f"Skills: {', '.join(item['Skills_Required'])}\n\n"
                f"Mode: {item['Mode']} | "
                f"Stipend: {item['Stipend_Range']}\n\n"
            )

        return respond(reply)

    # 6. Interview preparation
    if any(word in msg for word in [
        "interview", "mock interview", "interview questions",
    ]):
        return respond(
            "### 🎙️ Interview Preparation\n\n"
            "**Python:** What is the difference between a list and a tuple?\n\n"
            "**Answer:** A list is mutable, while a tuple is immutable.\n\n"
            "**SQL:** What is the difference between WHERE and HAVING?\n\n"
            "**Answer:** WHERE filters rows before grouping; HAVING "
            "filters groups after aggregation.\n\n"
            "**HR:** Tell me about yourself.\n\n"
            "**Tip:** Practise your introduction, core technical "
            "subjects, projects, and problem-solving questions."
        )

    # 7. Career recommendations only for career-related requests
    career_words = [
        "career", "job", "jobs", "suitable for me",
        "career options", "which field", "career path",
        "recommend a career", "recommend careers",
    ]

    if any(word in msg for word in career_words):
        recs = get_career_recommendations(
            skills_str=f"{user_message} {user_skills}",
            top_n=3,
        )

        if not recs:
            return respond(
                "I couldn't find a suitable career match. "
                "Tell me your skills and the type of work you enjoy."
            )

        reply = "### 🚀 Recommended Career Options\n\n"

        for item in recs:
            reply += (
                f"**{item['Role']} — {item['Match_Percentage']}% match**\n\n"
                f"Description: {item['Description']}\n\n"
                f"Matching skills: "
                f"{', '.join(item['Matching_Skills'])}\n\n"
                f"Skills to learn: "
                f"{', '.join(item['Missing_Skills'][:4])}\n\n"
                f"Tools: {', '.join(item['Tools'])}\n\n"
                f"Salary range: {item['Salary_Range']}\n\n"
            )

        return respond(reply)

    # 8. Do not show career recommendations for every unknown question
    return respond(
        "I couldn't identify that question yet. 😊\n\n"
        "You can ask me things like:\n"
        "- What is Python?\n"
        "- Explain DBMS.\n"
        "- Give me a Python Developer roadmap.\n"
        "- What skills should I learn to become a Data Analyst?\n"
        "- Suggest Java internships.\n"
        "- Give me interview questions.\n\n"
        "For answers to any general question, we can connect an AI model."
                )
