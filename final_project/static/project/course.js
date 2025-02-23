
const selectDropdown = document.getElementById("select_dropdown");

if (selectDropdown) {
    const categories = ["Business Administration/Management","Computer Science","Nursing","Biology","Psychology","Mechanical Engineering","Electrical Engineering","Civil Engineering","Economics","Political Science","Communication","Accounting","Marketing","Finance","Education","English Literature/Language","History","Sociology","Chemistry","Mathematics"].sort();
    
    //Create select form
    const formSelect = document.createElement("select");
    formSelect.classList.add("form-select", "mt-3", "form-select-lg");
    formSelect.name="category";
    formSelect.setAttribute("aria-label", "Category");
    formSelect.id = "form_select";
    
    //Create a default empty option
    const defaultOption = document.createElement('option');
    defaultOption.textContent = 'Select a category...';
    defaultOption.value = '';
    formSelect.appendChild(defaultOption);

    //Create all major options
    categories.forEach(category => {
        const optionCategory = document.createElement("option");
        optionCategory.value = category.split(" ").map(word => word.toLowerCase()).join("_");
        optionCategory.textContent = category;
        formSelect.appendChild(optionCategory);
    })
    
    
    selectDropdown.appendChild(formSelect)

    $('#form_select').select2({
        placeholder: 'Select a category',
        allowClear: true,
        width: '100%'
    });
}

const addLectureBtn = document.getElementById("add_lecture");
if(addLectureBtn) {
    addLectureBtn.addEventListener("click", () => {
        document.getElementById("form_add_lecture").style.display = 'block';
        addLectureBtn.style.display = 'none';
    })
}

const cancelBtn = document.getElementById("cancel_btn");
if(cancelBtn) {
    cancelBtn.addEventListener("click", () => {
        document.getElementById("form_add_lecture").style.display = 'none';
        addLectureBtn.style.display = 'block';
    })
}


const addQuiz = document.getElementById("add_quiz");
if (addQuiz) {
    addQuiz.addEventListener("click", () => {
        document.getElementById("add_quiz_form").style.display = 'block';
        addQuiz.style.display = 'none';
    });
}

const cancel_quiz = document.getElementById("cancel_quiz");
if (cancel_quiz) {
    cancel_quiz.addEventListener("click", () => {
        document.getElementById("add_quiz_form").style.display = 'none';
        addQuiz.style.display = 'block';
    });
}

let currentQuestion = 0;

function createForms(numberOfQuestions, quiz_id, lecture_id) {
    const container = document.getElementById("quiz_form_container");


    for (let i = 1; i <= numberOfQuestions; i++) {
        // Create form
        console.log(`quiz-form-${i}`);
        const questionForm = document.createElement("form");
        questionForm.id = `quiz-form-${i}`;
        questionForm.className = 'question-form';
        questionForm.method = "POST";
        questionForm.dataset.lectureId = lecture_id;
        questionForm.action = `{% url 'quizes:save_question_answer' %}`;

        const questionContent = `
            <div class="container">
            <h3>Question ${i}</h3>
            <div class="question-container">
                <input type="text" 
                       name="question_text" 
                       placeholder="Enter your question" 
                       class="form-control"
                       required>
            </div>
            <div class="answer-container" id="answer-container-${i}">
                <h4 class="my-4">Answer</h4>
                <div class="answer-list" id="answer-list-${i}">
                    <!-- Initiate 2 answer -->
                    ${createAnswerForm(i, 1)}
                    ${createAnswerForm(i, 2)}
                </div>
                <button type="button" 
                        class="btn btn-sm btn-primary" 
                        onclick="addAnswer(${i})">
                    Add more answer
                </button>
            </div>
            <div class="navigation-buttons">
                ${i === numberOfQuestions ? 
                    '<button type="submit" class="form-control">Finish</button>':
                    `<button type="submit" class="form-control">Next question</button>`}
            </div>
            </div>
        `;

        questionForm.innerHTML = questionContent;
        
        questionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitQuestionForm(this, quiz_id, lecture_id);
        });

        container.appendChild(questionForm);
    }

    showQuestion(0);
}

function remove_answer(questionNumber, answerNumber) {
    const answerForm = document.getElementById(`answer-form-${answerNumber}-question-${questionNumber}`);
    if (answerForm) {
        answerForm.remove();
    }
}

function createAnswerForm(questionNumber, answerNumber) {
    return `
        <div id="answer-form-${answerNumber}-question-${questionNumber}" class="d-flex justify-content-between mb-3">
            <input type="text" 
                   name="answer_text_${questionNumber}_${answerNumber}" 
                   class="form-control w-50"
                   placeholder="Answer" 
                   required>
            <label>
                <input type="checkbox" 
                       name="correct_answer_${questionNumber}" 
                       value="${answerNumber}">
                Correct answer
            </label>
            <button 
            class="btn btn-sm btn-outline-danger"
            onclick="remove_answer(${questionNumber}, ${answerNumber})"
            >x</button>
        </div>
    `;
}

function addAnswer(questionNumber) {
    const answerList = document.getElementById(`answer-list-${questionNumber}`);
    const answerCount = answerList.children.length + 1;
    
    answerList.insertAdjacentHTML('beforeend', createAnswerForm(questionNumber, answerCount));
}

function submitQuestionForm(form, quiz_id) {
    //Find number of the question
    const formId = form.id;
    const questionNumber = parseInt(formId.split('-')[2]);

    const lecture_id = form.dataset.lectureId;
    if (!lecture_id) {
        console.error("lecture_id is missing!");
        alert("Lecture ID is missing. Please try again.");
        return;
    }

    //Get question text
    const questionText = form.querySelector('input[name="question_text"]').value;
    
    // Get all answer inputs for this question
    const answerContainer = document.getElementById(`answer-list-${questionNumber}`);
    const answerForms = answerContainer.querySelectorAll('[id^="answer-form-"]');
    const correctAnswers = form.querySelectorAll(`input[name="correct_answer_${questionNumber}"]:checked`);
    if (correctAnswers.length === 0) {
        alert("Please select at least one correct answer for this question.");
        return false;
    }
    
    const answers = [];
    answerForms.forEach(answerForm => {
        answers.push({
            text: answerForm.querySelector('input[type="text"]').value,
            correct: answerForm.querySelector('input[type="checkbox"]').checked
        });
    })

    data = {
        quiz_id: quiz_id,
        question_text: questionText,
        answers: answers
    }

    console.log("Fetch data....")
    console.log(lecture_id)
    fetch(`/course/${lecture_id}/addquiz/save-question-answer/${quiz_id}/`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const totalQuestions = document.querySelectorAll('.question-form').length;
            if (questionNumber < totalQuestions) {
                showQuestion(questionNumber);
            } else {
                window.location.href = `/course/lecture/${lecture_id}`;
            }
        }
    })
    .catch(error => {
        alert('It occurs some error.');
    });
}

function showQuestion(currentQuestionNumber) {
    // Hide all form
    document.querySelectorAll('.question-form').forEach(form => {
        form.style.display = 'none';
    });
    
    //Show next form
    const nextFormId = `quiz-form-${currentQuestionNumber + 1}`;
    const nextForm = document.getElementById(nextFormId);
    if (nextForm) {
        nextForm.style.display = 'block';
    }
}

const addQuizForm = document.getElementById("add_quiz_form");
if(addQuizForm) {
    addQuizForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(addQuizForm);
        fetch(addQuizForm.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                console.log("number of questions: ", data.number_of_question);
                console.log("quiz_id: ", data.quiz_id);
                console.log("lecture_id: ", data.lecture_id);
                createForms(data.number_of_question, data.quiz_id, data.lecture_id);
                addQuizForm.style.display = "none";
            }
        })
        .catch(error => {
            console.log("error:", error);
            alert('Có lỗi xảy ra. Vui lòng thử lại.', error);
        });
    })
}

const courseAndTest = document.getElementById("course_and_test");
if(courseAndTest) {
    //Fetch data
    const student_id = courseAndTest.dataset.studentId;
    fetch(`/student_tests/${student_id}`)
        .then(response => response.json())
        .then(data => {
            if (!data || !data.courses) {
                courseAndTest.innerHTML = "<p>No courses found.</p>";
                return;
            }

            //Make div for each course
            data.courses.forEach(course => {
                let course_nb = 0
                const course_container = document.createElement("div");
                course_container.style = "padding: 20px; box-sizing: border-box;";
                course_container.classList.add("border-silence");
                course_container.innerHTML += `<button class="btn btn-primary button-title"><h3>Course ${course_nb += 1}: ${course.course.title}</h3></button>`
                const course_container_2 = document.createElement("div");
                course_container_2.classList.add("toggle-course");
                //Add all lectures of course
                course.lectures.forEach(lecture => {
                    const lecture_container = document.createElement("div");
                    lecture_container.style.overflowX = "auto";
                    lecture_container.innerHTML += `<h4>${lecture.title}</h4>`

                    //create a table with the lecture test score
                    const lecture_table = document.createElement("table");
                    lecture_table.classList.add("lecture-table", "table", "table-hover");
                    //create header for the table
                    lecture_table.innerHTML += `
                    <tr>
                        <th scope="col">Number</th>
                        <th scope="col">Quiz</th>
                        <th scope="col">Score</th>
                    </tr>
                    `
                    lecture_container.appendChild(lecture_table);
                    
                    //Add quize's cell
                    let i = 0
                    lecture.quizes.forEach(quiz => {
                        const tableRow = lecture_table.insertRow();
                        tableRow.insertCell().textContent = i+=1;
                        tableRow.insertCell().textContent = quiz.title;
                        tableRow.insertCell().textContent = quiz.score;
                    });
                    lecture_container.appendChild(lecture_table);
                    course_container_2.appendChild(lecture_container);
                    course_container.appendChild(course_container_2);
                });
                courseAndTest.appendChild(course_container);
            });

            let btnTitle = document.getElementsByClassName("button-title");
            console.log("Number of button-title elements found:", btnTitle.length);
            if (btnTitle) {
                console.log("all button: ", btnTitle);
                Array.from(btnTitle).forEach((btn) => {
                    btn.addEventListener("mouseover", function() {
                        const parentDiv = btn.closest('div'); 
                        if (parentDiv) {
                          parentDiv.classList.add('blue-border');
                        }
                      });
                
                      btn.addEventListener("mouseout", function() {
                        const parentDiv = btn.closest('div');
                        if (parentDiv) {
                          parentDiv.classList.remove('blue-border');
                        }
                      });
                    btn.addEventListener("click", (event) => {
                        const courseContent = btn.nextElementSibling;
                        courseContent.classList.toggle('show');
                    })
                })
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            courseAndTest.innerHTML = "<p>Error loading courses.</p>";
        });

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainBody = document.getElementById('main-body');

    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    
    if (isCollapsed) {
        sidebar.classList.add('collapsed');
        mainBody.classList.add('collapsed');
        menuToggle.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="20" height="20" viewBox="0 0 24 24">
        <path d="M 2 5 L 2 7 L 22 7 L 22 5 L 2 5 z M 2 11 L 2 13 L 22 13 L 22 11 L 2 11 z M 2 17 L 2 19 L 22 19 L 22 17 L 2 17 z"></path>
      </svg>`;
    }

    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainBody.classList.toggle('collapsed');
        
        const isNowCollapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebarCollapsed', isNowCollapsed);
        
        menuToggle.innerHTML = isNowCollapsed ? `<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="20" height="20" viewBox="0 0 24 24">
        <path d="M 2 5 L 2 7 L 22 7 L 22 5 L 2 5 z M 2 11 L 2 13 L 22 13 L 22 11 L 2 11 z M 2 17 L 2 19 L 22 19 L 22 17 L 2 17 z"></path>
      </svg>`
            :
        `<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="20" height="20" viewBox="0 0 50 50">
<path d="M 9.15625 6.3125 L 6.3125 9.15625 L 22.15625 25 L 6.21875 40.96875 L 9.03125 43.78125 L 25 27.84375 L 40.9375 43.78125 L 43.78125 40.9375 L 27.84375 25 L 43.6875 9.15625 L 40.84375 6.3125 L 25 22.15625 Z"></path>
</svg>`;
    });
});