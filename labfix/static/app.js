const form = document.getElementById("reportForm");
const submitButton = document.getElementById("submitButton");
const buttonText = document.getElementById("buttonText");
const spinner = document.getElementById("spinner");
const message = document.getElementById("message");

function showMessage(text, type) {
    message.textContent = text;
    message.className = `message ${type}`;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    showMessage("", "hidden");
    submitButton.disabled = true;
    buttonText.textContent = "Submitting...";
    spinner.classList.remove("hidden");

    const formData = new FormData(form);

    const payload = {
        student_name: formData.get("student_name"),
        lab_name: formData.get("lab_name"),
        pc_number: formData.get("pc_number"),
        problem_type: formData.get("problem_type"),
        description: formData.get("description")
    };

    try {
        const response = await fetch("/api/reports", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.message || "Unable to submit the report.");
        }

        // This is the important part:
        // after the database insert succeeds, open the separate confirmation page.
        window.location.href = data.redirect_url;

    } catch (error) {
        showMessage(error.message, "error");
        submitButton.disabled = false;
        buttonText.textContent = "Submit Report";
        spinner.classList.add("hidden");
    }
});
