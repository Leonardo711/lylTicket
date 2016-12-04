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

    function deleteForm(btn, prefix) {
        var forms = $('.item'); // Get all the forms
        var formCount = forms.length;
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents('.item').remove();
            // Update the total number of forms (2 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            // Go through the forms and set their indices, names and IDs
            forms = $(".item");
            formCount = forms.length;
            for (var i=0; i < formCount; i++) {
                $(forms.get(i)).find("[readonly=readonly]").val(i+1);
                $(forms.get(i)).children().children().children().each(function () {
                    updateElementIndex(this, prefix, i);
                });
            }
        } // End if
        else {
            alert("至少要有一个车站信息");
        }
        return false;
    }

    function addForm(btn, prefix) {
        var forms = $('.item'); // Get all the forms
        var formCount = forms.length;
        // You can only submit a maximum of 10 station for a train.
        if (formCount < 10) {
            var row = $(".item:last").clone(false).get(0);
            // Insert it after the last form
            tmp = parseInt($(row).find("[readonly=readonly]").val());
            $(row).find("[readonly=readonly]").val(tmp+1);
            $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);

            $(row).children().children().children().each(function () {
                updateElementIndex(this, prefix, formCount);
                $(this).val("");
                if ($(this).attr("readonly")=="readonly"){
                    $(this).val(formCount+1);
                }
            });

            // Add an event handler for the delete item/form link
            $(row).find("[name=delete]").click(function () {
                return deleteForm(this, prefix);
            });
            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
        } // End if
        else {
            alert("最多只能有10个车站。");
        }
        return false;
    }
    // Register the click event handlers
    $("#add").click(function () {
        return addForm(this, "form");
    });

    $("[name='delete']").click(function () {
        return deleteForm(this, "form");
    });
});