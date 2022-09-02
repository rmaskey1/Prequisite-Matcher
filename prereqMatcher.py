from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://catalog.sjsu.edu/preview_program.php?catoid=12&poid=3911').text
soup = BeautifulSoup(html_text, 'html.parser')
# print(soup)
courses = soup.find_all('li', class_ = 'acalog-course')
# print(courses)
# print(courses[0].a['onclick'])
count = 0

target_course = input('Enter course in the format *COURSE* *NUMBER*: ')

for course in courses:
    show = course.a['onclick'][11:].replace("'","").split(',')
    first = int(show[0])
    second =int(show[1])
    # print(first)
    # print(second)
    show_url = f'https://catalog.sjsu.edu/ajax/preview_course.php?catoid={first}&coid={second}&show'
    # print(show_url)
    course_text = requests.get(show_url).text
    course_soup = BeautifulSoup(course_text, 'lxml')
    bold_word = course_soup.find('strong')
    # print(bold_word)
    if 'Prerequisite(s):' in bold_word:
        prereq_courses = course_soup.find_all('a', id=True)
        for prereqs in prereq_courses:
            prereq = prereqs.string
            if prereq == target_course:
                print(course.text)
                count = count+1
        # print(prereq_courses)

if count == 0:
    print("This class is not a prerequisite for any courses")
else:
    print("Done!")