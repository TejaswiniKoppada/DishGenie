document.addEventListener("DOMContentLoaded", function () {
    const addIngredientButton = document.getElementById("add-ingredient");
    const ingredientInput = document.getElementById("ingredient-input");
    const ingredientImageInput = document.getElementById("ingredient-image");
    const toggleInputModeButton = document.getElementById("toggle-input-mode");
    const inventoryTableBody = document.getElementById("inventory-table").getElementsByTagName("tbody")[0];
    const errorMessage = document.getElementById("error-message");
    const voiceInputBtn = document.getElementById("voice-input");

    let inputMode = "text"; // Default mode is text input
    let recognition;

    // Initialize Web Speech API for voice input
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false; // Stop after one speech input
        recognition.interimResults = false; // Only final results
        recognition.lang = 'en-US'; // Language

        recognition.onstart = function () {
            voiceInputBtn.innerHTML = '<i class="fas fa-microphone-slash"></i> Listening...';
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript.trim();
            ingredientInput.value = transcript; // Populate the input field
            voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            checkIngredient(transcript); // Validate the ingredient
        };

        recognition.onerror = function (event) {
            console.error("Speech recognition error:", event.error);
            voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            errorMessage.textContent = "Error recognizing speech. Please try again.";
            errorMessage.style.display = "block";
        };

        recognition.onend = function () {
            voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        };
    } else {
        voiceInputBtn.style.display = "none"; // Hide voice button if not supported
        console.warn("Speech recognition not supported in this browser.");
    }

    // Toggle between text input and image upload
    toggleInputModeButton.addEventListener("click", () => {
        if (inputMode === "text") {
            inputMode = "image";
            ingredientInput.style.display = "none";
            ingredientImageInput.style.display = "block";
            toggleInputModeButton.textContent = "Switch to Text Input";
        } else {
            inputMode = "text";
            ingredientInput.style.display = "block";
            ingredientImageInput.style.display = "none";
            toggleInputModeButton.textContent = "Switch to Image Upload";
        }
    });

    // Fetch and update the inventory table
    function fetchAndUpdateInventory() {
        fetch("/get_inventory")
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    updateInventoryTable(data.inventory);
                } else {
                    inventoryTableBody.innerHTML = "<tr><td colspan='3'>No ingredients found.</td></tr>";
                }
            })
            .catch(error => {
                console.error("Error fetching inventory:", error);
            });
    }

    // Fetch inventory data when the page loads
    fetchAndUpdateInventory();

    // Add ingredient functionality
    addIngredientButton.addEventListener("click", () => {
        errorMessage.style.display = "none"; // Hide error message initially

        if (inputMode === "text") {
            const ingredient = ingredientInput.value.trim();
            if (!ingredient) {
                errorMessage.textContent = "Please enter an ingredient.";
                errorMessage.style.display = "block";
                return;
            }
            addIngredientToInventory(ingredient);
        } else {
            const file = ingredientImageInput.files[0];
            if (!file) {
                errorMessage.textContent = "Please upload an image.";
                errorMessage.style.display = "block";
                return;
            }
            predictIngredientFromImage(file);
        }
    });

    // Function to add ingredient to inventory
    function addIngredientToInventory(ingredient) {
        fetch("/add_ingredient", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredient: ingredient })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                ingredientInput.value = ""; // Clear the input field
                errorMessage.textContent = data.message; // Display success message
                errorMessage.style.color = "green";
                errorMessage.style.display = "block";
                fetchAndUpdateInventory(); // Update the table dynamically
            } else {
                errorMessage.textContent = data.message; // Display backend error message
                errorMessage.style.color = "red";
                errorMessage.style.display = "block";
            }
        })
        .catch(error => {
            console.error("Error adding ingredient:", error);
            errorMessage.textContent = "An error occurred. Please try again.";
            errorMessage.style.color = "red";
            errorMessage.style.display = "block";
        });
    }

    // Function to predict ingredient from image
    function predictIngredientFromImage(file) {
        const formData = new FormData();
        formData.append("file", file);

        fetch("/predict_ingredient", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                // Add the predicted ingredient to the inventory
                fetch("/add_ingredient", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ ingredient: data.ingredient })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        // Refresh the page to reflect changes
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error("Error adding ingredient:", error);
                });
            } else {
                errorMessage.textContent = data.message; // Display backend error message
                errorMessage.style.color = "red";
                errorMessage.style.display = "block";
            }
        })
        .catch(error => {
            console.error("Error predicting ingredient:", error);
            errorMessage.textContent = "An error occurred. Please try again.";
            errorMessage.style.color = "red";
            errorMessage.style.display = "block";
        });
    }

    // Function to update the inventory table
    function updateInventoryTable(inventory) {
        inventoryTableBody.innerHTML = ""; // Clear existing rows
        inventory.forEach(item => {
            const row = document.createElement("tr");

            // Add the 'dull-row' class if the status is "unavailable"
            if (item.status.toLowerCase() === "unavailable") {
                row.classList.add("dull-row");
            }

            // Add the +, -, and x symbols for actions
            const actionCell = `
                <td>
                    ${item.status.toLowerCase() === "unavailable" 
                        ? `<span class="add-btn" data-ingredient="${item.ingredient}">+</span>` 
                        : `<span class="minus-btn" data-ingredient="${item.ingredient}">-</span>`}
                    <span class="delete-btn" data-ingredient="${item.ingredient}">×</span>
                </td>
            `;

            row.innerHTML = `
                <td>${item.ingredient}</td>
                <td>${item.status}</td>
                ${actionCell}
            `;
            inventoryTableBody.appendChild(row);
        });

        // Add event listeners to delete buttons
        document.querySelectorAll(".delete-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const ingredient = btn.getAttribute("data-ingredient");
                deleteIngredient(ingredient);
            });
        });

        // Add event listeners to + buttons
        document.querySelectorAll(".add-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const ingredient = btn.getAttribute("data-ingredient");
                updateIngredientStatus(ingredient, "Available");
            });
        });

        // Add event listeners to - buttons
        document.querySelectorAll(".minus-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const ingredient = btn.getAttribute("data-ingredient");
                updateIngredientStatus(ingredient, "Unavailable");
            });
        });
    }

    // Function to delete an ingredient
    function deleteIngredient(ingredient) {
        fetch("/delete_ingredient", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredient: ingredient })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                fetchAndUpdateInventory(); // Refresh the inventory table
            }
        })
        .catch(error => {
            console.error("Error deleting ingredient:", error);
        });
    }

    // Function to update ingredient status
    function updateIngredientStatus(ingredient, status) {
        fetch("/update_ingredient_status", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredient: ingredient, status: status })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                fetchAndUpdateInventory(); // Refresh the inventory table
            }
        })
        .catch(error => {
            console.error("Error updating ingredient status:", error);
        });
    }

    // Voice input button click event
    voiceInputBtn.addEventListener("click", () => {
        if (recognition) {
            recognition.start(); // Start voice recognition
        }
    });
});