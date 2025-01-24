import requests
import pandas as pd
import numpy as np
from collections import defaultdict

# Define URLs for the datasets
historical_quiz_url = "https://api.jsonserve.com/XgAgFJ"
current_quiz_url = "https://api.jsonserve.com/rJvd7g"

# Fetch data from APIs
historical_quiz_data = requests.get(historical_quiz_url).json()
current_quiz_data = requests.get(current_quiz_url).json()

# Check if the current quiz data is a dictionary or a list
if isinstance(current_quiz_data, dict):
    current_quiz_data = current_quiz_data.get('data', [])
elif not isinstance(current_quiz_data, list):
    raise ValueError("current_quiz_data should be a list or a dictionary with a list.")

# Convert to pandas DataFrame
historical_df = pd.DataFrame(historical_quiz_data)
current_df = pd.DataFrame(current_quiz_data)

# Extract performance data from 'response_map' and 'quiz'
def extract_performance_data(df):
    topic_performance = defaultdict(list)
    difficulty_performance = defaultdict(list)

    for _, row in df.iterrows():
        response_map = row.get('response_map', {})
        quiz = row.get('quiz', {})

        if isinstance(response_map, dict) and isinstance(quiz, dict):
            for question_id, selected_option in response_map.items():
                question_details = quiz.get('questions', {}).get(question_id, {})
                topic = question_details.get('topic')
                difficulty = question_details.get('difficulty')
                correct_option = question_details.get('correct_option')
                is_correct = selected_option == correct_option

                if topic and difficulty:
                    topic_performance[topic].append(is_correct)
                    difficulty_performance[difficulty].append(is_correct)

    # Calculate accuracy for each topic and difficulty level
    topic_accuracy = {topic: np.mean(performance) for topic, performance in topic_performance.items()}
    difficulty_accuracy = {difficulty: np.mean(performance) for difficulty, performance in difficulty_performance.items()}

    return topic_accuracy, difficulty_accuracy

# Perform analysis on historical and current data
historical_topic_accuracy, historical_difficulty_accuracy = extract_performance_data(historical_df)
current_topic_accuracy, current_difficulty_accuracy = extract_performance_data(current_df)

# Debugging - Check the extracted accuracies
print("Historical Topic Accuracies:", historical_topic_accuracy)
print("Current Topic Accuracies:", current_topic_accuracy)
print("Historical Difficulty Accuracies:", historical_difficulty_accuracy)
print("Current Difficulty Accuracies:", current_difficulty_accuracy)

# Compare historical and current performance by topic and difficulty
def compare_performance(historical, current):
    comparison = {}
    all_keys = set(historical.keys()).union(set(current.keys()))

    for key in all_keys:
        historical_accuracy = historical.get(key, 0)
        current_accuracy = current.get(key, 0)
        change = current_accuracy - historical_accuracy
        comparison[key] = {
            "historical_accuracy": historical_accuracy,
            "current_accuracy": current_accuracy,
            "change": change
        }

    return comparison

topic_comparison = compare_performance(historical_topic_accuracy, current_topic_accuracy)
difficulty_comparison = compare_performance(historical_difficulty_accuracy, current_difficulty_accuracy)

# Debugging - Check performance comparison
print("Topic Comparison:", topic_comparison)
print("Difficulty Comparison:", difficulty_comparison)

# Generate key insights for the topics and difficulty levels
def generate_key_insights(topic_comparison, difficulty_comparison):
    topic_improvement = sum(1 for value in topic_comparison.values() if value['change'] > 0.02)  # Relaxed threshold
    topic_decline = sum(1 for value in topic_comparison.values() if value['change'] < -0.02)  # Relaxed threshold
    difficulty_improvement = sum(1 for value in difficulty_comparison.values() if value['change'] > 0.02)  # Relaxed threshold
    difficulty_decline = sum(1 for value in difficulty_comparison.values() if value['change'] < -0.02)  # Relaxed threshold

    insights = {
        "topic_improvement": topic_improvement,
        "topic_decline": topic_decline,
        "difficulty_improvement": difficulty_improvement,
        "difficulty_decline": difficulty_decline
    }

    return insights

insights = generate_key_insights(topic_comparison, difficulty_comparison)

# Debugging - Check key insights
print("Key Insights:", insights)

# Generate recommendations based on insights
def generate_recommendations(insights):
    recommendations = []
    if insights["topic_decline"] > 0:
        recommendations.append(f"Focus on {insights['topic_decline']} topics where performance declined.")
    if insights["difficulty_decline"] > 0:
        recommendations.append(f"Evaluate {insights['difficulty_decline']} difficulty levels where performance declined.")
    if insights["topic_improvement"] > 0:
        recommendations.append(f"Maintain improvement in {insights['topic_improvement']} topics.")
    if insights["difficulty_improvement"] > 0:
        recommendations.append(f"Maintain improvement in {insights['difficulty_improvement']} difficulty levels.")
    
    if not recommendations:
        recommendations.append("No major weaknesses detected. Keep up the good work!")
    
    return recommendations

recommendations = generate_recommendations(insights)

# Analyze student persona based on patterns in the data
def analyze_student_persona():
    persona = {
        "strengths": [],
        "weaknesses": [],
        "labels": [],
        "behavior": ""
    }

    # 1. Strengths: Identify topics and difficulty levels where the student excels
    if insights["topic_improvement"] > 0:
        persona["strengths"].append(f"Topics with improvement: {insights['topic_improvement']}")
    if insights["difficulty_improvement"] > 0:
        persona["strengths"].append(f"Difficulty levels with improvement: {insights['difficulty_improvement']}")
    
    # 2. Weaknesses: Identify topics and difficulty levels with decline
    if insights["topic_decline"] > 0:
        persona["weaknesses"].append(f"Topics with decline: {insights['topic_decline']}")
    if insights["difficulty_decline"] > 0:
        persona["weaknesses"].append(f"Difficulty levels with decline: {insights['difficulty_decline']}")
    
    # 3. Creative labels based on the pattern:
    if insights["topic_improvement"] == 0 and insights["difficulty_improvement"] == 0:
        persona["labels"].append("The Steady Student: No Major Improvements")
    if insights["topic_decline"] > 0 or insights["difficulty_decline"] > 0:
        persona["labels"].append("The Persistent Learner: Needs Focus in Specific Areas")
    if insights["topic_improvement"] > 0 and insights["difficulty_improvement"] > 0:
        persona["labels"].append("The Balanced Achiever: Improvement Across the Board")
    if insights["difficulty_decline"] > 0:
        persona["labels"].append("The Challenge Seeker: Struggling with Higher Difficulty Levels")

    # Behavior based on the analysis of performance across topics and difficulty
    if insights["topic_improvement"] > 0 and insights["topic_decline"] == 0:
        persona["behavior"] = "This student is highly adaptable and has shown growth in multiple areas."
    elif insights["topic_decline"] > 0:
        persona["behavior"] = "This student may be struggling with specific topics and could benefit from focused practice."
    elif insights["difficulty_decline"] > 0:
        persona["behavior"] = "This student is challenged by more difficult content but is trying to overcome it."
    else:
        persona["behavior"] = "This student is performing steadily across all levels with no major weaknesses."

    return persona

student_persona = analyze_student_persona()

# Print results
print("Historical vs Current Performance by Topic:")
for topic, accuracy in historical_topic_accuracy.items():
    current_accuracy = current_topic_accuracy.get(topic, 0)
    print(f"{topic}: Historical: {accuracy:.2f}, Current: {current_accuracy:.2f}, Change: {current_accuracy - accuracy:.2f}")

print("\nHistorical vs Current Performance by Difficulty:")
for difficulty, accuracy in historical_difficulty_accuracy.items():
    current_accuracy = current_difficulty_accuracy.get(difficulty, 0)
    print(f"{difficulty}: Historical: {accuracy:.2f}, Current: {current_accuracy:.2f}, Change: {current_accuracy - accuracy:.2f}")

print("\nKey Insights:")
print(f"Topics with improvement: {insights['topic_improvement']}")
print(f"Topics with decline: {insights['topic_decline']}")
print(f"Difficulty levels with improvement: {insights['difficulty_improvement']}")
print(f"Difficulty levels with decline: {insights['difficulty_decline']}")

print("\nRecommendations:")
for recommendation in recommendations:
    print(recommendation)

print("\nStudent Persona Analysis:")
print(f"Strengths: {', '.join(student_persona['strengths'])}")
print(f"Weaknesses: {', '.join(student_persona['weaknesses'])}")
print(f"Labels: {', '.join(student_persona['labels'])}")
print(f"Behavior: {student_persona['behavior']}")