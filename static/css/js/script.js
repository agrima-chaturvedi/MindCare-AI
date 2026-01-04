document.addEventListener("DOMContentLoaded", () => {
    const moodButtons = document.querySelectorAll(".mood-btn");
    const moodInput = document.getElementById("moodInput");

    moodButtons.forEach(button => {
        button.addEventListener("click", () => {
            // Set mood value in hidden input
            const selectedMood = button.dataset.mood;
            moodInput.value = selectedMood;

            // Remove highlight from all buttons
            moodButtons.forEach(btn => btn.classList.remove("active"));

            // Highlight selected button
            button.classList.add("active");
        });
    });
});
