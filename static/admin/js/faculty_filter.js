(function($) {
    $(document).ready(function() {
        const facultySelect = $('#id_faculty');
        const deptSelect = $('#id_dept_school');

        // Store original <option> list with faculty info
        const allOptions = deptSelect.find('option').clone();

        // Add faculty info to each option by looking it up from the option text
        // In a real project, better to render this server-side.
        allOptions.each(function() {
            const option = $(this);
            if (option.val()) {
                const faculty = option.text().match(/\[(.*?)\]$/); // If we put "[Faculty]" in label
                if (faculty) {
                    option.attr('data-faculty', faculty[1]);
                }
            }
        });

        facultySelect.on('change', function() {
            const selectedFaculty = $(this).val();
            deptSelect.empty().append('<option value="">---------</option>');

            if (selectedFaculty) {
                allOptions.each(function() {
                    const option = $(this);
                    if (!option.val()) return; // skip empty option
                    if (option.attr('data-faculty') === selectedFaculty) {
                        deptSelect.append(option.clone());
                    }
                });
            } else {
                deptSelect.append(allOptions.clone());
            }
        });
    });
})(django.jQuery);
