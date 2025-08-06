import streamlit as st
from typing import Dict, Any
import os


def initialize_session() -> None:
    session_defaults = {
        # User API configuration
        "user_api_key": "",
        "api_key_valid": False,
        "user_name": None,
        
        # Module selection
        "user_module_name": None,
        "user_module_name_ab": None,
        
        # Exam state
        "exam_done": False,
        "latest_grade": None,
        "latest_score": None,
        "new_score": False,
        
        # Exam session state
        "start_time": None,
        "auto_submit": False,
        "manual_submit": False,
        "grading_done": False,
        
        # Grading results storage
        "grading_results": {},      # Store individual question results
        "exam_total_score": 0.0,    # Store total score in session
        "exam_total_max_score": 0.0, # Store max score in session
        "student_answers": {},      # Store student answers
        
        # Study page state
        "last_chapter": None,
        "cards": [],
        "index": 0,
        "show_answer": False
    }
    
    # Only set defaults if not already present
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def get_user_name() -> str:
    return st.session_state.get("user_name", "")


def set_user_name(name: str) -> None:
    st.session_state.user_name = name


def get_user_api_key() -> str:
    return st.session_state.get("user_api_key", "")


def set_user_api_key(api_key: str) -> None:
    st.session_state.user_api_key = api_key


def get_user_module() -> tuple[str, str]:
    return (
        st.session_state.get("user_module_name", ""),
        st.session_state.get("user_module_name_ab", "")
    )


def set_user_module(module_name: str, module_ab: str) -> None:
    st.session_state.user_module_name = module_name
    st.session_state.user_module_name_ab = module_ab


def reset_exam_state() -> None:
    exam_keys = [
        "start_time", "auto_submit", "manual_submit", "grading_done", 
        "new_score", "grading_results",
        "exam_total_score", "exam_total_max_score", "student_answers"
    ]
    for key in exam_keys:
        if key in st.session_state:
            if key in ["auto_submit", "manual_submit", "grading_done", "new_score"]:
                st.session_state[key] = False
            elif key in ["grading_results", "student_answers"]:
                st.session_state[key] = {}
            elif key in ["exam_total_score", "exam_total_max_score"]:
                st.session_state[key] = 0.0
            else:
                st.session_state[key] = None


def store_grading_result(question_idx: int, result: str) -> None:
    """Store grading result for a specific question"""
    st.session_state.grading_results[question_idx] = result


def get_grading_result(question_idx: int) -> str:
    """Get stored grading result for a specific question"""
    return st.session_state.grading_results.get(question_idx, "")


def has_grading_result(question_idx: int) -> bool:
    """Check if grading result exists for a specific question"""
    return question_idx in st.session_state.grading_results


def add_to_total_score(score: float, max_score: float) -> None:
    """Add to the total exam score"""
    st.session_state.exam_total_score += score
    st.session_state.exam_total_max_score += max_score


def get_total_scores() -> tuple[float, float]:
    """Get total score and max score"""
    return st.session_state.exam_total_score, st.session_state.exam_total_max_score


def reset_total_scores() -> None:
    """Reset total scores to 0"""
    st.session_state.exam_total_score = 0.0
    st.session_state.exam_total_max_score = 0.0


def store_student_answer(question_idx: int, answer: str) -> None:
    """Store student answer for a specific question"""
    st.session_state.student_answers[question_idx] = answer


def get_student_answer(question_idx: int) -> str:
    """Get stored student answer for a specific question"""
    return st.session_state.student_answers.get(question_idx, "")


def get_session_info() -> Dict[str, Any]:
    """Get current session state for debugging"""
    return {
        "api_key_set": bool(st.session_state.get("user_api_key")),
        "module_selected": bool(st.session_state.get("user_module_name")),
        "exam_in_progress": bool(st.session_state.get("start_time")),
        "exam_done": st.session_state.get("exam_done", False)
    } 