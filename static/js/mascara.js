$(function(){
    $('.mask-phone').mask('0000-0000');
    $('.mask-dui').mask('00000000-0');
    $('.mask-licencia').mask('0000-0');
    $('.mask-date').mask('00/00/0000');
    $(".mask-texto").bind('keypress', function(event) {
        var regex = new RegExp("^[a-zA-Z ]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
          event.preventDefault();
          return false;
        }
    });
    $(".mask-textonumero").bind('keypress', function(event) {
        var regex = new RegExp("^[a-zA-Z0-9- ]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
          event.preventDefault();
          return false;
        }
    });
});
