$(document).ready(function(){
    // Code adapted from http://djangosnippets.org/snippets/1389/
    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+-)');
        var replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function deleteForm(btn, prefix, classname, warning2) {
		var forms = $(classname); // Get all the forms
		var formCount = forms.length;
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents(classname).remove();
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            // Go through the forms and set their indices, names and IDs
            forms = $(classname);
            formCount = forms.length;
            for (var i=0; i < formCount; i++) {
                $(forms.get(i)).find("[readonly=readonly]").val(i+1);
                $(forms.get(i)).children().children().children().each(function () {
                    updateElementIndex(this, prefix, i);
                });
            }
        } // End if
        else {
            alert(warning2);
        }
        return false;
    }

    function addForm(btn, prefix, classname,max_num, deletename, warning1, warning2) {
		var forms = $(classname); // Get all the forms
		var formCount = forms.length;
        // You can only submit a maximum of 10 station for a train.
        if (formCount < max_num) {
            var lastone = classname+":last"
            var row = $(lastone).clone(false).get(0);
            // Insert it after the last form
			tmp = parseInt($(row).find("[readonly=readonly]").val());
			$(row).find("[readonly=readonly]").val(tmp+1);
            $(row).removeAttr('id').hide().insertAfter(lastone).slideDown(300);

            $(row).children().children().children().each(function () {
                updateElementIndex(this, prefix, formCount);
                $(this).val("");
                if ($(this).attr("readonly")=="readonly"){
                    $(this).val(formCount+1);
                }
            });

            // Add an event handler for the delete item/form link
            var newAttr = "[name=" + deletename +"]"
            $(row).find(newAttr).click(function () {
                return deleteForm(this, prefix, classname ,warning2);
            });
            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
        } // End if
        else {
            alert(warning1);
        }
        return false;
    }
    // Register the click event handlers
    $("#add").click(function () {
        return addForm(this, "run_set", ".item", 10, "delete", "最多有10个车站", "最少有一个车站");
    });

    $("#add1").click(function () {
        return addForm(this, "seat_set", ".item1", 20, "delete1", "最多有20个车厢", "最少有一个车厢");
    });
    $("[name='delete']").click(function () {
        return deleteForm(this, "run_set", ".item", "最少有一个车站");
    });
    $("[name='delete1']").click(function () {
        return deleteForm(this, "seat_set", ".item1","最少有一个车厢");
    });
});
