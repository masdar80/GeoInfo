$(function () {

  $(".js-create-rdd").click(function () {
    $.ajax({
      url: 'rdd_list/create',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-rdd").modal("show");
      },
      success: function (data) {
        $("#modal-rdd .modal-content").html(data.html_form);
      }
    });
  });


  $("#modal-rdd").on("submit", ".js-rdd-create-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("rdd-table tbody").html(data.html_list_RDD);
          $("modal-rdd").modal("hide");
        }
        else {
          $("#modal-rdd .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });
});