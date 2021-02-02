function get_inst(e) {
  console.log('dziala')
  var id = this.dataset.id;
  var address = "/rest/get_inst/"
  var data = {"cat_id": id}
  $.get(address, data, function (data, status){
    $('#show').html(data);
  });
}
$(document).ready(function (){
  var cat_li = $(".inst");
  console.log(cat_li)
  cat_li.click(get_inst);
})

function get_form_info(e) {
    var bags_quantity = document.getElementById("bags").value;
    // var stuff = document.getElementById("stuff").dataset.id;
    var street = document.getElementById("address").value;
    var city = document.getElementById("city").value;
    var post_code = document.getElementById("postcode").value;
    var phone = document.getElementById("phone").value;
    var date = document.getElementById("date").value;
    var time = document.getElementById("time").value;
    var comments = document.getElementById("comments").value;
    // let institution = $('#chose').dataset.id;
    let page = "/rest/form_info/";
    let info = {"bags_quantity": bags_quantity, "street":street, "city":city, "post_code":post_code,
        "phone":phone, "date":date, "time":time, "comments":comments}
        $.get(page, info, function (info){
            $('#sum').html(info);
        })
}

$(document).ready(function () {
    let end_btn = $('#end')
    end_btn.click(get_form_info)
})