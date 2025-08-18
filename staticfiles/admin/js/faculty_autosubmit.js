(function($) {
    $(function() {
        const facultyField = document.getElementById("id_faculty");
        if (!facultyField) {
            console.warn("faculty_autosubmit.js: No faculty field found");
            return;
        }

        facultyField.addEventListener("change", function() {
            const facultyVal = this.value;
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
})(django.jQuery);
