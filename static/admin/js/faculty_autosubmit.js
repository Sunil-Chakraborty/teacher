(function($) {
    $(document).ready(function() {
        const facultyField = $('#id_faculty');
        facultyField.off('change.facultyFilter'); // avoid duplicate binding
        facultyField.on('change.facultyFilter', function() {
            const facultyVal = $(this).val();
            const baseUrl = window.location.pathname;
            const params = new URLSearchParams(window.location.search);
            if (facultyVal) {
                params.set('faculty', facultyVal);
            } else {
                params.delete('faculty');
            }
            window.location.href = baseUrl + '?' + params.toString();
        });
    });
})(django.jQuery);
