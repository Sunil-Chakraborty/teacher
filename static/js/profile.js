// profile.js
console.log("Profile.js is loaded");

// Modal Logic
document.addEventListener("DOMContentLoaded", function() {
    var editModal = document.getElementById("editPersonalDetailsModal");
    var editButton = document.getElementById("editPersonalDetailsButton");
    var closeEditModal = document.getElementById("closeEditModal");
    var editPersonalDetailsForm = document.getElementById("editPersonalDetailsForm");
    var qualificationModal = document.getElementById("qualificationModal");
    var qualificationBox = document.getElementById("qualificationBox");
    var closeQualificationModal = document.querySelector("#qualificationModal .close");
    var publicationModal = document.getElementById("publicationModal");
    var publicationBox = document.getElementById("publicationBox");
    var closePublicationModal = document.getElementById("closePublicationModal");

    // Open the Edit Personal Details modal
    editButton.onclick = function(event) {
		event.preventDefault(); // Prevent default link behavior
        editModal.style.display = "block";
    };

    // Close the Edit Personal Details modal
    closeEditModal.onclick = function() {
        editModal.style.display = "none";
    };

    // Close the modal when clicking outside the modal content
    window.onclick = function(event) {
        if (event.target == editModal) {
            editModal.style.display = "none";
        } else if (event.target == qualificationModal) {
            qualificationModal.style.display = "none";
        } else if (event.target == publicationModal) {
            publicationModal.style.display = "none";
        }
    };

    // Handle form submission via AJAX
    editPersonalDetailsForm.onsubmit = function(event) {
        event.preventDefault();  // Prevent the default form submission
        var formData = new FormData(editPersonalDetailsForm);  // Get form data

        var url = editPersonalDetailsForm.getAttribute('data-url');  // Get the URL from the form's data attribute

        fetch(url, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"  // Important for Django to recognize as an AJAX request
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Close the modal if successful
                editModal.style.display = "none";
                location.reload();  // Optionally, reload the page or update the profile section with new data
            } else {
                console.error("Form submission failed", data);
            }
        })
        .catch(error => {
            console.error('Error:', error);  // Correctly handling errors
        });
    };

    // Open the Qualifications modal
    qualificationBox.onclick = function() {
        qualificationModal.style.display = "block";
    };

    // Close the Qualifications modal
    closeQualificationModal.onclick = function() {
        qualificationModal.style.display = "none";
    };

    // Open the Publications modal
    publicationBox.onclick = function() {
        publicationModal.style.display = "block";
    };

    // Close the Publications modal
    closePublicationModal.onclick = function() {
        publicationModal.style.display = "none";
    };
});
