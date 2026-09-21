import os
import json
import logging
from typing import Dict, Any, List, Optional
from backend.app.config import settings

logger = logging.getLogger("edupulse.ai_service")

class AIService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        self.model = settings.GROQ_MODEL
        self.client = None
        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
                logger.info(f"Groq AI Client initialized with model {self.model}")
            except Exception as e:
                logger.warning(f"Could not initialize Groq client: {e}")

    def generate_ai_tutor_response(
        self,
        student_message: str,
        student_name: str,
        action_type: str = "general",
        topic_name: Optional[str] = None,
        mastery_score: Optional[float] = None,
        mastery_level: Optional[str] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
        context_mistake: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates an adaptive AI tutor explanation attuned to the student's current mastery level.
        """
        level_str = mastery_level or ("Beginner" if (mastery_score or 0) < 50 else "Developing" if (mastery_score or 0) < 75 else "Proficient")
        topic_ctx = f"Current Topic: {topic_name or 'Database Management Systems (DBMS)'}."
        
        system_prompt = (
            f"You are EduPulse AI, an empathetic, expert, high-pedagogy computer science and database tutor. "
            f"You are tutoring {student_name}. The student's mastery in this subject/topic is '{level_str}' "
            f"(Mastery Score: {mastery_score if mastery_score is not None else 'Not yet assessed'}/100).\n\n"
            f"Pedagogical Guidelines:\n"
            f"- If the student is 'Beginner' or has low mastery: Explain from intuitive analogies and fundamentals. Avoid deep mathematical jargon without defining it first.\n"
            f"- If the student is 'Developing': Bridge concepts with real-world schemas, relational tables, and intermediate queries.\n"
            f"- If the student is 'Proficient' or 'Mastered': Provide rigorous theoretical insights, edge cases, anomalies, and optimization trade-offs.\n"
            f"- Action Requested: {action_type}.\n"
            f"- Be concise, direct, helpful, and encourage the student. Use markdown formatting with code blocks and bullet points where helpful."
        )

        if context_mistake:
            system_prompt += (
                f"\nThe student recently made a mistake on this question:\n"
                f"Question: {context_mistake.get('question')}\n"
                f"Student Answered: {context_mistake.get('selected_answer')}\n"
                f"Correct Answer: {context_mistake.get('correct_answer')}\n"
                f"Standard Explanation: {context_mistake.get('explanation')}\n"
                f"Explain why their answer is incorrect and gently clarify the underlying misconception."
            )

        messages = [{"role": "system", "content": system_prompt}]
        if chat_history:
            for item in chat_history[-6:]:
                role = "assistant" if item.get("role") in ["assistant", "system"] else "user"
                messages.append({"role": role, "content": item.get("content", "")})
        
        # User message
        action_prefix = ""
        if action_type == "explain_simply":
            action_prefix = "Explain this simply in plain English: "
        elif action_type == "give_example":
            action_prefix = "Give me a concrete code/table example for: "
        elif action_type == "real_world_example":
            action_prefix = "Give me an intuitive real-world company/industry example of: "
        elif action_type == "test_me":
            action_prefix = "Ask me a conceptual multiple-choice check question on: "
        elif action_type == "explain_mistake":
            action_prefix = "Help me understand why my answer was wrong on: "

        user_content = f"{action_prefix}{student_message}" if action_prefix and action_prefix not in student_message else student_message
        messages.append({"role": "user", "content": user_content})

        if self.client:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    temperature=0.4,
                    max_tokens=1024,
                )
                reply = chat_completion.choices[0].message.content
                return {
                    "reply": reply,
                    "action_type": action_type,
                    "topic_name": topic_name,
                    "student_mastery_level": level_str,
                    "follow_up_suggestions": self._generate_follow_up_suggestions(action_type, topic_name)
                }
            except Exception as e:
                logger.error(f"Groq API call error: {e}")

        # Fallback offline response
        return self._generate_fallback_tutor_response(student_message, action_type, topic_name, level_str)

    def generate_quiz_questions(
        self,
        topic_name: str,
        difficulty: str = "medium",
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generates structured multiple-choice quiz questions with rigorous JSON schema validation.
        """
        prompt = (
            f"Generate exactly {count} distinct multiple choice questions for the topic '{topic_name}' "
            f"at difficulty level '{difficulty}'.\n"
            f"You MUST respond ONLY with a valid JSON array containing exactly {count} objects, with no surrounding commentary or markdown code fences.\n"
            f"Each object must follow this exact schema:\n"
            f"{{\n"
            f'  "question": "Question string",\n'
            f'  "option_a": "Option A text",\n'
            f'  "option_b": "Option B text",\n'
            f'  "option_c": "Option C text",\n'
            f'  "option_d": "Option D text",\n'
            f'  "correct_answer": "A",\n'
            f'  "explanation": "Clear explanation of why the correct option is right and others are wrong",\n'
            f'  "difficulty": "{difficulty}"\n'
            f"}}"
        )

        if self.client:
            try:
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a database instructor creating high-quality, unambiguous multiple-choice assessment questions. Always output valid raw JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    model=self.model,
                    temperature=0.3,
                    response_format={"type": "json_object"} if "json_object" in dir() else None
                )
                content = response.choices[0].message.content.strip()
                # Clean up any accidental markdown backticks
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()

                parsed = json.loads(content)
                questions_list = parsed if isinstance(parsed, list) else parsed.get("questions", [])
                
                # Validate format
                validated = []
                for q in questions_list:
                    if all(k in q for k in ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation"]):
                        ans = str(q["correct_answer"]).strip().upper()
                        if ans in ["A", "B", "C", "D"]:
                            q["correct_answer"] = ans
                            q["difficulty"] = difficulty
                            validated.append(q)

                if len(validated) >= count:
                    return validated[:count]
                elif validated:
                    return validated
            except Exception as e:
                logger.error(f"Error parsing AI quiz generator output: {e}")

        # Fallback to rich curated questions for topic
        return self._generate_fallback_quiz(topic_name, difficulty, count)

    def _generate_follow_up_suggestions(self, action_type: str, topic_name: Optional[str]) -> List[str]:
        t = topic_name or "this topic"
        return [
            f"Give me a real-world example of {t}",
            f"How does {t} apply to real database performance?",
            f"Test me with a practice question on {t}",
            "Can you explain that even more simply?"
        ]

    def _generate_fallback_tutor_response(
        self,
        message: str,
        action_type: str,
        topic_name: Optional[str],
        level: str
    ) -> Dict[str, Any]:
        """Pedagogical fallback when offline or during API downtime."""
        topic_str = topic_name or "Database Management"
        reply = (
            f"**EduPulse AI Tutor ({level} Level Guide)**\n\n"
            f"Regarding your query on **{topic_str}**:\n\n"
            f"> *\"{message}\"*\n\n"
            f"In relational databases, **{topic_str}** guarantees data integrity and optimal schema architecture. "
            f"When approaching this topic as a **{level}**, remember these fundamental pillars:\n\n"
            f"1. **Core Concept**: Every table should represent a single conceptual entity, with primary keys guaranteeing row identity.\n"
            f"2. **Elimination of Redundancy**: Avoid storing the same non-key attribute in multiple places to prevent insertion, deletion, and update anomalies.\n"
            f"3. **Practical Application**: Always verify functional dependencies ($X \\to Y$) to ensure attributes depend only on the candidate key.\n\n"
            f"Try taking a practice quiz on this topic to test your retention and elevate your mastery score!"
        )
        return {
            "reply": reply,
            "action_type": action_type,
            "topic_name": topic_name,
            "student_mastery_level": level,
            "follow_up_suggestions": self._generate_follow_up_suggestions(action_type, topic_name)
        }

    def _generate_fallback_quiz(self, topic_name: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        """Fallback question pool covering DBMS topics."""
        dbms_pool = [
            {
                "question": f"Which of the following is a primary goal of {topic_name} in relational systems?",
                "option_a": "Minimizing storage speed at the cost of duplicate records",
                "option_b": "Eliminating data redundancy and preventing anomalies",
                "option_c": "Allowing arbitrary unindexed linear scans on disk",
                "option_d": "Combining unrelated entities into a single universal table",
                "correct_answer": "B",
                "explanation": "A central objective of relational database design and normalization is eliminating redundant data to prevent update, insertion, and deletion anomalies.",
                "difficulty": difficulty
            },
            {
                "question": f"In {topic_name}, what ensures that relational references between tables remain valid?",
                "option_a": "Foreign Key Constraint (Referential Integrity)",
                "option_b": "Candidate Key Multiplicity",
                "option_c": "Second Normal Form decomposition",
                "option_d": "Uncommitted Read isolation level",
                "correct_answer": "A",
                "explanation": "Referential integrity via foreign key constraints ensures that a value in a child table must match a valid primary key in the parent table.",
                "difficulty": difficulty
            },
            {
                "question": f"When analyzing functional dependencies $X \\to Y$, which Armstrong's Axiom states that if $Y \\subseteq X$, then $X \\to Y$ holds?",
                "option_a": "Transitivity Rule",
                "option_b": "Augmentation Rule",
                "option_c": "Reflexivity Rule",
                "option_d": "Decomposition Rule",
                "correct_answer": "C",
                "explanation": "Armstrong's Reflexivity axiom states that if attribute set Y is a subset of X, then X functionally determines Y.",
                "difficulty": difficulty
            },
            {
                "question": "A table is in 2NF if it is in 1NF and what additional condition holds?",
                "option_a": "It contains no transitive dependencies",
                "option_b": "Every non-prime attribute is fully functionally dependent on the candidate key",
                "option_c": "Every determinant is a superkey",
                "option_d": "Multivalued dependencies are eliminated",
                "correct_answer": "B",
                "explanation": "2NF requires no partial dependencies—meaning every non-key attribute must depend on the whole candidate key, not a proper subset.",
                "difficulty": difficulty
            },
            {
                "question": "Which ACID property guarantees that concurrent database transactions execute without interfering with one another?",
                "option_a": "Atomicity",
                "option_b": "Consistency",
                "option_c": "Isolation",
                "option_d": "Durability",
                "correct_answer": "C",
                "explanation": "The Isolation property of ACID ensures that concurrent transactions do not interfere with each other and execute as if in serial order.",
                "difficulty": difficulty
            }
        ]
        return dbms_pool[:count]

ai_service = AIService()
