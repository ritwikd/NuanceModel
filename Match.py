import PreferenceList
import os

verbose = eval(os.environ['verbose'])

omniscient_ranking = [
    'Stanford',
    'Harvard',
    'Amherst College',
    'Juilliard',
    'University of Michigan',
    'UMass',
    'Ohio State',
    'Syracuse',
    'Alabama',
    'De Anza Community College'
]

preference_lists = PreferenceList.create_preference_lists()

student_gs = {}
university_gs = {}

for student in preference_lists[0]:
    pl = preference_lists[0][student]
    student_gs[student] = {
        'matched': False,
        'match': '',
        'preference_list': pl
    }

for university in preference_lists[1]:
    pl = preference_lists[1][university]
    university_gs[university] = {
        'matched': False,
        'match': '',
        'preference_list': pl
    }

# Only let universities offer
matches_sub = lambda n: [prop['matched'] for prop in n.values()]
matches = lambda t: matches_sub(student_gs) if t == 'students' else matches_sub(university_gs)

if verbose:
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
                        if verbose:
                            print student, 'unmatched. Matching with', university
                        student_gs[student]['matched'] = True
                        student_gs[student]['match'] = university
                        university_gs[university]['matched'] = True
                        university_gs[university]['match'] = student
                    else:
                        if verbose:
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

print "Matchings:"
for university in omniscient_ranking:
    print university.ljust(30), "matched with", university_gs[university]['match']
