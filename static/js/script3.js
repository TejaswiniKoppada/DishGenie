document.addEventListener("DOMContentLoaded", function () {
    const searchBar = document.getElementById("search-bar");
    const ingredientPicklist = document.getElementById("ingredient-picklist");
    const selectedIngredientsDiv = document.getElementById("selected-ingredients");
    const generateRecipeButton = document.getElementById("generate-recipe");
    const recipeResultDiv = document.getElementById("recipe-result");

    let selectedIngredients = [];

    // Fetch ingredients from the backend and populate the picklist
    fetch("/get_inventory?email=user@example.com") // Replace with actual user email
        .then(response => response.json())
        .then(data => {
            const ingredients = data.inventory
                .filter(item => item.status === "Available")
                .map(item => item.ingredient)
                .sort((a, b) => a.localeCompare(b)); // Sort ingredients alphabetically

            ingredients.forEach(ingredient => {
                const li = document.createElement("li");
                li.textContent = ingredient;
                li.addEventListener("click", () => {
                    if (!selectedIngredients.includes(ingredient)) {
                        selectedIngredients.push(ingredient);
                        updateSelectedIngredients();
                    }
                });
                ingredientPicklist.appendChild(li);
            });
        });

    // Handle search bar input
    searchBar.addEventListener("input", function () {
        const searchTerm = searchBar.value.toLowerCase();
        const ingredients = Array.from(ingredientPicklist.children);

        ingredients.forEach(ingredient => {
            if (ingredient.textContent.toLowerCase().includes(searchTerm)) {
                ingredient.style.display = "block";
            } else {
                ingredient.style.display = "none";
            }
        });
    });

    // Update selected ingredients display
    function updateSelectedIngredients() {
        selectedIngredientsDiv.innerHTML = "";
        selectedIngredients.forEach(ingredient => {
            const capsule = document.createElement("div");
            capsule.className = "ingredient-capsule";
            capsule.textContent = ingredient;
            const removeButton = document.createElement("span");
            removeButton.className = "remove";
            removeButton.textContent = "×";
            removeButton.addEventListener("click", () => {
                selectedIngredients = selectedIngredients.filter(item => item !== ingredient);
                updateSelectedIngredients();
            });
            capsule.appendChild(removeButton);
            selectedIngredientsDiv.appendChild(capsule);
        });
    }

    // Handle "Generate Recipe" button click
    generateRecipeButton.addEventListener("click", async function () {
        if (selectedIngredients.length === 0) {
            alert("Please select at least one ingredient.");
            return;
        }

        try {
            // Send selected ingredients to the backend
            const response = await fetch("/generate_recipe", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ ingredients: selectedIngredients }),
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
});