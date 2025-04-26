// document.addEventListener("DOMContentLoaded", function () {
//     const generateRecipeButton = document.getElementById("generate-recipe");
//     const recipeResultDiv = document.getElementById("recipe-result");

//     generateRecipeButton.addEventListener("click", async function () {
//         const selectedIngredients = Array.from(document.querySelectorAll("#ingredient-picklist option:checked")).map(option => option.value);

//         if (selectedIngredients.length === 0) {
//             recipeResultDiv.textContent = "Please select at least one ingredient.";
//             return;
//         }

//         try {
//             const response = await fetch("/generate_recipe", {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ ingredients: selectedIngredients })
//             });

//             const data = await response.json();
//             if (data.status === "success") {
//                 // Redirect to the recipe display page
//                 window.location.href = "/recipe_display";
//             } else {
//                 recipeResultDiv.textContent = data.message;
//             }
//         } catch (error) {
//             recipeResultDiv.textContent = "Failed to generate recipe. Please try again.";
//         }
//     });

//     // fetch('/generate_recipe', {
//     //     method: 'POST',
//     //     headers: { "Content-Type": "application/json" },
//     //     body: JSON.stringify({ ingredients: selectedIngredients })
//     // })
//     // .then(response => response.json())
//     // .then(data => {
//     //     console.log("🟢 Debug Response:", data);  // 🛠 Log the raw response
//     // })
//     // .catch(error => console.error("🔴 Fetch Error:", error));
    
    
// });
// document.getElementById('generate-recipe-btn').addEventListener('click', function() {
//     const selectedIngredients = Array.from(document.querySelectorAll('.ingredient-checkbox:checked')).map(cb => cb.value);

//     fetch('/generate_recipe', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ ingredients: selectedIngredients }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             if (data.redirect) {
//                 window.location.href = data.redirect;
//             } else {
//                 alert('Recipes generated successfully!');
//             }
//         } else {
//             alert(data.message || 'Failed to generate recipes. Please try again.');
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('An error occurred while generating recipes.');
//     });
// });





document.addEventListener('DOMContentLoaded', function () {
    const generateRecipeButton = document.getElementById('generate-recipe-button');

    if (generateRecipeButton) {
        generateRecipeButton.addEventListener('click', async function () {
            const ingredients = Array.from(document.querySelectorAll('.ingredient-checkbox:checked'))
                .map(checkbox => checkbox.value);

            if (ingredients.length === 0) {
                alert("Please select at least one ingredient.");
                return;
            }

            try {
                const response = await fetch('/generate_recipe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ ingredients: ingredients }),
                });

                const data = await response.json();

                if (data.success) {
                    // Redirect to the recipe display page
                    window.location.href = data.redirect;
                } else {
                    // Display error message
                    alert(data.message || "Failed to generate recipe. Please try again.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            }
        });
    }
});