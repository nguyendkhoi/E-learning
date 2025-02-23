# E-learning Web Project: Tomuss

## Project Description

This project is a Dajango-based e-learning web platform designed to both students and teachers. It provides a centralized online environment where instructors can create and manage courses, and students can enroll, learn, and take quizzes to track their learning progress.

## Distinctiveness and Complexity

Firstly, the platform's distinctiveness stems from its robust role-based user system, clearly differentiating between teachers and students with tailored functionalities for each. Teachers have the exclusive ability to create, manage, and remove courses and lectures, while students can enroll in courses and access learning materials.  Furthermore, the integration of a quiz system directly within the lecture structure adds a layer of interactive learning and assessment, moving beyond simple content delivery. This is evidenced by the code's decorators (`@teacher_required`, `@student_required`) that enforce role-based access control to different views and functionalities, and the inclusion of `Quiz` and `Result` models from a separate `quizes` app (implied by imports), showcasing a modular design that incorporates assessment tools into the learning process. This combination of role-specific experiences and built-in quizzing functionality sets this project apart from simpler course listing applications.

The project's complexity is significant in its implementation of user authentication and authorization, crucial for a secure and role-managed e-learning environment. The code features user registration, login, and logout functionalities, leveraging Django's built-in authentication system.  The custom `User` model extends Django's `AbstractUser` to include roles ('teacher', 'student'), and the application employs decorators to restrict access to views based on user roles. This is demonstrated in functions like `login_view`, `register`, and the use of `@teacher_required` and `@student_required` decorators throughout `views.py`.  Furthermore, the data model, defined in `models.py`, demonstrates complexity by structuring relationships between `User`, `Course`, and `Lecture`. The use of Foreign Keys and ManyToManyFields to link teachers to created courses, students to enrolled courses, and lectures to courses, establishes a relational database schema that is essential for managing the interconnected data within an e-learning platform.

The frontend of the application, where we have many templates, each of which displays different content. The JavaScript code (`script.js`) suggests features like dynamic form creation for quizzes, AJAX calls to fetch student test data (`/student_tests/${student_id}`), and dynamic updates of the course content display on the page. The use of `fetch` API calls in Javascript to `/student_tests/${student_id}` and `/course/<span class="math-inline">\{lecture\_id\}/addquiz/save\-question\-answer/</span>{quiz_id}/`  indicate a dynamic frontend that interacts with the backend to retrieve and update data without full page reloads.  Furthermore, the Javascript's DOM manipulation for creating question and answer forms (`createForms`, `createAnswerForm`, `addAnswer`) and showing/hiding elements suggests a rich, interactive user interface beyond simple static HTML pages, adding to the project's frontend complexity.

## File Descriptions

### Final Project App Files (`final_project` app)

*   **`views.py`**: This Python file contains the Django view functions that handle user requests and application logic. It defines functions for:
    *   `index`:  Displays the course listing based on user role (teacher or student) or a login message for unauthenticated users.
    *   `login_view`, `logout_view`: Handles user login and logout functionalities using Django's authentication system.
    *   `register`: Manages user registration, including checks for existing usernames/emails and password confirmation, and role assignment.
    *   `add_course`, `course_detail`, `remove_course_view`: Functions related to course creation, detail view, and removal, restricted to teacher roles.
    *   `add_lecture`, `lecture_views`, `remove_lecture`: Functions for lecture creation, display, and removal within courses, also teacher-restricted.
    *   `enroll_course`: Allows students to enroll in courses.
    *   `my_course`: Displays courses enrolled by the currently logged-in student.
    *   `profile`, `student_tests`, `people`: Functions to display user profiles, student test results (likely for teachers and students themselves), and lists of people in courses.
    *   Decorators `@teacher_required`, `@student_required`: Enforce role-based access control to specific views.
    *   `create_quiz`, `save_question_answer`, `quiz_view`, `save_quiz`:    Functions for quiz creation, display, and save answer

*   **`models.py`**: This Python file defines the Django models that represent the database structure of the e-learning platform. It includes:
    *   `User`:  Extends Django's `AbstractUser` to add `full_name` and `role` fields, with choices for 'student' and 'teacher'. Includes methods `is_teacher()` and `is_student()` to check user roles.
    *   `Course`: Model representing courses, including `description`, `title`, `category`, `owner` (ForeignKey to `User` with `role='teacher'`), and `students` (ManyToManyField to `User` with `role='student'`).
    *   `Lecture`: Model representing lectures within courses, including `courses` (ForeignKey to `Course`), `title`, `description`, `content` (textual content), and `video_file` (FileField for video uploads). Includes `get_all_quizzes()` method (implementation not shown but implied to retrieve quizzes associated with the lecture, likely from a related app).

*   **`script.js`**: This Javascript file contains frontend scripts to enhance user interaction.  Key functionalities include:
    *   Dynamic category dropdown creation using `select2` library for adding courses.
    *   Displaying/hiding lecture and quiz forms dynamically on course detail and lecture pages.
    *   Client-side form creation for quizzes, including questions and multiple-choice answers with correct answer selection.
    *   AJAX functionality using `fetch` API to submit quiz questions and answers to the backend and to retrieve student test data to display scores.
    *   Dynamic display of student course and test data fetched from `/student_tests/${student_id}` and rendering it into an expandable course list with lecture and quiz scores.
    *   Sidebar menu toggle functionality with local storage persistence for collapsed state.

*   **`decorators.py`** (Not explicitly shown but implied by imports in `views.py`): This file likely contains custom Django decorators:
    *   `teacher_required`: Decorator to restrict view access to users with the 'teacher' role.
    *   `student_required`: Decorator to restrict view access to users with the 'student' role.

*   **`urls.py`** (Implied, not shown):  This file defines the URL patterns for your Django project, mapping URLs to view functions defined in `views.py`. It would include URLs like:
    *   `/`, `/index/`:  For the index view.
    *   `/login/`, `/logout/`, `/register/`: For authentication views.
    *   `/course/add/`, `/course/<int:course_id>/`, `/course/<int:course_id>/remove/`: For course management views.
    *   `/course/<int:course_id>/addlecture/`, `/lecture/<int:lecture_id>/`, `/lecture/<int:lecture_id>/remove/`: For lecture management views.
    *   `/course/<int:course_id>/enroll/`: For course enrollment.
    *   `/my_course/`: For student's enrolled courses.
    *   `/profile/<int:user_id>/`, `/student_tests/<int:student_id>/`, `/people/`: For profile and user-related views.
    *   `/course/<int:lecture_id>/addquiz/`: For quiz creation (inferred from Javascript).
    *   `/course/<int:lecture_id}/addquiz/save-question-answer/<int:quiz_id>/`: For saving quiz questions and answers (inferred from Javascript).

*   **`templates/`** (Directory - structure not fully shown, but implied to exist): This directory contains HTML templates used by Django to render the frontend.  Likely includes templates such as:
    *   `project/index.html`: Template for the homepage/course listing.
    *   `project/login.html`: Template for the login page.
    *   `project/register.html`: Template for the registration page.
    *   `project/addCourse.html`: Template for adding a new course.
    *   `project/course_detail.html`: Templates for displaying course details.
    *   `project/addLecture.html` (likely, though form might be embedded in `course_detail.html`): Template for adding lectures.
    *   `project/lecture.html`: Template for displaying a lecture.
    *   `project/profile.html`: Template for user profiles.
    *   `project/people.html`: Template for displaying lists of people.
    *   Base template (e.g., `project/layout.html`) to provide a common layout structure.

*   **`static/`** (Directory - structure and content not fully shown): This directory contains static files like CSS, JavaScript, and images. Likely includes:
    *   `static/project/styles.css` (or similar): CSS stylesheets for styling the application.
    *   `static/project/script.js`: The Javascript file provided (`script.js`).
    *   `static/project/images`: Folder contain all the images of the web

### Quizzes App Files (`quizes` app)

*   **`quizes/views.py`**: This Python file contains the Django view functions for managing quizzes within the `quizes` app. It includes views for:
    *   `create_quiz`: Handles the creation of a new quiz, taking quiz name, number of questions, difficulty, and passing percentage as input. It associates the created quiz with a specific `Lecture`.
    *   `save_question_answer`:  Saves individual questions and their corresponding answers for a given quiz. It processes JSON data containing question text and a list of answers (including correct answer flags).
    *   `quiz_view`: Renders the quiz page for students to take a quiz. It retrieves a quiz and its questions, and prepares data to be displayed in the `quize.html` template.
    *   `save_quiz`: Processes student quiz submissions. It receives student answers via JSON, evaluates the answers against the correct answers, calculates the quiz score, and saves the `Result` in the database. It returns a JSON response indicating if the quiz was passed and the final score, along with detailed results.

*   **`quizes/models.py`**: This Python file defines the Django models for the quiz functionalities:
    *   `Quiz`: Model representing a quiz. Fields include `name`, `number_of_question`, `required_score_to_pass` (percentage), `difficulty` (using `DIFF_CHOICES` of 'easy', 'medium', 'hard'), and a ForeignKey `lecture` linking it to a `Lecture` in the `final_project` app.  It includes a method `get_questions()` to retrieve and randomize the quiz questions.
    *   `Question`: Model representing a question within a quiz. Fields include `text` (question text) and a ForeignKey `quiz` linking it to a `Quiz`.  It includes a method `get_answer()` to retrieve and randomize the answers for the question.
    *   `Answer`: Model representing a possible answer to a question. Fields include `text` (answer text), `correct` (BooleanField indicating if it's the correct answer), and a ForeignKey `question` linking it to a `Question`.
    *   `Result`: Model to store quiz results. Fields include a ForeignKey `quiz` linking it to a `Quiz`, a ForeignKey `user` linking it to a `User` from the `final_project` app, and `score` (FloatField) to store the student's score on the quiz.

*   **`quizes/urls.py`**: Defines the URL patterns for the `quizes` app:
    *   `create/`: URL pattern mapped to the `create_quiz` view, for quiz creation.
    *   `save-question-answer/<int:quiz_id>/`: URL pattern for the `save_question_answer` view, used to save questions and answers.
    *   `<int:quiz_id>/`: URL pattern for the `quiz_view` view, to display a specific quiz to users.
    *   `<int:quiz_id>/save_quiz/`: URL pattern for the `save_quiz` view, to handle quiz submissions and save results.

*   **`quizes/templates/`**: This directory contains HTML templates specifically used by the `quizes` app to render quiz-related views. It includes the following templates within a subdirectory (likely `quiz/` as per your image):
    *   **`quizes/templates/quiz/layout.html`**: This HTML template likely serves as a base layout for quiz-related pages. It may define the overall structure, common header, footer, and potentially include common CSS and JavaScript resources used across quiz pages. Templates like `quize.html` would likely extend this layout.
    *   **`quizes/templates/quiz/quize.html`**: This HTML template is responsible for rendering the actual quiz taking interface for students. It would include the display of quiz questions, answer choices, submission forms, and potentially real-time feedback areas during a quiz. It likely extends `layout.html` to maintain a consistent quiz page structure.

*   **`quizes/static/`**: This directory contains static files associated with the `quizes` app.  It includes a subdirectory (likely `quiz/` as per your image) for organization:
    *   **`quizes/static/quiz/js/quiz.js`**: This JavaScript file (located at `quizes/static/quiz/js/quiz.js`) likely contains frontend JavaScript code specific to the quiz functionalities.  It could handle:
        *   Interactive elements on the quiz taking page (`quize.html`).
        *   Client-side quiz logic or validation.
        *   Potentially AJAX interactions related to quiz submission or real-time feedback (though quiz submission AJAX is primarily handled in `script.js` at the project level, this file might handle other quiz-specific frontend interactions).

### Project-Level Files (Outside of Apps)

*   **`manage.py`**: Django management script.
*   **`requirements.txt`**:  Lists Python package dependencies for the entire project.

