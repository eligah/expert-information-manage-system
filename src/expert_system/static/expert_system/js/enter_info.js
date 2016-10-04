$(".form_datetime").datetimepicker({
    format: "dd MM yyyy ",
    autoclose: true,
    todayBtn: true,
    pickerPosition: "bottom-left"
});

$(document).ready(function () {
    $(".form-control").before('<span class="extra_text">*</span>');
    $(".add_liscence").bind("click", function () {
        $(".qualadd").show();
    });
    setallinput()
    if (typeof ($("#id_status").attr('value')) == "undefined") {
        // $("input[type='text']").attr('value', "xxxxxxxxx");
        $("#id_status").attr('value', '待填写');
    }
    $(".acc_model").bind("click", function () {
        va = $(".modal-body input[type='checkbox']");
        var fchecked = [];
        va.each(function (i, e) {
                if (e.checked == true) {
                    fchecked.push(e.value);
                }
            }
        );
        if (fchecked.length > 2) {
            alert('请选择两项');
            return false
        }
        else if (fchecked.length < 1) {
            alert('请至少选择一项');
            return false
        }
        else {
            con_field = document.getElementById("id_field");
            con_field.value = "";
            fchecked.forEach(function (e) {
                con_field.value += e + " ";
            });
            fchecked = [];
            $('#choose_eval').modal('hide')
        }
    });
    $("#btn-edit").bind("click", function () {
        document.getElementById("id_status").value = '待填写';
        $("input[type='text']").removeAttr('readonly');
        $("#btn-save").removeAttr('disabled');
        return false
    });
    $("#btn-save").bind("click", function () {
        // document.getElementById("id_status").value = ''
    });
    // $("#btn-submit").bind("click", function () {
    //     document.getElementById("id_status").value = '审查中'
    // })
    hidecalender()
});

function setallinput() {
    if ($("#id_status").attr('value') == '已修改') {
        $("#btn-save").attr('disabled', 'true');
        $("#btn-submit").removeAttr('disabled');
        $("input[type='text']").attr('readonly', "readonly");
    }
}

function hidecalender() {
    if ($("#id_status").attr('value') != '待填写') {
        $(".datetimepicker").hide();
        $(".qualadd").show();
    }
}

/**
 * Created by eligah on 2016/8/19.
 */
