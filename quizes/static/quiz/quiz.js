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

const quizForm = document.getElementById("quiz_form");
if(quizForm) {
    quizForm.addEventListener("submit", (e) => {
        e.preventDefault();
        
        const answers = [...document.getElementsByClassName('answer')];
        const data = {};
        answers.forEach(answer => {
            if(answer.checked) {
                data[answer.name] = answer.value
            } else {
                if (!data[answer.name]) {
                    data[answer.name] = null
                }
            }
        })

        console.log("data: ", data);
        const csrftoken = getCookie('csrftoken');
        const quiz_id = quizForm.getAttribute("data-quiz-id");
            fetch(`/quizes/${quiz_id}/save_quiz/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            results = data.results;
            quizForm.style.display = "none";
            results.forEach(result => {
                const resContainer = document.createElement('div');
                for (const [question, resp] of Object.entries(result)) {
                    const classes = ['container', 'p-3', 'text-light', 'h3'];
                    resContainer.classList.add(...classes);
                    resContainer.innerHTML += `${question} `;

                    if (resp=='not answered') {
                        resContainer.innerHTML += '-not answered';
                        resContainer.classList.add('bd-danger');
                    }
                    else {
                        const answer = resp["answered"];
                        const correct = resp["correct_answer"];

                        if (answer == correct) {
                            resContainer.classList.add("bg-success");
                            resContainer.innerHTML += `answered: ${answer}`;
                        }
                        else {
                            resContainer.classList.add("bg-danger");
                            resContainer.innerHTML += `| correct answer: ${correct} `;
                            resContainer.innerHTML += `| answered: ${answer}`;
                        }
                    }
                }
                const body = document.getElementsByTagName('body')[0]
                body.append(resContainer)
            })
            const showResult = document.getElementById("show-result");
            showResult.innerHTML = data.passed ? 
            `<p>Congrats you passed the quiz! ${data.score}%</p>`:
            `<p>Oups... :( Your result is ${data.score}%</p>`
        })
        .catch((error) => {
            console.log('Error: ', error);
        })
    })
}