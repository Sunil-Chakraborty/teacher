document.addEventListener("DOMContentLoaded", function() {
    console.log("faculty_autosubmit.js loaded (vanilla JS)");

    const facultyField = document.getElementById("id_faculty");
    if (!facultyField) {
        console.warn("faculty_autosubmit.js: No faculty field found");
        return;
    }
    console.log("Faculty field found:", facultyField);

    facultyField.addEventListener("change", function() {
        const facultyVal = this.value;
        console.log("Faculty changed to:", facultyVal);

        const baseUrl = window.location.pathname;
        const params = new URLSearchParams(window.location.search);

        if (facultyVal) {
            params.set("faculty", facultyVal);
        } else {
            params.delete("faculty");
        }

        const newUrl = baseUrl + "?" + params.toString();
        console.log("Redirecting to:", newUrl);
        window.location.href = newUrl;
    });
});
