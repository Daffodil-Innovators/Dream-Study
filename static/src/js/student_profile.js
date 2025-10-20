// Hide toggleable sections except for General Information
$(document).ready(function () {
  
    $(".toggleable-section").not("#personal-info").hide();

    // Toggle visibility of sections upon clicking the navigation links
    $(".toggle-section").click(function () {
        var target = $(this).attr("href");
        $(".toggleable-section").not(target).hide();  // Hide other sections
        $(target).show();  // Toggle visibility of the target section
    });

    // Get the anchor from the URL
    var anchor = window.location.hash;

    // If the anchor exists and corresponds to a section, show it
    if (anchor) {
        $(".toggleable-section").hide(); // Hide all sections
        $(anchor).show(); // Show the section corresponding to the anchor
    } else {
        // If no anchor is present, check for the id in the URL
        var urlParams = new URLSearchParams(window.location.search);
        var id = urlParams.get('id');

        // If id is present in the URL, show the corresponding section
        if (id) {
            $(".toggleable-section").hide(); // Hide all sections
            $("#" + id).show(); // Show the section corresponding to the id
        }
    }
     
});


function generateRandomId() {
    return Math.floor(10000000+ Math.random() * 90000000); // Generate a random 5-digit number
}


                           


function addSchoolFields() {
    // Increment the number of schools
    var numSchools = parseInt(document.getElementById("num_schools").value) + 1;

    // Generate a random item ID
    var randomItemId = generateRandomId();

    // Clone the template of the school fields
    var schoolFieldsTemplate = document.querySelector('.multiple-school');
    var newSchoolFields = schoolFieldsTemplate.cloneNode(true);

    // Update the IDs and names of the cloned fields to make them unique
    newSchoolFields.querySelectorAll('select, input').forEach(function(element) {
        var name = element.getAttribute('name');
        var newName = name.replace(/_[0-9]+/, '_' + randomItemId); // Replace all occurrences of "_1" with the random ID
        var id = newName; // Assign the same ID as the name for simplicity
        element.setAttribute('name', newName);
        element.setAttribute('id', id);
        element.value = ''; // Clear any previously entered value
    });

    // Add header for the new school
    var header = document.createElement('h5');
    header.textContent = 'Attended New School';
    header.classList.add('text-primary'); // Use classList.add() to add a class
    newSchoolFields.insertBefore(header, newSchoolFields.firstChild);

    // Create a div to contain the delete button
    var deleteDiv = document.createElement('div');
    deleteDiv.classList.add('delete-div'); // Add a class to the delete div
    deleteDiv.classList.add('delete-button');
    newSchoolFields.appendChild(deleteDiv); // Append the delete div to the newSchoolFields container

    // Add delete option within the delete div
    var deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'btn btn-danger delete-school';
    deleteBtn.addEventListener('click', function() {
        newSchoolFields.remove(); // Remove the form when delete button is clicked
    });
    deleteDiv.appendChild(deleteBtn); // Append the delete button to the delete div

    // Add the cloned fields to the form
    document.getElementById("additionalSchools").appendChild(newSchoolFields);

    // Update the number of schools in the hidden input field
    document.getElementById("num_schools").value = numSchools;

    // Check if the newly added form is the last one
    if (numSchools > 1 || numSchools === 1)  {
        // If it's not the last one, hide the delete link
        var deleteLink = newSchoolFields.querySelector('.delete-link');
        var attendHead = newSchoolFields.querySelector('.attend-head');
        if (deleteLink) {
            deleteLink.style.display = 'none';
            attendHead.style.display = 'none';
        }
    }
}

// Add event listener to the "Add Attended School" button
document.getElementById("addSchoolBtn").addEventListener("click", addSchoolFields);












// Hide English score form initially
$('.english-score-form').hide();
document.querySelectorAll('input[type="radio"][name="english_test_id"]').forEach(function (radio) {
    radio.addEventListener('change', function () {
        // Hide all score forms
        document.querySelectorAll('.english-score-form').forEach(function (scoreForm) {
            scoreForm.style.display = 'none';
        });

        // Show the selected score form
        var selectedTest = this.value;
        var correspondingScoreForm = document.querySelector('.' + selectedTest + '_score');
        if (correspondingScoreForm) {
            correspondingScoreForm.style.display = 'block';
        }
    });
});

// Initially hide the score section
document.addEventListener("DOMContentLoaded", function() {
    // Hide all .gre_gmt_score elements by default
    document.querySelectorAll('.gre_gmt_score').forEach(function(scoreSection) {
        scoreSection.style.display = 'none';
    });

    // Add event listener to checkbox
    document.querySelectorAll('.form-check-input').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            console.log('Checkbox change event triggered');
            var scoreSection = this.parentElement.querySelector('.gre_gmt_score');
            console.log('Score section:', scoreSection);
            if (scoreSection) {
                scoreSection.style.display = this.checked ? 'block' : 'none';
            }
        });
    });
});



document.addEventListener("DOMContentLoaded", function () {
    const testRadios = document.querySelectorAll('input[name="english_test_id"]');
    const scoreForms = document.querySelectorAll('.score-form');

    // Hide all score forms by default
    scoreForms.forEach(function (form) {
        form.style.display = 'none';
    });

    testRadios.forEach(function (radio) {
        radio.addEventListener('change', function () {
            const selectedTestId = this.value;

            // Hide all score forms
            scoreForms.forEach(function (form) {
                form.style.display = 'none';
            });

            // Show the score form corresponding to the selected test ID
            const selectedForm = document.getElementById('score-form-' + selectedTestId);
            if (selectedForm) {
                selectedForm.style.display = 'block';
            }
        });
    });
});





document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('studentProfileForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Perform form validation
        if (validateForm()) {
            // If validation succeeds, submit the form
            form.submit();
        }
    });
});

function validateForm() {
    let isValid = true;

    // Reset error messages
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(error => error.textContent = '');

    // Validate each form field
    const firstNameField = document.getElementById('first_name');
    if (firstNameField.value.trim() === '') {
        isValid = false;
        document.getElementById('first_name_error').textContent = 'Please enter your first name.';
    }

    const dobField = document.getElementById('dob');
    if (dobField.value.trim() === '') {
        isValid = false;
        document.getElementById('dob_error').textContent = 'Please enter your date of birth.';
    }

    const firstLanguageField = document.getElementById('first_language_id');
    if (firstLanguageField.value.trim() === '') {
        isValid = false;
        document.getElementById('first_language_error').textContent = 'Please enter your first language.';
    }

    const lastNameField = document.getElementById('last_name');
    if (lastNameField.value.trim() === '') {
        isValid = false;
        document.getElementById('last_name_error').textContent = 'Please enter your last name.';
    }

    const citizenshipField = document.getElementById('country_of_citizenship');
    if (citizenshipField.value.trim() === '') {
        isValid = false;
        document.getElementById('country_of_citizenship_error').textContent = 'Please select your country of citizenship.';
    }

    const passportNumberField = document.getElementById('passport_number');
    if (passportNumberField.value.trim() === '') {
        isValid = false;
        document.getElementById('passport_number_error').textContent = 'Please enter your passport number.';
    }

    const maritalStatusField = document.querySelector('input[name="marital_status"]:checked');
    if (!maritalStatusField) {
        isValid = false;
        document.getElementById('marital_status_error').textContent = 'Please select your marital status.';
    }

    const genderField = document.querySelector('input[name="gender"]:checked');
    if (!genderField) {
        isValid = false;
        document.getElementById('gender_error').textContent = 'Please select your gender.';
    }

    return isValid;
}


$('select[name="country_id"]').change(function () {
    var countryId = $(this).val();

    $.ajax({
        url: '/get_states?country_id=' + countryId,
        method: 'GET',
        success: function (states) {
            // Parse the JSON string into an array of objects
            states = JSON.parse(states);
             // Clear existing options
             $('#state_id').empty();
            // Populate options based on the response
            $('#state_id').append('<option value="" selected divisble>--Select State--</option>');
            $.each(states, function (index, state) {
                $('#state_id').append('<option value="' + state.id + '">' + state.name + '</option>');
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error('Error fetching states:', errorThrown);
        }
        
    });
});

// Dynamic filtering of district_id dropdown based on state_id

$('select[name="state_id"]').change(function () {
    var stateId = $(this).val();

    $.ajax({
        url: '/get_districts?state_id=' + stateId,
        method: 'GET',
        success: function (districts) {
            // Parse the JSON string into an array of objects
            districts = JSON.parse(districts);
             // Clear existing options
             $('#district_id').empty();
            // Populate options based on the response
            $('#district_id').append('<option value="" selected divisble>--Select City--</option>');

            $.each(districts, function (index, district) {
                $('#district_id').append('<option value="' + district.id + '">' + district.name + '</option>');
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error('Error fetching states:', errorThrown);
        }
        
    });
});
$(document).ready(function () {
    var dontHaveCheckbox = $('#dont_have');
    var notGetYetCheckbox = $('#not_get_yet');
    var languageTestType = $('select[name="language_test_type"]');
    var readingField = $('input[name="reading"]');
    var listeningField = $('input[name="listening"]');
    var speakingField = $('input[name="speaking"]');
    var writingField = $('input[name="writing"]');
    var totalScoreField = $('input[name="total_score"]');
    var dateOfExamField = $('input[name="date_of_exam"]');
    
    // Event listener for language test type
    languageTestType.change(function () {
        // If language test type is selected, uncheck the checkboxes
        dontHaveCheckbox.prop('checked', false);
        notGetYetCheckbox.prop('checked', false);
    });

    dontHaveCheckbox.change(function () {
        if ($(this).is(':checked')) {
            languageTestType.val('');
            readingField.val('');
            listeningField.val('');
            speakingField.val('');
            writingField.val('');
            totalScoreField.val('');
            dateOfExamField.val('');
        }
    });

    notGetYetCheckbox.change(function () {
        if ($(this).is(':checked')) {
            languageTestType.val('');
            readingField.val('');
            listeningField.val('');
            speakingField.val('');
            writingField.val('');
            totalScoreField.val('');
            dateOfExamField.val('');
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    var deleteLinks = document.querySelectorAll('.delete-school');

    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var schoolId = link.getAttribute('data-school-id');
            var confirmDelete = confirm('Are you sure you want to delete this attended school?');

            if (confirmDelete) {
                window.location.href = '/attended/delete/' + schoolId;
            }
        });
    });
});

function previewImages(event) {
    var preview = document.getElementById('image-preview');
    preview.innerHTML = '';

    var files = event.target.files;
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var reader = new FileReader();

        reader.onload = function(e) {
            var img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '100px'; // Adjust as needed
            img.style.marginRight = '10px'; // Optional: Add some space between images
            img.style.marginBottom = '10px'; // Optional: Add some space between images
            preview.appendChild(img);
        }

        reader.readAsDataURL(file);
    }
}





