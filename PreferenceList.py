import csv, operator

def create_preference_lists():
    student_data = list(csv.DictReader(open('model_data_student.csv')))
    university_data = list(csv.DictReader(open('model_data_university.csv')))

    for university in university_data:
        university['Ratings'] = {}

    for student in student_data:
        student['Ratings'] = {}
        student_rating_points = sum([int(x) for x in [
            student['Academic Ranking'],
            student['Safety'],
            student['Campus Amenities'],
            student['Social Life'],
            student['Cost']
        ]])

        adj_ar = float(student['Academic Ranking']) / student_rating_points
        adj_s = float(student['Safety']) / student_rating_points
        adj_ca = float(student['Campus Amenities']) / student_rating_points
        adj_sl = float(student['Social Life']) / student_rating_points
        adj_c = float(student['Cost']) / student_rating_points

        for university in university_data:
            university_rating_points = sum([int(x) for x in [
                university['GPA'],
                university['Test Scores'],
                university['Extracurricular'],
                university['Application Quality']
            ]])
            adj_gpa = float(university['GPA']) / university_rating_points
            adj_ts = float(university['Test Scores']) / university_rating_points
            adj_ec = float(university['Extracurricular']) / university_rating_points
            adj_aq = float(university['Application Quality']) / university_rating_points

            adj_gpa_rate = 100 * float(student['GPA']) / 4.0 * adj_gpa
            adj_ts_rate = 100 * float(student['SAT']) / 2400.0 * adj_ts
            adj_ec_rate = 100 * float(student['Extracurricular']) / 5.0 * adj_ec
            adj_aq_rate = float(student['Application Quality']) * adj_aq
            university_to_student_rate = round(sum([adj_gpa_rate, adj_ts_rate, adj_ec_rate, adj_aq_rate]), 3)
            university['Ratings'][student['Student Name']] = university_to_student_rate

            adj_ar_rate = float(university['Academic Ranking']) * adj_ar
            adj_s_rate = float(university['Safety']) * adj_s
            adj_ca_rate = float(university['Campus Amenities']) * adj_ca
            adj_sl_rate = float(university['Social Life']) * adj_sl
            adj_c_rate = float(university['Cost']) * adj_c
            student_to_university_rate = round(sum([adj_ar_rate, adj_s_rate, adj_ca_rate, adj_sl_rate, adj_c_rate]), 3)
            student['Ratings'][university['College Name']] = student_to_university_rate

    student_preference_lists = {}
    university_preference_lists = {}

    for student in student_data:
        university_ratings = student['Ratings']
        sorted_university_ratings = sorted(university_ratings.items(), key=operator.itemgetter(1), reverse=True)
        student_preference_lists[student['Student Name']] = [pair[0] for pair in sorted_university_ratings]

    for university in university_data:
        student_ratings = university['Ratings']
        sorted_student_ratings = sorted(student_ratings.items(), key=operator.itemgetter(1), reverse=True)
        university_preference_lists[university['College Name']] = [pair[0] for pair in sorted_student_ratings]

    return [student_preference_lists, university_preference_lists]