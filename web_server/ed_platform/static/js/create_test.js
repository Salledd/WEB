    document.addEventListener('DOMContentLoaded', function () {
        const questionContainer = document.getElementById('questions');
        const addQuestionButton = document.getElementById('add-question');

        addQuestionButton.addEventListener('click', function () {
            const questionForm = document.createElement('div');
            questionForm.classList.add('question-form');
            questionForm.innerHTML = `
                <textarea name="question_text" placeholder="Enter question text"></textarea>
                <h3>Choices</h3>
                <div class="choices">
                    <button type="button" class="add-choice">Add Choice</button>
                    <div class="choice-forms"></div>
                </div>
                <button type="button" class="remove-question">Remove Question</button>
            `;
            questionContainer.appendChild(questionForm);
        });

        questionContainer.addEventListener('click', function (e) {
            if (e.target.classList.contains('remove-question')) {
                e.target.closest('.question-form').remove();
            } else if (e.target.classList.contains('add-choice')) {
                const choiceContainer = e.target.closest('.choices').querySelector('.choice-forms');
                const choiceInput = document.createElement('div');
                choiceInput.innerHTML = `
                    <input type="text" name="choice_text" placeholder="Enter choice text">
                    <label>
                        <input type="checkbox" name="is_correct"> Correct
                    </label>
                    <button type="button" class="remove-choice">Remove</button>
                `;
                choiceContainer.appendChild(choiceInput);
            } else if (e.target.classList.contains('remove-choice')) {
                e.target.closest('div').remove();
            }
        });
    });
