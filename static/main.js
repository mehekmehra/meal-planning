var isFirstTime = false
var dbName
var meal
var ingredients
var category

function firstTime() {
    window.location.href = '/first_time';
}

// Function to handle add meal button click
function returningUser() {
    fetch('/returning_user')
    .then(response => {
        // Redirect to the add meal page after the request is complete
        window.location.href = '/adding_meals';
    })
    .catch(error => console.error('Error:', error));
}

function firstAddMeals() {
    
}

function submitInfo() {
    // Get the value from the input box
    dbName = document.getElementById('nameInput').value;
    email = document.getElementById('emailInput').value;
     // Send the name to the Flask backend
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
            messageDiv.innerHTML = data.message;  
            messageDiv.style.color = 'red';       
        }
        else {
            window.location.href = '/adding_meals';
        }
    });
}

function submitMeal() {
    meal = document.getElementById('mealInput').value;
    ingredients = document.getElementById('ingredientsInput').value;
    category = document.getElementById('categoryInput').value;

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
            messageDiv.innerHTML = data.message;  
            messageDiv.style.color = 'red';       
        }
    });
}

function scheduleMeals() {
    numWeeks = document.getElementById('numWeeks').value;
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
            messageDiv.innerHTML = data.message;  
            messageDiv.style.color = 'red';       
        }
    });

}