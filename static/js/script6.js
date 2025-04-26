document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-recipe');

    deleteButtons.forEach(button => {
        button.addEventListener('click', async function () {
            const recipeName = button.getAttribute('data-recipe-name');

            try {
                const response = await fetch('/delete_recipe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ recipe_name: recipeName }),
                });

                const data = await response.json();
                if (data.status === "success") {
                    
                    window.location.reload();  // Refresh the page to reflect changes
                } else {
                    alert("Failed to delete recipe. Please try again.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            }
        });
    });
});