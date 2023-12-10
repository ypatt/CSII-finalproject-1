def calculate_grade(score, best_score):
    # Assuming best_score is the highest score in the class
    # and grading is based on the percentage of the best score
    percentage = (score / best_score) * 100

    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    else:
        return 'F'
