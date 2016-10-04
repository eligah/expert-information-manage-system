/**
 * Created by eligah on 2016/8/20.
 */
$(document).ready(function () {
    setbutton()
})

function setbutton() {
    var str=$("#id_status").text().replace( /^\s+|\s+$/g, "" );
    // console.log(str)
    // alert(str == '审核中')
    if (str == '审核中') {
        $(".changestatus").removeAttr('disabled')
    }
    else
        $(".changestatus").attr('disabled', 'disabled')
}