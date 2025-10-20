const navigateToFormStep = (stepNumber) => {
    // Hide all form steps
    document.querySelectorAll(".form-step").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });

    // Mark all form steps as unfinished
    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });

    // Show the current form step
    const currentFormStep = document.querySelector("#step-" + stepNumber);
    if (currentFormStep) {
        currentFormStep.classList.remove("d-none");
    }

    // Select the form step circle (progress bar) and mark it as active
    const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
    if (formStepCircle) {
        formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
        formStepCircle.classList.add("form-stepper-active");
    }

    // Mark previous form steps as completed
    for (let index = 0; index < stepNumber; index++) {
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        if (formStepCircle) {
            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};

// Add event listeners to form navigation buttons
document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
    formNavigationBtn.addEventListener("click", () => {
        const stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
        navigateToFormStep(stepNumber);
    });
});

document.getElementById('student_create_application').addEventListener('submit', function (event) {
    event.preventDefault();
    const intakeSelect = document.getElementById('intake_list_select');
    const selectedIntake = intakeSelect.value;
    const intakeErrorMessage = document.getElementById('intake-error-message');

    if (!selectedIntake) {
        intakeErrorMessage.textContent = 'Please select an intake.';
        intakeErrorMessage.style.display = 'block';
        // Navigate to step three if intake is null
        navigateToFormStep(3);
    } else {
        intakeErrorMessage.textContent = '';
        intakeErrorMessage.style.display = 'none';
        // Submit the form if intake is not null
        this.submit();
    }
});
// agent part

const navigateToFormSteps = (stepNumber) => {
    // Hide all form steps
    document.querySelectorAll(".form-steps").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });

    // Mark all form steps as unfinished
    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });

    // Show the current form step
    const currentFormStep = document.querySelector("#steps-" + stepNumber);
    if (currentFormStep) {
        currentFormStep.classList.remove("d-none");
    }

    // Select the form step circle (progress bar) and mark it as active
    const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
    if (formStepCircle) {
        formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
        formStepCircle.classList.add("form-stepper-active");
    }

    // Mark previous form steps as completed
    for (let index = 0; index < stepNumber; index++) {
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        if (formStepCircle) {
            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};

// Add event listeners to form navigation buttons
document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
    formNavigationBtn.addEventListener("click", () => {
        const stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
        navigateToFormSteps(stepNumber);
    });
});

document.getElementById('student_create_applications').addEventListener('submit', function (event) {
    event.preventDefault();
    const intakeSelect = document.getElementById('intake_list_selects');
    const selectedIntake = intakeSelect.value;
    const intakeErrorMessage = document.getElementById('intake-error-messages');

    if (!selectedIntake) {
        intakeErrorMessage.textContent = 'Please select an intake.';
        intakeErrorMessage.style.display = 'block';
        // Navigate to step three if intake is null
        navigateToFormSteps(3);
    } else {
        intakeErrorMessage.textContent = '';
        intakeErrorMessage.style.display = 'none';
        // Submit the form if intake is not null
        this.submit();
    }
});

