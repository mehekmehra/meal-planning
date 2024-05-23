

function firstTime() {
    window.location.href = '/first_time';
}
function returningUser() {
    fetch('/returning_user')
    .then(response => {
        window.location.href = '/adding_meals';
    })
    .catch(error => console.error('Error:', error));
}

function firstAddMeals() {
    
}

function submitInfo() {
    const dbNameInput = document.getElementById('nameInput');
    const dbName = dbNameInput.value;
    const emailInput = document.getElementById('emailInput');
    const email = emailInput.value;

    fetch('/submit_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: dbName,
                               email: email
        }),
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('info_message');
        messageDiv.innerHTML = ''; 
        const message = document.createElement('p');
        message.textContent = data.message;

        if (data.status === "error") {      
            
            message.classList.add('errorMessage');
        } else {
            window.location.href = '/adding_meals';
            message.classList.add('successMessage');  
        }
        messageDiv.appendChild(message); 
        dbNameInput.value = "";
        emailInput.value = "";
    });
}

function submitMeal() {
    const mealInput = document.getElementById('mealInput');
    const meal = mealInput.value;
    const ingredientsInput = document.getElementById('ingredientsInput');
    const ingredients = ingredientsInput.value;
    const categoryInput = document.getElementById('categoryInput');
    const category = categoryInput.value

    fetch('/submit_meal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ meal_name: meal,
                               ingredients: ingredients,
                               category: category
        }),
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('meal_input_message');
        messageDiv.innerHTML = ''; 
        const message = document.createElement('p');
        message.textContent = data.message;

        if (data.status === "error") {
            message.classList.add('errorMessage');  
        } else {
            message.classList.add('successMessage'); 
        }
        messageDiv.appendChild(message); 
        mealInput.value = '';
        ingredientsInput.value = '';
    });
}

function scheduleMeals() {
    const numWeeksInput = document.getElementById('numWeeks');
    const numWeeks = numWeeksInput.value;
    fetch('/schedule_meals', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ num_weeks: numWeeks
        }),
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('num_weeks_message');
        messageDiv.innerHTML = ''; 
        const message = document.createElement('p');
        message.textContent = data.message;

        if (data.status === "error") { 
            message.classList.add('errorMessage'); 
        } else {
            message.classList.add('successMessage');   
        }
        messageDiv.appendChild(message); 
        numWeeksInput.value = '';
    });

}