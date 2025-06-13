
import streamlit as st
import json
import random

# Load questions from JSON
@st.cache_data
def load_questions():
    with open("business_law_all_chapters_mcq.json", "r") as f:
        return json.load(f)

questions = load_questions()

# Get list of unique chapters from questions
chapters = sorted(list(set(q["chapter"] for q in questions)))
selected_chapters = st.multiselect("Select chapters to practice:", chapters, default=chapters)

# Filter questions based on selected chapters
filtered_questions = [q for q in questions if q["chapter"] in selected_chapters]

# Shuffle questions once per session or when chapter selection changes
if "prev_selected_chapters" not in st.session_state or st.session_state.prev_selected_chapters != selected_chapters:
    st.session_state.shuffled_questions = random.sample(filtered_questions, len(filtered_questions))
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.show_answer = False
    st.session_state.prev_selected_chapters = selected_chapters

# Get current question
if st.session_state.q_index < len(st.session_state.shuffled_questions):
    q = st.session_state.shuffled_questions[st.session_state.q_index]
    st.subheader(f"Question {st.session_state.q_index + 1} of {len(st.session_state.shuffled_questions)}")
    st.write(f"**[{q['chapter']}]** {q['question']}")

    selected = st.radio("Choose your answer:", q["choices"], key=f"q{st.session_state.q_index}")

    if st.button("Submit Answer"):
        if st.session_state.show_answer:
            st.warning("You've already answered this question. Click 'Next Question' to continue.")
        else:
            st.session_state.show_answer = True
            if q["choices"].index(selected) == q["answer"]:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                correct_ans = q["choices"][q["answer"]]
                st.error(f"❌ Incorrect. The correct answer was: **{correct_ans}**")

    if st.session_state.show_answer:
        if st.button("Next Question"):
            st.session_state.q_index += 1
            st.session_state.show_answer = False
else:
    st.success(f"🎉 Quiz complete! Your score: {st.session_state.score} / {len(st.session_state.shuffled_questions)}")
    if st.button("Restart Quiz"):
        del st.session_state.shuffled_questions
        del st.session_state.q_index
        del st.session_state.score
        del st.session_state.show_answer
        del st.session_state.prev_selected_chapters
