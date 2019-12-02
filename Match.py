import PreferenceList

preference_lists = PreferenceList.create_preference_lists()

student_gs = {}
university_gs = {}

for student in preference_lists[0]:
    print student
    pl =  preference_lists[0][student]
    student_gs[student] = {
        'matched' : False,
        'match' : '',
        'preference_list' : pl
    }
    print preference_lists[0][student]

for university in preference_lists[1]:
    print university
    pl = preference_lists[1][university]
    university_gs[university] = {
        'matched' : False,
        'match' : '',
        'preference_list' : pl
    }
    print preference_lists[1][university]

# Only let universities offer
matches_sub = lambda n: [prop['matched'] for prop in n.values()]
matches = lambda t: matches_sub(student_gs) if t == 'students' else matches_sub(university_gs)

print(matches('students'))
print(matches('universities'))

students = preference_lists[0].keys()
universities = preference_lists[1].keys()

while False in matches('universities'):
    for university in universities:
        if not university_gs[university]['matched']:
            for student in university_gs[university]['preference_list']:
                if not university_gs[university]['matched']:
                    if not student_gs[student]['matched']:
                        print student, 'unmatched. Matching with', university
                        student_gs[student]['matched'] = True
                        student_gs[student]['match'] = university
                        university_gs[university]['matched'] = True
                        university_gs[university]['match'] = student
                    else:
                        print student, 'matched with ', student_gs[student]['match']
                        print "Attempting to match with ", university
                        current_match = student_gs[student]['match']
                        current_match_index = student_gs[student]['preference_list'].index(current_match)
                        new_match_index = student_gs[student]['preference_list'].index(university)
                        if new_match_index < current_match_index:
                            student_gs[student]['match'] = university
                            university_gs[university]['matched'] = True
                            university_gs[university]['match'] = student
                            university_gs[current_match]['matched'] = False
                            university_gs[current_match]['match'] = ''

for university in university_gs:
    print university, "matched with", university_gs[university]['match']


