

function toggle_class() {

    document.querySelectorAll('.org').forEach((e)=>{
        e.classList.remove('chosen_org')
    })
    this.classList.toggle('chosen_org')
}



function get_inst() {
  var id = this.dataset.id;
  this.classList.toggle('chosen_stuff')
  var address = "/rest/get_inst/"
  var data = {"cat_id": id}
  $.get(address, data, function (data){
    $('#show').html(data);
  });
}


function get_form_info() {
    let stuff_id_arr = []
    let bags_quantity = document.getElementById("bags").value;
    let stuff_id_node = document.querySelectorAll(".chosen_stuff");
    let stuff_id = Array.from(stuff_id_node)
    if (stuff_id) {
        stuff_id.forEach((e) => {
            stuff_id_arr.push(e.value)
        })
    }
    stuff_id_arr = stuff_id_arr.join()
    let street = document.getElementById("address").value;
    let city = document.getElementById("city").value;
    let post_code = document.getElementById("postcode").value;
    let phone = document.getElementById("phone").value;
    let date = document.getElementById("date").value;
    let time = document.getElementById("time").value;
    let comments = document.getElementById("comments").value;
    let institution = 0
    let inst = document.querySelector(".chosen_org")
    if (inst) {
        institution = inst.dataset.id;
    }
    let page = "/rest/form_info/";
    let info = {"bags_quantity": bags_quantity, "street":street, "city":city, "post_code":post_code,
        "phone":phone, "date":date, "time":time, "comments":comments, "stuff_id_arr": stuff_id_arr,
        "institution": institution}
     if (bags_quantity === '' || street === '' || city === '' || post_code === '' || phone === '' || date === '' ||
        time === '' || stuff_id_arr === '' || institution === '') {
         alert('Wszystkie pola sa wymagane')
     } else {
         $.get(page, info, function (info) {
             $('#sum').html(info);
         })
     }
}

function send_form_post() {
    let stuff_id_arr = []
    let bags_quantity = document.getElementById("bags").value;
    let stuff_id_node = document.querySelectorAll(".chosen_stuff");
    let stuff_id = Array.from(stuff_id_node)
    if (stuff_id) {
        stuff_id.forEach((e) => {
            stuff_id_arr.push(e.value)
        })
    }
    stuff_id_arr = stuff_id_arr.join()
    let street = document.getElementById("address").value;
    let city = document.getElementById("city").value;
    let post_code = document.getElementById("postcode").value;
    let phone = document.getElementById("phone").value;
    let date = document.getElementById("date").value;
    let time = document.getElementById("time").value;
    let comments = document.getElementById("comments").value;
    let institution = document.querySelector(".chosen_org").dataset.id;
    let page = "/addDonation/";
    console.log(institution)
    let info = {"bags_quantity": bags_quantity, "street":street, "city":city, "post_code":post_code,
        "phone":phone, "date":date, "time":time, "comments":comments, "stuff_id_arr": stuff_id_arr,
        "institution": institution, csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value}
        if (bags_quantity === '' || street === '' || city === '' || post_code === '' || phone === '' || date === '' ||
        time === '' || stuff_id_arr === '' || institution === '') {
        alert('Sprawdz czy nie pominales zadnego pola')
        } else {
         $.post(page, info, function (info){
            $('#sum').html(info);
            window.location.replace("/formConformation/")
        })
    }
}


$(document).ready(function (){

    var cat_li = $(".inst");
    cat_li.click(get_inst);


    let action_button = $("#show")
    action_button.click(() => {
        let inst_li = $(".org")
        inst_li.click(toggle_class)
    })

    let confirm = $("#confirm")
    confirm.click(send_form_post)


    let end_btn = $('#end')
    end_btn.click(get_form_info)

})
