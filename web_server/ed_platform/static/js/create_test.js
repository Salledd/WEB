document.addEventListener('DOMContentLoaded', function () {
    const questionsContainer = document.getElementById('questions');
    const addQuestionButton = document.getElementById('add-question');

    // Добавление нового вопроса
    addQuestionButton.addEventListener('click', function () {
        const questionCount = questionsContainer.children.length;
        const questionHTML = `
            <div class="question" data-index="${questionCount}" style="margin-bottom: 20px; padding: 15px; border: 1px solid #ccc; border-radius: 8px; background-color: #f9f9f9;">
                <textarea name="question_text" placeholder="Enter question text" style="width: 100%; height: 60px; padding: 8px; border-radius: 5px; border: 1px solid #ccc; margin-bottom: 10px;"></textarea>
                <h3 style="font-size: 18px; color: #555;">Choices</h3>
                <div class="choices" style="margin-bottom: 10px;">
                    <div style="margin-bottom: 10px;">
                        <input type="text" name="choice_text_${questionCount}" placeholder="Enter choice text" style="width: calc(80% - 10px); padding: 8px; border-radius: 5px; border: 1px solid #ccc;">
                        <label style="margin-left: 10px;">
                            <input type="checkbox" name="is_correct_${questionCount}" value="0"> Correct
                        </label>
                        <button type="button" class="remove-choice" style="margin-left: 10px; background-color: #ff4d4d; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Remove</button>
                    </div>
                </div>
                <button type="button" class="add-choice" style="background-color: #4CAF50; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer;">Add Choice</button>
                <button type="button" class="remove-question" style="margin-left: 10px; background-color: #ff4d4d; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer;">Remove Question</button>
            </div>`;
        questionsContainer.insertAdjacentHTML('beforeend', questionHTML);
    });

    // Удаление вопросов и добавление вариантов ответа
    questionsContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-question')) {
            const question = e.target.closest('.question');
            question.remove();
        } else if (e.target.classList.contains('add-choice')) {
            const question = e.target.closest('.question');
            const index = question.dataset.index;
            const choiceContainer = question.querySelector('.choices');
            const choiceCount = choiceContainer.querySelectorAll('input[type="text"]').length;
            const choiceHTML = `
                <div style="margin-bottom: 10px;">
                    <input type="text" name="choice_text_${index}" placeholder="Enter choice text" style="width: calc(80% - 10px); padding: 8px; border-radius: 5px; border: 1px solid #ccc;">
                    <label style="margin-left: 10px;">
                        <input type="checkbox" name="is_correct_${index}" value="${choiceCount}"> Correct
                    </label>
                    <button type="button" class="remove-choice" style="margin-left: 10px; background-color: #ff4d4d; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Remove</button>
                </div>`;
            choiceContainer.insertAdjacentHTML('beforeend', choiceHTML);
        } else if (e.target.classList.contains('remove-choice')) {
            const choice = e.target.closest('div');
            choice.remove();
        }
    });
});